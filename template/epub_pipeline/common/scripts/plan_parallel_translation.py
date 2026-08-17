#!/usr/bin/env python3
"""Build a quality-gated parallel translation work plan.

The common planner is provider-neutral.  It consumes an explicit capability
record supplied by the active client adapter; it never guesses that workers
exist and never selects a vendor model by name.
"""

from __future__ import annotations

import argparse
import json
import re
import tempfile
from collections import OrderedDict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_BOOK_ROOT = Path(__file__).resolve().parents[1]
LATIN_WORD = re.compile(r"\b[A-Za-z][A-Za-z'’-]*\b")
CJK_CHAR = re.compile(r"[\u3400-\u9fff]")
GPT_SPAWNED_WORKER_CAP = 4
NON_GPT_SPAWNED_WORKER_CAP = 8
CAPABILITY_CAP_FIELDS = (
    "advertised_max_spawned_workers",
    "user_max_spawned_workers",
    "rate_limit_max_spawned_workers",
    "budget_max_spawned_workers",
    "quality_max_spawned_workers",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plan adaptive producer/auditor translation concurrency.")
    parser.add_argument("--book-root", default=None)
    parser.add_argument("--capabilities", default="state/orchestration_capabilities.json")
    parser.add_argument("--runtime-state", default="state/orchestration_runtime.json")
    parser.add_argument("--output", default="qa/orchestration/work_plan.json")
    parser.add_argument("--write-plan", action="store_true")
    return parser.parse_args()


def read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object: {path.name}")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        return []
    values: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), start=1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"Expected a JSON object at {path.name}:{line_number}")
        values.append(value)
    return values


def source_size(text: str) -> int:
    return max(len(LATIN_WORD.findall(text)), len(CJK_CHAR.findall(text)))


def unit_weight(unit: dict[str, Any]) -> int:
    text = str(unit.get("source_text") or "")
    base = max(1, source_size(text))
    unit_type = str(unit.get("unit_type") or "paragraph")
    multiplier = {
        "heading": 0.35,
        "note": 1.35,
        "footnote": 1.35,
        "table": 1.55,
        "code": 1.55,
        "verse": 1.25,
    }.get(unit_type, 1.0)
    critical_markers = len(re.findall(r"\d|\b[A-Z][a-z]+\b|\[\^", text))
    multiplier += min(0.5, critical_markers * 0.025)
    return max(1, round(base * multiplier))


def workload_from_book(book_root: Path) -> dict[str, Any]:
    units = read_jsonl(book_root / "translation_units" / "units.jsonl")
    if units:
        chapters: OrderedDict[str, int] = OrderedDict()
        for unit in units:
            chapter = str(unit.get("chapter_id") or "").strip()
            if not chapter:
                raise ValueError("Canonical translation unit lacks chapter_id.")
            chapters[chapter] = chapters.get(chapter, 0) + unit_weight(unit)
        values = [
            {"chapter_id": chapter, "weighted_source_units": weight}
            for chapter, weight in chapters.items()
        ]
        return {
            "source": "canonical_translation_units",
            "weighted_source_units": sum(chapters.values()),
            "chapter_count": len(values),
            "chapters": values,
        }

    assessment = read_json(book_root / "output" / "release" / "translation_difficulty_assessment.json")
    profile = assessment.get("book_complexity_profile") if isinstance(assessment.get("book_complexity_profile"), dict) else {}
    total = int(profile.get("source_unit_count") or 0)
    chapter_count = int(profile.get("chapter_count") or 0)
    difficulty = int(assessment.get("overall_difficulty_score_1_to_5") or 3)
    weighted = round(total * (0.8 + difficulty * 0.1))
    chapters: list[dict[str, Any]] = []
    assigned = 0
    if chapter_count > 0:
        each = weighted // chapter_count
        for index in range(chapter_count):
            value = weighted - assigned if index == chapter_count - 1 else each
            assigned += value
            chapters.append({"chapter_id": f"{index + 1:03d}", "weighted_source_units": value})
    return {
        "source": "difficulty_assessment_fallback" if assessment else "unavailable",
        "weighted_source_units": weighted,
        "chapter_count": chapter_count,
        "chapters": chapters,
    }


def positive_cap(capabilities: dict[str, Any], key: str) -> int:
    value = capabilities.get(key)
    return value if isinstance(value, int) and not isinstance(value, bool) and value >= 0 else 0


def parse_utc_timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed.astimezone(timezone.utc)


def workload_cap(total: int, provider_family: str) -> int:
    if total < 50_000:
        return 0
    if total < 150_000:
        return 2
    if total < 300_000:
        return 3
    if total < 600_000 or provider_family == "gpt":
        return 4
    if total < 1_000_000:
        return 6
    return 8


def role_counts(worker_count: int) -> tuple[int, int]:
    if worker_count <= 0:
        return 0, 0
    if worker_count == 1:
        return 1, 0
    if worker_count <= 4:
        return worker_count - 1, 1
    auditors = 2
    return worker_count - auditors, auditors


def contiguous_bundles(chapters: list[dict[str, Any]], producer_count: int) -> list[dict[str, Any]]:
    if producer_count <= 0 or not chapters:
        return []
    producer_count = min(producer_count, len(chapters))
    bundles: list[dict[str, Any]] = []
    cursor = 0
    remaining_weight = sum(int(item.get("weighted_source_units") or 0) for item in chapters)
    for producer_index in range(producer_count):
        slots_left = producer_count - producer_index
        chapters_left = len(chapters) - cursor
        take: list[dict[str, Any]] = []
        taken_weight = 0
        target = remaining_weight / slots_left
        while cursor < len(chapters):
            chapters_after = len(chapters) - (cursor + 1)
            candidate = chapters[cursor]
            take.append(candidate)
            taken_weight += int(candidate.get("weighted_source_units") or 0)
            cursor += 1
            if taken_weight >= target and chapters_after >= slots_left - 1:
                break
            if chapters_after == slots_left - 1:
                break
        remaining_weight -= taken_weight
        bundles.append({
            "bundle_id": f"translation-bundle-{producer_index + 1:03d}",
            "owner_run_id": f"translator-{producer_index + 1:03d}",
            "chapter_ids": [str(item["chapter_id"]) for item in take],
            "weighted_source_units": taken_weight,
            "adjacent_chapter_affinity": True,
        })
    return bundles


def derive_worker_plan(
    workload: dict[str, Any],
    capabilities: dict[str, Any],
    runtime_state: dict[str, Any] | None = None,
) -> dict[str, Any]:
    runtime = runtime_state or {}
    chapters = workload.get("chapters") if isinstance(workload.get("chapters"), list) else []
    total = int(workload.get("weighted_source_units") or 0)
    provider_family = str(capabilities.get("provider_family") or "unknown")
    known_provider = provider_family in {"gpt", "non_gpt"}
    caps_complete_and_valid = all(
        key in capabilities
        and isinstance(capabilities.get(key), int)
        and not isinstance(capabilities.get(key), bool)
        and int(capabilities[key]) >= 0
        for key in CAPABILITY_CAP_FIELDS
    )
    verified_at = parse_utc_timestamp(capabilities.get("verified_at"))
    valid_until = parse_utc_timestamp(capabilities.get("valid_until"))
    verification_present = bool(capabilities.get("verified_at")) and bool(capabilities.get("valid_until"))
    now = datetime.now(timezone.utc)
    verification_shape_valid = (
        verified_at is not None
        and valid_until is not None
        and verified_at <= now
        and valid_until > verified_at
    )
    verification_current = verification_shape_valid and now < valid_until
    capability_ready = (
        capabilities.get("schema_version") == "1.0"
        and capabilities.get("supports_parallel_workers") is True
        and capabilities.get("user_allows_subagents") is True
        and known_provider
        and caps_complete_and_valid
        and verification_current
    )
    decision = "adaptive_parallel_enabled"
    if not capability_ready:
        count = 0
        if not capabilities or not known_provider:
            decision = "capability_unknown"
        elif capabilities.get("supports_parallel_workers") is not True or capabilities.get("user_allows_subagents") is not True:
            decision = "parallel_workers_disabled"
        elif capabilities.get("schema_version") != "1.0" or not caps_complete_and_valid:
            decision = "capability_invalid"
        elif not verification_present:
            decision = "capability_unverified"
        elif not verification_shape_valid:
            decision = "capability_invalid"
        else:
            decision = "capability_stale"
        hard_cap = 0
        book_cap = workload_cap(total, provider_family)
    elif len(chapters) < 2 or total < 50_000:
        count = 0
        decision = "workload_below_parallel_threshold"
        hard_cap = GPT_SPAWNED_WORKER_CAP if provider_family == "gpt" else NON_GPT_SPAWNED_WORKER_CAP
        book_cap = workload_cap(total, provider_family)
    else:
        hard_cap = GPT_SPAWNED_WORKER_CAP if provider_family == "gpt" else NON_GPT_SPAWNED_WORKER_CAP
        book_cap = workload_cap(total, provider_family)
        caps = [
            hard_cap,
            book_cap,
            positive_cap(capabilities, "advertised_max_spawned_workers"),
            positive_cap(capabilities, "user_max_spawned_workers"),
            positive_cap(capabilities, "rate_limit_max_spawned_workers"),
            positive_cap(capabilities, "budget_max_spawned_workers"),
            positive_cap(capabilities, "quality_max_spawned_workers"),
        ]
        maximum = min(caps)
        pilot_status = str(runtime.get("pilot_status") or "pending")
        required_pilot_fields = {
            "structural_violations",
            "name_policy_violations",
            "first_pass_semantic_rate",
            "rework_rate",
            "patch_conflict_rate",
        }
        pilot_evidence_complete = required_pilot_fields.issubset(runtime)
        count_field_names = ("structural_violations", "name_policy_violations")
        rate_field_names = ("first_pass_semantic_rate", "rework_rate", "patch_conflict_rate")

        def valid_count_field(key: str) -> bool:
            value = runtime.get(key)
            return isinstance(value, int) and not isinstance(value, bool) and value >= 0

        def valid_rate_field(key: str) -> bool:
            value = runtime.get(key)
            return (
                isinstance(value, (int, float))
                and not isinstance(value, bool)
                and 0.0 <= float(value) <= 1.0
            )

        supplied_evidence_invalid = any(
            key in runtime and not valid_count_field(key) for key in count_field_names
        ) or any(key in runtime and not valid_rate_field(key) for key in rate_field_names)
        pilot_evidence_valid = (
            pilot_evidence_complete
            and not supplied_evidence_invalid
            and all(valid_count_field(key) for key in count_field_names)
            and all(valid_rate_field(key) for key in rate_field_names)
        )
        known_blocking_violation = any(
            valid_count_field(key) and runtime[key] > 0 for key in count_field_names
        )
        threshold_failure = pilot_evidence_valid and (
            float(runtime["first_pass_semantic_rate"]) < 0.90
            or float(runtime["rework_rate"]) > 0.10
            or float(runtime["patch_conflict_rate"]) > 0.01
        )

        if capabilities.get("rate_limited") is True or runtime.get("rate_limited") is True:
            count = min(maximum, 1)
            decision = "quality_downscale_rate_limited"
        elif pilot_status == "failed" or known_blocking_violation:
            count = min(maximum, 1)
            decision = "quality_downscale"
        elif supplied_evidence_invalid:
            count = min(maximum, 1)
            decision = "quality_downscale_invalid_pilot_evidence"
        elif pilot_status == "passed" and not pilot_evidence_complete:
            count = min(maximum, 2)
            decision = "pilot_evidence_incomplete"
        elif threshold_failure:
            count = min(maximum, 1)
            decision = "quality_downscale"
        elif pilot_status == "passed":
            count = maximum
        else:
            count = min(maximum, 2)
            decision = "pilot_concurrency"

    producer_count, auditor_count = role_counts(count)
    bundles = contiguous_bundles(chapters, producer_count)
    auditor_ids = [f"auditor-{index + 1:03d}" for index in range(auditor_count)]
    return {
        "schema_version": "1.0",
        "decision_code": decision,
        "provider_family": provider_family,
        "worker_profile": str(capabilities.get("worker_profile") or ""),
        "weighted_source_units": total,
        "chapter_count": len(chapters),
        "spawned_worker_count": count,
        "coordinator_counts_toward_spawned_cap": False,
        "hard_spawned_worker_cap": hard_cap,
        "workload_spawned_worker_cap": book_cap,
        "role_counts": {
            "translation_producers": producer_count,
            "audit_consumers": auditor_count,
        },
        "translation_bundles": bundles,
        "audit_consumer_ids": auditor_ids,
        "merge_authority": "coordinator",
        "single_chapter_owner": True,
        "audit_must_be_independent_of_translation_owner": True,
        "canonical_target_shared_by_editions": True,
        "context_capsule": {
            "required": True,
            "fields": [
                "translation_contract_sha256",
                "proper_noun_revision",
                "occurrence_ledger_revision",
                "terminology_revision",
                "chapter_id",
                "neighboring_chapter_summaries",
                "style_constraints",
            ],
        },
        "scale_policy": {
            "initial_spawned_workers_max": 2,
            "scale_up_requires": {
                "pilot_status": "passed",
                "structural_violations": 0,
                "name_policy_violations": 0,
                "first_pass_semantic_rate_min": 0.90,
                "rework_rate_max": 0.10,
                "patch_conflict_rate_max": 0.01,
            },
            "scale_down_on": [
                "rate_limit",
                "structural_violation",
                "name_policy_violation",
                "semantic_pass_rate_below_threshold",
                "rework_above_threshold",
                "patch_conflict_above_threshold",
            ],
        },
    }


def write_json_atomic(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="\n", delete=False, dir=path.parent) as handle:
        handle.write(payload)
        temporary = Path(handle.name)
    temporary.replace(path)


def resolve_inside(book_root: Path, relative: str) -> Path:
    path = (book_root / relative).resolve()
    try:
        path.relative_to(book_root.resolve())
    except ValueError as exc:
        raise ValueError(f"Path escapes book root: {relative}") from exc
    return path


def main() -> None:
    args = parse_args()
    book_root = (Path(args.book_root) if args.book_root else DEFAULT_BOOK_ROOT).resolve()
    workload = workload_from_book(book_root)
    capabilities = read_json(resolve_inside(book_root, args.capabilities))
    runtime = read_json(resolve_inside(book_root, args.runtime_state))
    plan = derive_worker_plan(workload, capabilities, runtime)
    if args.write_plan:
        output = resolve_inside(book_root, args.output)
        write_json_atomic(output, plan)
        print(f"parallel translation plan: {plan['decision_code']}; workers={plan['spawned_worker_count']}; wrote {output.relative_to(book_root).as_posix()}")
    else:
        print(json.dumps(plan, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_BOOK_ROOT = Path(__file__).resolve().parents[1]
STRATA = ("paragraph", "table", "figure", "formula", "caption_note")
LOCAL_ABSOLUTE_PATH = re.compile(r"(?:[A-Za-z]:[\\/]|\\\\|file://)", re.IGNORECASE)
MIN_REVIEW_SCORE = 80
EXCELLENT_AVERAGE_SCORE = 92
EXCELLENT_LOWEST_SCORE = 88
SKILL_BACKFILL_PATH = "skills/translation-quality-defect-families/SKILL.md"
SKILL_BACKFILL_STATUSES = {"UPDATED", "MERGED", "NOT_APPLICABLE"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate post-EPUB stratified random spot-check artifacts.")
    parser.add_argument("--book-root", default=None, help="Book project root. Defaults to the parent of scripts/.")
    parser.add_argument("--output-dir", default="reviews/random_spotcheck", help="Random spot-check output directory.")
    parser.add_argument("--round", default="latest", help="Round id such as round_001, or latest.")
    parser.add_argument("--target-confidence", type=float, default=0.80, help="Required confidence threshold.")
    parser.add_argument("--require-pass", action="store_true", help="Require agent reviews and closure files to be PASS.")
    parser.add_argument(
        "--skip-excellence-gate",
        action="store_true",
        help=(
            "Only enforce hard publication minimums. By default, --require-pass also enforces "
            "the final-artifact excellence gate."
        ),
    )
    parser.add_argument(
        "--excellent-average-score",
        type=float,
        default=EXCELLENT_AVERAGE_SCORE,
        help="Minimum agent average_score for final-artifact excellence validation.",
    )
    parser.add_argument(
        "--excellent-lowest-score",
        type=float,
        default=EXCELLENT_LOWEST_SCORE,
        help="Minimum agent lowest_score for final-artifact excellence validation.",
    )
    parser.add_argument(
        "--min-current-run-pass-rounds",
        type=int,
        default=2,
        help=(
            "Require this many latest consecutive PASS rounds from the same current review_run_id. "
            "Must be >= 1; defaults to 2 unless the user explicitly overrides it. Legacy rounds "
            "without review_run_id/generated_at never count."
        ),
    )
    return parser.parse_args()


def resolve_book_root(value: str | None) -> Path:
    return (Path(value) if value else DEFAULT_BOOK_ROOT).resolve()


def relative_to_book(book_root: Path, path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(book_root).as_posix()
    except ValueError as exc:
        raise SystemExit(f"path must stay inside book root: {resolved}") from exc


def latest_round(output_dir: Path) -> Path:
    rounds: list[tuple[int, Path]] = []
    if output_dir.exists():
        for path in output_dir.iterdir():
            match = re.fullmatch(r"round_(\d{3})", path.name)
            if match and path.is_dir():
                rounds.append((int(match.group(1)), path))
    if not rounds:
        raise SystemExit(f"no random spot-check rounds found under {output_dir}")
    return sorted(rounds)[-1][1]


def round_dirs(output_dir: Path) -> list[Path]:
    rounds: list[tuple[int, Path]] = []
    if output_dir.exists():
        for path in output_dir.iterdir():
            match = re.fullmatch(r"round_(\d{3})", path.name)
            if match and path.is_dir():
                rounds.append((int(match.group(1)), path))
    return [path for _, path in sorted(rounds)]


def file_contains_status(path: Path, expected: str) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return bool(re.search(rf"status:\s*[\"']?{re.escape(expected)}[\"']?", text, flags=re.IGNORECASE))


def read_number_field(path: Path, field: str) -> float | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(rf"^{re.escape(field)}:\s*([0-9]+(?:\.[0-9]+)?)\s*$", text, flags=re.IGNORECASE | re.MULTILINE)
    return float(match.group(1)) if match else None


def read_text_field(path: Path, field: str) -> str | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    matches = re.findall(rf"^{re.escape(field)}:\s*(.*?)\s*$", text, flags=re.IGNORECASE | re.MULTILINE)
    if not matches:
        return None
    value = matches[-1].strip()
    if value.startswith('"'):
        closing = value.find('"', 1)
        if closing != -1:
            value = value[1:closing].strip()
    elif value.startswith("'"):
        closing = value.find("'", 1)
        if closing != -1:
            value = value[1:closing].strip()
    else:
        value = value.split("#", 1)[0].strip()
    return value


def read_bool_field(path: Path, field: str) -> bool | None:
    value = read_text_field(path, field)
    if value is None:
        return None
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    return None


def expected_agent_sample_count(manifest: dict, agent_name: str) -> int:
    sample_set = manifest.get("sample_sets", {}).get(agent_name, {})
    if not isinstance(sample_set, dict):
        return 0
    total = 0
    for samples in sample_set.values():
        if isinstance(samples, list):
            total += len(samples)
    return total


def agent_unit_ids(manifest: dict, agent_name: str) -> set[str]:
    sample_set = manifest.get("sample_sets", {}).get(agent_name, {})
    if not isinstance(sample_set, dict):
        return set()
    unit_ids: set[str] = set()
    for samples in sample_set.values():
        if not isinstance(samples, list):
            continue
        for sample in samples:
            if isinstance(sample, dict) and sample.get("id"):
                unit_ids.add(str(sample["id"]))
    return unit_ids


def scored_reviewed_unit_ids(review_path: Path, unit_ids: set[str]) -> set[str]:
    if not review_path.exists() or not unit_ids:
        return set()
    text = review_path.read_text(encoding="utf-8", errors="replace")
    scored: set[str] = set()
    for line in text.splitlines():
        if "|" not in line:
            continue
        matching_ids = [unit_id for unit_id in unit_ids if unit_id in line]
        if not matching_ids:
            continue
        cells = [cell.strip().strip("`") for cell in line.strip().strip("|").split("|")]
        has_score = any(re.fullmatch(r"(?:100|[1-9]?[0-9])(?:\.\d+)?", cell) for cell in cells)
        if has_score:
            scored.update(matching_ids)
    return scored


def stratum_confidence(info: dict) -> float:
    candidate_count = int(info.get("candidate_count", 0))
    sample_count = int(info.get("sample_count", 0))
    if candidate_count <= 0:
        return 1.0
    if bool(info.get("full_scan", False)) or sample_count >= candidate_count:
        return 1.0
    return float(info.get("estimated_confidence_after_planned_rounds", 0))


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def parse_utc_timestamp(value: str) -> datetime | None:
    if not value:
        return None
    try:
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def latest_artifact_baseline(book_root: Path) -> tuple[datetime | None, str]:
    candidates = [
        book_root / "output" / "release" / "release_state.json",
        book_root / "output" / "private_artifacts" / "private_artifact_state.json",
    ]
    existing = [path for path in candidates if path.exists()]
    if not existing:
        return None, ""
    latest = max(existing, key=lambda path: path.stat().st_mtime)
    return datetime.fromtimestamp(latest.stat().st_mtime, tz=timezone.utc), relative_to_book(book_root, latest)


def review_file_has_issue(review_path: Path) -> bool:
    if not review_path.exists():
        return False
    text = review_path.read_text(encoding="utf-8", errors="replace")
    if not file_contains_status(review_path, "PASS"):
        return True
    average_score = read_number_field(review_path, "average_score")
    lowest_score = read_number_field(review_path, "lowest_score")
    blocking_count = read_number_field(review_path, "blocking_issue_count")
    if average_score is not None and average_score < MIN_REVIEW_SCORE:
        return True
    if lowest_score is not None and lowest_score < MIN_REVIEW_SCORE:
        return True
    if blocking_count is not None and blocking_count > 0:
        return True
    return bool(re.search(r"\bP[0-2]\b", text, flags=re.IGNORECASE))


def round_has_review_issue(round_dir: Path) -> bool:
    reviews_dir = round_dir / "reviews"
    if not reviews_dir.exists():
        return False
    return any(review_file_has_issue(path) for path in reviews_dir.glob("*_review.md"))


def validate_issue_round_skill_backfill(book_root: Path, round_dir: Path) -> list[str]:
    errors: list[str] = []
    fix_log = round_dir / "fixes" / "fix_log.md"
    closure = round_dir / "verification" / "closure_check.md"
    rel_round = relative_to_book(book_root, round_dir)

    if not fix_log.exists():
        return [f"issue round missing fix log for translation-quality skill backfill decision: {rel_round}"]
    if not closure.exists():
        return [f"issue round missing closure check for translation-quality skill backfill decision: {rel_round}"]
    if not file_contains_status(fix_log, "PASS"):
        errors.append(f"issue round fix log must be PASS before final validation: {relative_to_book(book_root, fix_log)}")
    if not file_contains_status(closure, "PASS"):
        errors.append(f"issue round closure check must be PASS before final validation: {relative_to_book(book_root, closure)}")

    defect_family_count = read_number_field(fix_log, "defect_family_count")
    tq_family_count = read_number_field(fix_log, "translation_quality_defect_family_count")
    backfill_status = read_text_field(fix_log, "translation_quality_skill_backfill")
    backfill_path = read_text_field(fix_log, "translation_quality_skill_backfill_path")
    backfill_summary = read_text_field(fix_log, "translation_quality_skill_backfill_summary")
    not_applicable_reason = read_text_field(fix_log, "translation_quality_skill_backfill_not_applicable_reason")
    verified = read_bool_field(closure, "translation_quality_skill_backfill_verified")

    if defect_family_count is None:
        errors.append(f"issue round fix log missing defect_family_count: {relative_to_book(book_root, fix_log)}")
    if tq_family_count is None:
        errors.append(
            "issue round fix log missing translation-quality skill backfill decision: "
            f"{relative_to_book(book_root, fix_log)}"
        )
        return errors
    if backfill_status is None:
        errors.append(
            "issue round fix log missing translation_quality_skill_backfill: "
            f"{relative_to_book(book_root, fix_log)}"
        )
        return errors

    normalized_status = backfill_status.upper()
    if normalized_status not in SKILL_BACKFILL_STATUSES:
        errors.append(
            "translation_quality_skill_backfill must be UPDATED, MERGED, or NOT_APPLICABLE: "
            f"{relative_to_book(book_root, fix_log)}"
        )
    if tq_family_count > 0:
        if normalized_status not in {"UPDATED", "MERGED"}:
            errors.append(
                "translation-quality defect families require translation-quality skill backfill "
                f"UPDATED or MERGED: {relative_to_book(book_root, fix_log)}"
            )
        if backfill_path != SKILL_BACKFILL_PATH:
            errors.append(
                f"translation_quality_skill_backfill_path must be {SKILL_BACKFILL_PATH}: "
                f"{relative_to_book(book_root, fix_log)}"
            )
        if not backfill_summary or len(backfill_summary) < 20:
            errors.append(
                "translation_quality_skill_backfill_summary must describe the reusable lesson merged into the skill: "
                f"{relative_to_book(book_root, fix_log)}"
            )
        if verified is not True:
            errors.append(
                "closure_check must set translation_quality_skill_backfill_verified: true for translation-quality "
                f"defect families: {relative_to_book(book_root, closure)}"
            )
    elif normalized_status != "NOT_APPLICABLE":
        errors.append(
            "translation_quality_skill_backfill must be NOT_APPLICABLE when "
            f"translation_quality_defect_family_count is 0: {relative_to_book(book_root, fix_log)}"
        )
    elif not not_applicable_reason or len(not_applicable_reason) < 15:
        errors.append(
            "translation_quality_skill_backfill_not_applicable_reason is required when no translation-quality "
            f"family was found: {relative_to_book(book_root, fix_log)}"
        )

    return errors


def validate_current_run_issue_backfills(
    book_root: Path,
    output_dir: Path,
    *,
    latest_manifest: dict,
    baseline_at: datetime | None,
) -> tuple[list[str], list[str]]:
    run_id = str(latest_manifest.get("review_run_id", "")).strip()
    if not run_id:
        return [], []
    issue_rounds: list[str] = []
    errors: list[str] = []
    for round_dir in round_dirs(output_dir):
        manifest = read_json(round_dir / "random_sample_manifest.json")
        if manifest.get("review_run_id") != run_id:
            continue
        generated_at = parse_utc_timestamp(str(manifest.get("generated_at", "")))
        if generated_at is None:
            continue
        if baseline_at is not None and generated_at <= baseline_at:
            continue
        if not round_has_review_issue(round_dir):
            continue
        issue_rounds.append(relative_to_book(book_root, round_dir))
        errors.extend(validate_issue_round_skill_backfill(book_root, round_dir))
    return issue_rounds, errors


def validate_round_artifacts(
    book_root: Path,
    round_dir: Path,
    *,
    target_confidence: float,
    require_pass: bool,
    require_excellence_gate: bool,
    excellent_average_score: float,
    excellent_lowest_score: float,
) -> tuple[dict, dict[str, float], float, dict[str, dict[str, int | float | bool]], list[str]]:
    manifest_path = round_dir / "random_sample_manifest.json"
    errors: list[str] = []
    agent_review_checks: dict[str, dict[str, int | float | bool]] = {}
    confidence_by_stratum: dict[str, float] = {}
    release_confidence = 1.0
    if not manifest_path.exists():
        return {}, confidence_by_stratum, release_confidence, agent_review_checks, [
            f"missing manifest: {relative_to_book(book_root, manifest_path)}"
        ]

    manifest_text = manifest_path.read_text(encoding="utf-8")
    manifest = json.loads(manifest_text)
    if LOCAL_ABSOLUTE_PATH.search(manifest_text):
        errors.append(f"manifest contains a local absolute path: {relative_to_book(book_root, manifest_path)}")
    if manifest.get("schema_version") != "2.0":
        errors.append("manifest schema_version must be 2.0")
    if manifest.get("agents", 0) < 2:
        errors.append("at least two independent agents are required")

    strata = manifest.get("strata", {})
    for stratum in STRATA:
        info = strata.get(stratum)
        if info is None:
            errors.append(f"missing stratum summary: {stratum}")
            continue
        candidate_count = int(info.get("candidate_count", 0))
        sample_count = int(info.get("sample_count", 0))
        confidence = stratum_confidence(info)
        confidence_by_stratum[stratum] = round(confidence, 6)
        if candidate_count > 0 and sample_count <= 0:
            errors.append(f"stratum has candidates but no samples: {stratum}")
        if candidate_count > sample_count and confidence < target_confidence:
            errors.append(f"stratum confidence below target: {stratum}={confidence}")

    active_confidences = [
        confidence
        for stratum, confidence in confidence_by_stratum.items()
        if int(strata.get(stratum, {}).get("candidate_count", 0)) > 0
    ]
    release_confidence = round(min(active_confidences), 6) if active_confidences else 1.0
    manifest_release_confidence = float(manifest.get("release_confidence", release_confidence))
    if abs(manifest_release_confidence - release_confidence) > 0.000001:
        errors.append(
            f"manifest release_confidence mismatch: manifest={manifest_release_confidence}, computed={release_confidence}"
        )
    if release_confidence < target_confidence:
        errors.append(f"release_confidence below target: {release_confidence} < {target_confidence}")

    sample_sets = manifest.get("sample_sets", {})
    for agent_name in sample_sets:
        all_samples = round_dir / "samples" / agent_name / "all_samples.md"
        if not all_samples.exists():
            errors.append(f"missing agent sample file: {relative_to_book(book_root, all_samples)}")
        review_path = round_dir / "reviews" / f"{agent_name}_review.md"
        expected_count = expected_agent_sample_count(manifest, agent_name)
        reviewed_count = len(scored_reviewed_unit_ids(review_path, agent_unit_ids(manifest, agent_name)))
        agent_review_checks[agent_name] = {
            "expected_sample_count": expected_count,
            "scored_sample_row_count": reviewed_count,
            "all_samples_scored": reviewed_count >= expected_count if expected_count else True,
        }
        if not review_path.exists():
            errors.append(f"missing agent review file: {relative_to_book(book_root, review_path)}")
        elif require_pass:
            if not file_contains_status(review_path, "PASS"):
                errors.append(f"agent review is not PASS: {relative_to_book(book_root, review_path)}")
            average_score = read_number_field(review_path, "average_score")
            lowest_score = read_number_field(review_path, "lowest_score")
            blocking_count = read_number_field(review_path, "blocking_issue_count")
            if average_score is None or average_score < MIN_REVIEW_SCORE:
                errors.append(
                    f"agent average_score below {MIN_REVIEW_SCORE} or missing: {relative_to_book(book_root, review_path)}"
                )
            if lowest_score is None or lowest_score < MIN_REVIEW_SCORE:
                errors.append(
                    f"agent lowest_score below {MIN_REVIEW_SCORE} or missing: {relative_to_book(book_root, review_path)}"
                )
            if blocking_count is None or blocking_count != 0:
                errors.append(f"agent blocking_issue_count must be 0: {relative_to_book(book_root, review_path)}")
            if expected_count and reviewed_count < expected_count:
                errors.append(
                    "agent review must include scored rows for every sampled unit: "
                    f"{reviewed_count} < {expected_count}: {relative_to_book(book_root, review_path)}"
                )
            if require_excellence_gate:
                if average_score is None or average_score < excellent_average_score:
                    errors.append(
                        "agent average_score below final-artifact excellence threshold "
                        f"{excellent_average_score}: {relative_to_book(book_root, review_path)}"
                    )
                if lowest_score is None or lowest_score < excellent_lowest_score:
                    errors.append(
                        "agent lowest_score below final-artifact excellence threshold "
                        f"{excellent_lowest_score}: {relative_to_book(book_root, review_path)}"
                    )

    fix_log = round_dir / "fixes" / "fix_log.md"
    closure = round_dir / "verification" / "closure_check.md"
    if not fix_log.exists():
        errors.append(f"missing fix log: {relative_to_book(book_root, fix_log)}")
    elif require_pass and not file_contains_status(fix_log, "PASS"):
        errors.append(f"fix log is not PASS: {relative_to_book(book_root, fix_log)}")
    if not closure.exists():
        errors.append(f"missing closure check: {relative_to_book(book_root, closure)}")
    elif require_pass:
        if not file_contains_status(closure, "PASS"):
            errors.append(f"closure check is not PASS: {relative_to_book(book_root, closure)}")
        open_count = read_number_field(closure, "open_p0_p1_p2_count")
        if open_count is None or open_count != 0:
            errors.append(f"open_p0_p1_p2_count must be 0: {relative_to_book(book_root, closure)}")

    return manifest, confidence_by_stratum, release_confidence, agent_review_checks, errors


def count_current_run_pass_rounds(
    book_root: Path,
    output_dir: Path,
    *,
    latest_manifest: dict,
    target_confidence: float,
    baseline_at: datetime | None,
    require_excellence_gate: bool,
    excellent_average_score: float,
    excellent_lowest_score: float,
) -> tuple[str, list[str]]:
    run_id = str(latest_manifest.get("review_run_id", "")).strip()
    if not run_id:
        return "", []
    counted: list[str] = []
    for round_dir in reversed(round_dirs(output_dir)):
        manifest, _, _, _, errors = validate_round_artifacts(
            book_root,
            round_dir,
            target_confidence=target_confidence,
            require_pass=True,
            require_excellence_gate=require_excellence_gate,
            excellent_average_score=excellent_average_score,
            excellent_lowest_score=excellent_lowest_score,
        )
        if errors:
            break
        if manifest.get("review_run_id") != run_id:
            break
        generated_at = parse_utc_timestamp(str(manifest.get("generated_at", "")))
        if generated_at is None:
            break
        if baseline_at is not None and generated_at <= baseline_at:
            break
        counted.append(relative_to_book(book_root, round_dir))
    counted.reverse()
    return run_id, counted


def main() -> None:
    args = parse_args()
    if args.min_current_run_pass_rounds < 1:
        raise SystemExit("--min-current-run-pass-rounds must be >= 1")
    require_excellence_gate = bool(args.require_pass and not args.skip_excellence_gate)
    book_root = resolve_book_root(args.book_root)
    output_dir = (book_root / args.output_dir).resolve() if not Path(args.output_dir).is_absolute() else Path(args.output_dir).resolve()
    round_dir = latest_round(output_dir) if args.round == "latest" else output_dir / args.round
    errors: list[str] = []
    manifest, confidence_by_stratum, release_confidence, agent_review_checks, round_errors = validate_round_artifacts(
        book_root,
        round_dir,
        target_confidence=args.target_confidence,
        require_pass=args.require_pass,
        require_excellence_gate=require_excellence_gate,
        excellent_average_score=args.excellent_average_score,
        excellent_lowest_score=args.excellent_lowest_score,
    )
    errors.extend(round_errors)

    baseline_at, baseline_path = latest_artifact_baseline(book_root)
    current_run_issue_rounds: list[str] = []
    if args.require_pass:
        current_run_issue_rounds, backfill_errors = validate_current_run_issue_backfills(
            book_root,
            output_dir,
            latest_manifest=manifest,
            baseline_at=baseline_at,
        )
        errors.extend(backfill_errors)
    current_run_id, counted_current_run_rounds = count_current_run_pass_rounds(
        book_root,
        output_dir,
        latest_manifest=manifest,
        target_confidence=args.target_confidence,
        baseline_at=baseline_at,
        require_excellence_gate=require_excellence_gate,
        excellent_average_score=args.excellent_average_score,
        excellent_lowest_score=args.excellent_lowest_score,
    )
    if args.require_pass and args.min_current_run_pass_rounds > 0:
        if len(counted_current_run_rounds) < args.min_current_run_pass_rounds:
            errors.append(
                "current-run PASS rounds are insufficient: "
                f"{len(counted_current_run_rounds)} < {args.min_current_run_pass_rounds}; "
                "legacy PASS rounds without this review_run_id/generated_at or before the latest release/private artifact do not count"
            )

    report = {
        "round_dir": relative_to_book(book_root, round_dir),
        "target_confidence": args.target_confidence,
        "release_confidence": release_confidence,
        "confidence_by_stratum": confidence_by_stratum,
        "require_pass": args.require_pass,
        "publication_min_review_score": MIN_REVIEW_SCORE,
        "excellence_gate_required": require_excellence_gate,
        "excellent_average_score_required": args.excellent_average_score if require_excellence_gate else 0,
        "excellent_lowest_score_required": args.excellent_lowest_score if require_excellence_gate else 0,
        "agent_review_checks": agent_review_checks,
        "current_review_run_id": current_run_id,
        "current_run_issue_rounds_requiring_skill_backfill": current_run_issue_rounds,
        "current_run_pass_rounds_required": args.min_current_run_pass_rounds if args.require_pass else 0,
        "current_run_pass_rounds_count": len(counted_current_run_rounds),
        "current_run_pass_rounds": counted_current_run_rounds,
        "previous_artifact_baseline": baseline_path,
        "status": "FAIL" if errors else "PASS",
        "errors": errors,
    }
    (round_dir / "validation_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
        newline="\n",
    )

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)

    print(f"random spot-check artifacts valid: {round_dir}")
    print(f"release_confidence={release_confidence}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import argparse
import json
import math
import random
import re
import secrets
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path
from urllib.parse import unquote


DEFAULT_BOOK_ROOT = Path(__file__).resolve().parents[1]
STRATA = ("paragraph", "table", "figure", "formula", "caption_note")
BLOCKING_PRIORITY_RE = re.compile(r"\bP[0-2]\b", flags=re.IGNORECASE)


@dataclass(frozen=True)
class AuditUnit:
    id: str
    stratum: str
    file: str
    heading: str
    ordinal: int
    text: str
    asset_path: str = ""
    evidence_path: str = ""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Select deterministic, auditable, stratified random review samples "
            "for independent post-EPUB review agents."
        )
    )
    parser.add_argument("--book-root", default=None, help="Book project root. Defaults to the parent of scripts/.")
    parser.add_argument("--source-dir", default="chapters/final", help="Directory containing reader-facing Markdown.")
    parser.add_argument("--output-dir", default="reviews/random_spotcheck", help="Output directory for review rounds.")
    parser.add_argument("--agents", type=int, default=2, help="Number of independent reviewer sample sets.")
    parser.add_argument(
        "--samples-per-agent",
        type=int,
        default=60,
        help="Minimum paragraph/text samples per agent per round.",
    )
    parser.add_argument("--round", default="auto", help="Round id such as round_001, or auto.")
    parser.add_argument("--rounds-planned", type=int, default=4, help="Planned random-sampling iterations T.")
    parser.add_argument("--target-confidence", type=float, default=0.80, help="Minimum target discovery confidence.")
    parser.add_argument("--defect-rate", type=float, default=0.10, help="Minimum problem rate q to defend against.")
    parser.add_argument(
        "--profile",
        choices=("auto", "standard", "science"),
        default="auto",
        help="Sampling intensity profile. auto detects science/table-heavy overlays.",
    )
    parser.add_argument("--seed", default=None, help="Optional seed. If omitted, a random seed is generated and recorded.")
    return parser.parse_args()


def normalize(text: str) -> str:
    return " ".join(text.replace("\r\n", "\n").split())


def safe_id(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]+", "_", text).strip("_")


def resolve_book_root(value: str | None) -> Path:
    return (Path(value) if value else DEFAULT_BOOK_ROOT).resolve()


def resolve_inside_book(book_root: Path, value: str) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path.resolve()
    return (book_root / path).resolve()


def next_round_id(output_dir: Path) -> str:
    existing: list[int] = []
    if output_dir.exists():
        for path in output_dir.iterdir():
            match = re.fullmatch(r"round_(\d{3})", path.name)
            if match:
                existing.append(int(match.group(1)))
    return f"round_{(max(existing) + 1) if existing else 1:03d}"


def existing_round_dirs(output_dir: Path) -> list[Path]:
    rounds: list[tuple[int, Path]] = []
    if output_dir.exists():
        for path in output_dir.iterdir():
            match = re.fullmatch(r"round_(\d{3})", path.name)
            if match and path.is_dir():
                rounds.append((int(match.group(1)), path))
    return [path for _, path in sorted(rounds)]


def blocking_strata_for_round(round_dir: Path) -> set[str]:
    strata: set[str] = set()
    reviews_dir = round_dir / "reviews"
    if not reviews_dir.exists():
        return strata
    for review_path in reviews_dir.glob("*_review.md"):
        text = review_path.read_text(encoding="utf-8", errors="replace")
        for line in text.splitlines():
            if not BLOCKING_PRIORITY_RE.search(line):
                continue
            for stratum in STRATA:
                if f"::{stratum}::" in line:
                    strata.add(stratum)
    return strata


def recent_blocking_strata(output_dir: Path, limit: int = 2) -> list[set[str]]:
    rounds = existing_round_dirs(output_dir)
    return [blocking_strata_for_round(round_dir) for round_dir in reversed(rounds[-limit:])]


def detect_profile(book_root: Path, requested: str) -> str:
    if requested != "auto":
        return requested
    science_markers = (
        "qa/technical/verification_plan.md",
        "references/figure_redraw_spec.md",
        "metadata/reference_witness_policy.md",
        "qa/technical/diagram_table_inventory.md",
    )
    return "science" if any((book_root / marker).exists() for marker in science_markers) else "standard"


def stratum_policy(profile: str, agents: int, samples_per_agent: int) -> dict[str, dict[str, int]]:
    paragraph_min = max(agents * samples_per_agent, 120)
    if profile == "science":
        return {
            "paragraph": {"min_per_round": paragraph_min, "full_scan_if_lte": 0},
            "table": {"min_per_round": 20, "full_scan_if_lte": 80},
            "figure": {"min_per_round": 20, "full_scan_if_lte": 80},
            "formula": {"min_per_round": 20, "full_scan_if_lte": 100},
            "caption_note": {"min_per_round": 20, "full_scan_if_lte": 120},
        }
    return {
        "paragraph": {"min_per_round": paragraph_min, "full_scan_if_lte": 0},
        "table": {"min_per_round": 20, "full_scan_if_lte": 80},
        "figure": {"min_per_round": 20, "full_scan_if_lte": 80},
        "formula": {"min_per_round": 20, "full_scan_if_lte": 100},
        "caption_note": {"min_per_round": 20, "full_scan_if_lte": 120},
    }


def apply_issue_escalation(policy: dict[str, dict[str, int]], issue_sets: list[set[str]]) -> dict[str, dict[str, int]]:
    escalated = {stratum: dict(info) for stratum, info in policy.items()}
    latest = issue_sets[0] if issue_sets else set()
    previous = issue_sets[1] if len(issue_sets) > 1 else set()
    for stratum in STRATA:
        if stratum in latest:
            escalated[stratum]["blocking_issue_seen_in_previous_round"] = 1
        if stratum in latest and stratum in previous:
            escalated[stratum]["dedicated_audit_required_after_consecutive_blockers"] = 1
    return escalated


def required_total_samples(target_confidence: float, defect_rate: float) -> int:
    if not (0 < target_confidence < 1):
        raise SystemExit("--target-confidence must be between 0 and 1")
    if not (0 < defect_rate < 1):
        raise SystemExit("--defect-rate must be between 0 and 1")
    return math.ceil(math.log(1 - target_confidence) / math.log(1 - defect_rate))


def split_blocks(text: str) -> list[str]:
    return [block.strip() for block in text.replace("\r\n", "\n").split("\n\n") if block.strip()]


def is_table(block: str) -> bool:
    lines = [line.strip() for line in block.splitlines() if line.strip()]
    return (
        len(lines) >= 2
        and lines[0].startswith("|")
        and lines[1].startswith("|")
        and bool(re.search(r"\|\s*:?-{3,}:?\s*\|", lines[1]))
    )


def is_formula(block: str) -> bool:
    stripped = block.strip()
    return (
        stripped.startswith("$$")
        or stripped.startswith(r"\[")
        or "\\begin{equation" in stripped
        or "\\begin{align" in stripped
        or "\\begin{gather" in stripped
    )


def is_caption_or_note(block: str) -> bool:
    stripped = normalize(block)
    return bool(
        re.match(r"^(\[\^[^\]]+\]:|图\s*\d+|表\s*\d+|Figure\s+\d+|Table\s+\d+|注[:：])", stripped, re.IGNORECASE)
    )


def image_refs(block: str) -> list[tuple[str, str]]:
    refs: list[tuple[str, str]] = []
    for match in re.finditer(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", block):
        refs.append((match.group(1).strip(), match.group(2).strip()))
    for match in re.finditer(r"<img\b[^>]*\bsrc=[\"']([^\"']+)[\"'][^>]*>", block, flags=re.IGNORECASE):
        refs.append(("", match.group(1).strip()))
    return refs


def resolve_asset(book_root: Path, chapter_path: Path, ref: str) -> Path | None:
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", ref):
        return None
    clean = unquote(ref.split("#", 1)[0].split("?", 1)[0])
    candidates = [(chapter_path.parent / clean).resolve(), (book_root / clean).resolve()]
    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate
    return None


def unit_id(path: Path, stratum: str, ordinal: int) -> str:
    return f"{safe_id(path.stem)}::{stratum}::{ordinal:04d}"


def units_from_file(book_root: Path, path: Path) -> list[AuditUnit]:
    rel = path.relative_to(book_root).as_posix()
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    blocks = split_blocks(text)
    heading = ""
    counters = {stratum: 0 for stratum in STRATA}
    out: list[AuditUnit] = []

    for block in blocks:
        first = block.splitlines()[0].strip()
        if first.startswith("#"):
            heading = first.lstrip("#").strip()
            continue
        if first.startswith("```"):
            continue

        refs = image_refs(block)
        if refs:
            for alt, ref in refs:
                counters["figure"] += 1
                out.append(
                    AuditUnit(
                        id=unit_id(path, "figure", counters["figure"]),
                        stratum="figure",
                        file=rel,
                        heading=heading,
                        ordinal=counters["figure"],
                        text=normalize(block),
                        asset_path=ref,
                    )
                )
            continue

        if is_table(block):
            counters["table"] += 1
            out.append(
                AuditUnit(
                    id=unit_id(path, "table", counters["table"]),
                    stratum="table",
                    file=rel,
                    heading=heading,
                    ordinal=counters["table"],
                    text=block,
                )
            )
            continue

        if is_formula(block):
            counters["formula"] += 1
            out.append(
                AuditUnit(
                    id=unit_id(path, "formula", counters["formula"]),
                    stratum="formula",
                    file=rel,
                    heading=heading,
                    ordinal=counters["formula"],
                    text=block,
                )
            )
            continue

        if is_caption_or_note(block):
            counters["caption_note"] += 1
            out.append(
                AuditUnit(
                    id=unit_id(path, "caption_note", counters["caption_note"]),
                    stratum="caption_note",
                    file=rel,
                    heading=heading,
                    ordinal=counters["caption_note"],
                    text=normalize(block),
                )
            )
            continue

        plain = normalize(block)
        if len(plain) < 40:
            continue
        counters["paragraph"] += 1
        out.append(
            AuditUnit(
                id=unit_id(path, "paragraph", counters["paragraph"]),
                stratum="paragraph",
                file=rel,
                heading=heading,
                ordinal=counters["paragraph"],
                text=plain,
            )
        )
    return out


def collect_units(book_root: Path, source_dir: Path) -> list[AuditUnit]:
    if not source_dir.exists():
        raise SystemExit(f"source directory does not exist: {source_dir}")
    units: list[AuditUnit] = []
    for path in sorted(source_dir.rglob("*.md")):
        units.extend(units_from_file(book_root, path))
    return units


def choose_samples(
    units_by_stratum: dict[str, list[AuditUnit]],
    rng: random.Random,
    policy: dict[str, dict[str, int]],
    required_total: int,
    rounds_planned: int,
    defect_rate: float,
) -> tuple[dict[str, list[AuditUnit]], dict[str, dict[str, float | int | bool]]]:
    chosen: dict[str, list[AuditUnit]] = {}
    summary: dict[str, dict[str, float | int | bool]] = {}
    required_per_round = math.ceil(required_total / max(1, rounds_planned))

    for stratum in STRATA:
        candidates = units_by_stratum.get(stratum, [])
        count = len(candidates)
        if count == 0:
            chosen[stratum] = []
            summary[stratum] = {
                "candidate_count": 0,
                "sample_count": 0,
                "full_scan": False,
                "target_total_samples_for_confidence": required_total,
                "estimated_confidence_after_planned_rounds": 0.0,
            }
            continue

        stratum_policy = policy[stratum]
        min_per_round = max(required_per_round, stratum_policy["min_per_round"])
        full_threshold = stratum_policy["full_scan_if_lte"]
        dedicated_audit_required = bool(stratum_policy.get("dedicated_audit_required_after_consecutive_blockers", 0))
        full_scan = bool(full_threshold and count <= full_threshold)
        sample_count = count if full_scan else min(count, min_per_round)
        shuffled = candidates[:]
        rng.shuffle(shuffled)
        chosen[stratum] = shuffled[:sample_count]

        planned_total = min(count, sample_count * max(1, rounds_planned))
        confidence = 1.0 if planned_total >= count else 1 - ((1 - defect_rate) ** planned_total)
        summary[stratum] = {
            "candidate_count": count,
            "sample_count": sample_count,
            "full_scan": full_scan,
            "blocking_issue_seen_in_previous_round": bool(stratum_policy.get("blocking_issue_seen_in_previous_round", 0)),
            "dedicated_audit_required_after_consecutive_blockers": dedicated_audit_required,
            "target_total_samples_for_confidence": required_total,
            "estimated_confidence_after_planned_rounds": round(confidence, 6),
        }
    return chosen, summary


def release_confidence_from_summary(summary: dict[str, dict[str, float | int | bool]]) -> float:
    confidences: list[float] = []
    for info in summary.values():
        candidate_count = int(info.get("candidate_count", 0))
        if candidate_count <= 0:
            continue
        if bool(info.get("full_scan", False)):
            confidences.append(1.0)
        else:
            confidences.append(float(info.get("estimated_confidence_after_planned_rounds", 0.0)))
    return round(min(confidences), 6) if confidences else 1.0


def distribute_to_agents(samples_by_stratum: dict[str, list[AuditUnit]], agents: int) -> dict[str, dict[str, list[AuditUnit]]]:
    agent_sets: dict[str, dict[str, list[AuditUnit]]] = {
        f"agent_{chr(ord('a') + index)}": {stratum: [] for stratum in STRATA} for index in range(agents)
    }
    agent_names = list(agent_sets)
    for stratum, samples in samples_by_stratum.items():
        for index, sample in enumerate(samples):
            agent_sets[agent_names[index % agents]][stratum].append(sample)
    return agent_sets


def write_text(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8", newline="\n")


def copy_figure_evidence(book_root: Path, round_dir: Path, unit: AuditUnit) -> AuditUnit:
    source = resolve_asset(book_root, book_root / unit.file, unit.asset_path)
    if not source:
        return unit
    target = round_dir / "evidence" / "figures" / f"{safe_id(unit.id)}{source.suffix}"
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
    return AuditUnit(**{**asdict(unit), "evidence_path": target.relative_to(book_root).as_posix() if target.is_relative_to(book_root) else str(target)})


def write_evidence(book_root: Path, round_dir: Path, unit: AuditUnit) -> AuditUnit:
    if unit.stratum == "figure":
        return copy_figure_evidence(book_root, round_dir, unit)
    if unit.stratum in {"table", "formula"}:
        evidence_dir = round_dir / "evidence" / f"{unit.stratum}s"
        suffix = ".md"
        target = evidence_dir / f"{safe_id(unit.id)}{suffix}"
        write_text(target, [f"# {unit.id}", "", f"- file: `{unit.file}`", f"- heading: `{unit.heading or '(none)'}`", "", unit.text])
        return AuditUnit(**{**asdict(unit), "evidence_path": target.relative_to(book_root).as_posix() if target.is_relative_to(book_root) else str(target)})
    return unit


def sample_heading(stratum: str) -> str:
    return {
        "paragraph": "正文段落 / Paragraph",
        "table": "表格 / Table",
        "figure": "图片或图版 / Figure",
        "formula": "公式或证明块 / Formula or Proof Block",
        "caption_note": "图注、表注或注释 / Caption or Note",
    }[stratum]


def write_agent_samples(round_dir: Path, root_output_dir: Path, agent_name: str, samples_by_stratum: dict[str, list[AuditUnit]], seed: str) -> None:
    combined_lines = [
        f"# {agent_name} 分层随机抽检样本 / Stratified Random Spot-Check Samples",
        "",
        f"seed: `{seed}`",
        "",
        "## 强制评审要求 / Mandatory Review Rules",
        "",
        "- 必须逐个样本给出 0-100 分、问题类型、是否需要返工和理由。",
        "- 表格、图片、公式和图注不得被当作普通段落跳过。",
        "- 图片必须检查裁剪是否过大或过小、标签是否缺失、是否带入周边无关文字、插入点和说明是否正确。",
        "- 表格必须检查行列、表头、数值、单位、caption、XHTML 结构和原文对应关系。",
        "- 公式/证明块必须检查符号、依赖关系、上下文说明和读者可理解性。",
        "- 任一 P0/P1/P2 或单项 < 70 必须判为本轮 FAIL。",
        "",
    ]

    for stratum, samples in samples_by_stratum.items():
        if not samples:
            continue
        stratum_lines = [
            f"# {agent_name} - {sample_heading(stratum)}",
            "",
            f"seed: `{seed}`",
            f"sample_count: `{len(samples)}`",
            "",
        ]
        combined_lines.extend([f"## {sample_heading(stratum)}", ""])
        for idx, sample in enumerate(samples, 1):
            detail = [
                f"### Sample {idx}: `{sample.id}`",
                "",
                f"- stratum: `{sample.stratum}`",
                f"- file: `{sample.file}`",
                f"- heading: `{sample.heading or '(none)'}`",
                f"- ordinal: `{sample.ordinal}`",
            ]
            if sample.asset_path:
                detail.append(f"- asset_path: `{sample.asset_path}`")
            if sample.evidence_path:
                detail.append(f"- evidence_path: `{sample.evidence_path}`")
            detail.extend(
                [
                    "",
                    sample.text,
                    "",
                    "| score | issue_type | rework_required | priority | reason |",
                    "| --- | --- | --- | --- | --- |",
                    "|  |  |  |  |  |",
                    "",
                ]
            )
            stratum_lines.extend(detail)
            combined_lines.extend(detail)
        write_text(round_dir / "samples" / agent_name / f"{stratum}.md", stratum_lines)

    write_text(round_dir / "samples" / agent_name / "all_samples.md", combined_lines)
    write_text(root_output_dir / f"{agent_name}_samples.md", combined_lines)


def write_review_templates(round_dir: Path, agent_names: list[str]) -> None:
    for agent_name in agent_names:
        write_text(
            round_dir / "reviews" / f"{agent_name}_review.md",
            [
                f"# {agent_name} 抽检评审 / Spot-Check Review",
                "",
                'status: "DRAFT" # PASS | FAIL',
                "average_score: 0",
                "lowest_score: 0",
                "blocking_issue_count: 0",
                "",
                "## Findings",
                "",
                "| unit_id | score | issue_type | priority | rework_required | reason |",
                "| --- | --- | --- | --- | --- | --- |",
                "",
                "## Conclusion",
                "",
                "本文件必须由独立评审 Agent 填写。DRAFT 不得作为通过依据。",
            ],
        )

    write_text(
        round_dir / "fixes" / "fix_log.md",
        [
            "# 抽检返工记录 / Spot-Check Fix Log",
            "",
            'status: "DRAFT" # PASS | FAIL',
            "",
            "| unit_id | issue | fix_summary | fixed_file | fixed_by | verification |",
            "| --- | --- | --- | --- | --- | --- |",
            "",
            "所有被抽检发现的问题必须在本文件关闭；仅重新抽样不等于关闭旧问题。",
        ],
    )
    write_text(
        round_dir / "verification" / "closure_check.md",
        [
            "# 抽检闭环验证 / Spot-Check Closure Verification",
            "",
            'status: "DRAFT" # PASS | FAIL',
            "open_p0_p1_p2_count: 0",
            "new_seed_required_after_fix: true",
            "",
            "## Required Checks",
            "",
            "- [ ] 所有已发现 P0/P1/P2 均已定点复查关闭。",
            "- [ ] 修复后的文件重新通过 lint/build/EPUBCheck 中相关检查。",
            "- [ ] 若发生返工，下一轮使用新 seed 重新抽样。",
            "- [ ] 人工可在本轮目录下查看样本、证据、评审、修复和闭环记录。",
        ],
    )


def main() -> None:
    args = parse_args()
    if args.agents < 2:
        raise SystemExit("random spot-check requires at least 2 independent agents")

    book_root = resolve_book_root(args.book_root)
    source_dir = resolve_inside_book(book_root, args.source_dir)
    output_dir = resolve_inside_book(book_root, args.output_dir)
    round_id = next_round_id(output_dir) if args.round == "auto" else args.round
    round_dir = output_dir / round_id
    seed = args.seed or secrets.token_hex(16)
    rng = random.Random(seed)
    profile = detect_profile(book_root, args.profile)
    required_total = required_total_samples(args.target_confidence, args.defect_rate)

    units = collect_units(book_root, source_dir)
    if not units:
        raise SystemExit("no reader-facing audit units found")

    units_by_stratum: dict[str, list[AuditUnit]] = {stratum: [] for stratum in STRATA}
    for unit in units:
        units_by_stratum[unit.stratum].append(unit)

    recent_issue_sets = recent_blocking_strata(output_dir)
    policy = apply_issue_escalation(stratum_policy(profile, args.agents, args.samples_per_agent), recent_issue_sets)
    samples_by_stratum, strata_summary = choose_samples(
        units_by_stratum=units_by_stratum,
        rng=rng,
        policy=policy,
        required_total=required_total,
        rounds_planned=args.rounds_planned,
        defect_rate=args.defect_rate,
    )

    evidenced_samples: dict[str, list[AuditUnit]] = {stratum: [] for stratum in STRATA}
    for stratum, samples in samples_by_stratum.items():
        evidenced_samples[stratum] = [write_evidence(book_root, round_dir, sample) for sample in samples]

    agent_sets = distribute_to_agents(evidenced_samples, args.agents)
    for agent_name, samples in agent_sets.items():
        write_agent_samples(round_dir, output_dir, agent_name, samples, seed)
    write_review_templates(round_dir, list(agent_sets))

    manifest = {
        "schema_version": "2.0",
        "round_id": round_id,
        "seed": seed,
        "book_root": str(book_root),
        "source_dir": str(source_dir.relative_to(book_root).as_posix()),
        "output_dir": str(output_dir.relative_to(book_root).as_posix()) if output_dir.is_relative_to(book_root) else str(output_dir),
        "profile": profile,
        "agents": args.agents,
        "samples_per_agent_per_round": args.samples_per_agent,
        "rounds_planned": args.rounds_planned,
        "blocking_issue_strata_in_recent_rounds": [sorted(strata) for strata in recent_issue_sets],
        "target_confidence": args.target_confidence,
        "defect_rate": args.defect_rate,
        "release_confidence": release_confidence_from_summary(strata_summary),
        "release_confidence_model": "min_h(1 - (1 - defect_rate) ** planned_samples_h); full-scan strata count as 1.0",
        "required_total_samples_per_stratum_for_target": required_total,
        "strata": strata_summary,
        "sample_sets": {
            agent_name: {
                stratum: [asdict(sample) for sample in samples]
                for stratum, samples in samples_by_stratum.items()
            }
            for agent_name, samples_by_stratum in agent_sets.items()
        },
    }

    write_text(round_dir / "seed.txt", [seed])
    write_text(round_dir / "strata_summary.json", [json.dumps(strata_summary, ensure_ascii=False, indent=2)])
    manifest_json = json.dumps(manifest, ensure_ascii=False, indent=2)
    write_text(round_dir / "random_sample_manifest.json", [manifest_json])
    write_text(output_dir / "random_sample_manifest.json", [manifest_json])

    print(f"wrote stratified random review samples to {round_dir}")
    print(f"seed={seed}")
    print(f"profile={profile}")


if __name__ == "__main__":
    main()

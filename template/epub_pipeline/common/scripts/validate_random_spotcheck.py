from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


DEFAULT_BOOK_ROOT = Path(__file__).resolve().parents[1]
STRATA = ("paragraph", "table", "figure", "formula", "caption_note")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate post-EPUB stratified random spot-check artifacts.")
    parser.add_argument("--book-root", default=None, help="Book project root. Defaults to the parent of scripts/.")
    parser.add_argument("--output-dir", default="reviews/random_spotcheck", help="Random spot-check output directory.")
    parser.add_argument("--round", default="latest", help="Round id such as round_001, or latest.")
    parser.add_argument("--target-confidence", type=float, default=0.80, help="Required confidence threshold.")
    parser.add_argument("--require-pass", action="store_true", help="Require agent reviews and closure files to be PASS.")
    return parser.parse_args()


def resolve_book_root(value: str | None) -> Path:
    return (Path(value) if value else DEFAULT_BOOK_ROOT).resolve()


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


def stratum_confidence(info: dict) -> float:
    candidate_count = int(info.get("candidate_count", 0))
    sample_count = int(info.get("sample_count", 0))
    if candidate_count <= 0:
        return 1.0
    if bool(info.get("full_scan", False)) or sample_count >= candidate_count:
        return 1.0
    return float(info.get("estimated_confidence_after_planned_rounds", 0))


def main() -> None:
    args = parse_args()
    book_root = resolve_book_root(args.book_root)
    output_dir = (book_root / args.output_dir).resolve() if not Path(args.output_dir).is_absolute() else Path(args.output_dir).resolve()
    round_dir = latest_round(output_dir) if args.round == "latest" else output_dir / args.round
    manifest_path = round_dir / "random_sample_manifest.json"
    if not manifest_path.exists():
        raise SystemExit(f"missing manifest: {manifest_path}")

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    errors: list[str] = []
    if manifest.get("schema_version") != "2.0":
        errors.append("manifest schema_version must be 2.0")
    if manifest.get("agents", 0) < 2:
        errors.append("at least two independent agents are required")

    strata = manifest.get("strata", {})
    confidence_by_stratum: dict[str, float] = {}
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
        if candidate_count > sample_count and confidence < args.target_confidence:
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
    if release_confidence < args.target_confidence:
        errors.append(f"release_confidence below target: {release_confidence} < {args.target_confidence}")

    sample_sets = manifest.get("sample_sets", {})
    for agent_name in sample_sets:
        all_samples = round_dir / "samples" / agent_name / "all_samples.md"
        if not all_samples.exists():
            errors.append(f"missing agent sample file: {all_samples}")
        review_path = round_dir / "reviews" / f"{agent_name}_review.md"
        if not review_path.exists():
            errors.append(f"missing agent review file: {review_path}")
        elif args.require_pass:
            if not file_contains_status(review_path, "PASS"):
                errors.append(f"agent review is not PASS: {review_path}")
            average_score = read_number_field(review_path, "average_score")
            lowest_score = read_number_field(review_path, "lowest_score")
            blocking_count = read_number_field(review_path, "blocking_issue_count")
            if average_score is None or average_score < 75:
                errors.append(f"agent average_score below 75 or missing: {review_path}")
            if lowest_score is None or lowest_score < 70:
                errors.append(f"agent lowest_score below 70 or missing: {review_path}")
            if blocking_count is None or blocking_count != 0:
                errors.append(f"agent blocking_issue_count must be 0: {review_path}")

    fix_log = round_dir / "fixes" / "fix_log.md"
    closure = round_dir / "verification" / "closure_check.md"
    if not fix_log.exists():
        errors.append(f"missing fix log: {fix_log}")
    elif args.require_pass and not file_contains_status(fix_log, "PASS"):
        errors.append(f"fix log is not PASS: {fix_log}")
    if not closure.exists():
        errors.append(f"missing closure check: {closure}")
    elif args.require_pass:
        if not file_contains_status(closure, "PASS"):
            errors.append(f"closure check is not PASS: {closure}")
        open_count = read_number_field(closure, "open_p0_p1_p2_count")
        if open_count is None or open_count != 0:
            errors.append(f"open_p0_p1_p2_count must be 0: {closure}")

    report = {
        "round_dir": str(round_dir),
        "target_confidence": args.target_confidence,
        "release_confidence": release_confidence,
        "confidence_by_stratum": confidence_by_stratum,
        "require_pass": args.require_pass,
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

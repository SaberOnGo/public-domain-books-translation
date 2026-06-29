from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from zipfile import BadZipFile, ZipFile


DEFAULT_BOOK_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ALIGNMENT_MAP = "qa/bilingual_parallel/alignment_map.json"
DEFAULT_REPORT = "output/bilingual_parallel_check.json"

FORBIDDEN_LABELS = [
    "本章采用",
    "原文在前",
    "译文在后",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check bilingual parallel EPUB edition constraints.")
    parser.add_argument("--book-root", default=None, help="Book project root. Defaults to the parent of scripts/.")
    parser.add_argument("--write-report", action="store_true", help=f"Write {DEFAULT_REPORT}.")
    return parser.parse_args()


def resolve_book_root(value: str | None) -> Path:
    return (Path(value) if value else DEFAULT_BOOK_ROOT).resolve()


def rel(book_root: Path, path: Path) -> str:
    try:
        return path.relative_to(book_root).as_posix()
    except ValueError:
        return str(path)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def add_issue(issues: list[dict], rule: str, path: str, detail: str) -> None:
    issues.append({"rule": rule, "path": path, "detail": detail})


def state_enables_bilingual(state: dict) -> bool:
    if state.get("edition_type") == "bilingual_parallel":
        return True
    bilingual = state.get("bilingual_parallel")
    if isinstance(bilingual, dict) and bilingual.get("enabled") is True:
        return True
    for item in state.get("output_editions") or []:
        if isinstance(item, dict) and item.get("enabled") is True and item.get("edition_type") == "bilingual_parallel":
            return True
    return False


def enabled_editions(state: dict) -> list[dict]:
    configured = state.get("output_editions")
    if not isinstance(configured, list):
        return []
    return [item for item in configured if isinstance(item, dict) and item.get("enabled") is True]


def check_state(book_root: Path, state: dict, issues: list[dict]) -> tuple[bool, list[dict]]:
    enabled = state_enables_bilingual(state)
    if not enabled:
        return False, []

    editions = enabled_editions(state)
    by_type = {item.get("edition_type"): item for item in editions}
    for edition_type in ("target_only", "bilingual_parallel"):
        if edition_type not in by_type:
            add_issue(
                issues,
                "missing_enabled_edition",
                "state/pipeline_state.json",
                f"edition_type=bilingual_parallel requires enabled output_editions entry: {edition_type}",
            )

    bilingual = state.get("bilingual_parallel")
    if not isinstance(bilingual, dict):
        add_issue(
            issues,
            "missing_bilingual_config",
            "state/pipeline_state.json",
            "bilingual_parallel config object is required when the bilingual edition is enabled.",
        )
        return True, editions

    if bilingual.get("order") != "source_then_target":
        add_issue(
            issues,
            "unsupported_bilingual_order",
            "state/pipeline_state.json",
            "Bilingual EPUBs must use source_then_target order unless a book records a reviewed exception.",
        )
    if bilingual.get("target_only_must_not_regress") is not True:
        add_issue(
            issues,
            "target_only_regression_boundary_missing",
            "state/pipeline_state.json",
            "Set bilingual_parallel.target_only_must_not_regress=true to keep the target-only EPUB as a first-class artifact.",
        )
    policy = str(bilingual.get("policy") or "")
    if "bilingual_parallel_edition_policy.md" not in policy:
        add_issue(
            issues,
            "missing_bilingual_policy_reference",
            "state/pipeline_state.json",
            "bilingual_parallel.policy must reference references/bilingual_parallel_edition_policy.md.",
        )

    alignment_path = book_root / str(bilingual.get("alignment_map") or DEFAULT_ALIGNMENT_MAP)
    if not alignment_path.exists():
        add_issue(
            issues,
            "missing_alignment_map",
            rel(book_root, alignment_path),
            "Create the source-target paragraph alignment map before building or releasing the bilingual EPUB.",
        )

    return True, editions


def check_artifacts(book_root: Path, editions: list[dict], issues: list[dict]) -> None:
    for edition in editions:
        artifact = str(edition.get("artifact") or "")
        if not artifact:
            add_issue(
                issues,
                "missing_edition_artifact_path",
                "state/pipeline_state.json",
                f"Enabled edition {edition.get('edition_type') or '<unknown>'} has no artifact path.",
            )
            continue
        path = book_root / artifact
        if not path.exists():
            add_issue(
                issues,
                "missing_edition_artifact",
                artifact,
                f"Enabled edition artifact does not exist: {artifact}",
            )
            continue
        if path.stat().st_size <= 0:
            add_issue(
                issues,
                "empty_edition_artifact",
                artifact,
                f"Enabled edition artifact is empty: {artifact}",
            )


def load_alignment_units(path: Path) -> list[dict]:
    data = read_json(path)
    if isinstance(data, list):
        return data
    units = data.get("alignment_units")
    if isinstance(units, list):
        return units
    raise ValueError("alignment map must be a JSON object with alignment_units list, or a list of units")


def as_id_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def check_alignment_map(book_root: Path, state: dict, issues: list[dict]) -> int:
    bilingual = state.get("bilingual_parallel") if isinstance(state.get("bilingual_parallel"), dict) else {}
    alignment_path = book_root / str(bilingual.get("alignment_map") or DEFAULT_ALIGNMENT_MAP)
    if not alignment_path.exists():
        return 0
    rel_path = rel(book_root, alignment_path)
    try:
        units = load_alignment_units(alignment_path)
    except (json.JSONDecodeError, ValueError) as exc:
        add_issue(issues, "invalid_alignment_map", rel_path, str(exc))
        return 0

    seen_unit_ids: set[str] = set()
    seen_source: dict[str, str] = {}
    seen_target: dict[str, str] = {}
    for index, unit in enumerate(units, start=1):
        if not isinstance(unit, dict):
            add_issue(issues, "invalid_alignment_unit", rel_path, f"alignment_units[{index}] must be an object.")
            continue
        unit_id = str(unit.get("id") or f"alignment_units[{index}]")
        if unit_id in seen_unit_ids:
            add_issue(issues, "duplicate_alignment_unit_id", rel_path, f"Duplicate alignment unit id: {unit_id}")
        seen_unit_ids.add(unit_id)

        source_ids = as_id_list(unit.get("source_paragraphs"))
        target_ids = as_id_list(unit.get("target_paragraphs"))
        if not source_ids:
            add_issue(issues, "empty_source_mapping", rel_path, f"{unit_id} has no source_paragraphs.")
        if not target_ids:
            add_issue(issues, "empty_target_mapping", rel_path, f"{unit_id} has no target_paragraphs.")

        allow_reuse = unit.get("allow_reuse") is True
        if not allow_reuse:
            for source_id in source_ids:
                if source_id in seen_source:
                    add_issue(
                        issues,
                        "duplicate_source_paragraph_mapping",
                        rel_path,
                        f"{source_id} appears in both {seen_source[source_id]} and {unit_id}.",
                    )
                seen_source[source_id] = unit_id
            for target_id in target_ids:
                if target_id in seen_target:
                    add_issue(
                        issues,
                        "duplicate_target_paragraph_mapping",
                        rel_path,
                        f"{target_id} appears in both {seen_target[target_id]} and {unit_id}.",
                    )
                seen_target[target_id] = unit_id
    return len(units)


def extract_epub_xhtml(epub_path: Path) -> dict[str, str]:
    try:
        with ZipFile(epub_path) as archive:
            return {
                name: archive.read(name).decode("utf-8", errors="replace")
                for name in archive.namelist()
                if name.lower().endswith((".xhtml", ".html"))
            }
    except BadZipFile:
        return {}


def extract_epub_opf(epub_path: Path) -> str:
    try:
        with ZipFile(epub_path) as archive:
            for name in archive.namelist():
                if name.lower().endswith(".opf"):
                    return archive.read(name).decode("utf-8", errors="replace")
    except BadZipFile:
        return ""
    return ""


def language_matches(actual: str, expected: str) -> bool:
    actual = actual.strip().lower()
    expected = expected.strip().lower()
    if not actual or not expected:
        return False
    if actual == expected:
        return True
    if expected == "zh-hans" and actual in {"zh-cn", "zh-sg"}:
        return True
    if expected == "zh-hant" and actual in {"zh-tw", "zh-hk", "zh-mo"}:
        return True
    return actual.startswith(expected + "-") or expected.startswith(actual + "-")


def check_bilingual_package_metadata(book_root: Path, state: dict, issues: list[dict]) -> list[str]:
    bilingual_edition = next(
        (item for item in enabled_editions(state) if item.get("edition_type") == "bilingual_parallel"),
        {},
    )
    artifact = str(bilingual_edition.get("artifact") or "output/book_bilingual_parallel.epub")
    epub_path = book_root / artifact
    if not epub_path.exists():
        return []
    opf = extract_epub_opf(epub_path)
    if not opf:
        add_issue(
            issues,
            "missing_bilingual_package_metadata",
            artifact,
            "Could not inspect package OPF metadata in the bilingual EPUB.",
        )
        return []

    languages = [
        match.group(1).strip()
        for match in re.finditer(r"<(?:[A-Za-z0-9_-]+:)?language\b[^>]*>\s*([^<]+?)\s*</", opf, re.IGNORECASE)
    ]
    source_language = str(state.get("source_language") or "")
    target_language = str(state.get("target_language") or "")
    if source_language and not any(language_matches(item, source_language) for item in languages):
        add_issue(
            issues,
            "missing_source_language_metadata",
            artifact,
            f"Bilingual EPUB package metadata must include source language dc:language={source_language}.",
        )
    if target_language and not any(language_matches(item, target_language) for item in languages):
        add_issue(
            issues,
            "missing_target_language_metadata",
            artifact,
            f"Bilingual EPUB package metadata must include target language dc:language={target_language}.",
        )
    return languages


def staged_bilingual_xhtml(book_root: Path) -> dict[str, str]:
    candidates = [
        book_root / "output" / "epub_work_bilingual" / "EPUB",
        book_root / "output" / "bilingual_epub_work" / "EPUB",
        book_root / "output" / "book_bilingual_parallel" / "EPUB",
    ]
    files: dict[str, str] = {}
    for root in candidates:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            if path.is_file() and path.suffix.lower() in {".xhtml", ".html"}:
                files[rel(book_root, path)] = path.read_text(encoding="utf-8", errors="replace")
    return files


def count_class(text: str, class_name: str) -> int:
    pattern = re.compile(r'class\s*=\s*["\'][^"\']*\b' + re.escape(class_name) + r'\b[^"\']*["\']', re.IGNORECASE)
    return len(pattern.findall(text))


def class_elements_missing_lang(text: str, class_name: str) -> int:
    pattern = re.compile(
        r"<(?P<tag>[A-Za-z0-9:_-]+)\b(?P<attrs>[^>]*\bclass\s*=\s*[\"'][^\"']*\b"
        + re.escape(class_name)
        + r"\b[^\"']*[\"'][^>]*)>",
        re.IGNORECASE,
    )
    missing = 0
    for match in pattern.finditer(text):
        attrs = match.group("attrs")
        if not re.search(r"\blang\s*=", attrs) or not re.search(r"\bxml:lang\s*=", attrs):
            missing += 1
    return missing


def visible_bilingual_label_issues(text: str) -> list[str]:
    issues: list[str] = []
    label_pattern = re.compile(r">\s*(原文|译文)\s*[:：]?\s*<")
    for match in label_pattern.finditer(text):
        issues.append(match.group(1))
    for label in FORBIDDEN_LABELS:
        if label in text:
            issues.append(label)
    return sorted(set(issues))


def check_bilingual_xhtml(book_root: Path, state: dict, issues: list[dict]) -> tuple[int, int, int]:
    bilingual_edition = next(
        (item for item in enabled_editions(state) if item.get("edition_type") == "bilingual_parallel"),
        {},
    )
    artifact = str(bilingual_edition.get("artifact") or "output/book_bilingual_parallel.epub")
    files = staged_bilingual_xhtml(book_root)
    epub_path = book_root / artifact
    if epub_path.exists():
        for name, text in extract_epub_xhtml(epub_path).items():
            files[f"{artifact}!/{name}"] = text

    if not files:
        add_issue(
            issues,
            "missing_bilingual_xhtml",
            artifact,
            "No bilingual XHTML could be inspected from the EPUB or known staging directories.",
        )
        return 0, 0, 0

    total_units = 0
    total_sources = 0
    total_targets = 0
    for path, text in files.items():
        source_count = count_class(text, "bitext-source")
        target_count = count_class(text, "bitext-target")
        unit_count = count_class(text, "bitext-unit")
        total_units += unit_count
        total_sources += source_count
        total_targets += target_count

        if source_count != target_count:
            add_issue(
                issues,
                "uneven_bilingual_block_count",
                path,
                f"bitext-source count ({source_count}) must equal bitext-target count ({target_count}).",
            )
        missing_source_lang = class_elements_missing_lang(text, "bitext-source")
        missing_target_lang = class_elements_missing_lang(text, "bitext-target")
        if missing_source_lang:
            add_issue(
                issues,
                "source_block_missing_lang",
                path,
                f"{missing_source_lang} bitext-source blocks lack lang and xml:lang attributes.",
            )
        if missing_target_lang:
            add_issue(
                issues,
                "target_block_missing_lang",
                path,
                f"{missing_target_lang} bitext-target blocks lack lang and xml:lang attributes.",
            )
        for label in visible_bilingual_label_issues(text):
            add_issue(
                issues,
                "reader_visible_bilingual_label",
                path,
                f"Do not add repeated reader-facing bilingual labels or explanations: {label}",
            )

    if total_sources == 0 or total_targets == 0:
        add_issue(
            issues,
            "missing_bilingual_blocks",
            artifact,
            "Bilingual XHTML must contain bitext-source and bitext-target blocks.",
        )
    return total_units, total_sources, total_targets


def main() -> None:
    args = parse_args()
    book_root = resolve_book_root(args.book_root)
    state_path = book_root / "state" / "pipeline_state.json"
    issues: list[dict] = []

    if not state_path.exists():
        add_issue(issues, "missing_pipeline_state", "state/pipeline_state.json", "Missing pipeline state file.")
        state: dict = {}
    else:
        state = read_json(state_path)

    bilingual_enabled, editions = check_state(book_root, state, issues)
    alignment_units = 0
    bitext_units = 0
    bitext_sources = 0
    bitext_targets = 0
    package_languages: list[str] = []

    if bilingual_enabled:
        check_artifacts(book_root, editions, issues)
        alignment_units = check_alignment_map(book_root, state, issues)
        package_languages = check_bilingual_package_metadata(book_root, state, issues)
        bitext_units, bitext_sources, bitext_targets = check_bilingual_xhtml(book_root, state, issues)

    report = {
        "book_root": ".",
        "ok": not issues,
        "bilingual_enabled": bilingual_enabled,
        "enabled_editions": [
            {
                "edition_type": item.get("edition_type"),
                "artifact": item.get("artifact"),
            }
            for item in editions
        ],
        "alignment_units": alignment_units,
        "bitext_units": bitext_units,
        "bitext_sources": bitext_sources,
        "bitext_targets": bitext_targets,
        "package_languages": package_languages,
        "issues": issues,
    }
    if args.write_report:
        out = book_root / DEFAULT_REPORT
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if issues:
        for issue in issues[:80]:
            print(f"ERROR {issue['rule']}: {issue['path']} {issue['detail']}")
        if len(issues) > 80:
            print(f"... {len(issues) - 80} more issues")
        raise SystemExit(1)
    if bilingual_enabled:
        print(
            "bilingual parallel gate PASS: "
            f"editions={len(editions)} alignment_units={alignment_units} "
            f"bitext_source_blocks={bitext_sources} bitext_target_blocks={bitext_targets}"
        )
    else:
        print("bilingual parallel gate PASS: bilingual edition disabled")


if __name__ == "__main__":
    main()

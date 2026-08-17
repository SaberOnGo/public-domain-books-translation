from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_BOOK_ROOT = Path(__file__).resolve().parents[1]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a versioned EPUB release artifact and bilingual release note.")
    parser.add_argument("--book-root", default=None, help="Book project root. Defaults to the parent of scripts/.")
    parser.add_argument("--source-epub", default="output/book.epub", help="Source EPUB path relative to the book root.")
    parser.add_argument("--release-dir", default="output/release", help="Release directory relative to the book root.")
    parser.add_argument("--version", default=None, help="Explicit version such as v0.0.1. Defaults to next patch version.")
    parser.add_argument("--main-version", type=int, default=None, help="Main version used when no release state exists.")
    parser.add_argument("--sub-version", type=int, default=None, help="Sub version used when no release state exists.")
    parser.add_argument("--status", choices=("DRAFT", "PASS"), default="DRAFT", help="Release status.")
    parser.add_argument("--require-pass", action="store_true", help="Require PASS gate records before creating release.")
    parser.add_argument("--reason", default="", help="Release reason.")
    parser.add_argument("--changes", action="append", default=[], help="Release change entry. Can be repeated.")
    parser.add_argument("--issues", action="append", default=[], help="Issue entry. Can be repeated.")
    parser.add_argument("--fixes", action="append", default=[], help="Fix entry. Can be repeated.")
    parser.add_argument("--risks", action="append", default=[], help="Risk entry. Can be repeated.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite an existing release artifact for the same version.")
    return parser.parse_args()


def resolve_book_root(value: str | None) -> Path:
    return (Path(value) if value else DEFAULT_BOOK_ROOT).resolve()


def rel_or_abs(book_root: Path, path: Path) -> str:
    try:
        return path.relative_to(book_root).as_posix()
    except ValueError:
        return str(path)


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def read_text_field(path: Path, field: str) -> str | None:
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8", errors="replace")
    matches = re.findall(rf"(?im)^\s*{re.escape(field)}\s*:\s*(.*?)\s*$", text)
    if not matches:
        return None
    value = matches[-1].strip()
    if value.startswith(("'", '"')) and len(value) >= 2:
        value = value.strip("'\"")
    return value.split("#", 1)[0].strip()


def read_number_field(path: Path, field: str) -> float | None:
    value = read_text_field(path, field)
    if value is None:
        return None
    try:
        return float(value)
    except ValueError:
        return None


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


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def read_book_title(book_root: Path) -> str:
    metadata_path = book_root / "metadata" / "book.yaml"
    if not metadata_path.exists():
        return "book"
    for line in metadata_path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\s*title\s*:\s*(.+?)\s*$", line)
        if match:
            value = match.group(1).strip()
            if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                value = value[1:-1]
            return value.strip() or "book"
    return "book"


def safe_filename_part(value: str) -> str:
    value = re.sub(r'[<>:"/\\|?*\x00-\x1f]', "_", value)
    value = re.sub(r"\s+", " ", value).strip(" .")
    return value or "book"


LANGUAGE_FILENAME_LABELS = {
    "en": "英",
    "en-us": "英",
    "en-gb": "英",
    "zh": "中",
    "zh-hans": "中",
    "zh-cn": "中",
    "zh-sg": "中",
    "zh-hant": "繁中",
    "zh-tw": "繁中",
    "zh-hk": "繁中",
    "ja": "日",
    "jp": "日",
    "es": "西",
    "fr": "法",
    "de": "德",
    "it": "意",
    "ru": "俄",
    "ko": "韩",
    "kr": "韩",
    "ar": "阿",
    "id": "印尼",
    "grc": "古希",
    "lzh": "古汉",
    "sa": "梵",
}


def language_filename_label(value: str) -> str:
    normalized = value.strip().lower().replace("_", "-")
    if not normalized:
        return ""
    if normalized in LANGUAGE_FILENAME_LABELS:
        return LANGUAGE_FILENAME_LABELS[normalized]
    primary = normalized.split("-", 1)[0]
    if primary in LANGUAGE_FILENAME_LABELS:
        return LANGUAGE_FILENAME_LABELS[primary]
    return safe_filename_part(value)


def edition_release_suffix(edition: dict, state: dict) -> str:
    edition_type = edition.get("edition_type") or "target_only"
    if edition_type != "bilingual_parallel":
        return edition.get("suffix") or ""
    target = language_filename_label(str(state.get("target_language") or ""))
    source = language_filename_label(str(state.get("source_language") or ""))
    if target and source:
        return f"_{target}{source}双语"
    configured = edition.get("suffix") or ""
    if configured and configured != "_bilingual_parallel":
        return configured
    return "_双语"


def parse_version(version: str) -> tuple[int, int, int]:
    clean = version[1:] if version.startswith("v") else version
    parts = clean.split(".")
    if len(parts) != 3:
        raise SystemExit(f"version must use vX.Y.Z: {version}")
    return tuple(int(part) for part in parts)  # type: ignore[return-value]


def format_version(main: int, sub: int, patch: int) -> str:
    return f"v{main}.{sub}.{patch}"


def next_version(state: dict, main_override: int | None, sub_override: int | None) -> tuple[int, int, int, str]:
    if state:
        main = int(state.get("main_version", 0))
        sub = int(state.get("sub_version", 0))
        patch = int(state.get("patch_version", 0)) + 1
    else:
        main = 0 if main_override is None else main_override
        sub = 0 if sub_override is None else sub_override
        patch = 1
    return main, sub, patch, format_version(main, sub, patch)


def latest_round_dir(book_root: Path) -> Path | None:
    root = book_root / "reviews" / "random_spotcheck"
    if not root.exists():
        return None
    rounds: list[tuple[int, Path]] = []
    for path in root.iterdir():
        if path.is_dir() and path.name.startswith("round_"):
            try:
                rounds.append((int(path.name.split("_", 1)[1]), path))
            except ValueError:
                continue
    return sorted(rounds)[-1][1] if rounds else None


def safe_edition_type(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9_-]+", "_", value or "edition")


def expected_epubcheck_records(book_root: Path) -> list[dict]:
    state = read_json(book_root / "state" / "pipeline_state.json")
    configured = state.get("output_editions") if isinstance(state, dict) else None
    enabled = [item for item in configured or [] if isinstance(item, dict) and item.get("enabled") is True]
    if not enabled:
        enabled = [{"edition_type": "target_only", "artifact": "output/book.epub"}]
    records: list[dict] = []
    for item in enabled:
        edition_type = str(item.get("edition_type") or "target_only")
        artifact_value = str(item.get("artifact") or "output/book.epub")
        artifact = Path(artifact_value)
        artifact = artifact.resolve() if artifact.is_absolute() else (book_root / artifact).resolve()
        report_name = "epubcheck.json" if edition_type == "target_only" else f"epubcheck_{safe_edition_type(edition_type)}.json"
        report_path = book_root / "output" / report_name
        report = read_json(report_path)
        checker = report.get("checker", {}) if isinstance(report, dict) else {}
        evidence = report.get("lifebook_evidence", {}) if isinstance(report, dict) else {}
        artifact_hash = sha256(artifact) if artifact.is_file() else ""
        records.append(
            {
                "edition_type": edition_type,
                "artifact_path": rel_or_abs(book_root, artifact),
                "artifact_sha256": artifact_hash,
                "report_path": rel_or_abs(book_root, report_path) if report_path.is_file() else "",
                "report_artifact_sha256": str(evidence.get("artifact_sha256") or ""),
                "report_artifact_path": str(evidence.get("artifact_path") or ""),
                "report_edition_type": str(evidence.get("edition_type") or ""),
                "fatal": int(checker.get("nFatal", 0)) if checker else None,
                "error": int(checker.get("nError", 0)) if checker else None,
                "warning": int(checker.get("nWarning", 0)) if checker else None,
                "hash_match": bool(artifact_hash and evidence.get("artifact_sha256") == artifact_hash),
                "identity_match": bool(
                    evidence.get("artifact_path") == rel_or_abs(book_root, artifact)
                    and evidence.get("edition_type") == edition_type
                ),
            }
        )
    return records


def gate_summary(book_root: Path) -> dict:
    round_dir = latest_round_dir(book_root)
    validation_report = round_dir / "validation_report.json" if round_dir else None
    validation = read_json(validation_report) if validation_report else {}
    epubcheck_records = expected_epubcheck_records(book_root)
    target_epubcheck = next(
        (item for item in epubcheck_records if item.get("edition_type") == "target_only"),
        epubcheck_records[0] if epubcheck_records else {},
    )
    lint = read_json(book_root / "output" / "publication_lint.json")
    metrics_path = book_root / "output" / "release" / "translation_metrics.json"
    metrics = read_json(metrics_path)
    literary_review_path = book_root / "qa" / "literary_style" / "literary_style_review.md"
    artifact_gate_path = book_root / "output" / "translation_unit_artifact_check.json"
    artifact_gate = read_json(artifact_gate_path)
    artifact_gate_hashes = {
        str(item.get("kind")): str(item.get("epub_sha256") or "")
        for item in artifact_gate.get("artifacts", [])
        if isinstance(item, dict)
    }
    enabled_hashes = {
        ("bilingual" if item.get("edition_type") == "bilingual_parallel" else str(item.get("edition_type"))): str(item.get("artifact_sha256") or "")
        for item in epubcheck_records
    }
    lint_issues = lint.get("issues", []) if isinstance(lint, dict) else []
    estimate = metrics.get("pretranslation_estimate", {}) if isinstance(metrics, dict) else {}
    actual = metrics.get("post_translation_actual", {}) if isinstance(metrics, dict) else {}
    profile = estimate.get("book_complexity_profile", {}) if isinstance(estimate, dict) else {}
    return {
        "random_spotcheck_round": rel_or_abs(book_root, round_dir) if round_dir else "",
        "random_spotcheck_validation": rel_or_abs(book_root, validation_report) if validation_report and validation_report.exists() else "",
        "release_confidence": validation.get("release_confidence"),
        "random_spotcheck_status": validation.get("status", ""),
        "random_spotcheck_require_pass": bool(validation.get("require_pass", False)),
        "current_review_run_id": validation.get("current_review_run_id", ""),
        "current_run_pass_rounds_required": int(validation.get("current_run_pass_rounds_required", 0) or 0),
        "current_run_pass_rounds_count": int(validation.get("current_run_pass_rounds_count", 0) or 0),
        "epubcheck_path": target_epubcheck.get("report_path", ""),
        "epubcheck_fatal": target_epubcheck.get("fatal"),
        "epubcheck_error": target_epubcheck.get("error"),
        "epubcheck_warning": target_epubcheck.get("warning"),
        "epubcheck_records": epubcheck_records,
        "translation_artifact_gate_path": rel_or_abs(book_root, artifact_gate_path) if artifact_gate_path.is_file() else "",
        "translation_artifact_gate_status": artifact_gate.get("status", ""),
        "translation_artifact_reader_policy": artifact_gate.get("reader_policy", ""),
        "translation_artifact_reader_status": artifact_gate.get("reader_validation_status", ""),
        "translation_artifact_warnings": artifact_gate.get("warnings", []),
        "translation_artifact_hash_match": bool(enabled_hashes and artifact_gate_hashes == enabled_hashes),
        "publication_lint_path": "output/publication_lint.json" if lint else "",
        "publication_lint_issue_count": len(lint_issues) if lint else None,
        "translation_metrics_path": "output/release/translation_metrics.json" if metrics else "",
        "translation_metrics_status": metrics.get("metrics_status", "") if isinstance(metrics, dict) else "",
        "translation_metrics_estimate_status": estimate.get("status", "") if isinstance(estimate, dict) else "",
        "translation_metrics_actual_status": actual.get("status", "") if isinstance(actual, dict) else "",
        "translation_metrics_primary_book_type": profile.get("primary_book_type", "") if isinstance(profile, dict) else "",
        "translation_metrics_difficulty_level": estimate.get("difficulty_level", "") if isinstance(estimate, dict) else "",
        "translation_metrics_actual_difficulty_level": actual.get("actual_difficulty_level", "") if isinstance(actual, dict) else "",
        "translation_metrics_actual_active_hours": actual.get("actual_active_hours") if isinstance(actual, dict) else None,
        "translation_metrics_total_input_tokens": actual.get("total_input_tokens") if isinstance(actual, dict) else None,
        "translation_metrics_total_output_tokens": actual.get("total_output_tokens") if isinstance(actual, dict) else None,
        "literary_style_review_path": "qa/literary_style/literary_style_review.md" if literary_review_path.exists() else "",
        "literary_style_status": read_text_field(literary_review_path, "status") or "",
        "literary_target_only_reading_score": read_number_field(literary_review_path, "target_only_reading_score"),
        "literary_read_aloud_awkward_sentence_count": read_number_field(
            literary_review_path,
            "read_aloud_awkward_sentence_count",
        ),
        "literary_unresolved_style_debt_count": read_number_field(literary_review_path, "unresolved_style_debt_count"),
        "literary_literal_explanatory_style_debt_count": read_number_field(
            literary_review_path,
            "literal_explanatory_style_debt_count",
        ),
        "literary_high_impact_sections_reviewed": read_bool_field(
            literary_review_path,
            "high_impact_sections_reviewed",
        ),
        "literary_author_preface_and_first_chapter_reviewed": read_bool_field(
            literary_review_path,
            "author_preface_and_first_chapter_reviewed",
        ),
        "literary_source_fidelity_backcheck_after_polish": read_bool_field(
            literary_review_path,
            "source_fidelity_backcheck_after_polish",
        ),
    }


def require_pass_gates(summary: dict) -> None:
    errors: list[str] = []
    if summary.get("random_spotcheck_status") != "PASS":
        errors.append("latest random spot-check validation status is not PASS")
    if not summary.get("random_spotcheck_require_pass"):
        errors.append("latest random spot-check validation was not run with --require-pass")
    if not summary.get("current_review_run_id"):
        errors.append("latest random spot-check validation is missing current review_run_id evidence")
    required_rounds = int(summary.get("current_run_pass_rounds_required", 0) or 0)
    counted_rounds = int(summary.get("current_run_pass_rounds_count", 0) or 0)
    if required_rounds < 1 or counted_rounds < required_rounds:
        errors.append(
            f"current-run PASS round evidence is insufficient: {counted_rounds} < {max(required_rounds, 1)}"
        )
    confidence = summary.get("release_confidence")
    if confidence is None or float(confidence) < 0.80:
        errors.append("release_confidence is missing or below 0.80")
    epubcheck_records = summary.get("epubcheck_records") or []
    if not epubcheck_records:
        errors.append("EPUBCheck evidence is missing for enabled EPUB artifacts")
    for item in epubcheck_records:
        label = item.get("edition_type") or "unknown"
        if not item.get("report_path"):
            errors.append(f"EPUBCheck report is missing for {label}")
        if not item.get("hash_match"):
            errors.append(f"ARTIFACT_REPORT_HASH_MISMATCH: EPUBCheck report is stale or unbound for {label}")
        if not item.get("identity_match"):
            errors.append(f"ARTIFACT_REPORT_HASH_MISMATCH: EPUBCheck report artifact identity differs for {label}")
        if any(item.get(key) not in (0,) for key in ("fatal", "error", "warning")):
            errors.append(f"EPUBCheck fatal/error/warning count is not zero for {label}")
    if summary.get("translation_artifact_gate_status") != "PASS":
        errors.append("current translation-unit artifact gate is not PASS")
    if summary.get("translation_artifact_reader_policy") not in {"required", "if_available"}:
        errors.append("release artifact gate was not run with a release reader policy")
    if summary.get("translation_artifact_reader_status") not in {"PASS", "SKIPPED_UNAVAILABLE"}:
        errors.append("real-reader smoke test neither passed nor recorded SKIPPED_UNAVAILABLE")
    if not summary.get("translation_artifact_hash_match"):
        errors.append("translation-unit artifact evidence hashes do not match all enabled EPUBs")
    if not summary.get("publication_lint_path"):
        errors.append("output/publication_lint.json is missing")
    elif summary.get("publication_lint_issue_count") not in (0, None):
        errors.append("publication lint has unresolved issues")
    if not summary.get("translation_metrics_path"):
        errors.append("output/release/translation_metrics.json is missing")
    if summary.get("translation_metrics_estimate_status") != "PASS":
        errors.append("translation metrics pretranslation estimate is not PASS")
    if summary.get("translation_metrics_actual_status") != "PASS":
        errors.append("translation metrics post-translation actuals are not PASS")
    if not summary.get("literary_style_review_path"):
        errors.append("qa/literary_style/literary_style_review.md is missing")
    if summary.get("literary_style_status") != "PASS":
        errors.append("literary style review status is not PASS")
    if summary.get("literary_target_only_reading_score") != 5:
        errors.append("literary target-only reading score must be 5 for PASS release")
    if summary.get("literary_read_aloud_awkward_sentence_count") != 0:
        errors.append("literary read-aloud awkward sentence count must be 0 for PASS release")
    if summary.get("literary_unresolved_style_debt_count") != 0:
        errors.append("literary unresolved style debt count must be 0 for PASS release")
    if summary.get("literary_literal_explanatory_style_debt_count") != 0:
        errors.append("literary literal/explanatory style debt count must be 0 for PASS release")
    if summary.get("literary_high_impact_sections_reviewed") is not True:
        errors.append("high-impact openings/prefaces/first chapters were not reviewed")
    if summary.get("literary_author_preface_and_first_chapter_reviewed") is not True:
        errors.append("author/source preface and first chapter review is not complete")
    if summary.get("literary_source_fidelity_backcheck_after_polish") is not True:
        errors.append("source fidelity back-check after literary polish is not complete")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)


def bullet_lines(values: list[str], fallback: str) -> list[str]:
    items = values or [fallback]
    return [f"- {item}" for item in items]


def clean_note_text(value: str) -> str:
    return value.replace("^", "")


def enabled_output_editions(book_root: Path, fallback_source_epub: Path) -> tuple[list[dict], dict]:
    state = read_json(book_root / "state" / "pipeline_state.json")
    configured = state.get("output_editions") if isinstance(state, dict) else None
    editions: list[dict] = []
    if isinstance(configured, list):
        for item in configured:
            if not isinstance(item, dict) or item.get("enabled") is not True:
                continue
            artifact = item.get("artifact") or "output/book.epub"
            source = (book_root / artifact).resolve() if not Path(artifact).is_absolute() else Path(artifact).resolve()
            editions.append(
                {
                    "edition_type": item.get("edition_type") or "target_only",
                    "source": source,
                    "source_label": rel_or_abs(book_root, source),
                    "suffix": item.get("release_artifact_suffix") or "",
                }
            )
    if not editions:
        editions.append(
            {
                "edition_type": "target_only",
                "source": fallback_source_epub,
                "source_label": rel_or_abs(book_root, fallback_source_epub),
                "suffix": "",
            }
        )
    for edition in editions:
        if not edition["source"].exists():
            raise SystemExit(f"enabled EPUB artifact does not exist: {edition['source']}")
    return editions, state


def append_release_index(path: Path, version: str, epub_name: str, note_name: str, status: str, created_at: str) -> None:
    if not path.exists():
        path.write_text(
            "# Release Index / 版本发布索引\n\n| version | status | epub | release note | created_at |\n| --- | --- | --- | --- | --- |\n",
            encoding="utf-8",
            newline="\n",
        )
    with path.open("a", encoding="utf-8", newline="\n") as fh:
        fh.write(f"| {version} | {status} | `{epub_name}` | `{note_name}` | {created_at} |\n")


def prepend_release_note(path: Path, entry: str) -> None:
    title = "# Release Notes / 发布说明"
    if not path.exists():
        path.write_text(f"{title}\n\n{entry}", encoding="utf-8", newline="\n")
        return
    old = path.read_text(encoding="utf-8")
    if old.startswith(title):
        rest = old[len(title):].lstrip()
        path.write_text(f"{title}\n\n{entry}\n\n{rest}", encoding="utf-8", newline="\n")
    else:
        path.write_text(f"{title}\n\n{entry}\n\n---\n\n{old}", encoding="utf-8", newline="\n")


def main() -> None:
    args = parse_args()
    book_root = resolve_book_root(args.book_root)
    source_epub = (book_root / args.source_epub).resolve() if not Path(args.source_epub).is_absolute() else Path(args.source_epub).resolve()

    release_dir = (book_root / args.release_dir).resolve() if not Path(args.release_dir).is_absolute() else Path(args.release_dir).resolve()
    state_path = release_dir / "release_state.json"
    state = read_json(state_path)
    if args.version:
        main_version, sub_version, patch_version = parse_version(args.version)
        version = format_version(main_version, sub_version, patch_version)
    else:
        main_version, sub_version, patch_version, version = next_version(state, args.main_version, args.sub_version)

    summary = gate_summary(book_root)
    if args.require_pass or args.status == "PASS":
        require_pass_gates(summary)

    release_dir.mkdir(parents=True, exist_ok=True)
    release_title = safe_filename_part(read_book_title(book_root))
    editions, pipeline_state = enabled_output_editions(book_root, source_epub)
    note_name = "release_notes.md"
    release_note = release_dir / note_name
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    release_artifacts: list[dict] = []
    for edition in editions:
        epub_name = f"{release_title}{edition_release_suffix(edition, pipeline_state)}_{version}.epub"
        target_epub = release_dir / epub_name
        if not args.overwrite and target_epub.exists():
            raise SystemExit(
                f"release EPUB already exists for {version}: {epub_name}; create the next patch version or pass --overwrite deliberately"
            )
        shutil.copy2(edition["source"], target_epub)
        release_artifacts.append(
            {
                "edition_type": edition["edition_type"],
                "source_epub": edition["source_label"],
                "epub": epub_name,
                "sha256": sha256(target_epub),
                "size_bytes": target_epub.stat().st_size,
            }
        )

    reason = clean_note_text(
        args.reason
        or "Create a versioned EPUB release artifact from the current book build. / 将当前书籍构建产物固化为带版本号的 EPUB 发布文件。"
    )
    changes = [clean_note_text(item) for item in args.changes]
    issues = [clean_note_text(item) for item in args.issues]
    fixes = [clean_note_text(item) for item in args.fixes]
    risks = [clean_note_text(item) for item in args.risks]
    if summary.get("translation_artifact_reader_status") == "SKIPPED_UNAVAILABLE":
        risks.append(
            "REAL_READER_SKIPPED_UNAVAILABLE: no supported EPUB reader was detected on the build computer, so real-reader viewport and navigation smoke testing was not performed; full static gates and EPUBCheck still passed. / 构建电脑未检测到受支持 EPUB 阅读器，因此未执行真实阅读器视口与目录跳转冒烟测试；全书静态门禁和 EPUBCheck 仍已通过。"
        )
    note = [
        f"## Release {version} / 版本 {version}",
        "",
        f"status: {args.status}",
        f"main_version: {main_version}",
        f"sub_version: {sub_version}",
        f"patch_version: {patch_version}",
        f"created_at: {created_at}",
        "epubs:",
        *[f"- {item['edition_type']}: `{item['epub']}` sha256=`{item['sha256']}` size_bytes=`{item['size_bytes']}`" for item in release_artifacts],
        "",
        "## Release Reason / 发布原因",
        "",
        reason,
        "",
        "## Changes / 修改内容",
        "",
        *bullet_lines(changes, "Versioned EPUB artifact created; no content change was declared in command arguments. / 已创建版本化 EPUB 文件；命令参数未声明具体内容修改。"),
        "",
        "## Issues / 问题点",
        "",
        *bullet_lines(issues, "No new issue entry was declared for this release note. / 本发布说明未声明新的问题条目。"),
        "",
        "## Fixes / 修复方式",
        "",
        *bullet_lines(fixes, "No fix entry was declared for this release note. / 本发布说明未声明新的修复条目。"),
        "",
        "## QA And Evidence / QA 与证据",
        "",
        *[f"- source_epub_{item['edition_type']}: `{item['source_epub']}`" for item in release_artifacts],
        f"- random_spotcheck_round: `{summary.get('random_spotcheck_round') or 'MISSING'}`",
        f"- random_spotcheck_validation: `{summary.get('random_spotcheck_validation') or 'MISSING'}`",
        f"- random_spotcheck_status: `{summary.get('random_spotcheck_status') or 'MISSING'}`",
        f"- random_spotcheck_require_pass: `{summary.get('random_spotcheck_require_pass')}`",
        f"- current_review_run_id: `{summary.get('current_review_run_id') or 'MISSING'}`",
        f"- current_run_pass_rounds: `{summary.get('current_run_pass_rounds_count')}/{summary.get('current_run_pass_rounds_required')}`",
        f"- release_confidence: `{summary.get('release_confidence') if summary.get('release_confidence') is not None else 'MISSING'}`",
        f"- epubcheck: `{summary.get('epubcheck_path') or 'MISSING'}`",
        f"- epubcheck_fatal: `{summary.get('epubcheck_fatal') if summary.get('epubcheck_fatal') is not None else 'MISSING'}`",
        f"- epubcheck_error: `{summary.get('epubcheck_error') if summary.get('epubcheck_error') is not None else 'MISSING'}`",
        f"- epubcheck_warning: `{summary.get('epubcheck_warning') if summary.get('epubcheck_warning') is not None else 'MISSING'}`",
        *[
            f"- epubcheck_{item.get('edition_type')}: `{item.get('report_path') or 'MISSING'}` artifact_sha256=`{item.get('artifact_sha256') or 'MISSING'}` hash_match=`{item.get('hash_match')}`"
            for item in summary.get("epubcheck_records", [])
        ],
        f"- translation_artifact_gate: `{summary.get('translation_artifact_gate_path') or 'MISSING'}`",
        f"- translation_artifact_gate_status: `{summary.get('translation_artifact_gate_status') or 'MISSING'}`",
        f"- real_reader_validation_status: `{summary.get('translation_artifact_reader_status') or 'MISSING'}`",
        f"- publication_lint: `{summary.get('publication_lint_path') or 'MISSING'}`",
        f"- publication_lint_issue_count: `{summary.get('publication_lint_issue_count') if summary.get('publication_lint_issue_count') is not None else 'MISSING'}`",
        f"- translation_metrics: `{summary.get('translation_metrics_path') or 'MISSING'}`",
        f"- translation_metrics_estimate_status: `{summary.get('translation_metrics_estimate_status') or 'MISSING'}`",
        f"- translation_metrics_actual_status: `{summary.get('translation_metrics_actual_status') or 'MISSING'}`",
        f"- translation_metrics_primary_book_type: `{summary.get('translation_metrics_primary_book_type') or 'MISSING'}`",
        f"- translation_metrics_difficulty_level: `{summary.get('translation_metrics_difficulty_level') or 'MISSING'}`",
        f"- translation_metrics_actual_difficulty_level: `{summary.get('translation_metrics_actual_difficulty_level') or 'MISSING'}`",
        f"- translation_metrics_actual_active_hours: `{summary.get('translation_metrics_actual_active_hours') if summary.get('translation_metrics_actual_active_hours') is not None else 'MISSING'}`",
        f"- translation_metrics_total_tokens: `{(summary.get('translation_metrics_total_input_tokens') or 0) + (summary.get('translation_metrics_total_output_tokens') or 0)}`",
        f"- literary_style_review: `{summary.get('literary_style_review_path') or 'MISSING'}`",
        f"- literary_style_status: `{summary.get('literary_style_status') or 'MISSING'}`",
        f"- literary_target_only_reading_score: `{summary.get('literary_target_only_reading_score') if summary.get('literary_target_only_reading_score') is not None else 'MISSING'}`",
        f"- literary_read_aloud_awkward_sentence_count: `{summary.get('literary_read_aloud_awkward_sentence_count') if summary.get('literary_read_aloud_awkward_sentence_count') is not None else 'MISSING'}`",
        f"- literary_unresolved_style_debt_count: `{summary.get('literary_unresolved_style_debt_count') if summary.get('literary_unresolved_style_debt_count') is not None else 'MISSING'}`",
        f"- literary_literal_explanatory_style_debt_count: `{summary.get('literary_literal_explanatory_style_debt_count') if summary.get('literary_literal_explanatory_style_debt_count') is not None else 'MISSING'}`",
        f"- literary_high_impact_sections_reviewed: `{summary.get('literary_high_impact_sections_reviewed')}`",
        f"- literary_author_preface_and_first_chapter_reviewed: `{summary.get('literary_author_preface_and_first_chapter_reviewed')}`",
        "",
        "## Risks / 风险",
        "",
        *bullet_lines(risks, "If status is DRAFT, independent agent review or closure gates may still be incomplete. / 若状态为 DRAFT，独立 Agent 评审或闭环门禁可能尚未全部完成。"),
        "",
        "## Next Iteration / 下一轮迭代",
        "",
        "- Reader feedback, review comments, or automated QA findings should create the next patch release. / 后续读者反馈、审校意见或自动化 QA 发现的问题应进入下一个小版本发布。",
        "- Patch version increases by 1 for every release artifact created by this script. / 本脚本每创建一次发布产物，小版本号递增 1。",
        "",
    ]
    prepend_release_note(release_note, "\n".join(note))

    new_state = {
        "current_version": version,
        "main_version": main_version,
        "sub_version": sub_version,
        "patch_version": patch_version,
        "latest_epub": release_artifacts[0]["epub"],
        "latest_epubs": release_artifacts,
        "latest_release_note": note_name,
        "latest_status": args.status,
        "latest_created_at": created_at,
        "latest_sha256": release_artifacts[0]["sha256"],
        "latest_size_bytes": release_artifacts[0]["size_bytes"],
        "gate_summary": summary,
    }
    write_json(state_path, new_state)
    for item in release_artifacts:
        append_release_index(release_dir / "release_index.md", version, item["epub"], note_name, args.status, created_at)

    for item in release_artifacts:
        print(f"created {rel_or_abs(book_root, release_dir / item['epub'])}")
    print(f"updated {rel_or_abs(book_root, release_note)}")
    print(f"version={version}")


if __name__ == "__main__":
    main()

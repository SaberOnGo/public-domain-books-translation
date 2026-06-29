from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path


DEFAULT_BOOK_ROOT = Path(__file__).resolve().parents[1]
RISK_BOUNDARY = (
    "仅供个人自用，不传播，不商业使用。风险由个人承担。"
    "public-domain-books-translation 开源项目仅用于公版书翻译发布，不承担其他个人翻译、保存、传播或使用非公版内容导致的版权风险及责任。"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a versioned private-use EPUB artifact.")
    parser.add_argument("--book-root", default=None, help="Book project root. Defaults to the parent of scripts/.")
    parser.add_argument("--source-epub", default="output/book.epub", help="Source EPUB path relative to the book root.")
    parser.add_argument("--artifact-dir", default="output/private_artifacts", help="Private artifact directory relative to the book root.")
    parser.add_argument("--version", default=None, help="Explicit version such as v0.0.1. Defaults to next patch version.")
    parser.add_argument("--status", choices=("DRAFT", "PASS"), default="DRAFT", help="Private artifact status.")
    parser.add_argument("--require-pass", action="store_true", help="Require PASS gate records before creating PASS artifact.")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite an existing private artifact for the same version.")
    return parser.parse_args()


def resolve_book_root(value: str | None) -> Path:
    return (Path(value) if value else DEFAULT_BOOK_ROOT).resolve()


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_book_title(book_root: Path) -> str:
    metadata_path = book_root / "metadata" / "book.yaml"
    if not metadata_path.exists():
        return "book"
    for line in metadata_path.read_text(encoding="utf-8", errors="replace").splitlines():
        match = re.match(r"^\s*title\s*:\s*(.+?)\s*$", line)
        if match:
            value = match.group(1).strip().strip("\"'")
            return value or "book"
    return "book"


def safe_filename(value: str) -> str:
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
    return safe_filename(value)


def edition_private_suffix(edition: dict, state: dict) -> str:
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


def rel_or_abs(book_root: Path, path: Path) -> str:
    try:
        return path.relative_to(book_root).as_posix()
    except ValueError:
        return str(path)


def parse_version(value: str) -> tuple[int, int, int]:
    clean = value[1:] if value.startswith("v") else value
    parts = clean.split(".")
    if len(parts) != 3:
        raise SystemExit(f"version must use vX.Y.Z: {value}")
    return int(parts[0]), int(parts[1]), int(parts[2])


def format_version(main: int, sub: int, patch: int) -> str:
    return f"v{main}.{sub}.{patch}"


def next_version(state: dict) -> tuple[int, int, int, str]:
    if state:
        main = int(state.get("main_version", 0))
        sub = int(state.get("sub_version", 0))
        patch = int(state.get("patch_version", 0)) + 1
    else:
        main, sub, patch = 0, 0, 1
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


def gate_summary(book_root: Path) -> dict:
    round_dir = latest_round_dir(book_root)
    validation_report = round_dir / "validation_report.json" if round_dir else None
    validation = read_json(validation_report) if validation_report else {}
    epubcheck = read_json(book_root / "output" / "epubcheck.json")
    lint = read_json(book_root / "output" / "publication_lint.json")
    private_gate = read_json(book_root / "output" / "private_use_gate.json")
    private_reader = read_json(book_root / "output" / "private_reader_facing_policy_check.json")
    epubcheck_checker = epubcheck.get("checker", {}) if isinstance(epubcheck, dict) else {}
    lint_issues = lint.get("issues", []) if isinstance(lint, dict) else []
    return {
        "random_spotcheck_status": validation.get("status", ""),
        "random_spotcheck_require_pass": bool(validation.get("require_pass", False)),
        "current_review_run_id": validation.get("current_review_run_id", ""),
        "current_run_pass_rounds_required": int(validation.get("current_run_pass_rounds_required", 0) or 0),
        "current_run_pass_rounds_count": int(validation.get("current_run_pass_rounds_count", 0) or 0),
        "release_confidence": validation.get("release_confidence"),
        "epubcheck_fatal": int(epubcheck_checker.get("nFatal", 0)) if epubcheck_checker else None,
        "epubcheck_error": int(epubcheck_checker.get("nError", 0)) if epubcheck_checker else None,
        "publication_lint_issue_count": len(lint_issues) if lint else None,
        "private_use_gate_ok": private_gate.get("ok") if private_gate else None,
        "private_reader_gate_ok": private_reader.get("ok") if private_reader else None,
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
    if summary.get("epubcheck_fatal") not in (0, None) or summary.get("epubcheck_error") not in (0, None):
        errors.append("EPUBCheck fatal/error count is not zero")
    if summary.get("publication_lint_issue_count") not in (0, None):
        errors.append("publication lint has unresolved issues")
    if summary.get("private_use_gate_ok") is not True:
        errors.append("private-use gate did not pass")
    if summary.get("private_reader_gate_ok") is not True:
        errors.append("private reader-facing gate did not pass")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        raise SystemExit(1)


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


def append_index(path: Path, version: str, artifact_name: str, status: str, created_at: str) -> None:
    if not path.exists():
        path.write_text(
            "# Private Artifact Index / 私人产物索引\n\n| version | status | artifact | created_at |\n| --- | --- | --- | --- |\n",
            encoding="utf-8",
            newline="\n",
        )
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(f"| {version} | {status} | `{artifact_name}` | {created_at} |\n")


def prepend_note(path: Path, entry: str) -> None:
    title = "# Private Artifact Notes / 私人产物说明"
    if not path.exists():
        path.write_text(f"{title}\n\n{entry}", encoding="utf-8", newline="\n")
        return
    old = path.read_text(encoding="utf-8")
    rest = old[len(title):].lstrip() if old.startswith(title) else old
    path.write_text(f"{title}\n\n{entry}\n\n{rest}", encoding="utf-8", newline="\n")


def main() -> None:
    args = parse_args()
    book_root = resolve_book_root(args.book_root)
    source_epub = (book_root / args.source_epub).resolve() if not Path(args.source_epub).is_absolute() else Path(args.source_epub).resolve()
    artifact_dir = (book_root / args.artifact_dir).resolve() if not Path(args.artifact_dir).is_absolute() else Path(args.artifact_dir).resolve()
    state_path = artifact_dir / "private_artifact_state.json"
    state = read_json(state_path)
    if args.version:
        main_version, sub_version, patch_version = parse_version(args.version)
        version = format_version(main_version, sub_version, patch_version)
    else:
        main_version, sub_version, patch_version, version = next_version(state)

    summary = gate_summary(book_root)
    if args.require_pass or args.status == "PASS":
        require_pass_gates(summary)

    artifact_dir.mkdir(parents=True, exist_ok=True)
    title = safe_filename(read_book_title(book_root))
    created_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    editions, pipeline_state = enabled_output_editions(book_root, source_epub)
    private_artifacts: list[dict] = []
    for edition in editions:
        suffix = edition_private_suffix(edition, pipeline_state)
        artifact_name = f"{title}_private{suffix}_{version}.epub"
        target = artifact_dir / artifact_name
        if target.exists() and not args.overwrite:
            raise SystemExit(
                f"private artifact already exists for {version}: {artifact_name}; create the next patch version or pass --overwrite deliberately"
            )
        shutil.copy2(edition["source"], target)
        private_artifacts.append(
            {
                "edition_type": edition["edition_type"],
                "source_epub": edition["source_label"],
                "artifact": artifact_name,
                "sha256": sha256(target),
                "size_bytes": target.stat().st_size,
            }
        )
    entry = "\n".join(
        [
            f"## Private Artifact {version} / 私人产物 {version}",
            "",
            f"status: {args.status}",
            f"created_at: {created_at}",
            "epubs:",
            *[f"- {item['edition_type']}: `{item['artifact']}` sha256=`{item['sha256']}` size_bytes=`{item['size_bytes']}`" for item in private_artifacts],
            "",
            "## Use Boundary / 使用边界",
            "",
            RISK_BOUNDARY,
            "",
            "This is a private personal-study artifact, not a public release. Do not publish it to GitHub.",
            "",
        ]
    )
    notes_path = artifact_dir / "private_artifact_notes.md"
    prepend_note(notes_path, entry)
    for item in private_artifacts:
        append_index(artifact_dir / "private_artifact_index.md", version, item["artifact"], args.status, created_at)
    write_json(
        state_path,
        {
            "latest_version": version,
            "latest_status": args.status,
            "main_version": main_version,
            "sub_version": sub_version,
            "patch_version": patch_version,
            "latest_artifact": private_artifacts[0]["artifact"],
            "latest_artifacts": private_artifacts,
            "latest_sha256": private_artifacts[0]["sha256"],
            "artifact_visibility": "private_use_only",
            "public_release": False,
            "github_publish_allowed": False,
            "risk_boundary": RISK_BOUNDARY,
            "gate_summary": summary,
            "updated_at": created_at,
        },
    )
    for item in private_artifacts:
        print(f"created private artifact: {(artifact_dir / item['artifact']).relative_to(book_root).as_posix()}")


if __name__ == "__main__":
    main()

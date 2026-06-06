from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


DEFAULT_BOOK_ROOT = Path(__file__).resolve().parents[1]
NUMBERED_BOOK_DIR = re.compile(r"^\d+_[A-Za-z0-9][A-Za-z0-9._-]*$")

REQUIRED_SPEC_TOKENS = [
    "template/epub_pipeline/common/preproduction/stage1/_TEMPLATE.production_spec.md",
    "template/epub_pipeline/common/references/cover_design_policy.md",
    "template/epub_pipeline/common/references/book_info_frontmatter_policy.md",
    "template/epub_pipeline/common/references/epub_assets_figures_tables.md",
    "template/epub_pipeline/common/references/quality_gate_framework.md",
]

REQUIRED_PACKAGE_SCRIPTS = [
    "preflight:template",
    "check:chapter-controls",
    "cover:check",
    "reader:check",
    "lint:publication",
    "lint:assets",
    "build:epub",
    "release:draft",
    "release:create",
]

REQUIRED_GLOSSARY_COLUMNS = {
    "type",
    "source_term",
    "target_term",
    "display_policy",
    "note_text",
    "exception_reason",
    "forbidden_body_renderings",
}

TERM_TYPES_REQUIRING_DISPLAY_POLICY = {
    "historical_term",
    "technical_term",
    "industry_term",
    "symbol",
}

REQUIRED_LOCAL_REFERENCES = [
    "references/cover_design_policy.md",
    "references/book_info_frontmatter_policy.md",
    "references/epub_assets_figures_tables.md",
    "references/quality_gate_framework.md",
    "references/release_versioning.md",
]

PRIVATE_USE_SPEC_TOKEN = "template/epub_pipeline/modes/private_use/preproduction/stage1/_TEMPLATE.private_use_production_spec.md"

PRIVATE_USE_REQUIRED_FILES = [
    "references/private_use_cover_policy.md",
    "references/private_use_frontmatter_policy.md",
    "references/private_use_artifact_policy.md",
    "preproduction/stage1/_TEMPLATE.private_use_production_spec.md",
    "scripts/check_private_use_gate.py",
    "scripts/check_private_reader_facing_policy.py",
    "scripts/create_private_artifact.py",
    "scripts/build_private_epub.js",
]

PRIVATE_USE_PACKAGE_SCRIPTS = [
    "preflight:private-use",
    "reader:private-check",
    "build:private-epub",
    "private:artifact:draft",
    "private:artifact:create",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check that a book project is using the standard template workflow gate.")
    parser.add_argument("--book-root", default=None, help="Book project root. Defaults to the parent of scripts/.")
    parser.add_argument("--write-report", action="store_true", help="Write output/template_workflow_gate.json.")
    parser.add_argument("--chapter-controls-only", action="store_true", help="Only validate translated/final chapter control closure.")
    return parser.parse_args()


def resolve_book_root(value: str | None) -> Path:
    return (Path(value) if value else DEFAULT_BOOK_ROOT).resolve()


def find_repo_root(book_root: Path) -> Path | None:
    for candidate in [book_root, *book_root.parents]:
        if (candidate / "books").is_dir() and (candidate / "template").is_dir():
            return candidate
    return None


def display_root(book_root: Path, repo_root: Path | None) -> str:
    if repo_root is None:
        return "."
    try:
        return book_root.relative_to(repo_root).as_posix()
    except ValueError:
        return "."


def rel(book_root: Path, path: Path) -> str:
    try:
        return path.relative_to(book_root).as_posix()
    except ValueError:
        return str(path)


def add_issue(issues: list[dict], rule: str, detail: str, path: str = "") -> None:
    issues.append({"rule": rule, "path": path, "detail": detail})


def read_state_data(book_root: Path, issues: list[dict]) -> dict:
    state_path = book_root / "state" / "pipeline_state.json"
    if not state_path.exists():
        add_issue(issues, "missing_pipeline_state", "Missing state/pipeline_state.json.", rel(book_root, state_path))
        return {}
    try:
        return json.loads(state_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        add_issue(issues, "invalid_pipeline_state_json", f"Cannot parse pipeline_state.json: {exc}", rel(book_root, state_path))
        return {}


def check_numbered_project_path(book_root: Path, repo_root: Path | None, state_data: dict, issues: list[dict]) -> None:
    if repo_root is None:
        add_issue(issues, "repo_root_not_found", "Cannot find repository root containing books/ and template/.")
        return
    books_root = repo_root / "books"
    try:
        relative = book_root.relative_to(books_root)
    except ValueError:
        add_issue(issues, "book_root_outside_books", "Book project root must be under books/{target}/{number}_{target_language_title}_{target_language_author}.", str(book_root))
        return
    parts = relative.parts
    publication_mode = state_data.get("publication_mode", "public_domain")
    if len(parts) == 3 and parts[0] == "private":
        if publication_mode != "private_use":
            add_issue(
                issues,
                "private_project_without_private_mode",
                "Book projects under books/private/ require publication_mode=private_use.",
                relative.as_posix(),
            )
            return
        target, project_dir = parts[1], parts[2]
    elif len(parts) == 2:
        if publication_mode == "private_use":
            add_issue(
                issues,
                "private_mode_outside_private_tree",
                "publication_mode=private_use projects must be under books/private/{target}/{number}_{target_language_title}_{target_language_author}.",
                relative.as_posix(),
            )
            return
        target, project_dir = parts
    else:
        add_issue(issues, "book_root_not_numbered_target_project", "Book project root must be exactly books/{target}/{number}_{target_language_title}_{target_language_author} or books/private/{target}/{number}_{target_language_title}_{target_language_author}.", relative.as_posix())
        return
    if not target or target in {"scripts", "node_modules", "tools"}:
        add_issue(issues, "invalid_target_directory", "Target directory must be a language tag such as zh-Hans, en, ja, or es.", target)
    if not NUMBERED_BOOK_DIR.match(project_dir):
        add_issue(issues, "invalid_project_directory_name", "Project directory must start with a numeric prefix, for example 6_ptolemy_almagest.", project_dir)


def check_state(book_root: Path, repo_root: Path | None, state_data: dict, issues: list[dict]) -> None:
    state_path = book_root / "state" / "pipeline_state.json"
    if not state_data:
        return
    if repo_root is None:
        return
    expected = book_root.relative_to(repo_root).as_posix()
    actual = state_data.get("project_root")
    if actual != expected:
        add_issue(issues, "pipeline_state_project_root_mismatch", f"Expected project_root={expected!r}, found {actual!r}.", rel(book_root, state_path))
    if state_data.get("common_template_root") != "template/epub_pipeline/common":
        add_issue(issues, "missing_common_template_root_state", "pipeline_state.json must record common_template_root=template/epub_pipeline/common.", rel(book_root, state_path))


def production_specs(book_root: Path) -> list[Path]:
    stage1 = book_root / "preproduction" / "stage1"
    if not stage1.exists():
        return []
    return sorted(path for path in stage1.glob("*.md") if not path.name.startswith("_TEMPLATE"))


def check_production_spec(book_root: Path, state_data: dict, issues: list[dict]) -> None:
    specs = production_specs(book_root)
    if not specs:
        add_issue(issues, "missing_book_production_spec", "Missing a book-specific preproduction/stage1/*.md production spec.")
        return
    combined = "\n".join(path.read_text(encoding="utf-8", errors="replace") for path in specs)
    for token in REQUIRED_SPEC_TOKENS:
        if token not in combined:
            add_issue(issues, "production_spec_missing_template_basis", f"Production spec must explicitly cite {token}.", ", ".join(rel(book_root, path) for path in specs))
    publication_mode = state_data.get("publication_mode", "public_domain")
    if publication_mode == "private_use":
        if PRIVATE_USE_SPEC_TOKEN not in combined:
            add_issue(
                issues,
                "private_production_spec_missing_template_basis",
                f"Private-use production spec must explicitly cite {PRIVATE_USE_SPEC_TOKEN}.",
                ", ".join(rel(book_root, path) for path in specs),
            )
    elif PRIVATE_USE_SPEC_TOKEN in combined:
        add_issue(
            issues,
            "public_project_contains_private_use_reference",
            "Public projects must not cite the private-use production spec.",
            ", ".join(rel(book_root, path) for path in specs),
        )


def check_local_references(book_root: Path, issues: list[dict]) -> None:
    for reference in REQUIRED_LOCAL_REFERENCES:
        path = book_root / reference
        if not path.exists():
            add_issue(issues, "missing_local_common_reference", "Book project must carry the common reference file copied from the template.", reference)


def check_private_use_overlay_files(book_root: Path, state_data: dict, issues: list[dict]) -> None:
    publication_mode = state_data.get("publication_mode", "public_domain")
    found_private_files = [path for path in PRIVATE_USE_REQUIRED_FILES if (book_root / path).exists()]
    if publication_mode == "private_use":
        for path in PRIVATE_USE_REQUIRED_FILES:
            if not (book_root / path).exists():
                add_issue(
                    issues,
                    "missing_private_use_overlay_file",
                    "Private-use projects must carry the private_use mode overlay copied from template/epub_pipeline/modes/private_use/.",
                    path,
                )
    elif found_private_files:
        add_issue(
            issues,
            "public_project_contains_private_use_overlay",
            "Public projects must not contain private-use mode overlay files.",
            ", ".join(found_private_files),
        )


def check_package_scripts(book_root: Path, state_data: dict, issues: list[dict]) -> None:
    package_path = book_root / "package.json"
    if not package_path.exists():
        add_issue(issues, "missing_package_json", "Missing book-local package.json.", rel(book_root, package_path))
        return
    data = json.loads(package_path.read_text(encoding="utf-8"))
    scripts = data.get("scripts", {})
    for name in REQUIRED_PACKAGE_SCRIPTS:
        if name not in scripts:
            add_issue(issues, "missing_package_script", f"Missing package script {name!r}.", rel(book_root, package_path))
    publication_mode = state_data.get("publication_mode", "public_domain")
    if publication_mode == "private_use":
        for name in PRIVATE_USE_PACKAGE_SCRIPTS:
            if name not in scripts:
                add_issue(issues, "missing_private_package_script", f"Missing private-use package script {name!r}.", rel(book_root, package_path))
        if scripts.get("build:epub") != "npm run build:private-epub":
            add_issue(issues, "private_build_script_not_isolated", "Private-use build:epub must delegate to build:private-epub.", rel(book_root, package_path))
        private_build = scripts.get("build:private-epub", "")
        for required in ["preflight:template", "preflight:private-use", "lint:publication", "lint:assets", "cover:check", "reader:private-check", "build_private_epub.js"]:
            if required not in private_build:
                add_issue(issues, "private_build_script_missing_gate", f"build:private-epub must run {required}.", rel(book_root, package_path))
        private_release = scripts.get("private:artifact:create", "")
        for required in ["preflight:template", "preflight:private-use", "cover:check", "reader:private-check", "create_private_artifact.py", "--status PASS", "--require-pass"]:
            if required not in private_release:
                add_issue(issues, "private_artifact_script_missing_gate", f"private:artifact:create must run {required}.", rel(book_root, package_path))
        if scripts.get("release:create") != "npm run private:artifact:create":
            add_issue(issues, "private_release_alias_not_isolated", "Private-use release:create must delegate to private:artifact:create.", rel(book_root, package_path))
    else:
        for name in PRIVATE_USE_PACKAGE_SCRIPTS:
            if name in scripts:
                add_issue(issues, "public_project_contains_private_package_script", f"Public projects must not define private-use package script {name!r}.", rel(book_root, package_path))
        build = scripts.get("build:epub", "")
        for required in ["preflight:template", "lint:publication", "lint:assets", "cover:check", "reader:check"]:
            if required not in build:
                add_issue(issues, "build_script_missing_gate", f"build:epub must run {required}.", rel(book_root, package_path))
        for release_name in ["release:draft", "release:create"]:
            command = scripts.get(release_name, "")
            for required in ["preflight:template", "cover:check", "reader:check"]:
                if required not in command:
                    add_issue(issues, "release_script_missing_gate", f"{release_name} must run {required}.", rel(book_root, package_path))


def pass_marker_found(text: str, marker_names: tuple[str, ...]) -> bool:
    for marker in marker_names:
        pattern = rf"(?im)^\s*{re.escape(marker)}\s*[:=]\s*[\"']?PASS[\"']?\s*(?:#.*)?$"
        if re.search(pattern, text):
            return True
    if re.search(r"(?im)^结论\s*[:：]\s*PASS\s*$", text):
        return True
    if re.search(r"(?im)^PASS\s*$", text):
        return True
    return False


def true_marker_found(text: str, marker_names: tuple[str, ...]) -> bool:
    for marker in marker_names:
        pattern = rf"(?im)^\s*{re.escape(marker)}\s*[:=]\s*[`\"']?true[`\"']?\s*(?:#.*)?$"
        if re.search(pattern, text):
            return True
    return False


def latest_scalar_value(text: str, marker: str) -> str | None:
    pattern = rf"(?im)^\s*-?\s*{re.escape(marker)}\s*[:=]\s*[`\"']?([^`\"'\r\n#]+)[`\"']?\s*(?:#.*)?$"
    matches = re.findall(pattern, text)
    if not matches:
        return None
    return matches[-1].strip()


def latest_int_value(text: str, marker: str) -> int | None:
    value = latest_scalar_value(text, marker)
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def split_round_blocks(text: str) -> list[str]:
    starts = [match.start() for match in re.finditer(r"(?im)^\s{0,3}#{1,6}\s*round\b|^\s*-\s*round\s*[:=]", text)]
    if not starts:
        return []
    blocks = []
    for index, start in enumerate(starts):
        end = starts[index + 1] if index + 1 < len(starts) else len(text)
        blocks.append(text[start:end])
    return blocks


def check_chapter_control_closure(
    book_root: Path,
    control: Path,
    issues: list[dict],
    *,
    translated_chapter: Path | None = None,
) -> None:
    if not control.exists():
        detail = "Every translated/final chapter must have qa/chapter_controls/{chapter}.control.md."
        if translated_chapter is not None:
            detail = (
                "Every chapters/translated chapter must immediately close the per-chapter post-translation "
                "full-check gate before the next chapter may be translated."
            )
        add_issue(issues, "missing_chapter_post_translation_control", detail, rel(book_root, control))
        return

    text = control.read_text(encoding="utf-8", errors="replace")
    latest_status = latest_scalar_value(text, "latest_round_status") or latest_scalar_value(text, "control_status") or latest_scalar_value(text, "status")
    latest_allow = latest_scalar_value(text, "allow_next_chapter")
    latest_scope = latest_scalar_value(text, "scope") or latest_scalar_value(text, "checked_scope")
    latest_issues = latest_int_value(text, "issues_found")
    latest_fixes = latest_int_value(text, "fixes_applied")
    latest_unresolved = latest_int_value(text, "unresolved_blocking_issues")
    latest_expert_used = latest_scalar_value(text, "expert_translation_skill_used")
    latest_expert_status = latest_scalar_value(text, "expert_level_review_status")
    latest_polysemy_translation_status = latest_scalar_value(text, "polysemy_translation_stage_review")
    latest_polysemy_status = latest_scalar_value(text, "polysemy_context_review")
    latest_polysemy_unresolved = latest_int_value(text, "polysemy_unresolved_count")

    if latest_status != "PASS":
        add_issue(
            issues,
            "chapter_post_translation_control_not_pass",
            "Latest chapter post-translation full-check round must set latest_round_status: PASS.",
            rel(book_root, control),
        )
    if latest_allow != "true":
        add_issue(
            issues,
            "chapter_post_translation_control_not_closed",
            "Latest chapter post-translation full-check round must set allow_next_chapter: true.",
            rel(book_root, control),
        )
    if latest_scope != "FULL_CHAPTER":
        add_issue(
            issues,
            "chapter_post_translation_control_not_full_chapter",
            "Latest chapter post-translation check must record scope: FULL_CHAPTER.",
            rel(book_root, control),
        )
    if latest_issues != 0:
        add_issue(
            issues,
            "chapter_post_translation_control_latest_round_has_issues",
            "Latest full-chapter check must record issues_found: 0.",
            rel(book_root, control),
        )
    if latest_fixes != 0:
        add_issue(
            issues,
            "chapter_post_translation_control_latest_round_has_fixes",
            "A round that applied fixes cannot be the PASS round; append a new full-chapter recheck with fixes_applied: 0.",
            rel(book_root, control),
        )
    if latest_unresolved != 0:
        add_issue(
            issues,
            "chapter_post_translation_control_has_unresolved_blockers",
            "Latest full-chapter check must record unresolved_blocking_issues: 0.",
            rel(book_root, control),
        )
    if not re.search(r"中文|可读|润色|流畅|通俗|polish|readability", text, re.IGNORECASE):
        add_issue(
            issues,
            "chapter_post_translation_control_missing_readability_polish_scope",
            "Control file must explicitly record target-language readability/polish/naturalness review, not only semantic fidelity.",
            rel(book_root, control),
        )
    if latest_expert_used != "true":
        add_issue(
            issues,
            "chapter_post_translation_control_missing_expert_translation_skill",
            "Latest full-chapter check must record expert_translation_skill_used: true after using skills/expert-translation-quality/SKILL.md.",
            rel(book_root, control),
        )
    if latest_expert_status != "PASS":
        add_issue(
            issues,
            "chapter_post_translation_control_expert_review_not_pass",
            "Latest full-chapter check must record expert_level_review_status: PASS.",
            rel(book_root, control),
        )
    if latest_polysemy_translation_status != "PASS":
        add_issue(
            issues,
            "chapter_post_translation_control_polysemy_translation_stage_not_pass",
            "Latest full-chapter check must record polysemy_translation_stage_review: PASS to confirm translation-stage polysemy handling was audited.",
            rel(book_root, control),
        )
    if latest_polysemy_status != "PASS":
        add_issue(
            issues,
            "chapter_post_translation_control_polysemy_review_not_pass",
            "Latest full-chapter check must record polysemy_context_review: PASS.",
            rel(book_root, control),
        )
    if latest_polysemy_unresolved != 0:
        add_issue(
            issues,
            "chapter_post_translation_control_polysemy_unresolved",
            "Latest full-chapter check must record polysemy_unresolved_count: 0.",
            rel(book_root, control),
        )

    for block in split_round_blocks(text):
        round_issues = latest_int_value(block, "issues_found") or 0
        round_fixes = latest_int_value(block, "fixes_applied") or 0
        round_status = latest_scalar_value(block, "latest_round_status") or latest_scalar_value(block, "status")
        round_expert_status = latest_scalar_value(block, "expert_level_review_status")
        round_polysemy_translation_status = latest_scalar_value(block, "polysemy_translation_stage_review")
        round_polysemy_status = latest_scalar_value(block, "polysemy_context_review")
        round_polysemy_unresolved = latest_int_value(block, "polysemy_unresolved_count")
        if (round_issues > 0 or round_fixes > 0) and round_status == "PASS":
            add_issue(
                issues,
                "chapter_post_translation_control_fix_round_marked_pass",
                "A round that found issues or applied fixes must be FIXED_RECHECK_REQUIRED, not PASS; append a fresh full-chapter recheck.",
                rel(book_root, control),
            )
        if round_status == "PASS" and (
            round_expert_status != "PASS"
            or round_polysemy_translation_status != "PASS"
            or round_polysemy_status != "PASS"
            or round_polysemy_unresolved != 0
        ):
            add_issue(
                issues,
                "chapter_post_translation_control_pass_without_expert_polysemy_closure",
                "A PASS round must also close expert-level review, translation-stage polysemy handling, and polysemy context review with zero unresolved polysemy items.",
                rel(book_root, control),
            )


def reader_body_without_notes(text: str) -> str:
    note_heading = re.compile(r"(?im)^\s{0,3}#{1,6}\s*(译注|注释|脚注|尾注|术语说明|术语表|notes|endnotes|footnotes)\b.*$")
    match = note_heading.search(text)
    if match:
        text = text[: match.start()]
    kept_lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if re.match(r"^\[\^?.+?\]\s*[:：]", stripped):
            continue
        kept_lines.append(line)
    return "\n".join(kept_lines)


def split_forbidden_renderings(value: str) -> list[str]:
    return [item.strip() for item in re.split(r"[|；;]", value or "") if item.strip()]


def check_glossary_schema_and_forbidden_renderings(book_root: Path, issues: list[dict]) -> None:
    glossary_path = book_root / "glossary" / "terms.csv"
    if not glossary_path.exists():
        return
    try:
        with glossary_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fieldnames = set(reader.fieldnames or [])
            missing = sorted(REQUIRED_GLOSSARY_COLUMNS - fieldnames)
            if missing:
                add_issue(
                    issues,
                    "glossary_terms_missing_display_columns",
                    f"glossary/terms.csv must include columns for term display policy and forbidden body renderings: {', '.join(missing)}.",
                    rel(book_root, glossary_path),
                )
                return
            rows = list(reader)
    except csv.Error as exc:
        add_issue(issues, "glossary_terms_csv_invalid", f"Could not parse glossary/terms.csv: {exc}", rel(book_root, glossary_path))
        return

    for index, row in enumerate(rows, start=2):
        term_type = (row.get("type") or "").strip()
        source_term = (row.get("source_term") or "").strip()
        target_term = (row.get("target_term") or "").strip()
        display_policy = (row.get("display_policy") or "").strip()
        if term_type in TERM_TYPES_REQUIRING_DISPLAY_POLICY and (source_term or target_term) and not display_policy:
            add_issue(
                issues,
                "glossary_term_missing_display_policy",
                f"High-risk term row {index} must set display_policy.",
                rel(book_root, glossary_path),
            )
        if display_policy == "body_parenthetical_exception" and not (row.get("exception_reason") or "").strip():
            add_issue(
                issues,
                "glossary_term_parenthetical_exception_without_reason",
                f"Term row {index} allows body parenthetical source terms but has no exception_reason.",
                rel(book_root, glossary_path),
            )

    final_dir = book_root / "chapters" / "final"
    if not final_dir.exists():
        return
    final_bodies = []
    for chapter in sorted(path for path in final_dir.glob("*.md") if not path.name.startswith("_")):
        text = reader_body_without_notes(chapter.read_text(encoding="utf-8", errors="replace"))
        final_bodies.append((chapter, text))
    if not final_bodies:
        return

    for index, row in enumerate(rows, start=2):
        for forbidden in split_forbidden_renderings(row.get("forbidden_body_renderings") or ""):
            for chapter, body in final_bodies:
                if forbidden and forbidden in body:
                    add_issue(
                        issues,
                        "glossary_forbidden_body_rendering_found",
                        f"Forbidden body rendering from glossary row {index} appears in chapter body: {forbidden!r}. Move source-term explanation to notes/glossary or revise the term.",
                        rel(book_root, chapter),
                    )


def check_chapter_quality_artifacts(book_root: Path, issues: list[dict]) -> None:
    translated_dir = book_root / "chapters" / "translated"
    controls_dir = book_root / "qa" / "chapter_controls"
    if translated_dir.exists():
        translated_chapters = sorted(path for path in translated_dir.glob("*.md") if not path.name.startswith("_"))
        for chapter in translated_chapters:
            control = controls_dir / f"{chapter.stem}.control.md"
            check_chapter_control_closure(book_root, control, issues, translated_chapter=chapter)

    final_dir = book_root / "chapters" / "final"
    if not final_dir.exists():
        return
    final_chapters = sorted(path for path in final_dir.glob("*.md") if not path.name.startswith("_"))
    if not final_chapters:
        return
    controls_dir = book_root / "qa" / "chapter_controls"
    gates_dir = book_root / "qa" / "gates"
    for chapter in final_chapters:
        control = controls_dir / f"{chapter.stem}.control.md"
        check_chapter_control_closure(book_root, control, issues)
        gate = gates_dir / f"{chapter.stem}.gate.md"
        if not gate.exists():
            add_issue(
                issues,
                "missing_chapter_quality_gate",
                "Every chapters/final chapter must have qa/gates/{chapter}.gate.md.",
                rel(book_root, gate),
            )
        else:
            text = gate.read_text(encoding="utf-8", errors="replace")
            if not pass_marker_found(text, ("gate_status", "status")):
                add_issue(
                    issues,
                    "chapter_quality_gate_not_pass",
                    "Chapter quality gate must be PASS before the chapter can remain in chapters/final or the workflow can continue.",
                    rel(book_root, gate),
                )


def main() -> None:
    args = parse_args()
    book_root = resolve_book_root(args.book_root)
    repo_root = find_repo_root(book_root)
    issues: list[dict] = []
    state_data = read_state_data(book_root, issues)

    if not args.chapter_controls_only:
        check_numbered_project_path(book_root, repo_root, state_data, issues)
        check_state(book_root, repo_root, state_data, issues)
        check_production_spec(book_root, state_data, issues)
        check_local_references(book_root, issues)
        check_private_use_overlay_files(book_root, state_data, issues)
        check_package_scripts(book_root, state_data, issues)
        check_glossary_schema_and_forbidden_renderings(book_root, issues)
    check_chapter_quality_artifacts(book_root, issues)

    report = {
        "book_root": display_root(book_root, repo_root),
        "repo_root": ".",
        "ok": not issues,
        "issues": issues,
    }
    if args.write_report:
        out = book_root / "output" / "template_workflow_gate.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if issues:
        for issue in issues:
            location = f" {issue['path']}" if issue.get("path") else ""
            print(f"ERROR {issue['rule']}:{location} {issue['detail']}")
        raise SystemExit(1)
    print("template workflow gate PASS")


if __name__ == "__main__":
    main()

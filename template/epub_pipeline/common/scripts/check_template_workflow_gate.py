from __future__ import annotations

import argparse
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
    "cover:check",
    "reader:check",
    "lint:publication",
    "lint:assets",
    "build:epub",
    "release:draft",
    "release:create",
]

REQUIRED_LOCAL_REFERENCES = [
    "references/cover_design_policy.md",
    "references/book_info_frontmatter_policy.md",
    "references/epub_assets_figures_tables.md",
    "references/quality_gate_framework.md",
    "references/release_versioning.md",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check that a book project is using the standard template workflow gate.")
    parser.add_argument("--book-root", default=None, help="Book project root. Defaults to the parent of scripts/.")
    parser.add_argument("--write-report", action="store_true", help="Write output/template_workflow_gate.json.")
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
        add_issue(issues, "book_root_outside_books", "Book project root must be under books/{target}/{number}_{slug}.", str(book_root))
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
                "publication_mode=private_use projects must be under books/private/{target}/{number}_{slug}.",
                relative.as_posix(),
            )
            return
        target, project_dir = parts
    else:
        add_issue(issues, "book_root_not_numbered_target_project", "Book project root must be exactly books/{target}/{number}_{slug} or books/private/{target}/{number}_{slug}.", relative.as_posix())
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


def check_production_spec(book_root: Path, issues: list[dict]) -> None:
    specs = production_specs(book_root)
    if not specs:
        add_issue(issues, "missing_book_production_spec", "Missing a book-specific preproduction/stage1/*.md production spec.")
        return
    combined = "\n".join(path.read_text(encoding="utf-8", errors="replace") for path in specs)
    for token in REQUIRED_SPEC_TOKENS:
        if token not in combined:
            add_issue(issues, "production_spec_missing_template_basis", f"Production spec must explicitly cite {token}.", ", ".join(rel(book_root, path) for path in specs))


def check_local_references(book_root: Path, issues: list[dict]) -> None:
    for reference in REQUIRED_LOCAL_REFERENCES:
        path = book_root / reference
        if not path.exists():
            add_issue(issues, "missing_local_common_reference", "Book project must carry the common reference file copied from the template.", reference)


def check_package_scripts(book_root: Path, issues: list[dict]) -> None:
    package_path = book_root / "package.json"
    if not package_path.exists():
        add_issue(issues, "missing_package_json", "Missing book-local package.json.", rel(book_root, package_path))
        return
    data = json.loads(package_path.read_text(encoding="utf-8"))
    scripts = data.get("scripts", {})
    for name in REQUIRED_PACKAGE_SCRIPTS:
        if name not in scripts:
            add_issue(issues, "missing_package_script", f"Missing package script {name!r}.", rel(book_root, package_path))
    build = scripts.get("build:epub", "")
    for required in ["preflight:template", "lint:publication", "lint:assets", "cover:check", "reader:check"]:
        if required not in build:
            add_issue(issues, "build_script_missing_gate", f"build:epub must run {required}.", rel(book_root, package_path))
    for release_name in ["release:draft", "release:create"]:
        command = scripts.get(release_name, "")
        for required in ["preflight:template", "cover:check", "reader:check"]:
            if required not in command:
                add_issue(issues, "release_script_missing_gate", f"{release_name} must run {required}.", rel(book_root, package_path))


def main() -> None:
    args = parse_args()
    book_root = resolve_book_root(args.book_root)
    repo_root = find_repo_root(book_root)
    issues: list[dict] = []
    state_data = read_state_data(book_root, issues)

    check_numbered_project_path(book_root, repo_root, state_data, issues)
    check_state(book_root, repo_root, state_data, issues)
    check_production_spec(book_root, issues)
    check_local_references(book_root, issues)
    check_package_scripts(book_root, issues)

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

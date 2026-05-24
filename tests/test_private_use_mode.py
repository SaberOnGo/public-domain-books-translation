from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def copy_script(src_relative: str, repo_root: Path) -> None:
    src = REPO_ROOT / src_relative
    dst = repo_root / src_relative
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def write_minimal_template(repo_root: Path) -> None:
    common = repo_root / "template" / "epub_pipeline" / "common"
    language = repo_root / "template" / "epub_pipeline" / "en-zh-Hans"
    targets = repo_root / "template" / "epub_pipeline" / "targets" / "zh-Hans"
    (common / "state").mkdir(parents=True, exist_ok=True)
    (common / "references").mkdir(parents=True, exist_ok=True)
    (common / "preproduction" / "stage1").mkdir(parents=True, exist_ok=True)
    language.mkdir(parents=True, exist_ok=True)
    targets.mkdir(parents=True, exist_ok=True)
    (common / "state" / "pipeline_state.json").write_text(
        json.dumps({"status": "INIT"}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (common / "package.json").write_text(
        json.dumps(
            {
                "scripts": {
                    "preflight:template": "python scripts/check_template_workflow_gate.py",
                    "cover:check": "python scripts/check_cover_output_assets.py",
                    "reader:check": "python scripts/check_reader_facing_policy.py",
                    "lint:publication": "node scripts/publication_lint.js",
                    "lint:assets": "node scripts/asset_manifest_check.js",
                    "build:epub": "npm run preflight:template && npm run lint:publication && npm run lint:assets && npm run cover:check && npm run reader:check",
                    "release:draft": "npm run preflight:template && npm run cover:check && npm run reader:check && python scripts/create_release.py --status DRAFT",
                    "release:create": "npm run preflight:template && npm run cover:check && npm run reader:check && python scripts/create_release.py --status PASS --require-pass",
                }
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    for name in [
        "cover_design_policy.md",
        "book_info_frontmatter_policy.md",
        "epub_assets_figures_tables.md",
        "quality_gate_framework.md",
        "release_versioning.md",
    ]:
        (common / "references" / name).write_text(f"# {name}\n", encoding="utf-8")


def write_production_spec(book_root: Path) -> None:
    spec = book_root / "preproduction" / "stage1" / "production_spec.md"
    spec.parent.mkdir(parents=True, exist_ok=True)
    spec.write_text(
        "\n".join(
            [
                "template/epub_pipeline/common/preproduction/stage1/_TEMPLATE.production_spec.md",
                "template/epub_pipeline/common/references/cover_design_policy.md",
                "template/epub_pipeline/common/references/book_info_frontmatter_policy.md",
                "template/epub_pipeline/common/references/epub_assets_figures_tables.md",
                "template/epub_pipeline/common/references/quality_gate_framework.md",
            ]
        )
        + "\n",
        encoding="utf-8",
    )


class PrivateUseModeTests(unittest.TestCase):
    def test_create_book_project_private_use_writes_ignored_private_tree_and_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            copy_script("books/scripts/create_book_project.py", repo)
            write_minimal_template(repo)
            local_source = repo / "local-source.epub"
            local_source.write_bytes(b"private source")

            result = subprocess.run(
                [
                    sys.executable,
                    str(repo / "books" / "scripts" / "create_book_project.py"),
                    "private_book",
                    "--source-target",
                    "en-zh-Hans",
                    "--mode",
                    "private-use",
                    "--local-source-file",
                    str(local_source),
                    "--private-use-declaration",
                    "personal study only; no redistribution; no commercial use",
                ],
                cwd=repo,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("books/private/zh-Hans/1_private_book", result.stdout)
            project_root = repo / "books" / "private" / "zh-Hans" / "1_private_book"
            state = json.loads((project_root / "state" / "pipeline_state.json").read_text(encoding="utf-8"))
            self.assertEqual(state["project_root"], "books/private/zh-Hans/1_private_book")
            self.assertEqual(state["publication_mode"], "private_use")
            self.assertEqual(state["private_use"]["local_source_file_name"], "local-source.epub")
            self.assertEqual(state["private_use"]["redistribution_allowed"], False)
            self.assertEqual(state["private_use"]["commercial_use_allowed"], False)
            self.assertTrue((project_root / "metadata" / "private_use_declaration.md").exists())

    def test_template_workflow_gate_accepts_private_path_only_for_private_use_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            copy_script("template/epub_pipeline/common/scripts/check_template_workflow_gate.py", repo)
            write_minimal_template(repo)
            book_root = repo / "books" / "private" / "zh-Hans" / "1_private_book"
            shutil.copytree(repo / "template" / "epub_pipeline" / "common", book_root)
            write_production_spec(book_root)
            state_path = book_root / "state" / "pipeline_state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state.update(
                {
                    "project_root": "books/private/zh-Hans/1_private_book",
                    "common_template_root": "template/epub_pipeline/common",
                    "template_root": "template/epub_pipeline/en-zh-Hans",
                    "publication_mode": "private_use",
                }
            )
            state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(repo / "template" / "epub_pipeline" / "common" / "scripts" / "check_template_workflow_gate.py"),
                    "--book-root",
                    str(book_root),
                ],
                cwd=repo,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("template workflow gate PASS", result.stdout)


if __name__ == "__main__":
    unittest.main()

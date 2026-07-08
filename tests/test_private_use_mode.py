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
    if src_relative.endswith("check_template_workflow_gate.py"):
        coverage_src = REPO_ROOT / "template/epub_pipeline/common/scripts/check_translation_coverage.py"
        coverage_dst = repo_root / "template/epub_pipeline/common/scripts/check_translation_coverage.py"
        shutil.copy2(coverage_src, coverage_dst)


def merge_package_scripts(package_path: Path, overlay_path: Path) -> None:
    package = json.loads(package_path.read_text(encoding="utf-8"))
    overlay = json.loads(overlay_path.read_text(encoding="utf-8"))
    scripts = dict(package.get("scripts", {}))
    scripts.update(overlay.get("scripts", {}))
    package["scripts"] = scripts
    package_path.write_text(json.dumps(package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_minimal_template(repo_root: Path) -> None:
    common = repo_root / "template" / "epub_pipeline" / "common"
    language = repo_root / "template" / "epub_pipeline" / "English-to-Simplified-Chinese"
    targets = repo_root / "template" / "epub_pipeline" / "targets" / "zh-Hans"
    mode = repo_root / "template" / "epub_pipeline" / "modes" / "private_use"
    (common / "state").mkdir(parents=True, exist_ok=True)
    (common / "references").mkdir(parents=True, exist_ok=True)
    (common / "preproduction" / "stage1").mkdir(parents=True, exist_ok=True)
    (common / "scripts").mkdir(parents=True, exist_ok=True)
    language.mkdir(parents=True, exist_ok=True)
    targets.mkdir(parents=True, exist_ok=True)
    (mode / "references").mkdir(parents=True, exist_ok=True)
    (mode / "preproduction" / "stage1").mkdir(parents=True, exist_ok=True)
    (mode / "scripts").mkdir(parents=True, exist_ok=True)
    (common / "state" / "pipeline_state.json").write_text(
        json.dumps(
            {
                "status": "INIT",
                "quality_gate": {"release_state": "output/release/release_state.json"},
                "forbidden_shortcuts": [
                    "declaring DONE before output/release/release_state.json latest_status is PASS"
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (common / "package.json").write_text(
        json.dumps(
            {
                "scripts": {
                    "check:translation-coverage": "python scripts/check_translation_coverage.py --write-report",
                    "preflight:template": "python scripts/check_template_workflow_gate.py",
                    "check:chapter-controls": "npm run check:translation-coverage && python scripts/check_template_workflow_gate.py --chapter-controls-only",
                    "cover:check": "python scripts/check_cover_output_assets.py",
                    "reader:check": "python scripts/check_reader_facing_policy.py",
                    "lint:publication": "node scripts/publication_lint.js",
                    "lint:assets": "node scripts/asset_manifest_check.js",
                    "literary:scan": "python scripts/check_literary_style_gate.py --write-report",
                    "literary:validate": "python scripts/check_literary_style_gate.py --write-report --require-review-pass",
                    "build:epub": "npm run preflight:template && npm run lint:publication && npm run lint:assets && npm run cover:check && npm run reader:check",
                    "release:draft": "npm run preflight:template && npm run cover:check && npm run reader:check && npm run literary:scan && python scripts/create_release.py --status DRAFT",
                    "release:create": "npm run preflight:template && npm run cover:check && npm run reader:check && npm run literary:validate && python scripts/create_release.py --status PASS --require-pass",
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
        "proper_noun_display_policy.md",
        "note_marker_policy.md",
    ]:
        (common / "references" / name).write_text(f"# {name}\n", encoding="utf-8")
    (mode / "README.md").write_text("# Private use mode\n", encoding="utf-8")
    (mode / "references" / "private_use_cover_policy.md").write_text(
        "# Private cover\n\n个人学习版\n", encoding="utf-8"
    )
    (mode / "references" / "private_use_frontmatter_policy.md").write_text(
        "# Private frontmatter\n\n参考public-domain-books-translation 开源项目 个人自制\n", encoding="utf-8"
    )
    (mode / "references" / "private_use_artifact_policy.md").write_text(
        "# Private artifacts\n", encoding="utf-8"
    )
    (mode / "preproduction" / "stage1" / "_TEMPLATE.private_use_production_spec.md").write_text(
        "# Private production spec\n", encoding="utf-8"
    )
    for name in [
        "check_private_use_gate.py",
        "check_private_reader_facing_policy.py",
        "create_private_artifact.py",
        "build_private_epub.js",
    ]:
        (mode / "scripts" / name).write_text("print('private script placeholder')\n", encoding="utf-8")
    (mode / "package.json").write_text(
        json.dumps(
            {
                "scripts": {
                    "preflight:private-use": "python scripts/check_private_use_gate.py --write-report",
                    "reader:private-check": "python scripts/check_private_reader_facing_policy.py --write-report",
                    "build:private-epub": "npm run preflight:template && npm run preflight:private-use && npm run lint:publication && npm run lint:assets && npm run cover:check && node scripts/build_private_epub.js && npm run reader:private-check",
                    "build:epub": "npm run build:private-epub",
                    "private:artifact:draft": "npm run preflight:template && npm run preflight:private-use && npm run cover:check && npm run reader:private-check && python scripts/create_private_artifact.py --status DRAFT",
                    "private:artifact:create": "npm run preflight:template && npm run preflight:private-use && npm run cover:check && npm run reader:private-check && python scripts/create_private_artifact.py --status PASS --require-pass",
                    "release:draft": "npm run private:artifact:draft",
                    "release:create": "npm run private:artifact:create",
                }
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (language / "package.json").write_text(
        json.dumps(
            {
                "scripts": {
                    "lint:publication": "node scripts/publication_lint.js --target=zh-Hans --write-report",
                    "fix:publication": "node scripts/publication_lint.js --target=zh-Hans --fix --write-report",
                }
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


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
                "template/epub_pipeline/common/references/proper_noun_display_policy.md",
                "template/epub_pipeline/common/references/note_marker_policy.md",
                "template/epub_pipeline/modes/private_use/preproduction/stage1/_TEMPLATE.private_use_production_spec.md",
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
                    "English-to-Simplified-Chinese",
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
            self.assertEqual(
                state["quality_gate"]["release_state"],
                "output/private_artifacts/private_artifact_state.json",
            )
            declaration = (project_root / "metadata" / "private_use_declaration.md").read_text(encoding="utf-8")
            self.assertIn("风险由个人承担", declaration)
            self.assertIn("public-domain-books-translation 开源项目仅用于公版书翻译发布", declaration)
            self.assertTrue((project_root / "references" / "private_use_cover_policy.md").exists())
            self.assertTrue((project_root / "references" / "private_use_frontmatter_policy.md").exists())
            self.assertTrue((project_root / "references" / "private_use_artifact_policy.md").exists())
            self.assertTrue((project_root / "scripts" / "check_private_use_gate.py").exists())
            self.assertTrue((project_root / "scripts" / "create_private_artifact.py").exists())
            package = json.loads((project_root / "package.json").read_text(encoding="utf-8"))
            self.assertIn("private:artifact:create", package["scripts"])
            self.assertEqual(package["scripts"]["release:create"], "npm run private:artifact:create")
            self.assertIn("--target=zh-Hans", package["scripts"]["lint:publication"])
            self.assertIn("--target=zh-Hans", package["scripts"]["fix:publication"])
            self.assertIn("reader:check", package["scripts"])

    def test_create_book_project_public_mode_does_not_copy_private_overlay(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            copy_script("books/scripts/create_book_project.py", repo)
            write_minimal_template(repo)

            result = subprocess.run(
                [
                    sys.executable,
                    str(repo / "books" / "scripts" / "create_book_project.py"),
                    "public_book",
                    "--source-target",
                    "English-to-Simplified-Chinese",
                ],
                cwd=repo,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            project_root = repo / "books" / "zh-Hans" / "1_public_book"
            self.assertFalse((project_root / "references" / "private_use_cover_policy.md").exists())
            self.assertFalse((project_root / "scripts" / "check_private_use_gate.py").exists())
            package = json.loads((project_root / "package.json").read_text(encoding="utf-8"))
            self.assertNotIn("private:artifact:create", package["scripts"])

    def test_create_book_project_accepts_target_language_unicode_title_author_slug(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            copy_script("books/scripts/create_book_project.py", repo)
            write_minimal_template(repo)

            result = subprocess.run(
                [
                    sys.executable,
                    str(repo / "books" / "scripts" / "create_book_project.py"),
                    "天文学大成：第一卷？_托勒密",
                    "--source-target",
                    "English-to-Simplified-Chinese",
                ],
                cwd=repo,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("books/zh-Hans/1_天文学大成_第一卷_托勒密", result.stdout)
            self.assertTrue((repo / "books" / "zh-Hans" / "1_天文学大成_第一卷_托勒密").is_dir())

    def test_template_workflow_gate_accepts_private_path_only_for_private_use_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            copy_script("template/epub_pipeline/common/scripts/check_template_workflow_gate.py", repo)
            write_minimal_template(repo)
            book_root = repo / "books" / "private" / "zh-Hans" / "1_private_book"
            shutil.copytree(repo / "template" / "epub_pipeline" / "common", book_root)
            base_package = json.loads((book_root / "package.json").read_text(encoding="utf-8"))
            shutil.copytree(repo / "template" / "epub_pipeline" / "modes" / "private_use", book_root, dirs_exist_ok=True)
            (book_root / "package.json").write_text(json.dumps(base_package, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            merge_package_scripts(book_root / "package.json", repo / "template" / "epub_pipeline" / "modes" / "private_use" / "package.json")
            write_production_spec(book_root)
            state_path = book_root / "state" / "pipeline_state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state.update(
                {
                    "project_root": "books/private/zh-Hans/1_private_book",
                    "common_template_root": "template/epub_pipeline/common",
                    "template_root": "template/epub_pipeline/English-to-Simplified-Chinese",
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

    def test_template_workflow_gate_rejects_private_mode_without_overlay(self) -> None:
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
                    "template_root": "template/epub_pipeline/English-to-Simplified-Chinese",
                    "publication_mode": "private_use",
                }
            )
            state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

            for path in [
                book_root / "references" / "private_use_cover_policy.md",
                book_root / "references" / "private_use_frontmatter_policy.md",
                book_root / "references" / "private_use_artifact_policy.md",
                book_root / "scripts" / "check_private_use_gate.py",
            ]:
                if path.exists():
                    path.unlink()

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

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing_private_use_overlay_file", result.stdout)

    def test_template_workflow_gate_rejects_public_project_with_private_overlay(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            copy_script("template/epub_pipeline/common/scripts/check_template_workflow_gate.py", repo)
            write_minimal_template(repo)
            book_root = repo / "books" / "zh-Hans" / "1_public_book"
            shutil.copytree(repo / "template" / "epub_pipeline" / "common", book_root)
            shutil.copytree(repo / "template" / "epub_pipeline" / "modes" / "private_use", book_root, dirs_exist_ok=True)
            write_production_spec(book_root)
            state_path = book_root / "state" / "pipeline_state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state.update(
                {
                    "project_root": "books/zh-Hans/1_public_book",
                    "common_template_root": "template/epub_pipeline/common",
                    "template_root": "template/epub_pipeline/English-to-Simplified-Chinese",
                    "publication_mode": "public_domain",
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

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("public_project_contains_private_use_overlay", result.stdout)

    def test_template_workflow_gate_accepts_unicode_public_book_directory_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            copy_script("template/epub_pipeline/common/scripts/check_template_workflow_gate.py", repo)
            write_minimal_template(repo)
            book_root = repo / "books" / "zh-Hans" / "10_林伯洛斯特的女孩_吉恩·斯特拉顿-波特"
            shutil.copytree(repo / "template" / "epub_pipeline" / "common", book_root)
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
                        "template/epub_pipeline/common/references/proper_noun_display_policy.md",
                        "template/epub_pipeline/common/references/note_marker_policy.md",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            state_path = book_root / "state" / "pipeline_state.json"
            state = json.loads(state_path.read_text(encoding="utf-8"))
            state.update(
                {
                    "project_root": "books/zh-Hans/10_林伯洛斯特的女孩_吉恩·斯特拉顿-波特",
                    "common_template_root": "template/epub_pipeline/common",
                    "template_root": "template/epub_pipeline/English-to-Simplified-Chinese",
                    "publication_mode": "public_domain",
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

    def test_private_reader_gate_rejects_missing_private_cover_and_book_info(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            book_root = Path(tmp) / "books" / "private" / "zh-Hans" / "1_private_book"
            book_root.mkdir(parents=True)

            result = subprocess.run(
                [
                    sys.executable,
                    str(
                        REPO_ROOT
                        / "template"
                        / "epub_pipeline"
                        / "modes"
                        / "private_use"
                        / "scripts"
                        / "check_private_reader_facing_policy.py"
                    ),
                    "--book-root",
                    str(book_root),
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing_private_cover_frontmatter", result.stdout)
            self.assertIn("missing_private_book_info_frontmatter", result.stdout)

    def test_private_reader_gate_accepts_open_project_private_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            book_root = Path(tmp) / "books" / "private" / "zh-Hans" / "1_private_book"
            frontmatter = book_root / "frontmatter"
            frontmatter.mkdir(parents=True)
            (frontmatter / "cover.md").write_text("# 私人书籍封面\n\n作者：某作者\n", encoding="utf-8")
            (frontmatter / "book-info.md").write_text(
                "\n".join(
                    [
                        "# 书籍信息",
                        "",
                        "书名：私人书籍",
                        "作者：某作者",
                        "版本：私人学习版本",
                        "制作标识：参考public-domain-books-translation 开源项目 个人自制",
                        "本地书源：source.epub",
                        "书源校验：SHA256 abc123",
                        "",
                        "仅供个人自用，不传播，不商业使用。",
                        "",
                        "风险由个人承担。public-domain-books-translation 开源项目仅用于公版书翻译发布，不承担其他个人翻译、保存、传播或使用非公版内容导致的版权风险及责任。",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(
                        REPO_ROOT
                        / "template"
                        / "epub_pipeline"
                        / "modes"
                        / "private_use"
                        / "scripts"
                        / "check_private_reader_facing_policy.py"
                    ),
                    "--book-root",
                    str(book_root),
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_private_use_templates_do_not_prescribe_lifebook_reader_facing_private_wording(self) -> None:
        checked_files = [
            "AGENTS.md",
            "README.zh-CN.md",
            "template/epub_pipeline/README.md",
            "template/epub_pipeline/common/preproduction/stage1/_TEMPLATE.production_spec.md",
            "template/epub_pipeline/common/references/book_info_frontmatter_policy.md",
            "template/epub_pipeline/common/metadata/private_use_declaration.md",
            "template/epub_pipeline/common/metadata/rights_checklist.md",
            "template/epub_pipeline/modes/private_use/README.md",
            "template/epub_pipeline/modes/private_use/references/private_use_frontmatter_policy.md",
            "template/epub_pipeline/modes/private_use/references/private_use_artifact_policy.md",
            "template/epub_pipeline/modes/private_use/preproduction/stage1/_TEMPLATE.private_use_production_spec.md",
            "template/epub_pipeline/modes/private_use/scripts/create_private_artifact.py",
        ]
        forbidden = [
            "参考LifeBook书坊 个人自制",
            "LifeBook书坊仅发布 LifeBook 翻译发布系统",
            "LifeBook书坊不承担任何因其他个人翻译、保存、传播或使用非公版内容导致的版权风险及责任",
            "LifeBook Shufang publishes only the LifeBook translation publishing system",
            "LifeBook Shufang does not assume copyright risk or liability",
        ]

        failures = []
        for relative in checked_files:
            text = (REPO_ROOT / relative).read_text(encoding="utf-8")
            for snippet in forbidden:
                if snippet in text:
                    failures.append(f"{relative}: {snippet}")

        self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()

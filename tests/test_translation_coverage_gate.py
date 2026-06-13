from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "template" / "epub_pipeline" / "common" / "scripts" / "check_translation_coverage.py"
WORKFLOW_GATE = REPO_ROOT / "template" / "epub_pipeline" / "common" / "scripts" / "check_template_workflow_gate.py"
COMMON_PACKAGE = REPO_ROOT / "template" / "epub_pipeline" / "common" / "package.json"


def write_chapter(book_root: Path, relative: str, paragraphs: list[str]) -> None:
    path = book_root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n\n".join(paragraphs) + "\n", encoding="utf-8")


def write_pass_control(book_root: Path, chapter_stem: str) -> None:
    path = book_root / "qa" / "chapter_controls" / f"{chapter_stem}.control.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            [
                "# Chapter Control",
                "",
                "target_language_readability: PASS 中文可读，已润色。",
                "",
                "## Round 1",
                "",
                "scope: FULL_CHAPTER",
                "expert_translation_skill_used: true",
                "expert_level_review_status: PASS",
                "polysemy_translation_stage_review: PASS",
                "polysemy_context_review: PASS",
                "polysemy_unresolved_count: 0",
                "issues_found: 0",
                "fixes_applied: 0",
                "unresolved_blocking_issues: 0",
                "latest_round_status: PASS",
                "allow_next_chapter: true",
                "",
            ]
        ),
        encoding="utf-8",
    )


class TranslationCoverageGateTests(unittest.TestCase):
    def run_gate(self, book_root: Path, *extra: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--book-root",
                str(book_root),
                *extra,
            ],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_rejects_translated_chapter_that_drops_tail_paragraphs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            book_root = Path(tmp)
            source = ["# Chapter 7"] + [
                f"Source paragraph {index:02d} carries unique evidence marker {index:02d}."
                for index in range(1, 11)
            ]
            translated = ["# 第七章"] + [
                f"译文段落 {index:02d}，保留前半部分信息。"
                for index in range(1, 6)
            ]
            write_chapter(book_root, "chapters/src/007_chapter.md", source)
            write_chapter(book_root, "chapters/translated/007_chapter.md", translated)

            result = self.run_gate(book_root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("paragraph_block_coverage_low", result.stdout + result.stderr)

    def test_rejects_translated_chapter_with_missing_footnote_definitions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            book_root = Path(tmp)
            source = [
                "# Chapter 15",
                "First source paragraph uses a note.[^1]",
                "Second source paragraph uses another note.[^2]",
                "Third source paragraph keeps the final note.[^3]",
                "[^1]: First source note.",
                "[^2]: Second source note.",
                "[^3]: Third source note.",
            ]
            translated = [
                "# 第十五章",
                "第一段译文使用注释。[^1]",
                "第二段译文也使用注释。[^2]",
                "第三段译文仍然完整。",
                "[^1]: 第一条译注。",
            ]
            write_chapter(book_root, "chapters/src/015_chapter.md", source)
            write_chapter(book_root, "chapters/translated/015_chapter.md", translated)

            result = self.run_gate(book_root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("note_definition_coverage_low", result.stdout + result.stderr)
            self.assertIn("note_reference_coverage_low", result.stdout + result.stderr)

    def test_accepts_complete_translation_structure_and_writes_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            book_root = Path(tmp)
            source = [
                "# Chapter 1",
                "Alpha source paragraph with one note.[^1]",
                "Beta source paragraph continues the chapter.",
                "[^1]: Source note.",
            ]
            translated = [
                "# 第一章",
                "第一段译文保留正文信息，并设置注释。[^1]",
                "第二段译文继续本章内容。",
                "[^1]: 译注内容。",
            ]
            write_chapter(book_root, "chapters/src/001_chapter.md", source)
            write_chapter(book_root, "chapters/translated/001_chapter.md", translated)

            result = self.run_gate(book_root, "--write-report")

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = json.loads((book_root / "output" / "translation_coverage.json").read_text(encoding="utf-8"))
            self.assertTrue(report["ok"])
            self.assertEqual(report["chapters_checked"], 1)

    def test_workflow_gate_rejects_low_translation_coverage_even_with_pass_control(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            book_root = Path(tmp)
            source = ["# Chapter"] + [
                f"Source paragraph {index:02d} carries unique evidence marker {index:02d}."
                for index in range(1, 9)
            ]
            translated = ["# 章节", "译文只保留开头。", "译文继续一点点。"]
            write_chapter(book_root, "chapters/src/001_chapter.md", source)
            write_chapter(book_root, "chapters/translated/001_chapter.md", translated)
            write_pass_control(book_root, "001_chapter")
            state = book_root / "state" / "pipeline_state.json"
            state.parent.mkdir(parents=True, exist_ok=True)
            state.write_text(
                json.dumps({"project_root": ".", "common_template_root": "template/epub_pipeline/common"}),
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(WORKFLOW_GATE),
                    "--book-root",
                    str(book_root),
                    "--chapter-controls-only",
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("paragraph_block_coverage_low", result.stdout + result.stderr)

    def test_common_package_exposes_translation_coverage_gate_in_preflight(self) -> None:
        package = json.loads(COMMON_PACKAGE.read_text(encoding="utf-8"))
        scripts = package["scripts"]

        self.assertIn("check:translation-coverage", scripts)
        self.assertIn("check:translation-coverage", scripts["preflight:template"])
        self.assertIn("check:translation-coverage", scripts["check:chapter-controls"])


if __name__ == "__main__":
    unittest.main()

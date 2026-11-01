from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


def write_project(root: Path, body: str) -> None:
    (root / "scripts").mkdir(parents=True)
    shutil.copy2(
        REPO_ROOT / "template" / "epub_pipeline" / "common" / "scripts" / "publication_lint.js",
        root / "scripts" / "publication_lint.js",
    )
    (root / "chapters" / "final").mkdir(parents=True)
    (root / "frontmatter").mkdir(parents=True)
    (root / "metadata").mkdir(parents=True)
    (root / "chapters" / "final" / "001.md").write_text(body, encoding="utf-8")


def run_lint(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["node", "scripts/publication_lint.js", "--target=zh-Hans", *args],
        cwd=root,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


class PublicationLintSemicolonTests(unittest.TestCase):
    def test_reader_facing_chinese_semicolon_requires_exception(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_project(root, "前半句很长；后半句也很长。\n")

            result = run_lint(root)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("zh_semicolon_requires_justification", result.stderr)

    def test_reader_facing_chinese_semicolon_passes_with_line_level_exception(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_project(root, "前半句很长；后半句也很长。\n")
            exception_path = root / "qa" / "punctuation" / "semicolon_exceptions.json"
            exception_path.parent.mkdir(parents=True)
            exception_path.write_text(
                json.dumps(
                    [
                        {
                            "file": "chapters/final/001.md",
                            "line": 1,
                            "semicolon_count": 1,
                            "text_excerpt": "前半句很长",
                            "structure_type": "parallel_clauses",
                            "rewriting_attempted": True,
                            "reason": "两分句是同层并列结构，改成句号会断开修辞呼应。",
                            "approved_by": "agent",
                        }
                    ],
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )

            result = run_lint(root)

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_fix_does_not_convert_ascii_semicolon_to_chinese_semicolon(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_project(root, "前半句;后半句。\n")

            result = run_lint(root, "--fix")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("ascii_semicolon", result.stderr)
            text = (root / "chapters" / "final" / "001.md").read_text(encoding="utf-8")
            self.assertIn(";", text)


if __name__ == "__main__":
    unittest.main()

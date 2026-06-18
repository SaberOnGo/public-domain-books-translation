from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_GATE = REPO_ROOT / "template" / "epub_pipeline" / "common" / "scripts" / "check_template_workflow_gate.py"
PUBLICATION_LINT = REPO_ROOT / "template" / "epub_pipeline" / "common" / "scripts" / "publication_lint.js"


REQUIRED_SPEC_TOKENS = [
    "template/epub_pipeline/common/preproduction/stage1/_TEMPLATE.production_spec.md",
    "template/epub_pipeline/common/references/cover_design_policy.md",
    "template/epub_pipeline/common/references/book_info_frontmatter_policy.md",
    "template/epub_pipeline/common/references/epub_assets_figures_tables.md",
    "template/epub_pipeline/common/references/quality_gate_framework.md",
    "template/epub_pipeline/common/references/proper_noun_display_policy.md",
    "template/epub_pipeline/common/references/note_marker_policy.md",
]


REQUIRED_PACKAGE_SCRIPTS = [
    "preflight:template",
    "check:translation-coverage",
    "check:chapter-controls",
    "cover:check",
    "reader:check",
    "lint:publication",
    "lint:assets",
    "build:epub",
    "release:draft",
    "release:create",
]


def make_minimal_book(root: Path) -> None:
    state = root / "state" / "pipeline_state.json"
    state.parent.mkdir(parents=True, exist_ok=True)
    state.write_text(
        json.dumps(
            {
                "project_root": root.relative_to(REPO_ROOT).as_posix(),
                "common_template_root": "template/epub_pipeline/common",
                "publication_mode": "public_domain",
            }
        ),
        encoding="utf-8",
    )
    spec = root / "preproduction" / "stage1" / "production_spec.md"
    spec.parent.mkdir(parents=True, exist_ok=True)
    spec.write_text("\n".join(REQUIRED_SPEC_TOKENS) + "\n", encoding="utf-8")
    for reference in [
        "references/cover_design_policy.md",
        "references/book_info_frontmatter_policy.md",
        "references/epub_assets_figures_tables.md",
        "references/quality_gate_framework.md",
        "references/release_versioning.md",
        "references/proper_noun_display_policy.md",
        "references/note_marker_policy.md",
    ]:
        path = root / reference
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# Reference\n", encoding="utf-8")
    package = root / "package.json"
    scripts = {name: "echo ok" for name in REQUIRED_PACKAGE_SCRIPTS}
    scripts["build:epub"] = "npm run preflight:template && npm run lint:publication && npm run lint:assets && npm run cover:check && npm run reader:check"
    scripts["release:draft"] = "npm run preflight:template && npm run cover:check && npm run reader:check"
    scripts["release:create"] = "npm run preflight:template && npm run cover:check && npm run reader:check"
    package.write_text(
        json.dumps({"scripts": scripts}),
        encoding="utf-8",
    )


class ProperNounAndNotePolicyTests(unittest.TestCase):
    def test_workflow_gate_rejects_invalid_proper_noun_display_policy(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT / "books" / "zh-Hans") as tmp:
            book_root = Path(tmp).rename(Path(tmp).with_name(f"999_test_proper_noun_policy_{Path(tmp).name}"))
            try:
                make_minimal_book(book_root)
                proper_nouns = book_root / "glossary" / "proper_nouns.csv"
                proper_nouns.parent.mkdir(parents=True, exist_ok=True)
                proper_nouns.write_text(
                    "\n".join(
                        [
                            "source_name,target_name,category,display_policy,first_rendering,subsequent_rendering,note_required,repeat_original_allowed_when,notes",
                            "Nero,尼禄,historical_person,9,尼禄（Nero）,尼禄,false,,invalid option",
                        ]
                    )
                    + "\n",
                    encoding="utf-8",
                )

                result = subprocess.run(
                    [sys.executable, str(WORKFLOW_GATE), "--book-root", str(book_root)],
                    text=True,
                    encoding="utf-8",
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )

                self.assertNotEqual(result.returncode, 0)
                self.assertIn("proper_noun_invalid_display_policy", result.stdout + result.stderr)
            finally:
                if book_root.exists():
                    for path in sorted(book_root.rglob("*"), reverse=True):
                        if path.is_file():
                            path.unlink()
                        else:
                            path.rmdir()
                    book_root.rmdir()

    def test_workflow_gate_requires_display_policy_for_nonblank_proper_noun_row(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT / "books" / "zh-Hans") as tmp:
            book_root = Path(tmp).rename(Path(tmp).with_name(f"999_test_proper_noun_policy_{Path(tmp).name}"))
            try:
                make_minimal_book(book_root)
                proper_nouns = book_root / "glossary" / "proper_nouns.csv"
                proper_nouns.parent.mkdir(parents=True, exist_ok=True)
                proper_nouns.write_text(
                    "\n".join(
                        [
                            "source_name,target_name,category,display_policy,first_rendering,subsequent_rendering,note_required,repeat_original_allowed_when,notes",
                            "Nero,尼禄,historical_person,,尼禄（Nero）,尼禄,false,,missing display policy",
                        ]
                    )
                    + "\n",
                    encoding="utf-8",
                )

                result = subprocess.run(
                    [sys.executable, str(WORKFLOW_GATE), "--book-root", str(book_root)],
                    text=True,
                    encoding="utf-8",
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )

                self.assertNotEqual(result.returncode, 0)
                self.assertIn("proper_noun_missing_display_policy", result.stdout + result.stderr)
            finally:
                if book_root.exists():
                    for path in sorted(book_root.rglob("*"), reverse=True):
                        if path.is_file():
                            path.unlink()
                        else:
                            path.rmdir()
                    book_root.rmdir()

    def test_publication_lint_rejects_disallowed_note_markers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            book_root = Path(tmp)
            chapter = book_root / "chapters" / "final" / "001.md"
            chapter.parent.mkdir(parents=True, exist_ok=True)
            chapter.write_text(
                "# 第一章\n\n这一句用了不允许的小圆圈注号①。\n\n这一句用了不允许的裸注标签注。\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                ["node", str(PUBLICATION_LINT), "--target=zh-Hans"],
                cwd=book_root,
                text=True,
                encoding="utf-8",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("disallowed_note_marker", result.stdout + result.stderr)

    def test_publication_lint_rejects_later_circled_and_fullwidth_bare_note_digits(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            book_root = Path(tmp)
            chapter = book_root / "chapters" / "final" / "001.md"
            chapter.parent.mkdir(parents=True, exist_ok=True)
            chapter.write_text(
                "# 第一章\n\n这一句用了不允许的后续带圈注号㉑。\n\n这一句用了不允许的全角裸数字。１\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                ["node", str(PUBLICATION_LINT), "--target=zh-Hans"],
                cwd=book_root,
                text=True,
                encoding="utf-8",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("disallowed_note_marker", result.stdout + result.stderr)

    def test_publication_lint_allows_approved_note_marker_families(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            book_root = Path(tmp)
            chapter = book_root / "chapters" / "final" / "001.md"
            chapter.parent.mkdir(parents=True, exist_ok=True)
            chapter.write_text(
                "# 第一章\n\n尼禄（Nero）[1]。奥古斯都（Augustus）（2）。塔西佗（Tacitus）注3。\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                ["node", str(PUBLICATION_LINT), "--target=zh-Hans"],
                cwd=book_root,
                text=True,
                encoding="utf-8",
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_workflow_gate_requires_note_flag_for_policy_five(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT / "books" / "zh-Hans") as tmp:
            book_root = Path(tmp).rename(Path(tmp).with_name(f"999_test_proper_noun_policy_{Path(tmp).name}"))
            try:
                make_minimal_book(book_root)
                proper_nouns = book_root / "glossary" / "proper_nouns.csv"
                proper_nouns.parent.mkdir(parents=True, exist_ok=True)
                proper_nouns.write_text(
                    "\n".join(
                        [
                            "source_name,target_name,category,display_policy,first_rendering,subsequent_rendering,note_required,repeat_original_allowed_when,notes",
                            "Nero,尼禄,historical_person,5,尼禄（Nero）,尼禄,false,,missing required note",
                        ]
                    )
                    + "\n",
                    encoding="utf-8",
                )

                result = subprocess.run(
                    [sys.executable, str(WORKFLOW_GATE), "--book-root", str(book_root)],
                    text=True,
                    encoding="utf-8",
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )

                self.assertNotEqual(result.returncode, 0)
                self.assertIn("proper_noun_policy_5_requires_note", result.stdout + result.stderr)
            finally:
                if book_root.exists():
                    for path in sorted(book_root.rglob("*"), reverse=True):
                        if path.is_file():
                            path.unlink()
                        else:
                            path.rmdir()
                    book_root.rmdir()

    def test_workflow_gate_rejects_policy_five_without_note_marker_in_first_rendering(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT / "books" / "zh-Hans") as tmp:
            book_root = Path(tmp).rename(Path(tmp).with_name(f"999_test_proper_noun_policy_{Path(tmp).name}"))
            try:
                make_minimal_book(book_root)
                proper_nouns = book_root / "glossary" / "proper_nouns.csv"
                proper_nouns.parent.mkdir(parents=True, exist_ok=True)
                proper_nouns.write_text(
                    "\n".join(
                        [
                            "source_name,target_name,category,display_policy,first_rendering,subsequent_rendering,note_required,repeat_original_allowed_when,notes",
                            "Nero,尼禄,historical_person,5,尼禄（Nero）,尼禄,true,,missing first-rendering marker",
                        ]
                    )
                    + "\n",
                    encoding="utf-8",
                )

                result = subprocess.run(
                    [sys.executable, str(WORKFLOW_GATE), "--book-root", str(book_root)],
                    text=True,
                    encoding="utf-8",
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )

                self.assertNotEqual(result.returncode, 0)
                self.assertIn("proper_noun_policy_5_first_rendering_missing_note_marker", result.stdout + result.stderr)
            finally:
                if book_root.exists():
                    for path in sorted(book_root.rglob("*"), reverse=True):
                        if path.is_file():
                            path.unlink()
                        else:
                            path.rmdir()
                    book_root.rmdir()

    def test_workflow_gate_rejects_invalid_note_required_value(self) -> None:
        with tempfile.TemporaryDirectory(dir=REPO_ROOT / "books" / "zh-Hans") as tmp:
            book_root = Path(tmp).rename(Path(tmp).with_name(f"999_test_proper_noun_policy_{Path(tmp).name}"))
            try:
                make_minimal_book(book_root)
                proper_nouns = book_root / "glossary" / "proper_nouns.csv"
                proper_nouns.parent.mkdir(parents=True, exist_ok=True)
                proper_nouns.write_text(
                    "\n".join(
                        [
                            "source_name,target_name,category,display_policy,first_rendering,subsequent_rendering,note_required,repeat_original_allowed_when,notes",
                            "Nero,尼禄,historical_person,3,尼禄（Nero）,尼禄,maybe,,invalid boolean",
                        ]
                    )
                    + "\n",
                    encoding="utf-8",
                )

                result = subprocess.run(
                    [sys.executable, str(WORKFLOW_GATE), "--book-root", str(book_root)],
                    text=True,
                    encoding="utf-8",
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )

                self.assertNotEqual(result.returncode, 0)
                self.assertIn("proper_noun_invalid_note_required", result.stdout + result.stderr)
            finally:
                if book_root.exists():
                    for path in sorted(book_root.rglob("*"), reverse=True):
                        if path.is_file():
                            path.unlink()
                        else:
                            path.rmdir()
                    book_root.rmdir()


if __name__ == "__main__":
    unittest.main()

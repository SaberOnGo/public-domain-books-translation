from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = REPO_ROOT / "template" / "epub_pipeline"

LANGUAGE_PAIR_TEMPLATE_ALIASES = {
    "de-zh-Hans": "German-to-Simplified-Chinese",
    "en-zh-Hans": "English-to-Simplified-Chinese",
    "es-zh-Hans": "Spanish-to-Simplified-Chinese",
    "fr-zh-Hans": "French-to-Simplified-Chinese",
    "grc-zh-Hans": "Ancient-Greek-to-Simplified-Chinese",
    "it-zh-Hans": "Italian-to-Simplified-Chinese",
    "ja-zh-Hans": "Japanese-to-Simplified-Chinese",
    "ko-zh-Hans": "Korean-to-Simplified-Chinese",
    "lzh-zh-Hans": "Literary-Chinese-to-Simplified-Chinese",
    "ru-zh-Hans": "Russian-to-Simplified-Chinese",
    "sa-zh-Hans": "Sanskrit-to-Simplified-Chinese",
}


class LanguagePairTemplateNameTests(unittest.TestCase):
    def test_language_pair_template_directories_use_readable_full_names(self) -> None:
        for legacy_name, full_name in LANGUAGE_PAIR_TEMPLATE_ALIASES.items():
            self.assertFalse(
                (TEMPLATE_ROOT / legacy_name).exists(),
                f"legacy short template directory should be renamed: {legacy_name}",
            )
            self.assertTrue(
                (TEMPLATE_ROOT / full_name).is_dir(),
                f"missing readable template directory: {full_name}",
            )

    def test_create_book_project_accepts_full_template_name_and_legacy_alias(self) -> None:
        for source_target in ["English-to-Simplified-Chinese", "en-zh-Hans"]:
            with self.subTest(source_target=source_target):
                result = subprocess.run(
                    [
                        sys.executable,
                        str(REPO_ROOT / "books" / "scripts" / "create_book_project.py"),
                        "template_name_smoke_delete_me",
                        "--source-target",
                        source_target,
                        "--dry-run",
                    ],
                    cwd=REPO_ROOT,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )

                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertRegex(result.stdout, r"books/zh-Hans/\d+_template_name_smoke_delete_me")


if __name__ == "__main__":
    unittest.main()

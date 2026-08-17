from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
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

    def test_language_overlay_cannot_remove_canonical_translation_release_gates(self) -> None:
        script = REPO_ROOT / "books" / "scripts" / "create_book_project.py"
        spec = importlib.util.spec_from_file_location("lifebook_create_book_project_test", script)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "package.json"
            shutil.copyfile(TEMPLATE_ROOT / "common" / "package.json", destination)
            module.merge_package_json(
                TEMPLATE_ROOT / "Ancient-Greek-to-Simplified-Chinese" / "package.json",
                destination,
            )
            scripts = json.loads(destination.read_text(encoding="utf-8"))["scripts"]
            self.assertIn("translation:contract:validate", scripts["preflight:template"])
            self.assertIn("translation:prebuild", scripts["build:epub"])
            self.assertIn("translation:artifact:release-validate", scripts["release:create"])
            self.assertIn("--all-enabled", scripts["check:epub"])
            self.assertIn("reader:static-check", scripts["reader:check"])
            self.assertIn("plan_parallel_translation.py", scripts["translation:orchestration:plan"])

    def test_every_language_translation_prompt_uses_canonical_patches(self) -> None:
        prompts = sorted(TEMPLATE_ROOT.glob("*-to-*/prompts/07_translate_chapters_*.md"))
        self.assertGreaterEqual(len(prompts), 10)
        for prompt in prompts:
            with self.subTest(prompt=prompt.relative_to(REPO_ROOT).as_posix()):
                text = prompt.read_text(encoding="utf-8")
                self.assertIn("translation_units/", text)
                self.assertIn("chapter patch", text)
                self.assertIn("CAS", text)
                self.assertIn("proper_nouns.csv", text)
                self.assertIn("adaptive_parallel_orchestration.md", text)
                self.assertNotIn("章节译文先写入 `chapters/translated/`", text)
                self.assertNotIn("- `chapters/translated/{same_filename}.md`", text)

    def test_ai_parallel_execution_guidance_is_referenced_and_provider_neutral(self) -> None:
        guide_name = "ai_parallel_execution_guidance.md"
        guide_path = TEMPLATE_ROOT / "common" / "references" / guide_name
        entry_points = [
            REPO_ROOT / "AGENTS.md",
            TEMPLATE_ROOT / "README.md",
            TEMPLATE_ROOT / "common" / "README.md",
            TEMPLATE_ROOT / "common" / "references" / "adaptive_parallel_orchestration.md",
        ]

        self.assertTrue(guide_path.is_file(), f"missing AI execution guide: {guide_path}")
        guide = guide_path.read_text(encoding="utf-8")
        for entry_point in entry_points:
            with self.subTest(entry_point=entry_point.relative_to(REPO_ROOT).as_posix()):
                self.assertIn(guide_name, entry_point.read_text(encoding="utf-8"))

        self.assertIn("gpt-5.6-luna", guide)
        self.assertIn("reasoning effort `max`", guide)
        self.assertIn("SHOULD", guide)
        self.assertIn("用户明确指令", guide)
        self.assertIn("does not implement a runtime task queue", guide)
        self.assertNotIn("luna_worker", guide)

        orchestration = entry_points[-1].read_text(encoding="utf-8")
        self.assertNotIn("For Codex", orchestration)
        self.assertNotIn("对 Codex", orchestration)


if __name__ == "__main__":
    unittest.main()

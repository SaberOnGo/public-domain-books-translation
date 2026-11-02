import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "template/epub_pipeline/common/scripts"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


profile = load(SCRIPTS / "profile_translationese.py", "profile_translationese")
routed = load(SCRIPTS / "check_routed_items.py", "check_routed_items")
book_info = load(SCRIPTS / "generate_book_info.py", "generate_book_info")
sync_tools = load(REPO / "books/scripts/sync_book_tools.py", "sync_book_tools")


class TranslationeseProfileTests(unittest.TestCase):
    def test_semicolon_heavy_text_is_flagged_and_native_rhythm_is_not(self):
        heavy = "他走进屋子；他的妻子坐在窗前；他的孩子在门外玩耍。" * 60
        native = "天黑以后，雨停了。院子里的老槐树滴着水，母亲在灶前烧火，锅里的粥咕嘟咕嘟地响。" * 40
        self.assertTrue(any(flag.startswith("semicolon") for flag in profile.profile_text(heavy)["flags"]))
        self.assertEqual([], profile.profile_text(native)["flags"])

    def test_speaker_labels_and_speech_colons_do_not_count_as_explanatory(self):
        text = profile.clean_markdown("沃尔特：我要钱。\n\n露丝：你要钱做什么？\n\n他说：“走吧。”")
        self.assertEqual(0.0, profile.profile_text(text)["rates_per_10k"]["explanatory_colon"])


class RoutedItemsTests(unittest.TestCase):
    def test_open_items_fail_until_closure_is_recorded(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "qa/gates").mkdir(parents=True)
            (root / "qa/gates/009.gate.md").write_text("status: PASS_WITH_ROUTED_ITEMS\n- 终稿前需核对译名。\n", encoding="utf-8")
            self.assertEqual("FAIL", routed.check(root)["status"])
            time.sleep(0.05)
            (root / "qa/routed_items").mkdir(parents=True)
            (root / "qa/routed_items/closure.md").write_text("- 009：已核对并修改\nopen_routed_items: 0\n", encoding="utf-8")
            self.assertEqual("PASS", routed.check(root)["status"])


class BookInfoGeneratorTests(unittest.TestCase):
    def book(self, root, contributor_name="SaberOnGo", synopsis="一位哥特小说叙述者讲述伦敦的离奇遭遇。"):
        (root / "metadata").mkdir(parents=True)
        (root / "metadata/book.yaml").write_text("\n".join([
            'title: "甲虫"', 'original_title: "The Beetle"', 'author: "理查德·马什"', 'author_original: "Richard Marsh"',
            'author_years: "1857—1915"', f'translator_name: "{contributor_name}"', 'translation_date: "2026-06"',
            'source_name: "Project Gutenberg #5164"', 'source_url: "https://www.gutenberg.org/ebooks/5164"']) + "\n", encoding="utf-8")
        (root / "metadata/book_info_sections.md").write_text(
            f"## 本书简介\n\n{synopsis}\n\n## 作者简介\n\n英国通俗小说作家。\n\n## 创作背景\n\n1897 年出版。\n", encoding="utf-8")

    def test_generates_fixed_layout_with_personal_credit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.book(root)
            text, errors = book_info.build(root, "translated")
        self.assertEqual([], errors)
        self.assertIn("译制：LifeBook 书坊 SaberOnGo", text)
        self.assertIn("作者：理查德·马什（Richard Marsh，1857—1915）", text)

    def test_tool_names_and_production_details_in_synopsis_fail(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.book(root, contributor_name="Codex", synopsis="本书依据 Project Gutenberg 译制。")
            _, errors = book_info.build(root, "translated")
        self.assertTrue(any("AI tool" in error for error in errors))
        self.assertTrue(any("本书简介" in error for error in errors))

    def test_source_original_edition_is_not_credited_as_translated(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.book(root)
            text, _ = book_info.build(root, "source_original")
        self.assertNotIn("译制", text)
        self.assertIn("EPUB 制作", text)


class SyncBookToolsTests(unittest.TestCase):
    def test_dry_run_reports_and_apply_updates_with_backup(self):
        with tempfile.TemporaryDirectory(dir=REPO / "books") as tmp:
            book = Path(tmp)
            (book / "scripts").mkdir()
            (book / "state").mkdir()
            (book / "state/pipeline_state.json").write_text("{}", encoding="utf-8")
            (book / "scripts/build_epub.js").write_text("// old copy\n", encoding="utf-8")
            (book / "scripts/my_book_only.py").write_text("print('keep')\n", encoding="utf-8")
            (book / "package.json").write_text(json.dumps({"scripts": {"build:epub": "custom"}}), encoding="utf-8")
            report = sync_tools.sync(book, apply=False)
            self.assertIn("build_epub.js", report["changed"])
            self.assertIn("my_book_only.py", report["book_only"])
            self.assertEqual("// old copy\n", (book / "scripts/build_epub.js").read_text(encoding="utf-8"))
            sync_tools.sync(book, apply=True)
            self.assertNotEqual("// old copy\n", (book / "scripts/build_epub.js").read_text(encoding="utf-8"))
            self.assertEqual("print('keep')\n", (book / "scripts/my_book_only.py").read_text(encoding="utf-8"))
            backups = list((book / "output/history").glob("tool_sync_*/scripts/build_epub.js"))
            self.assertEqual(1, len(backups))
            scripts = json.loads((book / "package.json").read_text(encoding="utf-8"))["scripts"]
            self.assertEqual("custom", scripts["build:epub"])
            self.assertIn("check:final-epub", scripts)
            self.assertTrue((book / "state/tool_versions.json").exists())


if __name__ == "__main__":
    unittest.main()

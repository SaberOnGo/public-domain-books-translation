import base64
import importlib.util
import shutil
import subprocess
import sys
import tempfile
import textwrap
import unittest
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "template/epub_pipeline/common/scripts"
PNG = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jWZkAAAAASUVORK5CYII=")
HASH = "0" * 64


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


bilingual = load("build_bilingual_epub")
final_gate = load("check_final_epub")


class BilingualBlockRenderingTests(unittest.TestCase):
    def test_cjk_prose_lines_join_without_spaces(self):
        html = bilingual.render_text_block("据说，菲尔丁曾举杯诅咒那个发明戏剧第五幕的人。\n"
                                           "校注完一部浩繁的书，再编好一份详尽的索引，若有人不肯把发明序言的人算作人类的恩人，倒也情有可原。")
        self.assertEqual(1, len(html))
        self.assertIn("的人。校注完", html[0])

    def test_space_after_cjk_sentence_punctuation_is_removed(self):
        self.assertEqual(["<p>平时单身独处。眼下正是繁殖季节。</p>"], bilingual.render_text_block("平时单身独处。 眼下正是繁殖季节。"))

    def test_verse_keeps_line_breaks(self):
        html = bilingual.render_text_block("我们村寨里美人很多，\n她们眼底的黑暗中星光闪烁。\n爱她们很甜，是令人羡慕的命运；")
        self.assertIn("很多，<br />她们", html[0])

    def test_quote_list_and_separator_markup_become_structure(self):
        self.assertEqual(
            ['<blockquote><p>我死后，只愿有诚实的纪事者，<br />传扬我的名声。</p></blockquote>'],
            bilingual.render_text_block("> 我死后，只愿有诚实的纪事者，<br />\n> 传扬我的名声。"),
        )
        self.assertEqual(["<ol><li>外表</li><li>现实</li></ol>"], bilingual.render_text_block("1. 外表\n2. 现实"))
        self.assertEqual([], bilingual.render_text_block("* * *"))

    def test_paragraph_followed_by_raw_blockquote_is_split(self):
        html = bilingual.render_text_block("最适合借诗人的语言来描写：\n<blockquote>\n——“一片幽暗的大洋，<br />没有边界；\n</blockquote>")
        self.assertEqual("<p>最适合借诗人的语言来描写：</p>", html[0])
        self.assertEqual("<blockquote>", html[1])
        self.assertNotIn("&lt;", "".join(html))

    def test_english_lines_still_join_with_spaces_and_italics_render(self):
        html = bilingual.render_text_block(
            "Fielding, it is said, drank confusion to the man who invented the fifth act of a play.\n"
            "He who has edited an extensive work might well be pardoned, as _Rome_ shows.")
        self.assertIn("a play. He who", html[0])
        self.assertIn("<em>Rome</em>", html[0])

    def test_bilingual_identifier_differs_from_target_only_identifier(self):
        base = "urn:uuid:12345678-1234-5678-1234-567812345678"
        self.assertNotEqual(base, bilingual.edition_identifier({"identifier": base}))
        self.assertTrue(bilingual.edition_identifier({"identifier": base}).startswith("urn:uuid:"))
        self.assertEqual("lifebook-x-bilingual-parallel", bilingual.edition_identifier({"identifier": "lifebook-x"}))


class TargetOnlyBuilderTests(unittest.TestCase):
    def book(self, root, chapter, preface="# Preface\n"):
        (root / "scripts").mkdir()
        for name in ("build_epub.js", "run_python.js"):
            shutil.copy(SCRIPTS / name, root / "scripts" / name)
        for folder in ("chapters/final", "frontmatter", "metadata", "assets/images"):
            (root / folder).mkdir(parents=True)
        (root / "assets/images/cover.png").write_bytes(PNG)
        (root / "metadata/book.yaml").write_text(
            "title: 测试书\nauthor: 作者\nlanguage: zh-Hans\nidentifier: urn:uuid:12345678-1234-5678-1234-567812345678\n",
            encoding="utf-8")
        (root / "frontmatter/cover.md").write_text("# 封面\n\n![测试书封面](../assets/images/cover.png)\n", encoding="utf-8")
        (root / "frontmatter/preface.md").write_text(preface, encoding="utf-8")
        (root / "frontmatter/translator_note.md").write_text(
            "<!-- lifebook:placeholder\n模板占位说明\n-->\n# 译者说明\n", encoding="utf-8")
        (root / "chapters/final/001_chapter.md").write_text(textwrap.dedent(chapter), encoding="utf-8")
        return subprocess.run(["node", str(root / "scripts/build_epub.js")], cwd=root,
                              capture_output=True, text=True, encoding="utf-8")

    def test_rendering_placeholders_cover_and_reader_gate(self):
        chapter = """\
            # 第一章

            据说，菲尔丁曾举杯诅咒那个发明戏剧第五幕的人。
            校注完一部浩繁的书，再编好一份详尽的索引，若有人不肯把发明序言的人算作人类的恩人，倒也情有可原。

            我们村寨里美人很多，
            她们眼底的黑暗中星光闪烁。
            爱她们很甜，是令人羡慕的命运；

            > 我死后，只愿有诚实的纪事者，<br />
            > 传扬我的名声。

            1. 外表
            2. 现实

            * * *

            一片幽暗、无边的大洋，<br />没有边界。
            """
        with tempfile.TemporaryDirectory(dir=REPO / "books") as tmp:
            root = Path(tmp)
            result = self.book(root, chapter)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            with zipfile.ZipFile(root / "output/book.epub") as archive:
                names = archive.namelist()
                self.assertNotIn("EPUB/preface.xhtml", names)
                self.assertNotIn("EPUB/translator_note.xhtml", names)
                cover = archive.read("EPUB/cover.xhtml").decode("utf-8")
                body = archive.read("EPUB/001_chapter.xhtml").decode("utf-8")
            self.assertNotIn("<h1", cover)
            self.assertNotIn("figcaption", cover)
            self.assertIn("的人。校注完", body)
            self.assertIn("很多，<br />她们", body)
            self.assertIn("<blockquote>", body)
            self.assertIn("<ol><li>外表</li><li>现实</li></ol>", body)
            self.assertNotIn("* * *", body)
            self.assertNotIn("&lt;br", body)
            report, _ = final_gate.check_epub(root / "output/book.epub")
            self.assertEqual("PASS", report.summary()["status"], report.summary()["issues"])

    def test_multi_element_unit_is_wrapped_once(self):
        chapter = f"""\
            # 第一章

            <!-- lifebook-unit:unit-1 source-sha256:{HASH} target-sha256:{HASH} -->
            最适合借诗人的语言来描写：
            > 一片幽暗、无边的大洋，<br />
            > 没有边界。

            <!-- lifebook-unit:unit-2 source-sha256:{HASH} target-sha256:{HASH} -->
            第二段。
            """
        with tempfile.TemporaryDirectory(dir=REPO / "books") as tmp:
            root = Path(tmp)
            result = self.book(root, chapter)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            with zipfile.ZipFile(root / "output/book.epub") as archive:
                body = archive.read("EPUB/001_chapter.xhtml").decode("utf-8")
        self.assertIn('<div class="unit" data-unit-id="unit-1"', body)
        self.assertIn('<p data-unit-id="unit-2"', body)

    def test_unedited_template_text_blocks_the_build(self):
        with tempfile.TemporaryDirectory(dir=REPO / "books") as tmp:
            result = self.book(Path(tmp), "# 第一章\n\n正文。\n", preface="# 前言\n\n本页为模板占位。\n")
        self.assertNotEqual(0, result.returncode)
        self.assertIn("template placeholder", result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()

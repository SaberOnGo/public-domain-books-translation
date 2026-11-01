import importlib.util
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / "template/epub_pipeline/common/scripts"


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


final_gate = load("check_final_epub")


def xhtml(body, lang="zh-Hans"):
    return (f'<?xml version="1.0" encoding="utf-8"?><html xmlns="http://www.w3.org/1999/xhtml" '
            f'xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="{lang}" lang="{lang}"><head><title>t</title></head>'
            f"<body>{body}</body></html>")


def make_epub(path, docs, identifier="urn:uuid:00000000-0000-4000-8000-000000000001",
              contributor="LifeBook 书坊", languages=("zh-Hans",), nav_labels=None):
    nav_labels = nav_labels or [name for name, _ in docs]
    items = "".join(f'<item id="d{i}" href="{name}" media-type="application/xhtml+xml"/>' for i, (name, _) in enumerate(docs))
    spine = "".join(f'<itemref idref="d{i}"/>' for i in range(len(docs)))
    langs = "".join(f"<dc:language>{lang}</dc:language>" for lang in languages)
    opf = (f'<?xml version="1.0" encoding="utf-8"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="id">'
           f'<metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="id">{identifier}</dc:identifier>'
           f"<dc:title>测试书</dc:title><dc:creator>作者</dc:creator><dc:contributor>{contributor}</dc:contributor>{langs}</metadata>"
           f'<manifest><item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>'
           f'<item id="cover-img" href="images/cover.png" media-type="image/png" properties="cover-image"/>{items}</manifest>'
           f"<spine>{spine}</spine></package>")
    links = "".join(f'<li><a href="{name}">{label}</a></li>' for (name, _), label in zip(docs, nav_labels))
    nav = xhtml(f'<nav epub:type="toc" id="toc"><ol>{links}</ol></nav>'
                f'<nav epub:type="landmarks"><ol><li><a epub:type="cover" href="cover.xhtml">封面</a></li></ol></nav>')
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("mimetype", "application/epub+zip")
        archive.writestr("META-INF/container.xml",
                         '<?xml version="1.0"?><container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">'
                         '<rootfiles><rootfile full-path="EPUB/package.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')
        archive.writestr("EPUB/package.opf", opf)
        archive.writestr("EPUB/nav.xhtml", nav)
        archive.writestr("EPUB/images/cover.png", b"png")
        for name, body in docs:
            archive.writestr(f"EPUB/{name}", xhtml(body))


CLEAN_DOCS = [
    ("cover.xhtml", '<figure class="cover"><img src="images/cover.png" alt="测试书封面"/></figure>'),
    ("book_info.xhtml", "<h1>书籍信息</h1><p>译制：LifeBook 书坊 译制</p>"),
    ("001_chapter.xhtml", "<h1>第一章 家族</h1><p>据说，菲尔丁曾举杯诅咒那个发明戏剧第五幕的人。</p>"
                          "<p>第一章 家族的由来，另见后文。</p>"
                          "<blockquote><p>我们村寨里美人很多，<br/>她们眼底的黑暗中星光闪烁。</p></blockquote>"),
]


class FinalEpubGateTests(unittest.TestCase):
    def check(self, docs, **kwargs):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "book.epub"
            make_epub(path, docs, **kwargs)
            report, _ = final_gate.check_epub(path)
            return report.summary()

    def test_clean_book_passes(self):
        result = self.check(CLEAN_DOCS, nav_labels=["封面", "书籍信息", "第一章 家族"])
        self.assertEqual("PASS", result["status"], result["issues"])

    def test_reader_visible_residue_is_reported(self):
        docs = [
            ("cover.xhtml", '<h1>封面</h1><figure><img src="images/cover.png" alt="封面"/><figcaption>测试书封面</figcaption></figure>'),
            ("preface.xhtml", "<h1>Preface</h1>"),
            ("001_chapter.xhtml",
             "<p>## 第一章</p>"
             "<p>一片幽暗、无边的大洋，&lt;br /&gt;没有边界。</p>"
             "<p>据说，菲尔丁曾举杯诅咒那个人。 校注完一部浩繁的书。</p>"
             "<p>**航行目的——舰队编成。**</p>"
             "<p>_来源部：第二卷 魂不守舍的人_</p>"
             '<p>她说"挂掉"了。</p>'
             "<p>[插图：马修·A·亨森]</p>"
             "<p>* * *</p>"),
            ("002_chapter.xhtml", ""),
        ]
        result = self.check(docs, contributor="LifeBook 书坊 + Codex", nav_labels=["封面", "Preface", "001_chapter_i", "x"])
        counts = result["rule_counts"]
        for rule in ("cover_visible_text", "placeholder_page", "markdown_heading_marker", "escaped_html_tag",
                     "cjk_ascii_space", "markdown_emphasis_marker", "ascii_quote_in_cjk", "illustration_placeholder",
                     "print_separator", "empty_page", "tool_name_in_frontmatter", "nav_label_looks_like_filename"):
            self.assertIn(rule, counts, rule)
        self.assertEqual("FAIL", result["status"])

    def test_bilingual_edition_needs_two_languages_and_its_own_identifier(self):
        bilingual_doc = [("bilingual_001.xhtml",
                          '<section class="bitext-unit"><div class="bitext-source" lang="en"><p>Hello.</p></div>'
                          '<div class="bitext-target" lang="zh-Hans"><p>你好。</p></div></section>')]
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "book.epub"
            bilingual = Path(tmp) / "book_bilingual_parallel.epub"
            make_epub(target, CLEAN_DOCS)
            make_epub(bilingual, CLEAN_DOCS[:2] + bilingual_doc, languages=("zh-Hans",))
            results = final_gate.check_editions([(target, "target_only"), (bilingual, "bilingual_parallel")])
        self.assertIn("duplicate_identifier_across_editions", results[1]["rule_counts"])
        self.assertIn("bilingual_language_metadata", results[1]["rule_counts"])


if __name__ == "__main__":
    unittest.main()

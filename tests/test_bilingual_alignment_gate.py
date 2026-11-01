import importlib.util
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "template/epub_pipeline/common/scripts/check_bilingual_alignment.py"
spec = importlib.util.spec_from_file_location("check_bilingual_alignment", SCRIPT)
alignment = importlib.util.module_from_spec(spec)
sys.modules["check_bilingual_alignment"] = alignment
spec.loader.exec_module(alignment)

# Twenty paragraph pairs whose Chinese length is proportional to the English word count.
PAIRS = []
for i in range(20):
    words = 20 + (i % 5) * 6
    english = " ".join(["word"] * (words - 2)) + f" chapter {1800 + i}."
    chinese = "这是一段完整的中文译文" * (words // 6) + f"，第{1800 + i}章。"
    PAIRS.append((english, chinese))


def make_bilingual(path, pairs):
    units = "".join(
        f'<section class="bitext-unit" data-align-id="u{i}"><div class="bitext-source" lang="en"><p>{src}</p></div>'
        f'<div class="bitext-target" lang="zh-Hans"><p>{tgt}</p></div></section>'
        for i, (src, tgt) in enumerate(pairs)
    )
    doc = f'<?xml version="1.0" encoding="utf-8"?><html xmlns="http://www.w3.org/1999/xhtml"><head><title>c</title></head><body>{units}</body></html>'
    opf = ('<?xml version="1.0"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="id">'
           '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="id">x</dc:identifier></metadata>'
           '<manifest><item id="c" href="bilingual_001.xhtml" media-type="application/xhtml+xml"/></manifest>'
           '<spine><itemref idref="c"/></spine></package>')
    with zipfile.ZipFile(path, "w") as archive:
        archive.writestr("mimetype", "application/epub+zip")
        archive.writestr("META-INF/container.xml",
                         '<?xml version="1.0"?><container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">'
                         '<rootfiles><rootfile full-path="EPUB/package.opf" media-type="application/oebps-package+xml"/></rootfiles></container>')
        archive.writestr("EPUB/package.opf", opf)
        archive.writestr("EPUB/bilingual_001.xhtml", doc)


class BilingualAlignmentGateTests(unittest.TestCase):
    def analyse(self, pairs):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "b.epub"
            make_bilingual(path, pairs)
            return alignment.analyse(alignment.read_pairs(path))

    def test_aligned_book_passes(self):
        result = self.analyse(PAIRS)
        self.assertEqual("PASS", result["status"], result["issues"][:3])

    def test_heading_paired_with_paragraph_fails(self):
        # The target of a short heading carries a whole paragraph, so the next pairs drift by one.
        sources = [src for src, _ in PAIRS[:8]] + ["Showing versus Telling"] + [src for src, _ in PAIRS[8:]]
        targets = [tgt for _, tgt in PAIRS[:8]] + [tgt for _, tgt in PAIRS[8:]] + ["展示与告知"]
        result = self.analyse(list(zip(sources, targets)))
        self.assertEqual("FAIL", result["status"])
        self.assertTrue(result["extreme_length_mismatches"] or result["misaligned_runs"])

    def test_kept_original_verse_is_a_warning_not_a_failure(self):
        pairs = PAIRS[:10] + [("Parva quidem regio, sed relligione priorum nota, celebrated in song and story.",
                               "Parva quidem regio, sed relligione priorum nota.")] + PAIRS[10:]
        result = self.analyse(pairs)
        self.assertEqual("PASS", result["status"], result["issues"][:3])
        self.assertEqual(1, result["untranslated_blocks"])


if __name__ == "__main__":
    unittest.main()

from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from xml.etree import ElementTree as ET

REPO = Path(__file__).resolve().parents[1]
SCRIPTS = REPO / 'template/epub_pipeline/common/scripts'


class NavigationLanguageTests(unittest.TestCase):
    def build_and_check(self, language, expected, overrides=''):
        with tempfile.TemporaryDirectory(dir=REPO / 'books') as temp:
            book = Path(temp)
            for name in ['scripts', 'metadata', 'state', 'frontmatter', 'chapters/src',
                         'chapters/final', 'qa/bilingual_parallel']:
                (book / name).mkdir(parents=True)
            for name in ['build_epub.js', 'build_bilingual_epub.py', 'run_python.js']:
                shutil.copyfile(SCRIPTS / name, book / 'scripts' / name)
            (book / 'metadata/book.yaml').write_text(
                f'title: Test Book\nauthor: Author\nlanguage: {language}\n{overrides}', encoding='utf-8')
            (book / 'frontmatter/cover.md').write_text('# Cover\n\nCover fixture.\n', encoding='utf-8')
            (book / 'frontmatter/book-info.md').write_text('# Book Information\n\nEdition fixture.\n', encoding='utf-8')
            (book / 'chapters/src/001.md').write_text('# 源语章节\n\n源段。\n', encoding='utf-8')
            (book / 'chapters/final/001.md').write_text('# English Chapter\n\nTarget paragraph.\n', encoding='utf-8')
            state = {'source_language': 'zh-Hans', 'target_language': language,
                     'edition_type': 'bilingual_parallel', 'bilingual_parallel': {'enabled': True}}
            (book / 'state/pipeline_state.json').write_text(json.dumps(state), encoding='utf-8')
            units = []
            for i, (source, target, kind) in enumerate([
                    ('源语章节', 'English Chapter', 'heading'), ('源段。', 'Target paragraph.', 'body')]):
                units.append({'id': f'u{i}', 'chapter': 'chapters/final/001.md', 'target_file': 'chapters/final/001.md',
                              'source_text': source, 'target_text': target, 'unit_type': kind,
                              'markdown_heading_level': 1 if kind == 'heading' else 0,
                              'source_sha256': hashlib.sha256(source.encode()).hexdigest(),
                              'target_sha256': hashlib.sha256(target.encode()).hexdigest()})
            (book / 'qa/bilingual_parallel/alignment_map.json').write_text(json.dumps(units), encoding='utf-8')
            for command in [['node', str(book / 'scripts/build_epub.js')],
                            [sys.executable, str(book / 'scripts/build_bilingual_epub.py')]]:
                result = subprocess.run(command, cwd=book, capture_output=True, text=True, encoding='utf-8')
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            ns = {'h': 'http://www.w3.org/1999/xhtml', 'epub': 'http://www.idpf.org/2007/ops'}
            for name in ['book.epub', 'book_bilingual_parallel.epub']:
                with zipfile.ZipFile(book / 'output' / name) as archive:
                    nav = ET.fromstring(archive.read('EPUB/nav.xhtml'))
                self.assertEqual(expected[0], nav.find('h:head/h:title', ns).text)
                self.assertEqual(expected[0], nav.find(".//h:nav[@id='toc']/h:h1", ns).text)
                landmarks = nav.find(".//h:nav[@epub:type='landmarks']", ns)
                self.assertIsNotNone(landmarks)
                self.assertEqual(expected[1], landmarks.find('h:h2', ns).text)
                self.assertEqual(expected[2:], [a.text for a in landmarks.findall('.//h:a', ns)])

    def test_english_navigation_in_both_editions(self):
        self.build_and_check('en', ['Contents', 'Guide', 'Cover', 'Book Information'])

    def test_chinese_navigation_keeps_existing_labels(self):
        self.build_and_check('zh-Hans', ['目录', '导览', '封面', '书籍信息'])

    def test_other_target_can_supply_localized_labels(self):
        self.build_and_check('fr', ['Sommaire & notes', 'Repères', 'Couverture', 'Informations'],
                             'navigation_title: Sommaire & notes\nnavigation_landmarks_title: Repères\n'
                             'navigation_cover_title: Couverture\nnavigation_book_info_title: Informations\n')


if __name__ == '__main__':
    unittest.main()

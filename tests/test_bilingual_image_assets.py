import base64
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from xml.etree import ElementTree as ET
import zipfile

REPO=Path(__file__).resolve().parents[1]
SCRIPT=REPO/'template/epub_pipeline/common/scripts/build_bilingual_epub.py'
PNG=base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jWZkAAAAASUVORK5CYII=')

class BilingualImageAssetsTests(unittest.TestCase):
    def fixture(self, root, ref='../../assets/images/illustration.png'):
        for name in ['metadata','references','state','frontmatter','chapters/src','chapters/final','qa/bilingual_parallel','assets/images']:
            (root/name).mkdir(parents=True)
        (root/'assets/images/cover.png').write_bytes(PNG)
        (root/'assets/images/illustration.png').write_bytes(PNG)
        (root/'metadata/book.yaml').write_text('title: Image fixture\nauthor: Test Author\nlanguage: en\n',encoding='utf-8')
        (root/'references/reader_facing_titles.json').write_text(json.dumps({'chapters/final/001.md':'1. Compact navigation title'}),encoding='utf-8')
        (root/'frontmatter/cover.md').write_text('# Cover\n\n![Cover illustration](../assets/images/cover.png)\n',encoding='utf-8')
        state={'source_language':'zh-Hans','target_language':'en','edition_type':'bilingual_parallel','bilingual_parallel':{'enabled':True}}
        (root/'state/pipeline_state.json').write_text(json.dumps(state),encoding='utf-8')
        texts=[('第一章','First Chapter','heading'),(f'![原图]({ref})',f'![A woodland illustration.]({ref})','image'),('原段。','A complete target paragraph.','body')]
        rows=[]
        for i,(source,target,kind) in enumerate(texts):
            rows.append(dict(id=f'unit-{i}',chapter='chapters/final/001.md',source_file='chapters/src/001.md',target_file='chapters/final/001.md',
                source_text=source,target_text=target,unit_type=kind,markdown_heading_level=1 if kind=='heading' else 0,
                source_sha256=hashlib.sha256(source.encode()).hexdigest(),target_sha256=hashlib.sha256(target.encode()).hexdigest()))
        for side,folder in [('source','src'),('target','final')]:
            (root/f'chapters/{folder}/001.md').write_text('\n\n'.join(('# ' if x['unit_type']=='heading' else '')+x[f'{side}_text'] for x in rows)+'\n',encoding='utf-8')
        (root/'qa/bilingual_parallel/alignment_map.json').write_text(json.dumps(rows,ensure_ascii=False),encoding='utf-8')

    def run_build(self, root):
        return subprocess.run([sys.executable,str(SCRIPT),'--book-root',str(root)],capture_output=True,text=True,encoding='utf-8')

    def test_cover_and_paired_image_packaged_with_caption_and_manifest(self):
        with tempfile.TemporaryDirectory(dir=REPO/'books') as tmp:
            root=Path(tmp);self.fixture(root)
            result=self.run_build(root);self.assertEqual(0,result.returncode,result.stdout+result.stderr)
            ns={'h':'http://www.w3.org/1999/xhtml','o':'http://www.idpf.org/2007/opf'}
            with zipfile.ZipFile(root/'output/book_bilingual_parallel.epub') as archive:
                opf=ET.fromstring(archive.read('EPUB/package.opf'))
                images=[x for x in opf.findall('o:manifest/o:item',ns) if x.get('media-type','').startswith('image/')]
                self.assertEqual(2,len(images),'cover and original illustration must be declared exactly once')
                self.assertEqual(1,sum('cover-image' in x.get('properties','').split() for x in images))
                for item in images:self.assertEqual(PNG,archive.read('EPUB/'+item.get('href')))
                chapter=ET.fromstring(archive.read('EPUB/bilingual_001.xhtml'))
                self.assertEqual(2,len(chapter.findall('.//h:h1',ns)), 'a short nav label must not add a third visible heading')
                figure=chapter.findall('.//h:figure',ns);self.assertEqual(2,len(figure))
                self.assertEqual(['原图','A woodland illustration.'],[x.find('h:figcaption',ns).text for x in figure])
                for f in figure:
                    img=f.find('h:img',ns);self.assertEqual(PNG,archive.read('EPUB/'+img.get('src')))
                cover=ET.fromstring(archive.read('EPUB/cover.xhtml'));self.assertIsNotNone(cover.find('.//h:img',ns))
                css=archive.read('EPUB/styles/book.css').decode();self.assertIn('max-width:100%',css)

    def test_invalid_image_references_fail_instead_of_literal_markdown(self):
        for ref in ['../../assets/images/missing.png','https://example.invalid/image.png','../../../../outside.png']:
            with self.subTest(ref=ref),tempfile.TemporaryDirectory(dir=REPO/'books') as tmp:
                root=Path(tmp);self.fixture(root,ref);result=self.run_build(root)
                self.assertNotEqual(0,result.returncode,result.stdout+result.stderr)
                self.assertFalse((root/'output/book_bilingual_parallel.epub').exists())

if __name__=='__main__':unittest.main()

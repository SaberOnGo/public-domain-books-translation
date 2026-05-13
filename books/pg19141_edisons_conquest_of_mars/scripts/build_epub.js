const fs = require('fs');
const path = require('path');
const zlib = require('zlib');

const root = path.resolve(__dirname, '..');
const finalDir = path.join(root, 'chapters', 'final');
const outputDir = path.join(root, 'output');
const outFile = path.join(outputDir, 'book.epub');
const cnOutFile = path.join(outputDir, '爱迪生征服火星.epub');
const titleMapPath = path.join(root, 'metadata', 'chapter_title_map.yaml');

const meta = {
  title: '爱迪生征服火星',
  subtitle: "Edison's Conquest of Mars",
  originalTitle: "Edison's Conquest of Mars",
  author: 'Garrett P. Serviss',
  authorZh: '加勒特·P. 瑟维斯',
  translator: 'LifeBook 书坊',
  translationDate: '2026-05-13',
  language: 'zh-CN',
  originalLanguage: 'en',
  identifier: 'pg19141-zh-cn-lifebook-v1',
  publisher: 'LifeBook 书坊',
  sourceUrl: 'https://www.gutenberg.org/ebooks/19141',
  sourceId: 'Project Gutenberg #19141',
  originalPublication: '1898 年英文原著。本译本依据 Project Gutenberg #19141 公版文本制作。',
  description: '本书是美国早期科幻小说，承接威尔斯《世界大战》的火星入侵想象，写托马斯·爱迪生组织科学家与地球舰队，以电力飞船和分解射线反攻火星。本中文 EPUB 由 LifeBook 书坊依据 Project Gutenberg #19141 公版英文原文新译制作，翻译时间为 2026-05-13。源文本在美国为公版，跨地区发行前仍应按目标国家或地区复核版权状态。',
  rights: '源文本：Project Gutenberg #19141，美国公版文本。中文译本：LifeBook 书坊译制，发行和授权由项目所有者决定。'
};
const coverJpgPath = path.join(root, 'assets', 'cover.jpg');
const coverPngPath = path.join(root, 'assets', 'cover.png');
const coverImageName = fs.existsSync(coverJpgPath) ? 'cover.jpg' : (fs.existsSync(coverPngPath) ? 'cover.png' : 'cover.svg');
const coverImageType = coverImageName.endsWith('.jpg') ? 'image/jpeg' : (coverImageName.endsWith('.png') ? 'image/png' : 'image/svg+xml');
const coverImageData = coverImageName.endsWith('.jpg') ? fs.readFileSync(coverJpgPath) : (coverImageName.endsWith('.png') ? fs.readFileSync(coverPngPath) : coverSvg());
function esc(text) {
  return String(text)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function inline(text) {
  const placeholders = [];
  let s = String(text).replace(/_([^_\n]{1,120})_/g, (_, inner) => {
    const key = `\u0000${placeholders.length}\u0000`;
    placeholders.push(`<em>${esc(inner)}</em>`);
    return key;
  });
  s = esc(s);
  placeholders.forEach((value, i) => {
    s = s.replace(new RegExp(`\\u0000${i}\\u0000`, 'g'), value);
  });
  return s;
}

function unquoteYamlValue(value) {
  const trimmed = String(value || '').trim();
  if (!trimmed) return '';
  if ((trimmed.startsWith('"') && trimmed.endsWith('"')) || (trimmed.startsWith("'") && trimmed.endsWith("'"))) {
    return trimmed.slice(1, -1).replace(/\\"/g, '"').replace(/\\'/g, "'");
  }
  return trimmed;
}

function readChapterTitleMap(filePath) {
  if (!fs.existsSync(filePath)) return {};
  const map = {};
  let current = null;
  const lines = fs.readFileSync(filePath, 'utf8').replace(/\r\n/g, '\n').split('\n');
  for (const line of lines) {
    const chapterMatch = line.match(/^  ([^:\s][^:]*\.md):\s*$/);
    if (chapterMatch) {
      current = chapterMatch[1].trim();
      map[current] = {};
      continue;
    }
    const fieldMatch = line.match(/^    ([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$/);
    if (current && fieldMatch) {
      map[current][fieldMatch[1]] = unquoteYamlValue(fieldMatch[2]);
    }
  }
  return map;
}

function crc32(buf) {
  let c = ~0;
  for (const b of buf) {
    c ^= b;
    for (let k = 0; k < 8; k++) c = (c >>> 1) ^ (0xedb88320 & -(c & 1));
  }
  return (~c) >>> 0;
}

function dosDateTime(date = new Date()) {
  const year = Math.max(1980, date.getFullYear());
  const time = (date.getHours() << 11) | (date.getMinutes() << 5) | Math.floor(date.getSeconds() / 2);
  const day = ((year - 1980) << 9) | ((date.getMonth() + 1) << 5) | date.getDate();
  return { time, day };
}

function zipBuffer(files) {
  const chunks = [];
  const central = [];
  let offset = 0;
  const { time, day } = dosDateTime();
  for (const file of files) {
    const nameBuf = Buffer.from(file.name, 'utf8');
    const data = Buffer.isBuffer(file.data) ? file.data : Buffer.from(file.data);
    const method = file.store ? 0 : 8;
    const compressed = file.store ? data : zlib.deflateRawSync(data, { level: 9 });
    const crc = crc32(data);

    const local = Buffer.alloc(30 + nameBuf.length);
    local.writeUInt32LE(0x04034b50, 0);
    local.writeUInt16LE(20, 4);
    local.writeUInt16LE(0x0800, 6);
    local.writeUInt16LE(method, 8);
    local.writeUInt16LE(time, 10);
    local.writeUInt16LE(day, 12);
    local.writeUInt32LE(crc, 14);
    local.writeUInt32LE(compressed.length, 18);
    local.writeUInt32LE(data.length, 22);
    local.writeUInt16LE(nameBuf.length, 26);
    local.writeUInt16LE(0, 28);
    nameBuf.copy(local, 30);
    chunks.push(local, compressed);

    const cen = Buffer.alloc(46 + nameBuf.length);
    cen.writeUInt32LE(0x02014b50, 0);
    cen.writeUInt16LE(20, 4);
    cen.writeUInt16LE(20, 6);
    cen.writeUInt16LE(0x0800, 8);
    cen.writeUInt16LE(method, 10);
    cen.writeUInt16LE(time, 12);
    cen.writeUInt16LE(day, 14);
    cen.writeUInt32LE(crc, 16);
    cen.writeUInt32LE(compressed.length, 20);
    cen.writeUInt32LE(data.length, 24);
    cen.writeUInt16LE(nameBuf.length, 28);
    cen.writeUInt16LE(0, 30);
    cen.writeUInt16LE(0, 32);
    cen.writeUInt16LE(0, 34);
    cen.writeUInt16LE(0, 36);
    cen.writeUInt32LE(0, 38);
    cen.writeUInt32LE(offset, 42);
    nameBuf.copy(cen, 46);
    central.push(cen);
    offset += local.length + compressed.length;
  }
  const centralOffset = offset;
  for (const c of central) {
    chunks.push(c);
    offset += c.length;
  }
  const end = Buffer.alloc(22);
  end.writeUInt32LE(0x06054b50, 0);
  end.writeUInt16LE(0, 4);
  end.writeUInt16LE(0, 6);
  end.writeUInt16LE(files.length, 8);
  end.writeUInt16LE(files.length, 10);
  end.writeUInt32LE(offset - centralOffset, 12);
  end.writeUInt32LE(centralOffset, 16);
  end.writeUInt16LE(0, 20);
  chunks.push(end);
  return Buffer.concat(chunks);
}

function mdToHtml(md, titleMeta = null) {
  const lines = md.replace(/\r\n/g, '\n').split('\n');
  const blocks = [];
  let paragraph = [];
  let pre = [];
  let inPre = false;
  let firstHeadingRendered = false;

  function flushParagraph() {
    if (!paragraph.length) return;
    const text = paragraph.join(' ');
    if (/^(?:\*\s*){3,}$/.test(text.trim()) || /^-{3,}$/.test(text.trim())) {
      paragraph = [];
    } else {
      blocks.push(`<p>${inline(text)}</p>`);
    }
    paragraph = [];
  }
  function flushPre() {
    if (pre.length) {
      blocks.push(`<pre>${esc(pre.join('\n'))}</pre>`);
      pre = [];
    }
  }

  for (const line of lines) {
    if (/^```/.test(line)) {
      if (inPre) {
        flushPre();
        inPre = false;
      } else {
        flushParagraph();
        inPre = true;
      }
      continue;
    }
    if (inPre) {
      pre.push(line);
    } else if (/^# /.test(line)) {
      flushParagraph();
      if (!firstHeadingRendered && titleMeta && titleMeta.display_title) {
        blocks.push(formatChapterHeading(titleMeta));
      } else {
        blocks.push(formatHeading(line.replace(/^# /, '').trim(), 1));
      }
      firstHeadingRendered = true;
    } else if (/^## /.test(line)) {
      flushParagraph();
      blocks.push(formatHeading(line.replace(/^## /, '').trim(), 2));
    } else if (!line.trim()) {
      flushParagraph();
    } else {
      paragraph.push(line.trim());
    }
  }
  flushParagraph();
  flushPre();
  return blocks.join('\n');
}

function formatHeading(title, level) {
  const tag = level === 1 ? 'h1' : 'h2';
  const m = title.match(/^(第[一二三四五六七八九十]+章)\s*(.*)$/);
  if (level === 1 && m) {
    return `<h1><span class="chapter-kicker">${esc(m[1])}</span>${m[2] ? `<span class="chapter-title">${inline(m[2])}</span>` : ''}</h1>`;
  }
  return `<${tag}>${inline(title)}</${tag}>`;
}

function formatChapterHeading(titleMeta) {
  const displayTitle = titleMeta.display_title || titleMeta.nav_title || '';
  const subtitle = titleMeta.subtitle || '';
  const m = displayTitle.match(/^(第[一二三四五六七八九十百]+章|附录[一二三四五六七八九十]+)\s*(.*)$/);
  const main = m ? `<span class="chapter-kicker">${esc(m[1])}</span>${m[2] ? `<span class="chapter-title">${inline(m[2])}</span>` : ''}` : inline(displayTitle);
  return `<h1>${main}</h1>${subtitle ? `<p class="chapter-subtitle">${inline(subtitle)}</p>` : ''}`;
}

function xhtml(title, body, cssHref = 'style.css', extraHead = '') {
  return `<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="zh-CN" xml:lang="zh-CN">
<head>
  <meta charset="utf-8"/>
  <title>${esc(title)}</title>
  <link rel="stylesheet" type="text/css" href="${esc(cssHref)}"/>
  ${extraHead}
</head>
<body>
${body}
</body>
</html>`;
}

function readTitle(md, fallback) {
  const match = md.match(/^#\s+(.+)$/m);
  return match ? match[1].trim() : fallback;
}

function coverSvg() {
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="2400" viewBox="0 0 1600 2400" role="img" aria-label="${esc(meta.title)}封面">
  <defs>
    <linearGradient id="space" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#08111f"/>
      <stop offset="0.55" stop-color="#202936"/>
      <stop offset="1" stop-color="#5e1f17"/>
    </linearGradient>
    <linearGradient id="mars" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#f0a05b"/>
      <stop offset="0.6" stop-color="#ad3f2c"/>
      <stop offset="1" stop-color="#5f1817"/>
    </linearGradient>
  </defs>
  <rect width="1600" height="2400" fill="url(#space)"/>
  <circle cx="1160" cy="570" r="310" fill="url(#mars)" opacity="0.96"/>
  <path d="M910 520 C1040 455 1190 485 1390 430" fill="none" stroke="#f5c16f" stroke-width="22" opacity="0.38"/>
  <path d="M910 650 C1070 600 1195 660 1430 575" fill="none" stroke="#381313" stroke-width="18" opacity="0.35"/>
  <circle cx="310" cy="350" r="5" fill="#fff7da"/><circle cx="470" cy="520" r="4" fill="#fff7da"/><circle cx="650" cy="310" r="6" fill="#fff7da"/><circle cx="1320" cy="1010" r="5" fill="#fff7da"/>
  <path d="M250 1710 C480 1560 650 1640 825 1480 C1020 1305 1210 1410 1460 1200 L1460 2240 L250 2240 Z" fill="#1b2833" opacity="0.9"/>
  <path d="M300 1765 L960 1185 L1015 1245 L360 1830 Z" fill="#d7e9f6" opacity="0.72"/>
  <path d="M942 1138 L1088 1265 L1022 1315 L890 1190 Z" fill="#f6d678"/>
  <path d="M360 1850 C560 1760 720 1810 890 1660 C1080 1490 1235 1565 1460 1380 L1460 2240 L360 2240 Z" fill="#6d251d" opacity="0.9"/>
  <text x="800" y="360" text-anchor="middle" font-family="Noto Serif CJK SC, Source Han Serif SC, STSong, SimSun, serif" font-size="72" fill="#f4d891" letter-spacing="8">LifeBook 公版新译</text>
  <text x="800" y="760" text-anchor="middle" font-family="Noto Serif CJK SC, Source Han Serif SC, STSong, SimSun, serif" font-weight="700" font-size="150" fill="#fff7df">爱迪生</text>
  <text x="800" y="950" text-anchor="middle" font-family="Noto Serif CJK SC, Source Han Serif SC, STSong, SimSun, serif" font-weight="700" font-size="150" fill="#fff7df">征服火星</text>
  <line x1="410" y1="1055" x2="1190" y2="1055" stroke="#f4d891" stroke-width="5" opacity="0.78"/>
  <text x="800" y="1225" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="54" fill="#f4d891">Edison's Conquest of Mars</text>
  <text x="800" y="1365" text-anchor="middle" font-family="Noto Serif CJK SC, Source Han Serif SC, STSong, SimSun, serif" font-size="58" fill="#fff7df">加勒特·P. 瑟维斯 著</text>
  <text x="800" y="1455" text-anchor="middle" font-family="Noto Serif CJK SC, Source Han Serif SC, STSong, SimSun, serif" font-size="52" fill="#f4d891">LifeBook 书坊 译制</text>
  <text x="800" y="2110" text-anchor="middle" font-family="Noto Serif CJK SC, Source Han Serif SC, STSong, SimSun, serif" font-size="44" fill="#f6ddb2">依据 Project Gutenberg #19141 公版原文制作</text>
</svg>`;
}

function coverPage(coverImageName) {
  return xhtml('封面', `<section epub:type="cover" class="cover-page"><img class="cover-image" src="images/${coverImageName}" alt="${esc(meta.title)}"/></section>`);
}

function bookInfoPage() {
  return xhtml('版本说明', `<section epub:type="frontmatter" class="book-info">
<h1>版本说明</h1>
<dl>
  <dt>中文书名</dt><dd>${esc(meta.title)}</dd>
  <dt>英文原名</dt><dd><em>${esc(meta.originalTitle)}</em></dd>
  <dt>作者</dt><dd>${esc(meta.authorZh)}（${esc(meta.author)}）</dd>
  <dt>译者</dt><dd>${esc(meta.translator)}</dd>
  <dt>翻译时间</dt><dd>${esc(meta.translationDate)}</dd>
  <dt>原文来源</dt><dd>${esc(meta.sourceId)}，${esc(meta.sourceUrl)}</dd>
  <dt>公版说明</dt><dd>本译本依据 Project Gutenberg 提供的美国公版英文文本制作。跨国家或地区发行、商业使用或平台上架前，仍应按目标地区法律复核版权状态。</dd>
</dl>
<h2>本书简介</h2>
<p>${inline(meta.description)}</p>
<h2>原书信息</h2>
<p>${inline(meta.originalPublication)}</p>
</section>`);
}

fs.mkdirSync(outputDir, { recursive: true });

const chapterFiles = fs.readdirSync(finalDir)
  .filter((name) => name.endsWith('.md'))
  .sort();

if (!chapterFiles.length) throw new Error('No final chapter markdown files found in chapters/final');

const chapterTitleMap = readChapterTitleMap(titleMapPath);
const chapters = chapterFiles.map((file, idx) => {
  const md = fs.readFileSync(path.join(finalDir, file), 'utf8');
  const titleMeta = chapterTitleMap[file] || {};
  const title = titleMeta.nav_title || readTitle(md, `Chapter ${idx + 1}`);
  const displayTitle = titleMeta.display_title || title;
  const subtitle = titleMeta.subtitle || '';
  const href = `chapters/${file.replace(/\.md$/, '.xhtml')}`;
  return { id: `chap${idx + 1}`, file, title, displayTitle, subtitle, href, html: xhtml(displayTitle, mdToHtml(md, titleMeta), '../style.css') };
});

const navItems = [
  '<li><a href="book-info.xhtml">版本说明</a></li>',
  ...chapters.map((ch) => `<li><a href="${esc(ch.href)}">${esc(ch.title)}</a></li>`)
].join('\n');
const manifestItems = chapters.map((ch) => `<item id="${ch.id}" href="${esc(ch.href)}" media-type="application/xhtml+xml"/>`).join('\n    ');
const spineItems = chapters.map((ch) => `<itemref idref="${ch.id}"/>`).join('\n    ');
const modified = new Date().toISOString().replace(/\.\d{3}Z$/, 'Z');

const stylesheet = `@page { margin: 5pt; }
html { -webkit-text-size-adjust: 100%; }
body {
  font-size: 1em;
  line-height: 1.72;
  margin: 0;
  padding: 0 0.6em;
  text-align: justify;
}
p { text-indent: 2em; margin: 0.22em 0; widows: 2; orphans: 2; }
em { font-style: italic; }
h1, h2 {
  text-align: center;
  font-weight: 600;
  page-break-after: avoid;
  break-after: avoid;
}
h1 {
  font-size: 1.18em;
  line-height: 1.38;
  margin: 1.8em 0 1.2em;
  letter-spacing: 0.03em;
}
h2 { font-size: 1.05em; line-height: 1.4; margin: 1.5em 0 0.8em; }
.chapter-kicker { display: block; font-size: 1em; color: #334; margin-bottom: 0.35em; }
.chapter-title { display: block; font-size: 1em; }
.chapter-subtitle { text-indent: 0; text-align: center; font-size: 0.88em; line-height: 1.45; margin: -0.65em 0 1.4em; color: #445; }
pre { white-space: pre-wrap; line-height: 1.5; font-size: 0.92em; }
a { color: inherit; text-decoration: none; }
nav#toc ol { padding-left: 1.4em; }
nav#toc li { margin: 0.45em 0; line-height: 1.45; }
.cover-page { margin: 0; padding: 0; text-align: center; page-break-after: always; }
.cover-page .cover-image { display: block; width: 100%; height: auto; max-height: 100%; margin: 0 auto; }
.book-info h1 { margin-top: 1.2em; }
.book-info p { text-indent: 2em; }
dl { margin: 0.5em 0 1.2em; }
dt { font-weight: 600; margin-top: 0.65em; }
dd { margin-left: 0; padding-left: 1.2em; line-height: 1.55; }
`;

const packageOpf = `<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" unique-identifier="bookid" version="3.0" xml:lang="zh-CN">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="bookid">${esc(meta.identifier)}</dc:identifier>
    <dc:title>${esc(meta.title)}</dc:title>
    <dc:title id="original-title">${esc(meta.originalTitle)}</dc:title>
    <meta refines="#original-title" property="title-type">original</meta>
    <dc:creator id="creator">${esc(meta.author)}</dc:creator>
    <meta refines="#creator" property="role" scheme="marc:relators">aut</meta>
    <meta refines="#creator" property="alternate-script">${esc(meta.authorZh)}</meta>
    <dc:contributor id="translator">${esc(meta.translator)}</dc:contributor>
    <meta refines="#translator" property="role" scheme="marc:relators">trl</meta>
    <dc:language>${esc(meta.language)}</dc:language>
    <dc:publisher>${esc(meta.publisher)}</dc:publisher>
    <dc:date>${esc(meta.translationDate)}</dc:date>
    <dc:source>${esc(meta.sourceUrl)}</dc:source>
    <dc:description>${esc(meta.description)}</dc:description>
    <dc:rights>${esc(meta.rights)}</dc:rights>
    <dc:subject>早期科幻</dc:subject>
    <dc:subject>火星小说</dc:subject>
    <dc:subject>公版书新译</dc:subject>
    <meta property="dcterms:modified">${modified}</meta>
    <meta property="schema:translationOfWork">${esc(meta.originalTitle)}</meta>
    <meta property="schema:translator">${esc(meta.translator)}</meta>
    <meta name="cover" content="cover-image"/>
  </metadata>
  <manifest>
    <item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>
    <item id="css" href="style.css" media-type="text/css"/>
    <item id="cover" href="cover.xhtml" media-type="application/xhtml+xml"/>
    <item id="book-info" href="book-info.xhtml" media-type="application/xhtml+xml"/>
    <item id="cover-image" href="images/${coverImageName}" media-type="${coverImageType}" properties="cover-image"/>
    ${manifestItems}
  </manifest>
  <spine>
    <itemref idref="cover" linear="no"/>
    <itemref idref="book-info"/>
    ${spineItems}
  </spine>
  <guide>
    <reference type="cover" title="封面" href="cover.xhtml"/>
    <reference type="toc" title="目录" href="nav.xhtml"/>
  </guide>
</package>`;

const nav = xhtml('目录', `<nav epub:type="toc" id="toc"><h1>目录</h1><ol>${navItems}</ol></nav>
<nav epub:type="landmarks" hidden="hidden"><h2>导航</h2><ol><li><a epub:type="cover" href="cover.xhtml">封面</a></li><li><a epub:type="frontmatter" href="book-info.xhtml">版本说明</a></li><li><a epub:type="bodymatter" href="${esc(chapters[0].href)}">正文开始</a></li></ol></nav>`);

const files = [];
files.push({ name: 'mimetype', data: Buffer.from('application/epub+zip'), store: true });
files.push({ name: 'META-INF/container.xml', data: `<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="EPUB/package.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>` });
files.push({ name: 'EPUB/style.css', data: stylesheet });
files.push({ name: 'EPUB/images/' + coverImageName, data: coverImageData });
files.push({ name: 'EPUB/cover.xhtml', data: coverPage(coverImageName) });
files.push({ name: 'EPUB/book-info.xhtml', data: bookInfoPage() });
files.push({ name: 'EPUB/nav.xhtml', data: nav });
for (const ch of chapters) files.push({ name: `EPUB/${ch.href}`, data: ch.html });
files.push({ name: 'EPUB/package.opf', data: packageOpf });

const buffer = zipBuffer(files);
fs.writeFileSync(path.join(outputDir, 'cover.svg'), coverSvg());
if (coverImageName === 'cover.jpg') fs.copyFileSync(coverJpgPath, path.join(outputDir, 'cover.jpg'));
if (coverImageName === 'cover.png') fs.copyFileSync(coverPngPath, path.join(outputDir, 'cover.png'));
fs.writeFileSync(outFile, buffer);
fs.writeFileSync(cnOutFile, buffer);
console.log(outFile);
console.log(cnOutFile);






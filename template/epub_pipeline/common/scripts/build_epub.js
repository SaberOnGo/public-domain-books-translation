const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');
const { randomUUID } = require('crypto');

const root = path.resolve(__dirname, '..');
const finalDir = path.join(root, 'chapters', 'final');
const frontmatterDir = path.join(root, 'frontmatter');
const outDir = path.join(root, 'output');
const workDir = path.join(outDir, 'epub_work');
const epubPath = path.join(outDir, 'book.epub');

function readText(file) {
  return fs.readFileSync(file, 'utf8').replace(/\r\n/g, '\n').replace(/\r/g, '\n');
}

function writeText(file, text) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, text, 'utf8');
}

function listFiles(dir, ext) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir)
    .filter((name) => name.toLowerCase().endsWith(ext))
    .sort()
    .map((name) => path.join(dir, name));
}

function parseYaml(file) {
  if (!fs.existsSync(file)) return {};
  const out = {};
  for (const line of readText(file).split('\n')) {
    const match = /^([A-Za-z0-9_-]+):\s*(.*)$/.exec(line);
    if (!match) continue;
    out[match[1]] = match[2].replace(/^["']|["']$/g, '').trim();
  }
  return out;
}

function escapeHtml(text) {
  return text
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function inline(text) {
  return escapeHtml(text).replace(/`([^`]+)`/g, '<code>$1</code>');
}

function parseMarkdownTable(lines, start) {
  const rows = [];
  let i = start;
  while (i < lines.length) {
    const line = lines[i].trim();
    if (!line.startsWith('|') || !line.endsWith('|')) break;
    rows.push(line.slice(1, -1).split('|').map((cell) => cell.trim()));
    i += 1;
  }
  if (rows.length < 2 || !rows[1].every((cell) => /^:?-{3,}:?$/.test(cell))) return null;
  return { rows: [rows[0], ...rows.slice(2)], next: i };
}

function tableHtml(rows) {
  const header = rows[0];
  const bodyRows = rows.slice(1);
  const thead = `<thead><tr>${header.map((cell) => `<th scope="col">${inline(cell)}</th>`).join('')}</tr></thead>`;
  const tbody = bodyRows.map((row) => {
    const padded = [...row, ...Array(Math.max(0, header.length - row.length)).fill('')].slice(0, header.length);
    return `<tr>${padded.map((cell) => `<td>${inline(cell)}</td>`).join('')}</tr>`;
  }).join('');
  return `<div class="table-wrap" role="region" aria-label="结构化表格"><table><caption>结构化表格</caption>${thead}<tbody>${tbody}</tbody></table></div>`;
}

function isRawHtmlLine(line) {
  return /^<\/?(section|p|aside|div|span|blockquote|ol|ul|li|dl|dt|dd|sup|a|em|strong|br)\b[^>]*>/.test(line.trim());
}

function slug(file) {
  return path.basename(file, path.extname(file)).replace(/[^A-Za-z0-9_-]+/g, '_');
}

function frontmatterRank(file) {
  const name = path.basename(file, path.extname(file)).toLowerCase();
  const ranks = {
    cover: 0,
    book_info: 1,
    'book-info': 1,
    translator_note: 2,
    'translator-note': 2,
    edition_note: 2,
    'edition-note': 2,
    preface: 3,
  };
  return Object.prototype.hasOwnProperty.call(ranks, name) ? ranks[name] : 10;
}

function mediaType(file) {
  const ext = path.extname(file).toLowerCase();
  if (ext === '.css') return 'text/css';
  if (ext === '.svg') return 'image/svg+xml';
  if (ext === '.png') return 'image/png';
  if (ext === '.jpg' || ext === '.jpeg') return 'image/jpeg';
  if (ext === '.webp') return 'image/webp';
  if (ext === '.xhtml') return 'application/xhtml+xml';
  throw new Error(`Unsupported EPUB asset type: ${file}`);
}

function resolveBookPath(fromFile, ref) {
  if (/^[a-z]+:\/\//i.test(ref) || ref.startsWith('file://') || /^[A-Za-z]:[\\/]/.test(ref)) {
    throw new Error(`EPUB asset reference must be relative: ${ref}`);
  }
  const resolved = path.resolve(path.dirname(fromFile), ref);
  if (!resolved.startsWith(root + path.sep)) {
    throw new Error(`EPUB asset escapes book root: ${ref}`);
  }
  if (!fs.existsSync(resolved)) {
    throw new Error(`Missing EPUB asset: ${ref}`);
  }
  return resolved;
}

function markdownToBody(file, imageMap) {
  const out = [];
  let para = [];
  const flush = () => {
    if (para.length) {
      out.push(`<p>${inline(para.join(' ').trim())}</p>`);
      para = [];
    }
  };

  const lines = readText(file).split('\n');
  for (let i = 0; i < lines.length; i += 1) {
    const raw = lines[i];
    const line = raw.trimEnd();
    if (!line.trim()) {
      flush();
      continue;
    }
    if (isRawHtmlLine(line)) {
      flush();
      out.push(line.trim());
      continue;
    }
    const table = parseMarkdownTable(lines, i);
    if (table) {
      flush();
      out.push(tableHtml(table.rows));
      i = table.next - 1;
      continue;
    }
    const image = /^!\[([^\]]*)\]\(([^)]+)\)$/.exec(line.trim());
    if (image) {
      flush();
      const src = resolveBookPath(file, image[2]);
      const copied = copyAsset(src, 'images');
      imageMap.set(copied.href, copied);
      out.push(`<figure><img src="${copied.href}" alt="${escapeHtml(image[1])}" /><figcaption>${inline(image[1])}</figcaption></figure>`);
      continue;
    }
    const heading = /^(#{1,6})\s+(.+)$/.exec(line);
    if (heading) {
      flush();
      const level = Math.min(heading[1].length, 3);
      out.push(`<h${level}>${inline(heading[2].trim())}</h${level}>`);
      continue;
    }
    const ordered = /^\d+\.\s+(.+)$/.exec(line.trim());
    if (ordered) {
      flush();
      out.push(`<p class="list-item">${inline(ordered[1])}</p>`);
      continue;
    }
    para.push(line.trim());
  }
  flush();
  return out.join('\n');
}

function xhtml(title, body) {
  return `<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="zh-CN" lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>${escapeHtml(title)}</title>
  <link rel="stylesheet" type="text/css" href="styles/book.css" />
</head>
<body>
${body}
</body>
</html>
`;
}

function copyAsset(src, folder) {
  const targetName = path.basename(src);
  const rel = `${folder}/${targetName}`;
  const target = path.join(workDir, 'EPUB', rel);
  fs.mkdirSync(path.dirname(target), { recursive: true });
  fs.copyFileSync(src, target);
  return { href: rel, mediaType: mediaType(src) };
}

function cleanWorkDir() {
  fs.rmSync(workDir, { recursive: true, force: true });
  fs.mkdirSync(path.join(workDir, 'META-INF'), { recursive: true });
  fs.mkdirSync(path.join(workDir, 'EPUB', 'styles'), { recursive: true });
  fs.mkdirSync(path.join(workDir, 'EPUB', 'images'), { recursive: true });
}

function writeContainer() {
  writeText(path.join(workDir, 'mimetype'), 'application/epub+zip');
  writeText(path.join(workDir, 'META-INF', 'container.xml'), `<?xml version="1.0" encoding="utf-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="EPUB/package.opf" media-type="application/oebps-package+xml" />
  </rootfiles>
</container>
`);
}

function writeCss() {
  writeText(path.join(workDir, 'EPUB', 'styles', 'book.css'), `body{line-height:1.72;margin:0;padding:1.2em;overflow-wrap:break-word}p{margin:0 0 .7em;text-indent:2em}h1{font-size:1.55em;line-height:1.25}h2{font-size:1.2em}h3{font-size:1.05em}img{max-width:100%;height:auto}figure{margin:1.2em 0;text-align:center;break-inside:avoid}figcaption{font-size:.88em;line-height:1.45}code{font-family:monospace;overflow-wrap:anywhere}.list-item{text-indent:0;margin-left:1.5em}.parallel-passage{margin:0 0 1.15em}.source-text{color:#4c3828}.modern-text{color:#1f1f1f}aside{font-size:.88em;line-height:1.55;margin:.25em 0 .75em 2em;color:#4b4b4b}.table-wrap{display:block;width:100%;max-width:100%;margin:.8em 0 1.2em;overflow:visible}table{border-collapse:collapse;width:100%;max-width:100%;table-layout:fixed;font-size:.74em;line-height:1.34;page-break-inside:auto;break-inside:auto}caption{font-size:.9em;line-height:1.35;margin:0 0 .35em;text-align:left}th,td{border:1px solid #777;padding:.22em .28em;vertical-align:top;white-space:normal;overflow-wrap:anywhere;word-break:break-word}th{font-weight:600;background:#f2f2f2}tr{page-break-inside:avoid;break-inside:avoid}`);
}

function zipEpub() {
  fs.rmSync(epubPath, { force: true });
  const code = `
import pathlib, zipfile
root = pathlib.Path(${JSON.stringify(workDir)})
out = pathlib.Path(${JSON.stringify(epubPath)})
with zipfile.ZipFile(out, "w") as zf:
    zf.write(root / "mimetype", "mimetype", compress_type=zipfile.ZIP_STORED)
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.name != "mimetype":
            zf.write(path, path.relative_to(root).as_posix(), compress_type=zipfile.ZIP_DEFLATED)
`;
  const result = spawnSync(process.execPath, [path.join(__dirname, 'run_python.js'), '-c', code], { encoding: 'utf8' });
  if (result.status !== 0) {
    process.stderr.write(result.stderr || result.stdout);
    process.exit(result.status || 1);
  }
}

function main() {
  const chapters = listFiles(finalDir, '.md');
  if (!chapters.length) {
    console.error('No final chapters found under chapters/final. Build is blocked until chapter gates pass.');
    process.exit(1);
  }

  const metadata = parseYaml(path.join(root, 'metadata', 'book.yaml'));
  const title = metadata.title || metadata['title_zh'] || metadata['title_zh_hans'] || 'Untitled Book';
  const creator = metadata.author || metadata.creator || 'Unknown';
  const contributor = metadata.contributor || 'LifeBook 书坊';
  const publisher = metadata.publisher || 'LifeBook 书坊';
  const source = metadata.source_url || metadata.source || metadata.source_text_url || '';
  const description = metadata.description || metadata.subtitle || '';
  const rights = metadata.rights || '';
  const date = metadata.date || '';
  const language = metadata.language || 'zh-CN';
  const id = metadata.identifier || `urn:uuid:${randomUUID()}`;
  const imageMap = new Map();

  cleanWorkDir();
  writeContainer();
  writeCss();

  const spine = [];
  const manifestItems = [
    '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav" />',
    '<item id="css" href="styles/book.css" media-type="text/css" />',
  ];
  const navItems = [];

  const frontmatter = listFiles(frontmatterDir, '.md').sort((a, b) => {
    const rank = frontmatterRank(a) - frontmatterRank(b);
    return rank || path.basename(a).localeCompare(path.basename(b));
  });
  const allDocs = [...frontmatter, ...chapters];
  allDocs.forEach((file, index) => {
    const idref = `doc${index + 1}`;
    const href = `${slug(file)}.xhtml`;
    const firstHeading = (readText(file).match(/^#\s+(.+)$/m) || [null, path.basename(file, '.md')])[1];
    const body = markdownToBody(file, imageMap);
    writeText(path.join(workDir, 'EPUB', href), xhtml(firstHeading, body));
    manifestItems.push(`<item id="${idref}" href="${href}" media-type="application/xhtml+xml" />`);
    spine.push(`<itemref idref="${idref}" />`);
    navItems.push(`<li><a href="${href}">${escapeHtml(firstHeading)}</a></li>`);
  });

  for (const asset of imageMap.values()) {
    const idref = `asset-${manifestItems.length}`;
    const properties = asset.href === 'images/cover.jpg' ? ' properties="cover-image"' : '';
    manifestItems.push(`<item id="${idref}" href="${asset.href}" media-type="${asset.mediaType}"${properties} />`);
  }

  const coverHref = allDocs.find((file) => slug(file) === 'cover') ? 'cover.xhtml' : '';
  const bookInfoFile = allDocs.find((file) => ['book_info', 'book-info'].includes(slug(file)));
  const bookInfoHref = bookInfoFile ? `${slug(bookInfoFile)}.xhtml` : '';

  writeText(path.join(workDir, 'EPUB', 'nav.xhtml'), `<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="zh-CN" lang="zh-CN">
<head><meta charset="utf-8" /><title>目录</title><link rel="stylesheet" type="text/css" href="styles/book.css" /></head>
<body>
<nav epub:type="toc" id="toc"><h1>目录</h1><ol>${navItems.join('\n')}</ol></nav>
<nav epub:type="landmarks" id="landmarks" hidden="hidden"><h2>导览</h2><ol>
${coverHref ? `<li><a epub:type="cover" href="${coverHref}">封面</a></li>` : ''}
${bookInfoHref ? `<li><a epub:type="frontmatter" href="${bookInfoHref}">书籍信息</a></li>` : ''}
</ol></nav>
</body>
</html>
`);

  const modified = new Date().toISOString().replace(/\.\d{3}Z$/, 'Z');
  writeText(path.join(workDir, 'EPUB', 'package.opf'), `<?xml version="1.0" encoding="utf-8"?>
<package version="3.0" unique-identifier="bookid" xmlns="http://www.idpf.org/2007/opf">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/">
    <dc:identifier id="bookid">${escapeHtml(id)}</dc:identifier>
    <dc:title>${escapeHtml(title)}</dc:title>
    <dc:creator>${escapeHtml(creator)}</dc:creator>
    <dc:contributor>${escapeHtml(contributor)}</dc:contributor>
    <dc:publisher>${escapeHtml(publisher)}</dc:publisher>
    <dc:language>${escapeHtml(language)}</dc:language>
    ${date ? `<dc:date>${escapeHtml(date)}</dc:date>` : ''}
    ${source ? `<dc:source>${escapeHtml(source)}</dc:source>` : ''}
    ${description ? `<dc:description>${escapeHtml(description)}</dc:description>` : ''}
    ${rights ? `<dc:rights>${escapeHtml(rights)}</dc:rights>` : ''}
    <meta property="dcterms:modified">${modified}</meta>
  </metadata>
  <manifest>
    ${manifestItems.join('\n    ')}
  </manifest>
  <spine>
    ${spine.join('\n    ')}
  </spine>
</package>
`);

  fs.mkdirSync(outDir, { recursive: true });
  zipEpub();
  console.log(`wrote ${path.relative(root, epubPath)}`);
}

main();

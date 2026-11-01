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

function navigationLabels(metadata, language) {
  const defaults = language.startsWith('zh')
    ? { toc: '目录', landmarks: '导览', cover: '封面', bookInfo: '书籍信息' }
    : { toc: 'Contents', landmarks: 'Guide', cover: 'Cover', bookInfo: 'Book Information' };
  return {
    toc: escapeHtml(metadata.navigation_title || defaults.toc),
    landmarks: escapeHtml(metadata.navigation_landmarks_title || defaults.landmarks),
    cover: escapeHtml(metadata.navigation_cover_title || defaults.cover),
    bookInfo: escapeHtml(metadata.navigation_book_info_title || defaults.bookInfo),
  };
}

const CJK_TEXT = '\\u3001-\\u303f\\u3040-\\u30ff\\u3400-\\u4dbf\\u4e00-\\u9fff\\uf900-\\ufaff\\uff01-\\uff0f\\uff1a-\\uff20\\uff3b-\\uff40\\uff5b-\\uff65';
const CJK_CHAR = new RegExp(`[${CJK_TEXT}]`);
const CJK_QUOTES = '“”‘’';
// Sentence-level storage sometimes rejoins CJK sentences with ASCII spaces; readers must not see them.
const SPACE_AFTER_CJK_PUNCT = new RegExp(`(?<=[，。！？；：、）」』〉》】…”’])[ \\u00a0]+(?=[${CJK_TEXT}“‘「『（《〈【])`, 'g');
const LINE_BREAK = ' ';
const TRAILING_BR = /<br\s*\/?>\s*$/i;
const SENTENCE_END = /[。！？!?…]+[”’」』）)]*$/;
const THEMATIC_BREAK = /^(?:[*\-_]\s*){3,}$/;
const QUOTE_LINE = /^>\s?/;
const LIST_LINE = /^(?:([-*+])|(\d{1,3})[.)])\s+(\S.*)$/;
const RAW_TAG_LINE = /^<\/?(?:blockquote|ol|ul|section|aside|div|figure|table)\b[^>]*>$/i;
const IMAGE_LINE = /^!\[([^\]]*)\]\(([^)]+)\)$/;
const VERSE_LINE_MAX_CJK = 32;
const VERSE_LINE_MAX_LATIN = 48;
const PLACEHOLDER_MARKER = /<!--\s*lifebook:placeholder\b/i;
const LEGACY_PLACEHOLDER = /本页为模板占位|译本前言模板|译者说明模板|模板占位|Translator Name/i;

function isCjkBoundary(left, right) {
  const leftCjk = CJK_CHAR.test(left);
  const rightCjk = CJK_CHAR.test(right);
  return (leftCjk || CJK_QUOTES.includes(left)) && (rightCjk || CJK_QUOTES.includes(right)) && (leftCjk || rightCjk);
}

// Several short lines in one block are verse, a song, an address or a letter heading: keep the breaks.
// Two short lines that each end a sentence are more likely two prose sentences stored one per line.
function looksLikeVerse(lines) {
  if (lines.length < 2) return false;
  const limit = lines.some((line) => CJK_CHAR.test(line)) ? VERSE_LINE_MAX_CJK : VERSE_LINE_MAX_LATIN;
  if (!lines.every((line) => [...line].length <= limit)) return false;
  return lines.length >= 3 || !SENTENCE_END.test(lines[0]);
}

// Join a block's source lines: verse and hard breaks keep LINE_BREAK, CJK prose joins without spaces.
function joinLines(rawLines) {
  const lines = [];
  for (const raw of rawLines) {
    const hard = / {2}$/.test(raw) || /\\$/.test(raw.trimEnd()) || TRAILING_BR.test(raw.trim());
    const line = raw.trim().replace(/\\$/, '').replace(TRAILING_BR, '').trim();
    if (line) lines.push([line, hard]);
  }
  if (!lines.length) return '';
  const verse = looksLikeVerse(lines.map(([line]) => line));
  let out = lines[0][0];
  for (let i = 1; i < lines.length; i += 1) {
    const line = lines[i][0];
    if (verse || lines[i - 1][1]) out += LINE_BREAK + line;
    else if (isCjkBoundary(out[out.length - 1], line[0])) out += line;
    else out += ` ${line}`;
  }
  return out;
}

function inline(text) {
  return escapeHtml(text.replace(SPACE_AFTER_CJK_PUNCT, ''))
    .replace(/&lt;br\s*\/?&gt;/gi, LINE_BREAK)
    .replace(/&lt;\/?(?:blockquote|p|div|section)(?:\s[^&]*)?&gt;/gi, '')
    .replace(/&lt;(\/?)(em|strong|i|b|sup|sub|small)&gt;/gi, (match, slash, tag) => `<${slash}${tag.toLowerCase()}>`)
    .replace(/(^|[^\w])\[(\d+)\](?!\w)/g, '$1<sup class="note-ref">[$2]</sup>')
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/__([^_]+)__/g, '<strong>$1</strong>')
    .replace(/(^|[^*])\*([^*]+)\*(?!\*)/g, '$1<em>$2</em>')
    .replace(/(^|[^_\w])_([^_]+)_(?![_\w])/g, '$1<em>$2</em>')
    .split(LINE_BREAK).join('<br />');
}

// 'skip' for marked or heading-only placeholders, 'fail' for unedited template text, else 'ok'.
function frontmatterStatus(file) {
  const text = readText(file);
  if (PLACEHOLDER_MARKER.test(text)) return 'skip';
  const body = text.replace(/<!--[\s\S]*?-->/g, '');
  if (LEGACY_PLACEHOLDER.test(body)) return 'fail';
  const content = body.split('\n').filter((line) => line.trim() && !/^\s*#{1,6}\s/.test(line));
  return content.length ? 'ok' : 'skip';
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
  let caption = '';
  let captionIndex = start - 1;
  while (captionIndex >= 0 && !lines[captionIndex].trim()) captionIndex -= 1;
  if (captionIndex >= 0 && /^表(?:\s|[:：])/.test(lines[captionIndex].trim())) {
    caption = lines[captionIndex].trim();
  }
  return { rows: [rows[0], ...rows.slice(2)], next: i, caption };
}

function tableHtml(rows, caption) {
  const header = rows[0];
  const bodyRows = rows.slice(1);
  const accessibleCaption = caption || '结构化表格';
  const thead = `<thead><tr>${header.map((cell) => `<th scope="col">${inline(cell)}</th>`).join('')}</tr></thead>`;
  const tbody = bodyRows.map((row) => {
    const padded = [...row, ...Array(Math.max(0, header.length - row.length)).fill('')].slice(0, header.length);
    return `<tr>${padded.map((cell) => `<td>${inline(cell)}</td>`).join('')}</tr>`;
  }).join('');
  return `<div class="table-wrap" role="region" aria-label="${escapeHtml(accessibleCaption)}"><table><caption>${inline(accessibleCaption)}</caption>${thead}<tbody>${tbody}</tbody></table></div>`;
}

function isRawHtmlLine(line) {
  return /^<\/?(section|p|aside|div|span|blockquote|ol|ul|li|dl|dt|dd|sup|sub|a|em|strong|br)\b[^>]*>/.test(line.trim());
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

function loadReaderTitles() {
  const file = path.join(root, 'references', 'reader_facing_titles.json');
  if (!fs.existsSync(file)) return {};
  const parsed = JSON.parse(readText(file));
  if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) {
    throw new Error(`Reader-facing titles must be a JSON object: ${file}`);
  }
  return parsed;
}

function readerTitle(file, readerTitles) {
  const key = path.relative(root, file).split(path.sep).join('/');
  const override = readerTitles[key];
  if (typeof override === 'string' && override.trim()) return override.trim();
  const heading = (readText(file).match(/^#\s+(.+)$/m) || [null, ''])[1];
  if (heading && heading.trim()) return heading.trim();
  throw new Error(`Missing reader-facing Markdown title and override: ${key}`);
}

function hasMarkdownHeading(file) {
  return /^#\s+(.+)$/m.test(readText(file));
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

function markdownToBody(file, imageMap, options = {}) {
  const cover = Boolean(options.cover);
  const out = [];
  let para = [];
  let quote = null;
  let list = null;
  let unit = null;
  const markerPattern = /^<!--\s*lifebook-unit:([^\s]+)\s+source-sha256:([0-9a-f]{64})\s+target-sha256:([0-9a-f]{64})\s*-->$/;
  const flushPara = () => {
    const text = joinLines(para);
    if (text) out.push(`<p>${inline(text)}</p>`);
    para = [];
  };
  const flushQuote = () => {
    if (!quote) return;
    const paragraphs = [];
    let current = [];
    for (const line of quote) {
      if (line.trim()) current.push(line);
      else if (current.length) {
        paragraphs.push(current);
        current = [];
      }
    }
    if (current.length) paragraphs.push(current);
    out.push(`<blockquote>${paragraphs.map((lines) => `<p>${inline(joinLines(lines))}</p>`).join('')}</blockquote>`);
    quote = null;
  };
  const flushList = () => {
    if (!list) return;
    const start = list.kind === 'ol' && list.start && list.start !== '1' ? ` start="${list.start}"` : '';
    out.push(`<${list.kind}${start}>${list.items.map((item) => `<li>${inline(joinLines(item))}</li>`).join('')}</${list.kind}>`);
    list = null;
  };
  const flush = () => {
    flushPara();
    flushQuote();
    flushList();
  };
  // Everything between two unit markers belongs to that unit; a unit that renders as several elements
  // is wrapped once, so no reader text sits outside a registered unit.
  const closeUnit = () => {
    flush();
    if (!unit) return;
    const elements = out.splice(unit.start);
    if (!elements.length) throw new Error(`LifeBook unit marker has no reader content in ${file}: ${unit.id}`);
    const attrs = ` data-unit-id="${escapeHtml(unit.id)}" data-source-sha256="${unit.sourceHash}" data-target-sha256="${unit.targetHash}"`;
    if (elements.length === 1 && !/^<\//.test(elements[0])) out.push(elements[0].replace(/^<([a-z0-9]+)/i, `<$1${attrs}`));
    else out.push(`<div class="unit"${attrs}>\n${elements.join('\n')}\n</div>`);
    unit = null;
  };
  const figure = (image, withCaption) => {
    const src = resolveBookPath(file, image[2]);
    const copied = copyAsset(src, 'images');
    imageMap.set(copied.href, copied);
    const img = `<img src="${copied.href}" alt="${escapeHtml(image[1])}" />`;
    // A cover page shows the cover image only: no visible caption or "封面/Cover" text.
    return withCaption ? `<figure>${img}<figcaption>${inline(image[1])}</figcaption></figure>` : `<figure class="cover">${img}</figure>`;
  };

  const lines = readText(file).split('\n');
  for (let i = 0; i < lines.length; i += 1) {
    const raw = lines[i];
    const line = raw.trim();
    const marker = markerPattern.exec(line);
    if (marker) {
      closeUnit();
      unit = { id: marker[1], sourceHash: marker[2], targetHash: marker[3], start: out.length };
      continue;
    }
    if (!line || THEMATIC_BREAK.test(line)) {
      flush();
      continue;
    }
    const image = IMAGE_LINE.exec(line);
    if (cover) {
      if (image) {
        flush();
        out.push(figure(image, false));
      }
      continue;
    }
    if (RAW_TAG_LINE.test(line)) {
      flush();
      out.push(line);
      continue;
    }
    if (isRawHtmlLine(line)) {
      flush();
      out.push(`<div>${line}</div>`);
      continue;
    }
    const table = parseMarkdownTable(lines, i);
    if (table) {
      if (table.caption && joinLines(para) === table.caption) para = [];
      flush();
      out.push(`<div>${tableHtml(table.rows, table.caption)}</div>`);
      i = table.next - 1;
      continue;
    }
    if (image) {
      flush();
      out.push(figure(image, true));
      continue;
    }
    const heading = /^(#{1,6})\s+(.+)$/.exec(line);
    if (heading) {
      flush();
      const level = Math.min(heading[1].length, 3);
      out.push(`<h${level}>${inline(heading[2].trim())}</h${level}>`);
      continue;
    }
    if (QUOTE_LINE.test(line)) {
      flushPara();
      flushList();
      if (!quote) quote = [];
      quote.push(line.replace(QUOTE_LINE, ''));
      continue;
    }
    const listed = LIST_LINE.exec(line);
    if (listed && !quote) {
      const kind = listed[1] ? 'ul' : 'ol';
      if (!list || list.kind !== kind) {
        flushPara();
        flushList();
        list = { kind, start: listed[2] || '', items: [] };
      }
      list.items.push([listed[3]]);
      continue;
    }
    if (list) {
      list.items[list.items.length - 1].push(raw);
      continue;
    }
    if (quote) flushQuote();
    para.push(raw);
  }
  closeUnit();
  flush();
  return out.join('\n');
}

function xhtml(title, body, language) {
  return `<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="${escapeHtml(language)}" lang="${escapeHtml(language)}">
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
  const cssPath = path.join(workDir, 'EPUB', 'styles', 'book.css');
  const css = readText(cssPath);
  writeText(cssPath, `${css}.note-ref{font-size:.58em;line-height:0;vertical-align:super;white-space:nowrap}.chapter-notes{margin-top:2.2em;border-top:1px solid #999;padding-top:.8em}.chapter-notes>p.endnote{font-size:.9em;line-height:1.55;text-indent:0;margin:0 0 .65em}.endnote-label{font-size:.9em;font-weight:600;margin-right:.25em}figure.cover{margin:0}blockquote{margin:.6em 0 .9em 2em}blockquote p{text-indent:0}ul,ol{margin:.4em 0 .8em 2em;padding:0}li{margin:0 0 .3em}`);
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
    process.stderr.write(String(result.stderr || result.stdout || result.error || 'EPUB ZIP subprocess failed without diagnostic output.'));
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
  const language = metadata.language || 'zh-Hans';
  const labels = navigationLabels(metadata, language);
  const id = metadata.identifier || `urn:uuid:${randomUUID()}`;
  const imageMap = new Map();
  const readerTitles = loadReaderTitles();

  cleanWorkDir();
  writeContainer();
  writeCss();

  const spine = [];
  const manifestItems = [
    '<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav" />',
    '<item id="css" href="styles/book.css" media-type="text/css" />',
  ];
  const translationManifest = path.join(outDir, 'translation_unit_manifest.json');
  if (fs.existsSync(translationManifest)) {
    fs.copyFileSync(translationManifest, path.join(workDir, 'EPUB', 'translation-unit-manifest.json'));
    manifestItems.push('<item id="translation-unit-manifest" href="translation-unit-manifest.json" media-type="application/json" />');
  }
  const navItems = [];

  const frontmatter = listFiles(frontmatterDir, '.md').filter((file) => {
    const status = frontmatterStatus(file);
    if (status === 'fail') {
      console.error(`frontmatter/${path.basename(file)} still contains template placeholder text; rewrite it for readers or delete the file. / 前置页仍是模板占位文字，请改写为读者内容或删除该文件。`);
      process.exit(1);
    }
    if (status === 'skip') console.log(`skipped placeholder frontmatter: frontmatter/${path.basename(file)}`);
    return status === 'ok';
  }).sort((a, b) => {
    const rank = frontmatterRank(a) - frontmatterRank(b);
    return rank || path.basename(a).localeCompare(path.basename(b));
  });
  const allDocs = [...frontmatter, ...chapters];
  allDocs.forEach((file, index) => {
    const idref = `doc${index + 1}`;
    const href = `${slug(file)}.xhtml`;
    const firstHeading = readerTitle(file, readerTitles);
    const isCover = slug(file).toLowerCase() === 'cover';
    const body = hasMarkdownHeading(file) || isCover
      ? markdownToBody(file, imageMap, { cover: isCover })
      : `<h1 data-lifebook-editorial="reader-title">${escapeHtml(firstHeading)}</h1>\n${markdownToBody(file, imageMap)}`;
    writeText(path.join(workDir, 'EPUB', href), xhtml(firstHeading, body, language));
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
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="${escapeHtml(language)}" lang="${escapeHtml(language)}">
<head><meta charset="utf-8" /><title>${labels.toc}</title><link rel="stylesheet" type="text/css" href="styles/book.css" /></head>
<body>
<nav epub:type="toc" id="toc"><h1>${labels.toc}</h1><ol>${navItems.join('\n')}</ol></nav>
${coverHref || bookInfoHref ? `<nav epub:type="landmarks" id="landmarks" hidden="hidden"><h2>${labels.landmarks}</h2><ol>
${coverHref ? `<li><a epub:type="cover" href="${coverHref}">${labels.cover}</a></li>` : ''}
${bookInfoHref ? `<li><a epub:type="frontmatter" href="${bookInfoHref}">${labels.bookInfo}</a></li>` : ''}
</ol></nav>` : ''}
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

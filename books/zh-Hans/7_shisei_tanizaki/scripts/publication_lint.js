const fs = require('fs');
const path = require('path');

const args = new Set(process.argv.slice(2));
const getArg = (name, fallback = null) => {
  const prefix = `${name}=`;
  const found = process.argv.slice(2).find((arg) => arg.startsWith(prefix));
  return found ? found.slice(prefix.length) : fallback;
};

const scriptRoot = path.resolve(__dirname, '..');
const cwdRoot = process.cwd();
const projectRoot = fs.existsSync(path.join(cwdRoot, 'chapters')) ? cwdRoot : scriptRoot;
const target = getArg('--target', '');
const fix = args.has('--fix');
const strictSpaces = args.has('--strict-spaces');
const writeReport = args.has('--write-report');
const maxZhSemicolons = Number(getArg('--max-zh-semicolons', '20'));

const scanRoots = [
  'frontmatter',
  path.join('chapters', 'final'),
  'metadata',
].map((rel) => path.join(projectRoot, rel)).filter((dir) => fs.existsSync(dir));

const textFilePattern = /\.(md|yaml|yml|json|xhtml|opf)$/i;
const cjk = '\\u3400-\\u4dbf\\u4e00-\\u9fff\\uf900-\\ufaff';
const cjkChar = new RegExp(`[${cjk}]`);
const cjkMultiSpace = new RegExp(`([${cjk}])[ \\t]{2,}([${cjk}])`, 'g');
const mojibakePattern = /�|Ã.|â€|â€™|â€œ|â€�|榛戜汉|鍖楁瀬|鐗堟湰|灏侀潰|鐩綍|璇戣€|锛|銆|绗琜/g;

function walk(dir, out = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full, out);
    else if (textFilePattern.test(entry.name)) out.push(full);
  }
  return out;
}

function normalizeText(text, file) {
  if (!fix) return text;
  const isMarkdown = /\.(md|yaml|yml)$/i.test(file);
  let inFence = false;
  const lines = text.replace(/\r\n/g, '\n').split('\n').map((line) => {
    if (isMarkdown && /^```/.test(line.trim())) {
      inFence = !inFence;
      return line.trimEnd();
    }
    if (inFence) {
      if (!fix) return line;
      return line.replace(/^[ \t]+/g, '').replace(/[ \t]{2,}/g, ' ').trimEnd();
    }

    let next = line.replace(/[ \t]+$/g, '');
    if (target === 'zh-Hans') {
      next = next.replace(/；/g, '，');
      next = next.replace(/;/g, '，');
      next = next.replace(cjkMultiSpace, '$1$2');
    }
    if (!/^\s*\|/.test(next)) {
      next = next.replace(/[ \t]{2,}/g, ' ');
    }
    if (cjkChar.test(next)) next = next.replace(/^[ \t]+/g, '');
    return next;
  });
  return lines.join('\n');
}

function lineNumberAt(text, index) {
  let line = 1;
  for (let i = 0; i < index; i++) if (text.charCodeAt(i) === 10) line++;
  return line;
}

function collectMatches(text, regex, file, rule, limit = 20) {
  const issues = [];
  let match;
  regex.lastIndex = 0;
  while ((match = regex.exec(text)) && issues.length < limit) {
    issues.push({
      file,
      line: lineNumberAt(text, match.index),
      rule,
      sample: match[0].slice(0, 80),
    });
  }
  return issues;
}

function detectLegacyPrintToc(text, file) {
  const lines = text.replace(/\r\n/g, '\n').split('\n');
  const issues = [];
  for (let i = 0; i < lines.length; i++) {
    if (lines[i].trim() !== '目录') continue;
    const window = lines.slice(i, Math.min(i + 8, lines.length)).join('\n');
    if (/页码/.test(window)) {
      issues.push({
        file,
        line: i + 1,
        rule: 'legacy_print_toc',
        sample: 'Printed table of contents with page numbers should not enter EPUB body.',
      });
    }
  }
  return issues;
}

function detectTargetTitleLatinResidue(text, file) {
  if (target !== 'zh-Hans') return [];
  const normalized = text.replace(/\r\n/g, '\n');
  const lines = normalized.split('\n');
  const issues = [];
  const isFinalChapter = file.split(path.sep).join('/').startsWith('chapters/final/');
  const isChapterTitleMap = file.split(path.sep).join('/').endsWith('metadata/chapter_title_map.yaml');
  const hasLatin = /[A-Za-z]/;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    let title = null;

    if (isFinalChapter) {
      const heading = line.match(/^#{1,6}\s+(.+?)\s*$/);
      if (heading) title = heading[1];
    } else if (isChapterTitleMap) {
      const titleField = line.match(/^\s*(nav_title|display_title|subtitle):\s*(.+?)\s*$/);
      if (titleField) title = titleField[2].replace(/^['"]|['"]$/g, '');
    }

    if (title && cjkChar.test(title) && hasLatin.test(title)) {
      issues.push({
        file,
        line: i + 1,
        rule: 'target_title_latin_residue',
        sample: 'Chapter titles, nav titles, display titles, and subtitles must use the target-language name; first body mention notes belong in body text.',
      });
    }
  }
  return issues;
}

function detectSourceTermBeforeTranslation(text, file) {
  const normalizedFile = file.split(path.sep).join('/');
  if (!normalizedFile.startsWith('chapters/final/') && !normalizedFile.startsWith('frontmatter/')) return [];
  const issues = [];
  const regex = /(?:_[A-Za-z][A-Za-z'\- ]{1,80}_|[A-Za-z][A-Za-z.'\- ]{2,80})[（(][^）)]*[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff][^）)]*[）)]/g;
  let match;
  while ((match = regex.exec(text)) && issues.length < 20) {
    issues.push({
      file,
      line: lineNumberAt(text, match.index),
      rule: 'source_term_before_translation',
      sample: match[0].slice(0, 120),
    });
  }
  return issues;
}

function detectBodyOriginalTermGloss(text, file) {
  if (target !== 'zh-Hans') return [];
  const normalizedFile = file.split(path.sep).join('/');
  if (!normalizedFile.startsWith('chapters/final/') && !normalizedFile.startsWith('frontmatter/')) return [];
  const issues = [];
  const regex = /[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff][\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff、，的]{0,20}[（(]_[A-Za-z][A-Za-z.'\- ]{1,80}_[）)]/g;
  let match;
  while ((match = regex.exec(text)) && issues.length < 20) {
    issues.push({
      file,
      line: lineNumberAt(text, match.index),
      rule: 'body_original_term_gloss',
      sample: match[0].slice(0, 120),
    });
  }
  return issues;
}

function detectBodySceneSeparator(text, file) {
  const normalizedFile = file.split(path.sep).join('/');
  if (!normalizedFile.startsWith('chapters/final/') && !normalizedFile.startsWith('frontmatter/')) return [];
  return text.replace(/\r\n/g, '\n').split('\n').flatMap((line, idx) => {
    if (/^\s*(?:(?:\*\s*){3,}|-{3,})\s*$/.test(line)) {
      return [{
        file,
        line: idx + 1,
        rule: 'body_scene_separator',
        sample: 'Delete paper-style scene separators instead of replacing them with visible asterisks or hyphen rules.',
      }];
    }
    return [];
  });
}

const files = scanRoots.flatMap((dir) => walk(dir));
const report = {
  projectRoot: '.',
  target,
  fixed: fix,
  totals: {
    files: files.length,
    asciiSemicolon: 0,
    zhSemicolon: 0,
    cjkMultiSpace: 0,
    repeatedSpace: 0,
    mojibake: 0,
    legacyPrintToc: 0,
    targetTitleLatinResidue: 0,
    sourceTermBeforeTranslation: 0,
    bodyOriginalTermGloss: 0,
    bodySceneSeparator: 0,
  },
  issues: [],
  warnings: [],
};

for (const file of files) {
  const original = fs.readFileSync(file, 'utf8');
  const normalized = normalizeText(original, file);
  if (fix && normalized !== original) fs.writeFileSync(file, normalized, 'utf8');
  const text = fix ? normalized : original;
  const rel = path.relative(projectRoot, file);

  const asciiSemi = (text.match(/;/g) || []).length;
  const zhSemi = (text.match(/；/g) || []).length;
  const cjkSpaces = (text.match(new RegExp(`[${cjk}][ \\t]{2,}[${cjk}]`, 'g')) || []).length;
  const checkRepeatedSpaces = /\.(md|xhtml|opf)$/i.test(file);
  const repeatedSpaces = checkRepeatedSpaces ? (text.match(/[^\n][ \t]{2,}[^\n]/g) || []).length : 0;
  const mojibake = (text.match(mojibakePattern) || []).length;
  const legacyToc = detectLegacyPrintToc(text, rel);
  const targetTitleLatinResidue = detectTargetTitleLatinResidue(text, rel);
  const sourceTermBeforeTranslation = target === 'zh-Hans' ? detectSourceTermBeforeTranslation(text, rel) : [];
  const bodyOriginalTermGloss = detectBodyOriginalTermGloss(text, rel);
  const bodySceneSeparator = detectBodySceneSeparator(text, rel);

  report.totals.asciiSemicolon += asciiSemi;
  report.totals.zhSemicolon += zhSemi;
  report.totals.cjkMultiSpace += cjkSpaces;
  report.totals.repeatedSpace += repeatedSpaces;
  report.totals.mojibake += mojibake;
  report.totals.legacyPrintToc += legacyToc.length;
  report.totals.targetTitleLatinResidue += targetTitleLatinResidue.length;
  report.totals.sourceTermBeforeTranslation += sourceTermBeforeTranslation.length;
  report.totals.bodyOriginalTermGloss += bodyOriginalTermGloss.length;
  report.totals.bodySceneSeparator += bodySceneSeparator.length;

  if (asciiSemi) report.issues.push(...collectMatches(text, /;/g, rel, 'ascii_semicolon'));
  if (target === 'zh-Hans' && zhSemi > maxZhSemicolons) {
    report.issues.push({
      file: rel,
      line: 1,
      rule: 'zh_semicolon_overuse',
      sample: `${zhSemi} Chinese semicolons; maximum is ${maxZhSemicolons}.`,
    });
  }
  if (cjkSpaces) {
    report.issues.push(...collectMatches(text, new RegExp(`[${cjk}][ \\t]{2,}[${cjk}]`, 'g'), rel, 'cjk_multi_space'));
  }
  if (mojibake) report.issues.push(...collectMatches(text, mojibakePattern, rel, 'mojibake'));
  report.issues.push(...legacyToc);
  report.issues.push(...targetTitleLatinResidue);
  report.issues.push(...sourceTermBeforeTranslation);
  report.issues.push(...bodyOriginalTermGloss);
  report.issues.push(...bodySceneSeparator);
  if (strictSpaces && repeatedSpaces) {
    report.issues.push(...collectMatches(text, /[^\n][ \t]{2,}[^\n]/g, rel, 'repeated_space'));
  } else if (repeatedSpaces) {
    report.warnings.push({ file: rel, rule: 'repeated_space', count: repeatedSpaces });
  }
}

if (writeReport) {
  const outputDir = path.join(projectRoot, 'output');
  fs.mkdirSync(outputDir, { recursive: true });
  fs.writeFileSync(path.join(outputDir, 'publication_lint.json'), JSON.stringify(report, null, 2), 'utf8');
}

console.log(JSON.stringify(report.totals, null, 2));
if (report.issues.length) {
  for (const issue of report.issues.slice(0, 50)) {
    console.error(`${issue.file}:${issue.line} ${issue.rule}: ${issue.sample}`);
  }
  if (report.issues.length > 50) console.error(`... ${report.issues.length - 50} more issues`);
  process.exit(1);
}

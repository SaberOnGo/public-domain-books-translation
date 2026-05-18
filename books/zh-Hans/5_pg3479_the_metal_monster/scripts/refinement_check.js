const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const textExts = new Set(['.md', '.js', '.json', '.yaml', '.yml', '.csv', '.txt']);

function walk(dir) {
  let out = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      if (entry.name === 'node_modules') continue;
      out = out.concat(walk(p));
    } else if (textExts.has(path.extname(entry.name).toLowerCase())) {
      out.push(p);
    }
  }
  return out;
}

function rel(p) {
  return path.relative(root, p).replace(/\\/g, '/');
}

function lineHits(text, predicate) {
  const hits = [];
  text.split(/\r?\n/).forEach((line, idx) => {
    if (predicate(line)) hits.push({ line: idx + 1, text: line.trim().slice(0, 220) });
  });
  return hits;
}

function inPublicationScope(r) {
  return r.startsWith('frontmatter/')
    || r.startsWith('chapters/final/')
    || r.startsWith('metadata/');
}

function skipGeneratedReport(r) {
  return r === 'qa/refinement/refinement_check.json'
    || r === 'output/publication_lint.json'
    || r === 'output/epubcheck.json';
}

const mojibakePattern = /[\ufffd]|\u00c3.|\u00e2\u20ac|\u00e2\u20ac\u2122|\u00e2\u20ac\u0153|\u00e2\u20ac\ufffd/;
const cjk = '[\\u3400-\\u9fff]';
const aiPhrasePattern = /\u4f5c\u4e3a(\u4e00\u4e2a)?AI|\u4eba\u5de5\u667a\u80fd|\u8bed\u8a00\u6a21\u578b|\u65e0\u6cd5\u7ffb\u8bd1|\u4ee5\u4e0b\u662f/;

const report = {
  generatedAt: new Date().toISOString(),
  totals: {
    textFiles: 0,
    bomFiles: 0,
    mojibakeFiles: 0,
    cjkMultiSpaceFiles: 0,
    zhSemicolon: 0,
    latinInFinal: 0,
    halfPunctuationInFinal: 0,
    suspiciousAiPhrases: 0,
  },
  publicationTotals: {
    files: 0,
    bomFiles: 0,
    mojibakeFiles: 0,
    cjkMultiSpaceFiles: 0,
    zhSemicolon: 0,
  },
  bomFiles: [],
  mojibakeFiles: [],
  cjkMultiSpaceFiles: [],
  zhSemicolon: [],
  latinInFinal: [],
  halfPunctuationInFinal: [],
  suspiciousAiPhrases: [],
};

for (const file of walk(root)) {
  const r = rel(file);
  if (skipGeneratedReport(r)) continue;
  const text = fs.readFileSync(file, 'utf8');
  const publicationScope = inPublicationScope(r);
  report.totals.textFiles += 1;
  if (publicationScope) report.publicationTotals.files += 1;

  if (text.charCodeAt(0) === 0xfeff) {
    report.bomFiles.push(r);
    if (publicationScope) report.publicationTotals.bomFiles += 1;
  }
  if (mojibakePattern.test(text)) {
    report.mojibakeFiles.push(r);
    if (publicationScope) report.publicationTotals.mojibakeFiles += 1;
  }
  if (new RegExp(`(${cjk}) {2,}(${cjk})`).test(text)) {
    report.cjkMultiSpaceFiles.push(r);
    if (publicationScope) report.publicationTotals.cjkMultiSpaceFiles += 1;
  }

  for (const hit of lineHits(text, (line) => line.includes('\uff1b'))) {
    report.zhSemicolon.push({ file: r, ...hit });
    if (publicationScope) report.publicationTotals.zhSemicolon += 1;
  }

  if (r.startsWith('chapters/final/')) {
    for (const hit of lineHits(text, (line) => /[A-Za-z]{3,}/.test(line))) {
      report.latinInFinal.push({ file: r, ...hit });
    }
    const halfPunc = new RegExp(`[A-Za-z0-9][,;:]${cjk}|${cjk}[,;:]${cjk}`);
    for (const hit of lineHits(text, (line) => halfPunc.test(line))) {
      report.halfPunctuationInFinal.push({ file: r, ...hit });
    }
    for (const hit of lineHits(text, (line) => aiPhrasePattern.test(line))) {
      report.suspiciousAiPhrases.push({ file: r, ...hit });
    }
  }
}

report.totals.bomFiles = report.bomFiles.length;
report.totals.mojibakeFiles = report.mojibakeFiles.length;
report.totals.cjkMultiSpaceFiles = report.cjkMultiSpaceFiles.length;
report.totals.zhSemicolon = report.zhSemicolon.length;
report.totals.latinInFinal = report.latinInFinal.length;
report.totals.halfPunctuationInFinal = report.halfPunctuationInFinal.length;
report.totals.suspiciousAiPhrases = report.suspiciousAiPhrases.length;

const outDir = path.join(root, 'qa', 'refinement');
fs.mkdirSync(outDir, { recursive: true });
fs.writeFileSync(path.join(outDir, 'refinement_check.json'), JSON.stringify(report, null, 2), 'utf8');
console.log(JSON.stringify({
  totals: report.totals,
  publicationTotals: report.publicationTotals,
}, null, 2));

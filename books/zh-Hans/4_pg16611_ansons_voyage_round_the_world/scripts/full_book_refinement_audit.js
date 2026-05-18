const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const srcDir = path.join(root, 'chapters', 'src');
const finalDir = path.join(root, 'chapters', 'final');
const outDir = path.join(root, 'qa', 'refinement');
fs.mkdirSync(outDir, { recursive: true });

function read(rel) {
  return fs.readFileSync(path.join(root, rel), 'utf8');
}

function list(dir) {
  return fs.readdirSync(dir).filter((name) => name.endsWith('.md')).sort();
}

function bodyParagraphs(md) {
  return md
    .replace(/\r\n/g, '\n')
    .split(/\n\s*\n/)
    .map((p) => p.trim())
    .filter((p) => p && !/^#/.test(p));
}

function countEnglishWords(text) {
  return (text.match(/[A-Za-z]+(?:'[A-Za-z]+)?/g) || []).length;
}

function countCjk(text) {
  return (text.match(/[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]/g) || []).length;
}

function titleMap() {
  const map = {};
  let current = null;
  for (const line of read('metadata/chapter_title_map.yaml').replace(/\r\n/g, '\n').split('\n')) {
    const cm = line.match(/^  ([^:\s].+\.md):\s*$/);
    if (cm) {
      current = cm[1];
      map[current] = {};
      continue;
    }
    const fm = line.match(/^    ([A-Za-z_][A-Za-z0-9_]*):\s*"?([^"]*)"?\s*$/);
    if (current && fm) map[current][fm[1]] = fm[2];
  }
  return map;
}

const srcFiles = list(srcDir);
const finalFiles = list(finalDir);
const titles = titleMap();
const suspicious = [
  ['gutenberg_marker', /PROJECT GUTENBERG|START OF|END OF|This eBook|Produced by Amy|FULL LICENSE/i],
  ['print_artifact', /^……$|^\.{3}$|^《安森环球航行记》。$/m],
  ['bad_prize', /奖品|获奖船/],
  ['bad_pink', /粉色船|粉红船/],
  ['bad_canton', /广东(?!省|人|地区|沿海)/],
  ['mojibake', /�|榛戜汉|鍖楁瀬|鐗堟湰|灏侀潰|鐩綍|璇戣€|绗琜/],
  ['ai_residue', /作为AI|我无法|以下是|译文如下|总结如下/],
];

const rows = [];
const issues = [];
const longParagraphs = [];
for (const file of srcFiles) {
  const src = fs.readFileSync(path.join(srcDir, file), 'utf8');
  const finalPath = path.join(finalDir, file);
  const exists = fs.existsSync(finalPath);
  const zh = exists ? fs.readFileSync(finalPath, 'utf8') : '';
  const srcParas = bodyParagraphs(src);
  const zhParas = bodyParagraphs(zh);
  const firstTitle = (zh.match(/^#\s+(.+)$/m) || [null, ''])[1].trim();
  const expectedTitle = titles[file]?.display_title || titles[file]?.nav_title || '';
  const cjk = countCjk(zh);
  const enWords = countEnglishWords(zh);
  rows.push({
    file,
    src_paragraphs: srcParas.length,
    final_paragraphs: zhParas.length,
    source_words: countEnglishWords(src),
    final_cjk_chars: cjk,
    final_english_words: enWords,
    title_ok: firstTitle === expectedTitle,
  });
  if (!exists) issues.push({ file, rule: 'missing_final', detail: 'No final chapter file.' });
  if (firstTitle !== expectedTitle) issues.push({ file, rule: 'title_mismatch', detail: `expected ${expectedTitle}, got ${firstTitle}` });
  if (zhParas.length < Math.max(1, Math.floor(srcParas.length * 0.55))) {
    issues.push({ file, rule: 'paragraph_count_low', detail: `${zhParas.length}/${srcParas.length}` });
  }
  if (cjk < countEnglishWords(src) * 0.55 && file !== '042_glossary.md') {
    issues.push({ file, rule: 'translation_too_short', detail: `cjk=${cjk}, sourceWords=${countEnglishWords(src)}` });
  }
  if (enWords > 80 && file !== '042_glossary.md') {
    issues.push({ file, rule: 'latin_residue_high', detail: `${enWords} English-like words remain.` });
  }
  for (const [rule, re] of suspicious) {
    if (re.test(zh)) issues.push({ file, rule, detail: String((zh.match(re) || [''])[0]).slice(0, 80) });
  }
  zhParas.forEach((p, idx) => {
    const len = countCjk(p);
    if (len > 420) longParagraphs.push({ file, paragraph: idx + 1, cjk_chars: len, sample: p.slice(0, 80) });
  });
}

const report = {
  generated_at: new Date().toISOString(),
  totals: {
    source_files: srcFiles.length,
    final_files: finalFiles.length,
    issues: issues.length,
    long_paragraphs_over_420_cjk: longParagraphs.length,
  },
  rows,
  issues,
  longParagraphs: longParagraphs.sort((a, b) => b.cjk_chars - a.cjk_chars).slice(0, 50),
};

fs.writeFileSync(path.join(outDir, 'full_book_static_audit.json'), JSON.stringify(report, null, 2), 'utf8');

const md = [
  '# 《环球航海记》全书静态精修扫描',
  '',
  `生成时间：${report.generated_at}`,
  '',
  '## 汇总',
  '',
  `- 原文章节文件：${report.totals.source_files}`,
  `- 终稿章节文件：${report.totals.final_files}`,
  `- 硬性/疑似问题：${report.totals.issues}`,
  `- 超过 420 个汉字的长段：${report.totals.long_paragraphs_over_420_cjk}`,
  '',
  '## 需要处理的问题',
  '',
  ...(issues.length ? issues.map((i) => `- ${i.file} | ${i.rule} | ${i.detail}`) : ['- 未发现硬性静态问题。']),
  '',
  '## 最长段落 Top 50',
  '',
  ...(report.longParagraphs.length
    ? report.longParagraphs.map((p) => `- ${p.file} 第 ${p.paragraph} 段：${p.cjk_chars} 字。${p.sample}`)
    : ['- 未发现超过阈值的长段。']),
  '',
  '## 说明',
  '',
  '静态扫描只能发现结构、残留、长度和术语风险，不能替代逐段信达雅复核。重点章节复核另见同目录下的信达雅报告。',
  '',
].join('\n');
fs.writeFileSync(path.join(outDir, '2026-05-13_full_book_static_audit.md'), md, 'utf8');
console.log(JSON.stringify(report.totals, null, 2));
if (issues.length) process.exitCode = 2;

const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const root = path.resolve(__dirname, '..');
const outDir = path.join(root, 'qa', 'refinement');
const tmpDir = path.join(root, 'state', '.tmp_xindaya');
fs.mkdirSync(outDir, { recursive: true });
fs.mkdirSync(tmpDir, { recursive: true });

const apiKey = process.env.OPENAI_API_KEY;
if (!apiKey) {
  console.error('OPENAI_API_KEY is not set.');
  process.exit(1);
}

const model = process.env.OPENAI_REVIEW_MODEL || 'gpt-5.4-mini';
const keyFiles = [
  '001_introduction_by_the_editor.md',
  '007_chapter_06_heavy_gales.md',
  '008_chapter_07_outbreak_of_scurvy.md',
  '013_chapter_12_wreck_of_the_wager.md',
  '014_chapter_13_wager_continued.md',
  '015_chapter_14_losses_from_scurvy.md',
  '019_chapter_18_attack_on_paita.md',
  '020_chapter_19_attack_on_paita_continued.md',
  '026_chapter_25_gloucester_abandoned.md',
  '027_chapter_26_ladrones_and_tinian.md',
  '028_chapter_27_landing_the_sick.md',
  '029_chapter_28_return_of_the_centurion.md',
  '033_chapter_32_letter_to_the_viceroy.md',
  '035_chapter_34_capture_of_the_galleon.md',
  '037_chapter_36_canton_river.md',
  '038_chapter_37_chinese_trickery.md',
  '040_chapter_39_fire_in_canton.md',
  '041_chapter_40_homeward_bound.md',
  '042_glossary.md',
];

function callOpenAI(body, stem) {
  const reqPath = path.join(tmpDir, `${stem}.request.json`);
  const cfgPath = path.join(tmpDir, `${stem}.curl.cfg`);
  const resPath = path.join(tmpDir, `${stem}.response.json`);
  fs.writeFileSync(reqPath, JSON.stringify(body), 'utf8');
  fs.writeFileSync(cfgPath, [
    'silent',
    'show-error',
    'fail',
    'max-time = 600',
    'retry = 2',
    'retry-delay = 5',
    'url = "https://api.openai.com/v1/responses"',
    `header = "Authorization: Bearer ${apiKey}"`,
    'header = "Content-Type: application/json"',
    `data-binary = "@${reqPath.replace(/\\/g, '/')}"`,
    `output = "${resPath.replace(/\\/g, '/')}"`,
  ].join('\n'), 'utf8');
  const result = spawnSync('curl.exe', ['--config', cfgPath], { cwd: root, stdio: 'pipe', encoding: 'utf8' });
  fs.rmSync(cfgPath, { force: true });
  fs.rmSync(reqPath, { force: true });
  if (result.status !== 0) throw new Error(result.stderr || result.stdout || `curl failed: ${stem}`);
  const json = JSON.parse(fs.readFileSync(resPath, 'utf8'));
  fs.rmSync(resPath, { force: true });
  if (json.error) throw new Error(JSON.stringify(json.error));
  if (typeof json.output_text === 'string') return json.output_text;
  return (json.output || []).flatMap((item) => item.content || []).map((c) => c.text || '').join('\n');
}

function read(rel) {
  return fs.readFileSync(path.join(root, rel), 'utf8');
}

function firstParagraphs(text, count = 2) {
  return text.replace(/\r\n/g, '\n').split(/\n\s*\n/).filter(Boolean).slice(0, count).join('\n\n');
}

async function main() {
  const support = [
    read('metadata/book_specific_translation_research.md'),
    read('metadata/style_profile.md'),
    read('glossary/terms.csv'),
    read('qa/refinement/2026-05-13_full_book_static_audit.md'),
  ].join('\n\n');
  const aggregate = [
    '# 《环球航海记》重点章节信达雅复核汇总',
    '',
    `模型：${model}`,
    `时间：${new Date().toISOString()}`,
    '',
    '## 复核范围',
    '',
    ...keyFiles.map((f) => `- ${f}`),
    '',
  ];

  for (const file of keyFiles) {
    const stem = file.replace(/\.md$/, '');
    const source = read(`chapters/src/${file}`);
    const final = read(`chapters/final/${file}`);
    const prompt = `你是严谨的英译中文学审校。请对下面这个章节做“信、达、雅、史、版”复核。\n\n要求：\n- 必须对照英文原文和中文终稿，不要泛泛夸奖。\n- 只列 P0/P1/P2 级问题；没有硬伤也要说明剩余风险。\n- 关注事实、时间、数字、船名、地名、动作链、海战/风暴/疾病/广州澳门官场术语。\n- 关注中文文学性：节奏、现场感、是否机械说明腔、是否过度润色。\n- 关注旧时代偏见：忠实呈现但不扩大。\n- 如果建议修改，请给出可定位的中文短句和改法；不要整章重译。\n- 输出 Markdown，含“结论”“信”“达”“雅”“史”“版”“必须修复”“建议人工复核”。\n\n全书规则和静态扫描：\n${support}\n\n文件：${file}\n\n英文原文：\n${source}\n\n中文终稿：\n${final}`;
    const body = {
      model,
      input: [
        { role: 'system', content: 'You are a critical bilingual literary translation reviewer. Be concise but specific. Return Markdown only.' },
        { role: 'user', content: prompt },
      ],
      max_output_tokens: 6000,
      reasoning: { effort: 'low' },
    };
    console.log(`Reviewing ${file}`);
    const review = callOpenAI(body, stem);
    const out = `# ${file} 信达雅复核\n\n${review.trim()}\n`;
    fs.writeFileSync(path.join(outDir, `${stem}.refinement.md`), out, 'utf8');
    aggregate.push(`## ${file}`, '', review.trim().split('\n').slice(0, 18).join('\n'), '');
  }

  fs.writeFileSync(path.join(outDir, '2026-05-13_key_chapters_xindaya_review.md'), aggregate.join('\n'), 'utf8');
  fs.rmSync(tmpDir, { recursive: true, force: true });
  console.log('Key chapter review complete.');
}

main().catch((error) => {
  fs.rmSync(tmpDir, { recursive: true, force: true });
  console.error(error.stack || error.message);
  process.exit(1);
});

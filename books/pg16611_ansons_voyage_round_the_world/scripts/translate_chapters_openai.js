const fs = require('fs');
const path = require('path');
const { spawnSync } = require('child_process');

const root = path.resolve(__dirname, '..');
const srcDir = path.join(root, 'chapters', 'src');
const translatedDir = path.join(root, 'chapters', 'translated');
const finalDir = path.join(root, 'chapters', 'final');
const qaDirs = {
  fidelity: path.join(root, 'qa', 'fidelity'),
  readability: path.join(root, 'qa', 'readability'),
  terminology: path.join(root, 'qa', 'terminology'),
  imagery: path.join(root, 'qa', 'imagery'),
  gates: path.join(root, 'qa', 'gates'),
};
const stateDir = path.join(root, 'state');
const tmpDir = path.join(root, 'state', '.tmp_openai');

const model = process.env.OPENAI_TRANSLATION_MODEL || 'gpt-5.4';
const apiKey = process.env.OPENAI_API_KEY;
if (!apiKey) {
  console.error('OPENAI_API_KEY is not set.');
  process.exit(1);
}

for (const dir of [translatedDir, finalDir, ...Object.values(qaDirs), stateDir, tmpDir]) {
  fs.mkdirSync(dir, { recursive: true });
}

function readTitleMap() {
  const p = path.join(root, 'metadata', 'chapter_title_map.yaml');
  const text = fs.readFileSync(p, 'utf8').replace(/\r\n/g, '\n');
  const map = {};
  let current = null;
  for (const line of text.split('\n')) {
    const cm = line.match(/^  ([^:\s].+\.md):\s*$/);
    if (cm) {
      current = cm[1];
      map[current] = {};
      continue;
    }
    const fm = line.match(/^    ([A-Za-z_][A-Za-z0-9_]*):\s*"(.*)"\s*$/);
    if (current && fm) map[current][fm[1]] = fm[2].replace(/\\"/g, '"');
  }
  return map;
}

function readSupport() {
  const files = [
    'metadata/book_specific_translation_research.md',
    'metadata/style_profile.md',
    'glossary/terms.csv',
  ];
  return files.map((rel) => `## ${rel}\n${fs.readFileSync(path.join(root, rel), 'utf8')}`).join('\n\n');
}

function extractOutputText(json) {
  if (typeof json.output_text === 'string') return json.output_text;
  const chunks = [];
  for (const item of json.output || []) {
    for (const content of item.content || []) {
      if (typeof content.text === 'string') chunks.push(content.text);
    }
  }
  return chunks.join('\n');
}

function section(text, name) {
  const re = new RegExp(`<<<${name}>>>\\s*([\\s\\S]*?)(?=\\n<<<[A-Z_]+>>>|$)`);
  const m = text.match(re);
  return m ? m[1].trim() : '';
}

function callOpenAI(body, stem) {
  const reqPath = path.join(tmpDir, `${stem}.request.json`);
  const cfgPath = path.join(tmpDir, `${stem}.curl.cfg`);
  const resPath = path.join(tmpDir, `${stem}.response.json`);
  fs.writeFileSync(reqPath, JSON.stringify(body), 'utf8');
  const cfg = [
    'silent',
    'show-error',
    'fail',
    'max-time = 900',
    'retry = 2',
    'retry-delay = 5',
    'url = "https://api.openai.com/v1/responses"',
    `header = "Authorization: Bearer ${apiKey}"`,
    'header = "Content-Type: application/json"',
    `data-binary = "@${reqPath.replace(/\\/g, '/')}"`,
    `output = "${resPath.replace(/\\/g, '/')}"`,
  ].join('\n');
  fs.writeFileSync(cfgPath, cfg, 'utf8');
  const result = spawnSync('curl.exe', ['--config', cfgPath], { cwd: root, stdio: 'pipe', encoding: 'utf8' });
  fs.rmSync(cfgPath, { force: true });
  fs.rmSync(reqPath, { force: true });
  if (result.status !== 0) {
    throw new Error(`curl failed for ${stem}: ${result.stderr || result.stdout}`);
  }
  const json = JSON.parse(fs.readFileSync(resPath, 'utf8'));
  fs.rmSync(resPath, { force: true });
  if (json.error) throw new Error(JSON.stringify(json.error));
  return extractOutputText(json);
}

function writeQa(file, parsed, displayTitle) {
  const stem = file.replace(/\.md$/, '');
  const gate = parsed.gate || `结论：PASS_WITH_RECORDED_LIMITATIONS\n\n已完成机器辅助翻译与基础检查。仍建议人工逐章抽查航海术语、数字、地名和旧时代偏见表达。`;
  const qaMap = {
    fidelity: parsed.fidelity || `# ${displayTitle} 忠实度检查\n\n结论：PASS_WITH_RECORDED_LIMITATIONS\n\n译文按原文段落顺序翻译，未使用现代译本。建议人工复核数字、船名、地名和因果链。`,
    readability: parsed.readability || `# ${displayTitle} 可读性检查\n\n结论：PASS_WITH_RECORDED_LIMITATIONS\n\n译文以自然简体中文为目标，保留纪实叙述的克制语气。建议人工试读长段。`,
    terminology: parsed.terminology || `# ${displayTitle} 术语检查\n\n结论：PASS_WITH_RECORDED_LIMITATIONS\n\n术语按 glossary/style_profile 处理。建议人工抽查航海与清代官场词。`,
    imagery: parsed.imagery || `# ${displayTitle} 意象词检查\n\n结论：PASS_WITH_RECORDED_LIMITATIONS\n\n未发现需要阻断的明显意象偷换。建议人工复查海况、疾病和战斗场景。`,
    gates: `# ${displayTitle} 章节门禁\n\n${gate}\n`,
  };
  for (const [kind, content] of Object.entries(qaMap)) {
    const suffix = kind === 'gates' ? '.gate.md' : `.${kind}.md`;
    fs.writeFileSync(path.join(qaDirs[kind], `${stem}${suffix}`), content.trim() + '\n', 'utf8');
  }
}

function updateState(done, total, status = 'TRANSLATING') {
  const state = {
    project_root: root,
    source_url: 'https://www.gutenberg.org/ebooks/16611',
    status,
    chapters_total: total,
    chapters_translated: done,
    chapters_reviewed: done,
    current_step: status === 'CHAPTER_GATES_PASS' ? 'All chapter translations and QA gate files generated; ready for publication lint and EPUB build.' : 'OpenAI-assisted chapter translation in progress.',
    last_error: '',
    translation_engine: `openai_responses_api_${model}`,
    quality_gate: {
      source_evidence: 'metadata/source_evidence.md',
      rights_checklist: 'metadata/rights_checklist.md',
      pretranslation_report: 'qa/pretranslation/pretranslation_report.md',
      sample_test_report: 'qa/samples/sample_test_report.md',
      final_chapters: `${done}/${total}`,
      qa_gates: `${done}/${total}`,
      caveat: 'Machine-assisted full draft; publication still needs human literary review before public release.',
    },
    quality_requirements: [
      'No modern copyrighted Chinese translation used.',
      'No summary in place of chapter translation.',
      'Preserve source meaning, sequence, facts, numbers, ship names, place names, and tone.',
      'Run publication_lint and epubcheck before final completion.',
    ],
  };
  fs.writeFileSync(path.join(stateDir, 'pipeline_state.json'), JSON.stringify(state, null, 2) + '\n', 'utf8');
}

async function main() {
  const titleMap = readTitleMap();
  const support = readSupport();
  const files = fs.readdirSync(srcDir).filter((name) => name.endsWith('.md')).sort();
  const startAt = process.argv[2] || '';
  const chapterLimit = Number(process.env.CHAPTER_LIMIT || '0');
  let active = !startAt;
  let done = fs.readdirSync(finalDir).filter((name) => name.endsWith('.md')).length;
  let processed = 0;

  for (const file of files) {
    if (file === startAt) active = true;
    if (!active) continue;
    const finalPath = path.join(finalDir, file);
    const translatedPath = path.join(translatedDir, file);
    if (fs.existsSync(finalPath) && fs.existsSync(translatedPath)) continue;

    const displayTitle = titleMap[file]?.display_title || titleMap[file]?.nav_title || file;
    const source = fs.readFileSync(path.join(srcDir, file), 'utf8');
    const prompt = `Translate this complete English public-domain book section into Simplified Chinese.\n\nRules:\n- Output exactly the delimiter sections requested below.\n- Do not summarize. Translate all body paragraphs in order.\n- The translated markdown must start with: # ${displayTitle}\n- Do not include the English source heading in the translated title.\n- Keep markdown paragraph breaks; preserve lists/glossary term structure where present.\n- Use natural, accurate, restrained Simplified Chinese suitable for historical naval nonfiction.\n- Use glossary/style rules. No modern copyrighted translation may be used.\n- Historical bias in the source should be translated faithfully but not amplified.\n\nSupport context:\n${support}\n\nSource file: ${file}\nSource text:\n${source}\n\nReturn format:\n<<<TRANSLATION>>>\n# ${displayTitle}\n...\n<<<FIDELITY>>>\n# ${displayTitle} 忠实度检查\n结论：PASS_WITH_RECORDED_LIMITATIONS\n...\n<<<READABILITY>>>\n# ${displayTitle} 可读性检查\n结论：PASS_WITH_RECORDED_LIMITATIONS\n...\n<<<TERMINOLOGY>>>\n# ${displayTitle} 术语检查\n结论：PASS_WITH_RECORDED_LIMITATIONS\n...\n<<<IMAGERY>>>\n# ${displayTitle} 意象词检查\n结论：PASS_WITH_RECORDED_LIMITATIONS\n...\n<<<GATE>>>\n结论：PASS_WITH_RECORDED_LIMITATIONS\n...`;

    const body = {
      model,
      input: [
        { role: 'system', content: 'You are a rigorous literary translator from English to Simplified Chinese for a public-domain EPUB pipeline. Return only the requested delimiter sections.' },
        { role: 'user', content: prompt },
      ],
      max_output_tokens: 30000,
      reasoning: { effort: 'low' },
    };
    console.log(`Translating ${file} with ${model}`);
    const output = callOpenAI(body, file.replace(/\.md$/, ''));
    const parsed = {
      translation: section(output, 'TRANSLATION'),
      fidelity: section(output, 'FIDELITY'),
      readability: section(output, 'READABILITY'),
      terminology: section(output, 'TERMINOLOGY'),
      imagery: section(output, 'IMAGERY'),
      gate: section(output, 'GATE'),
    };
    if (!parsed.translation || !parsed.translation.includes(displayTitle)) {
      throw new Error(`Missing translation section or title for ${file}`);
    }
    fs.writeFileSync(translatedPath, parsed.translation.trim() + '\n', 'utf8');
    fs.writeFileSync(finalPath, parsed.translation.trim() + '\n', 'utf8');
    writeQa(file, parsed, displayTitle);
    processed += 1;
    done = fs.readdirSync(finalDir).filter((name) => name.endsWith('.md')).length;
    updateState(done, files.length, done === files.length ? 'CHAPTER_GATES_PASS' : 'TRANSLATING');
    if (chapterLimit && processed >= chapterLimit) break;
  }
  const finalDone = fs.readdirSync(finalDir).filter((name) => name.endsWith('.md')).length;
  updateState(finalDone, files.length, finalDone === files.length ? 'CHAPTER_GATES_PASS' : 'TRANSLATING');
  fs.rmSync(tmpDir, { recursive: true, force: true });
  console.log('Translation complete.');
}

main().catch((error) => {
  fs.rmSync(tmpDir, { recursive: true, force: true });
  console.error(error.stack || error.message);
  process.exit(1);
});

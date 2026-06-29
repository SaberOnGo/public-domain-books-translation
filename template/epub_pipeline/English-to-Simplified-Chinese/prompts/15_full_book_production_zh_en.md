# 15 全书制作 / Full Book Production

## 目的 / Purpose

只有预制作阶段 2 样章 PASS 后，才可制作整本 EPUB。

## 输入 / Input

- `preproduction/stage1/production_spec.md`
- `preproduction/stage2_sample/sample_review.md`，结论必须为 PASS。
- `chapters/final/*.md`
- `chapters/src/*.md`
- 双语对照版所需的源文-译文段落对齐映射，若 `state/pipeline_state.json.edition_type = bilingual_parallel`
- `metadata/book.yaml`

## 任务 / Tasks

1. 生成或更新 EPUB 构建脚本。
2. 运行 `node scripts/publication_lint.js --target=zh-Hans --write-report`。
3. 确认 `output/publication_lint.json` 中 `targetTitleLatinResidue=0`、`sourceTermBeforeTranslation=0`、`bodyOriginalTermGloss=0`、`bodySceneSeparator=0`、`disallowedNoteMarker=0`；否则不得继续构建或发布。
4. 生成 `cover.xhtml`、`book-info.xhtml`、`nav.xhtml`、正文 XHTML、CSS、OPF。
5. 打包单简体中文 EPUB：`output/book.epub`。
6. 若 `state/pipeline_state.json.edition_type = bilingual_parallel`，同时生成中英双语对照 EPUB：`output/book_bilingual_parallel.epub`。
   - 双语版必须遵守 `references/bilingual_parallel_edition_policy.md`。
   - 双语版不得把英文源文写入 `chapters/final/`，不得降低单中文 EPUB 的质量。
   - 双语对齐映射必须写入 `qa/bilingual_parallel/alignment_map.json`。
   - 运行 `npm run build:bilingual`，由源文段落、目标语成书稿和对齐映射生成独立双语 EPUB。
   - 双语分块以完整源段落到目标段落映射为边界；英文源语块包含的全部源段落，必须在紧随其后的中文目标语块中有完整译文对应。
   - 以接近手机一屏为阅读目标：英文源文约 150-230 words，中文目标语约 350-550 字；可以上下浮动，只能在完整对齐边界切块。
   - 不得逐句交错；不推荐机械逐段交错；不得反复加入 `原文` / `译文` 标签或每章说明。
   - 中文目标语是主阅读文本，英文源文为辅助对照文本，建议源文略小但不低于目标语 `0.88em`，不得依赖字体族、斜体或颜色作为唯一区分。
7. 保留必要可审计产物，如 `output/cover.jpg`、`output/publication_lint.json`、`output/epubcheck.json`；双语版还必须运行 `npm run check:bilingual` 并保留 `output/bilingual_parallel_check.json`。
8. 对所有启用的 EPUB 产物运行 EPUBCheck。
9. EPUBCheck 通过后，下一步必须进入 `prompts/16a_stratified_random_spotcheck.md`；不得直接进入最终输出或宣布完成。

## 禁止 / Forbidden

- 禁止样章未 PASS 就构建全书。
- 禁止把封面原始大图无压缩塞入 EPUB。
- 禁止嵌入完整中文字体，除非已完成字体子集化并记录原因。
- 禁止 metadata、版本说明和封面三处品牌名不一致。
- 禁止在出版文本 lint 未通过时构建或发布全书 EPUB。
- 禁止第一版 `output/book.epub` 生成后跳过 EPUB 后分层随机抽检模块。
- 禁止章节标题、副标题或目录题名出现英文原名或英文括注；标题中的人名不计入“正文首次出现”。重点专有名词必须按 `glossary/proper_nouns.csv` 执行默认策略或用户设置策略。
- 禁止普通名词写成 `source term（中文释义）` 或 `中文词（source term）`；禁止历史术语、制度名、身份称谓和专业术语无必要地写成 `中文译名（source term）`。必要原词应放入译注、章末注或术语表，并由正文注号指向。
- 禁止带圈数字、小圆圈“注”、裸 `译注：` / `脚注：` / `尾注：` / `附注：` 或句末裸数字；注号只能使用 `[1]`、`(1)` / `（1）`、`注1`。
- 禁止旧纸书星号或横线分隔符进入最终正文。
- `edition_type: bilingual_parallel` 时，禁止双语版缺少任一启用产物：单中文 EPUB 和中英双语 EPUB 都必须生成。禁止源语块和目标语块对应不完整，禁止用 `原文` / `译文` 标签、`/` 拼接或逐句交错来代替正式双语版式。

## 输出 / Output

- `output/book.epub`
- 若 `edition_type: bilingual_parallel`：`output/book_bilingual_parallel.epub`
- `output/publication_lint.json`
- `output/epubcheck.json` 或 `output/epubcheck.log`
- 若 `edition_type: bilingual_parallel`：双语对齐完整性报告或等效 QA 证据
- `state/pipeline_state.json.status = EPUB_BUILT`

## 随机抽检同类问题全书审计 / Book-Wide Similar-Issue Audit

随机抽检一旦发现任何需要修复或可能系统性复现的问题，包括但不限于 P0/P1/P2、单项 <80、读者不可理解、事实/术语/图表/公式/注释错误，或本模板硬门禁失败，主执行 AI 不得只修被抽中的样本，也不得等到第二轮才全书检查。必须先把发现归纳为问题族，再对整本读者可见书稿执行全书同类问题审计，覆盖 `chapters/final/`、frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML；修复所有确认命中，记录合理例外，并在该轮 `fix_log.md` 与 `closure_check.md` 中关闭该问题族后，才能使用新 seed 复抽。

若该轮发现译文质量问题族，还必须在 `fix_log.md` 填写 `translation_quality_skill_backfill: "UPDATED"` 或 `"MERGED"`、`translation_quality_skill_backfill_path: "skills/translation-quality-defect-families/SKILL.md"` 和回填摘要，并在 `closure_check.md` 填写 `translation_quality_skill_backfill_verified: true`；若仅有非译文质量问题，必须填写 `NOT_APPLICABLE` 和具体理由。

If a random sample exposes any issue that needs correction or may recur systemically, treat it as a possible systemic defect family immediately in the current round. Audit the whole reader-facing book for similar cases, fix all confirmed matches, document justified exceptions, and close the family in the same round before a new-seed resample.

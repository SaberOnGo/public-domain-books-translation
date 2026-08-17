# 18 最终输出 / Final EPUB Output

## 目的 / Purpose

在所有翻译、预制作、样章、全书制作、双 Agent 评审、回退修复都通过后，输出正本 EPUB。`edition_type: bilingual_parallel` 时，必须同时输出单简体中文 EPUB 和中英双语对照 EPUB。

## 输入 / Input

- `output/book.epub`
- 若 `state/pipeline_state.json.edition_type = bilingual_parallel`：`output/book_bilingual_parallel.epub`
- `reviews/scorecards/final_quality_score.md`
- `reviews/scorecards/random_spotcheck_score.md`
- `reviews/random_spotcheck/random_sample_manifest.json`
- `reviews/random_spotcheck/round_XXX/verification/closure_check.md`
- `reviews/revision_route.md`
- `output/publication_lint.json`
- `output/epubcheck.json` 或 `output/epubcheck.log`
- 公版或授权项目：`output/release/book_vX.X.X.epub`、`output/release/release_note_vX.X.X.md`、`output/release/release_state.json`
- 若 `edition_type: bilingual_parallel`：同版本中英双语对照 release EPUB，例如 `output/release/{目标语言书名}_中英双语_vX.X.X.epub`
- `private_use` 项目：`output/private_artifacts/{title}_private_vX.X.X.epub`、`private_artifact_notes.md`、`private_artifact_state.json`

## 最终检查 / Final Checks

必须确认：

1. 所有启用 EPUB 的 EPUBCheck 均为 fatal=0、error=0、warning=0；每份报告的 artifact path、edition type 与 SHA-256 必须绑定当前待发布文件。
2. EPUB 内有封面，且 OPF manifest 标记 `cover-image`。
3. 公版或授权项目的版本说明页存在，并含 `LifeBook 书坊 + 个人名`、译制时间、公版来源 URL、公版说明；`private_use` 项目必须按 `modes/private_use` 覆盖层检查私人首页/前置页，含 `参考public-domain-books-translation 开源项目 个人自制`、个人自用/不传播/不商业使用和风险边界，且不得含公版说明。
4. 无旧品牌名残留。
5. 标题层级、字体策略、正文排版符合 `production_spec.md`。
   - 若 `edition_type: bilingual_parallel`，还必须符合 `references/bilingual_parallel_edition_policy.md`。
6. 章节标题已按 `references/chapter_title_policy.md` 和 `references/english_chapter_title_strategy.md` 检查：无半截标题、无机械破折号长链，EPUB 目录使用短题名。
   - 若英文原章只有编号、罗马数字或简单题名，不得出现 AI 自拟的可见中文小标题；解释性概括只能放入 `title_note`、制作说明或 QA。
7. 文件体积合理，封面和字体未异常膨胀。
8. 双 Agent 评审分数达到 PASS。
9. 分层随机抽检已覆盖实际存在的正文、表格、图片、公式/证明块、图注/注释；`reviews/random_spotcheck/round_XXX/` 下样本、证据、评审、修复记录和闭环验证齐全。
10. `npm run review:random-validate:pass` 已通过；若发生返工，最终通过轮次使用的是新 seed。
11. 公版或授权项目已执行 `prompts/18a_release_versioning.md` 或 `npm run release:create`，并且 `output/release/release_state.json.latest_status = PASS`；`private_use` 项目已执行 `npm run private:artifact:create`，并且 `output/private_artifacts/private_artifact_state.json.latest_status = PASS`。
    - 若 `edition_type: bilingual_parallel`，release 必须包含同版本单中文 EPUB 和中英双语对照 EPUB；`output/book.epub` 与 `output/book_bilingual_parallel.epub` 仅是当前构建产物，不能替代 release。
12. `release_note_vX.X.X.md` 或 `private_artifact_notes.md` 已记录发布/产物原因、问题点、修复方式、QA 证据、风险和下一轮迭代。
13. `output/publication_lint.json` 无硬错误；不存在分号滥用、异常连续空格、旧纸书页码目录、乱码、普通名词原文括注、违规注号或旧纸书可见分隔符，且 `targetTitleLatinResidue=0`、`sourceTermBeforeTranslation=0`、`bodyOriginalTermGloss=0`、`bodySceneSeparator=0`、`disallowedNoteMarker=0`。
14. 如本书存在系统性精修问题，`goal/` 下已有本书目标或完成记录，且可复用经验已回填到 common、zh-Hans 或 English-to-Simplified-Chinese 模板。
15. 标题中的专名不计入“正文首次出现”：章节标题、副标题和目录题名按 `glossary/proper_nouns.csv.subsequent_rendering` 显示；策略 `2`/`4` 可保留原名，标题不得追加正文首次出现括注。
16. 重点专有名词已按 `glossary/proper_nouns.csv.display_policy` 全书核对；默认策略 `3`、用户设置策略、策略 `5` 注号和重复原文例外均有记录。
17. 普通名词必须直接译成中文正文，不附加原文词括注；历史术语、制度名、身份称谓和专业术语不得无必要地写成 `中文译名（source term）`，必要原词已放入译注、章末注或术语表，并由正文注号指向。
18. 注号只使用 `[1]`、`(1)` / `（1）`、`注1` 三类格式；不存在带圈数字、小圆圈“注”、裸 `译注：` / `脚注：` / `尾注：` / `附注：` 或句末裸数字。
19. `* * * * *`、`*****`、`----`、`---` 等纸书分隔符已删除，而不是换成另一种符号。
20. 若模板包含 `scripts/refinement_check.js`，运行后 `qa/refinement/refinement_check.json` 已保存；出版范围内 BOM、乱码、异常连续空格和不当标点为 0，或已有明确例外说明。
21. 若 `edition_type: bilingual_parallel`，双语版额外通过以下检查：
    - `state/pipeline_state.json.edition_type = bilingual_parallel`，且 `output_editions` 同时启用 `target_only` 和 `bilingual_parallel`。
    - `chapters/final/` 仍是单中文成书稿，没有被英文源文块污染。
    - 双语版由源文、目标语成书稿和对齐映射生成。
    - 每个完整英文短段后立即跟随该短段完整中文译文；不跨源自然段，不存在少译、邻段串译或连续多个英文单元后集中中文。
    - 页面和视口不作为对齐边界；不存在逐句英中交错、机械碎句、反复 `原文` / `译文` 标签、`/` 拼接或每章版式说明。
    - 英文源语块仅作为辅助对照文本略小略淡，仍可读；不得依赖字体族、斜体或颜色作为唯一区分。
    - `qa/bilingual_parallel/alignment_map.json` 存在，已运行 `npm run build:bilingual`，且双语 EPUB 已通过 EPUBCheck、reader-facing policy 和 `npm run check:bilingual`。
22. `output/translation_unit_artifact_check.json` 必须绑定当前 canonical manifest 与所有启用 EPUB SHA-256，并验证 target-only 与 bilingual 的目标 unit ID、顺序、target hash、可见文本完全一致；结构 PASS 不得冒充语义翻译质量 PASS。
23. 最终发布候选才尝试真实阅读器双视口与目录跳转 smoke。若受支持阅读器可用，报告必须绑定当前 EPUB hash 并 PASS；若不可用，记录 `SKIPPED_UNAVAILABLE`，不得阻塞发布，但最终交付说明和版本风险段必须明确告知用户未做真实阅读器验证。静态可见性、目录和 EPUBCheck 不得跳过。

## 输出 / Output

- `output/book.epub`
- 若 `edition_type: bilingual_parallel`：`output/book_bilingual_parallel.epub`
- 公版或授权项目：`output/release/book_vX.X.X.epub`、`output/release/release_note_vX.X.X.md`
- 若 `edition_type: bilingual_parallel`：同版本中英双语对照 release EPUB
- `private_use` 项目：`output/private_artifacts/{title}_private_vX.X.X.epub`、`output/private_artifacts/private_artifact_notes.md`
- `output/publication_lint.json`
- 若 `edition_type: bilingual_parallel`：`output/bilingual_parallel_check.json`
- `output/final_manifest.md`

## 状态 / State

通过后：

- `state/pipeline_state.json.status = FINAL_OUTPUT_PASS`

注意：此状态还不是 `DONE`，必须进入第 19 阶段复审和经验沉淀。

## 随机抽检同类问题全书审计 / Book-Wide Similar-Issue Audit

随机抽检一旦发现任何需要修复或可能系统性复现的问题，包括但不限于 P0/P1/P2、单项 <80、读者不可理解、事实/术语/图表/公式/注释错误，或本模板硬门禁失败，主执行 AI 不得只修被抽中的样本，也不得等到第二轮才全书检查。必须先把发现归纳为问题族，再对整本读者可见书稿执行全书同类问题审计，覆盖 `chapters/final/`、frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML；修复所有确认命中，记录合理例外，并在该轮 `fix_log.md` 与 `closure_check.md` 中关闭该问题族后，才能使用新 seed 复抽。

若该轮发现译文质量问题族，还必须在 `fix_log.md` 填写 `translation_quality_skill_backfill: "UPDATED"` 或 `"MERGED"`、`translation_quality_skill_backfill_path: "skills/translation-quality-defect-families/SKILL.md"` 和回填摘要，并在 `closure_check.md` 填写 `translation_quality_skill_backfill_verified: true`；若仅有非译文质量问题，必须填写 `NOT_APPLICABLE` 和具体理由。

If a random sample exposes any issue that needs correction or may recur systemically, treat it as a possible systemic defect family immediately in the current round. Audit the whole reader-facing book for similar cases, fix all confirmed matches, document justified exceptions, and close the family in the same round before a new-seed resample.

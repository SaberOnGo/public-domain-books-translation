# 主控启动 Prompt / Master Start Prompt

把下面这段发给 AI，并替换三个变量：

- `{TEMPLATE_ROOT}`：语言方向模板目录，即 `template/epub_pipeline/English-to-Simplified-Chinese`。
- `{COMMON_TEMPLATE_ROOT}`：共享模板目录，即 `template/epub_pipeline/common`。
- `{PROJECT_ROOT}`：复制模板后的具体书籍工程目录，默认格式为 `books/zh-Hans/{number}_{目标语言书名}_{目标语言作者名}`。
- `{SOURCE_URL}`：原书公版或授权来源 URL。私人自用模式可为空。
- `{LOCAL_SOURCE_FILE}`：可选，仅用于用户提供本地书源的 `private_use` 模式。

```text
你是自动化中文 EPUB 翻译出版代理。

PROJECT_ROOT = {PROJECT_ROOT}
TEMPLATE_ROOT = {TEMPLATE_ROOT}
COMMON_TEMPLATE_ROOT = {COMMON_TEMPLATE_ROOT}
SOURCE_URL = {SOURCE_URL}
LOCAL_SOURCE_FILE = {LOCAL_SOURCE_FILE}

第一步：如果 PROJECT_ROOT 不存在，必须优先运行 `books/scripts/create_book_project.py` 自动创建 `books/zh-Hans/{number}_{目标语言书名}_{目标语言作者名}`，由脚本先把 COMMON_TEMPLATE_ROOT 复制到 PROJECT_ROOT，再把 TEMPLATE_ROOT 覆盖复制到 PROJECT_ROOT。

严禁直接在 COMMON_TEMPLATE_ROOT 或 TEMPLATE_ROOT 内制作具体书籍。它们是只读模板，只能作为复制来源。所有抓取、研究、翻译、QA、EPUB 输出都必须写入 PROJECT_ROOT。

必须按以下顺序读取并执行：

1. README.md
2. PIPELINE_SPEC.md
3. automation_contract.md
4. prompts/00_orchestrator_zh_en.md

然后由 00_orchestrator_zh_en.md 串联执行全部 prompts。

硬性要求：

- 先核查原文来源和版权/公版/授权状态；若用户提供本地书源并声明个人自用、不传播、不商业使用，则进入 `private_use` 模式，读取并应用 `template/epub_pipeline/modes/private_use/` 覆盖层规则，记录 `metadata/private_use_declaration.md`。公开发布权利不明确且没有私人本地书源时停止。
- 未完成模板复制，不得抓取原文。
- 先完成通用翻译研究和本书专项翻译研究。
- 正式翻译前必须完成 qa/pretranslation/pretranslation_report.md，且结论为 PASS。
- 预翻译失败时必须回溯，不得跳过。
- 翻译调用必须瘦身，只输出译文；不得把 release、EPUB、lint、QA 文件结构、随机抽检或版本化产物规则塞进翻译 prompt，也不得把 QA 报告、解释、流程记录混入 `chapters/translated/`。
- 翻译阶段第一目标是自然中文正文：译文必须像一本自然的中文书，长句要能拆，短句不能省成提纲；术语一致和出版格式不得压倒中文可读性。
- 分章译文不得直接进入 chapters/final。
- 每章翻译后必须立即创建并执行 `qa/chapter_controls/{NNN_slug}.control.md`，作为“每章译后，全量检查并修复节点”。该节点只检查当前章，必须检查该章正文、注释、图表/表格/公式/图片的文字接口、样式、读者可见内容、通俗化、可读性、润色、名词术语和注释等，不得只检查用户点名项目，也不得扩大成全书章节检查。
- 每章 control 必须先做只看中文的独立可读性复查：中文独立阅读评分低于 4/5、20 句朗读中明显拗口超过 1 句，或关键句不断气时，即使事实大体准确也必须返工。
- 若该章 control 最近一轮不是全章零问题 PASS，必须修复并追加不可变复查轮；更严格项目/profile 规则仍优先。发现并修复问题的轮次只能记为 `FIXED_RECHECK_REQUIRED`，不得直接 PASS。只有绑定精确有序 unit、当前 chapter digest、零问题/修复/未解阻塞的密封 PASS 才能让该章进入后续审校或 `chapters/final/`；其他独立 owner 的章节可按自适应计划继续。复杂图表/资产问题应路由到资产/技术门禁并阻止终稿/构建/release，不让本节点无限循环。
- 每章必须完成 fidelity/readability/imagery/terminology/gate 报告。
- 只有 gate PASS 的 canonical generation 才可由物化脚本投影到 `chapters/final`；任何 agent 不得直接写或手改投影。
- 全部章节完成后必须进入预制作阶段 1，制定封面、metadata、字体、排版、标题、作者信息、版本说明等规格。
- 必须先制作样章 EPUB；若 state/human_feedback_control.md 中 human_required=false，则自动检查并继续；若 true，则等待用户。
- 样章 PASS 后才可制作全书 EPUB。
- 第一版全书 EPUB 完成后必须执行分层随机抽检模块：运行确定性抽样脚本，抽样正文段落、表格、图片、公式/证明块、图注和注释，保留 `reviews/random_spotcheck/round_XXX/` 下的样本、证据、评审、修复和闭环记录，并在最终输出前通过 `npm run review:random-validate:pass`。
- 随机抽检闭环通过后必须执行版本化产物模块：公版或授权项目运行 `npm run release:create`，生成 `output/release/book_vX.X.X.epub`、中英文 `release_note_vX.X.X.md`、`release_state.json` 和 `release_index.md`；`private_use` 项目运行 `npm run private:artifact:create`，生成 `output/private_artifacts/{title}_private_vX.X.X.epub`、`private_artifact_notes.md`、`private_artifact_state.json` 和 `private_artifact_index.md`。
- 分层随机抽检通过后，必须派生 2 个独立 Agent 严格评审，并输出评分表。
- 评审发现问题必须按 revision_route 回到对应阶段返工。
- 最终生成 `output/book.epub`。公版或授权项目把可发布版本固化到 `output/release/book_vX.X.X.epub`；`private_use` 项目把本地私人产物固化到 `output/private_artifacts/`，不得作为公开 release。
- 必须运行 epubcheck 或等价校验，fatal/error 为 0 才可进入最终输出。
- 完成后必须做全阶段复审，总结经验教训，写入 retrospective，并在需要时递增模板版本。
- 译文要优秀、可读、有中文叙述气息；不得机械直译、不得越界发挥、不得省字式翻译。

如果需要人类审阅，只能由控制文件决定；默认 human_required=false，AI 自动执行。
```

## 随机抽检同类问题全书审计 / Book-Wide Similar-Issue Audit

随机抽检一旦发现任何需要修复或可能系统性复现的问题，包括但不限于 P0/P1/P2、单项 <80、读者不可理解、事实/术语/图表/公式/注释错误，或本模板硬门禁失败，主执行 AI 不得只修被抽中的样本，也不得等到第二轮才全书检查。必须先把发现归纳为问题族，再对整本读者可见书稿执行全书同类问题审计，覆盖 `chapters/final/`、frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML；修复所有确认命中，记录合理例外，并在该轮 `fix_log.md` 与 `closure_check.md` 中关闭该问题族后，才能使用新 seed 复抽。

若该轮发现译文质量问题族，还必须在 `fix_log.md` 填写 `translation_quality_skill_backfill: "UPDATED"` 或 `"MERGED"`、`translation_quality_skill_backfill_path: "skills/translation-quality-defect-families/SKILL.md"` 和回填摘要，并在 `closure_check.md` 填写 `translation_quality_skill_backfill_verified: true`；若仅有非译文质量问题，必须填写 `NOT_APPLICABLE` 和具体理由。

If a random sample exposes any issue that needs correction or may recur systemically, treat it as a possible systemic defect family immediately in the current round. Audit the whole reader-facing book for similar cases, fix all confirmed matches, document justified exceptions, and close the family in the same round before a new-seed resample.

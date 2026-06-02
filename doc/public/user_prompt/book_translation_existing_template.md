# 书籍翻译执行 Prompt：已有源语言模板

适用场景：仓库里已经有对应语言方向模板，例如 `ja-zh-Hans`、`en-zh-Hans` 或 `grc-zh-Hans`。

用户入口只需要包含三项内容：

- 我要翻译的书：`{书名、作者、来源线索，或本地文件路径}`
- 目标语言：`{例如 简体中文 / English / 日本語 / Español}`
- 自动选择 prompt 规则：执行本文件；若源语言模板不存在，则改用 `doc/public/user_prompt/book_translation_new_template.md`

把上面三项内容和下面 prompt 一起发给 AI Agent。

```text
你是在 public-domain-books-translation 仓库内工作的 EPUB 翻译出版 Agent。公开项目必须使用公版或授权来源；非公版书只能在用户提供本地书源并声明个人自用、不传播、不商业使用时进入 `private_use` 模式。

用户入口只提供三项内容：
- 我要翻译的书：{用户填写}
- 目标语言：{用户填写}
- 自动选择 prompt 规则：已有源语言模板时执行本文件；没有源语言模板时改用 `doc/public/user_prompt/book_translation_new_template.md`

除此之外，源语言、可靠公版/授权来源 URL 或私人本地书源模式、source-target 语言方向、目标语言标签、目录名、是否需要 profile、建书目录编号，都必须由你自动判断、自动记录。不要要求用户补充这些技术字段，除非版权状态、来源权利无法确认，或用户请求非公版私人自用但没有提供本地书源文件。

任务目标：
严格依据当前仓库规则创建并完成这本书的 EPUB 翻译项目。公开项目最终必须生成 `books/{target}/{number}_{目标语言书名}_{目标语言作者名}/output/release/` 下 latest_status=PASS 的可发布 EPUB。私人自用项目必须位于被 Git 忽略的 `books/private/{target}/{number}_{目标语言书名}_{目标语言作者名}/`，其版本化 EPUB 只是个人自用产物，不得发布到 GitHub。`output/book.epub` 不能单独作为完成依据。

执行规则：

1. 第一件事必须读取仓库根目录 `AGENTS.md`。
2. 然后读取当前任务相关模板文件，至少包括：
   - `template/epub_pipeline/README.md`
   - `template/epub_pipeline/common/README.md`
   - `template/epub_pipeline/common/preproduction/stage1/_TEMPLATE.production_spec.md`
   - `template/epub_pipeline/common/references/quality_gate_framework.md`
   - `template/epub_pipeline/common/references/stratified_random_spotcheck.md`
   - `template/epub_pipeline/common/references/release_versioning.md`
   - `template/epub_pipeline/common/references/cover_design_policy.md`
   - `template/epub_pipeline/common/references/book_info_frontmatter_policy.md`
   - `template/epub_pipeline/common/references/epub_assets_figures_tables.md`
   - `template/epub_pipeline/common/prompts/08a_chapter_post_translation_control.md`
   - `template/epub_pipeline/common/prompts/16a_stratified_random_spotcheck.md`
   - `skills/translation-quality-defect-families/SKILL.md`
   - 若进入私人自用模式，还必须读取 `template/epub_pipeline/modes/private_use/README.md`、`references/private_use_cover_policy.md`、`references/private_use_frontmatter_policy.md`、`references/private_use_artifact_policy.md`
   - 匹配的 `template/epub_pipeline/targets/{target}/`
   - 匹配的 `template/epub_pipeline/{source-target}/`
3. 不得依赖记忆、历史执行经验或假设；必须以当前仓库文件为准。
4. 根据书名、作者、来源线索或本地文件，自动判断源语言和目标语言标签，自动选择 source-target 模板。
5. 若 SOURCE_URL 未由用户提供且用户没有提供本地书源文件，必须自动查找可靠公版或授权来源，例如 Project Gutenberg、青空文库、Wikisource、Internet Archive、Gallica、国家图书馆/大学馆藏等；不得自动查找非公版全文。
6. 若用户给的是本地文件并声明个人自用、不传播、不商业使用，使用 `books/scripts/create_book_project.py --mode private-use --local-source-file ... --private-use-declaration ...` 创建 `books/private/{target}/{next_number}_{目标语言书名}_{目标语言作者名}/`，并记录 `metadata/private_use_declaration.md`。本地文件存在不等于可发布；私人模式不得输出公开 release。
7. 不得使用现代受版权保护译本、盗版站、来源不明 EPUB 或用户无权提交的材料。
8. 确认 `template/epub_pipeline/{source-target}` 已存在；若不存在，不要硬套其他模板，改用“没有源语言模板”的公共 prompt 流程。
9. 公开项目必须使用 `books/scripts/create_book_project.py` 创建 `books/{target}/{next_number}_{目标语言书名}_{目标语言作者名}/`；私人自用项目必须使用同一脚本的 `--mode private-use` 创建 `books/private/{target}/{next_number}_{目标语言书名}_{目标语言作者名}/`。目录名由你根据目标语言书名和作者名自动生成：目标语言是中文就使用中文，目标语言是日语就使用日语，目标语言是英语就使用英语。
10. 若同书目录已存在，先检查其状态；不得覆盖。若已 PASS，报告现状；若未完成，继续补齐；若需要新版本，使用新 slug 或按 release 规则迭代。
11. 所有原文、译文、QA、EPUB、release、book-specific metadata 只能写入该书目录，不得写回 `template/`。
12. 翻译前必须完成并记录：
    - `metadata/source_evidence.md`
    - `metadata/rights_checklist.md`
    - 源语言 profile：使用语言模板规定的文件名；若模板未规定，创建 `metadata/source_text_profile.md`
    - `qa/textual/` 下的文本疑难记录
    - `metadata/book_specific_translation_research.md`
    - `metadata/style_profile.md`
    - `glossary/terms.csv`
    - `qa/pretranslation/pretranslation_report.md`，且结论为 PASS
    - `qa/samples/sample_test_report.md`，且结论为 PASS
13. 必须完成分章翻译和每章译后全量检查闭环。每章写入 `chapters/translated/{chapter}.md` 后，必须立即执行当前章全量检查并修复：对照整章原文和整章译文，覆盖忠实度、漏译误译、目标语言顺读、文学性、可读性和吸引力、教学/解释节奏、术语稳定、专名/案例/标题一致性、标题/小标题、注释、图表/公式/表格/图片文字接口、源语言句法残留、过硬过直句、过度解释、无依据加戏、读者可见 AI/制作痕迹、乱码/异常空格和旧纸书残留。只要发现任何问题，先修复该章，但该轮只能记录为 `FIXED_RECHECK_REQUIRED`，不能 PASS；必须追加新一轮整章复查。只有最新一轮记录 `scope: FULL_CHAPTER`、`issues_found: 0`、`fixes_applied: 0`、`unresolved_blocking_issues: 0`、`latest_round_status: PASS`、`allow_next_chapter: true` 时，才可进入下一章、`chapters/final/` 或章节 gate。不同章节可以并行，但每章必须独立闭环。
14. 若任一章节检查、审校或修订发现可复现译文质量问题族，例如短句切断、比喻自撞、排比标点拖拽、代词指代不清、源语言句法残留、术语漂移、标题超载、过度解释或加戏，必须使用 `skills/translation-quality-defect-families/SKILL.md`：在本书记录发现方式、归纳、低 token 同类审计、修复、例外和复查；先用 `rg`、术语表、禁用写法、标题表、章节控制记录和小上下文原文对照收集候选，只把候选片段交给 agent 复核；书内闭环后只把可复用经验合并进该 skill，不盲目重复追加。
15. 必须完成 `preproduction/stage1/production_spec.md`、样章检查、全书 EPUB 构建。
16. 构建和发布前必须清理或重建 staging 输出，避免旧 XHTML、链接或资产污染新门禁。
17. 必须运行并通过：
    - `npm run build:epub`
    - `npm run check:epub`
    - `npm run lint:publication` 或等价 publication lint
    - `npm run lint:assets` 或等价 asset manifest check
    - `npm run preflight:template`
    - `npm run cover:check`
    - `npm run reader:check`
18. 第一版全书 EPUB 后必须执行分层随机抽检与问题族追杀：
    - 以 reader-facing audit units 为总体。
    - 覆盖实际存在的 paragraphs、tables、figures、formulas/proof blocks、captions/notes。
    - 每轮生成 `reviews/random_spotcheck/round_XXX/` 下的 seed、manifest、samples、evidence、Agent A/B 独立评审、fix_log、closure_check。
    - 任一样本或任一 Agent 发现 P0/P1/P2、单项 <70、读者读不懂、忠实度偏移、事实/叙述关系误解、源语言句法硬搬、无依据润饰、术语/专名/标题/译注/表格/图片/公式错误，必须在当轮归纳为问题族，对整本读者可见书稿执行全书同类审计，并修复全部确认命中；不得只修被抽中的样本，不得等第二轮才查全书。
    - 译文质量问题族必须先用低 token 方法审计：`rg`、`glossary/terms.csv`、`forbidden_body_renderings`、标题映射、章节控制记录、抽样 manifest 和小上下文原文对照；只把候选片段交给 agent 复核。
    - 修复后必须在本轮 `fix_log.md` 和 `closure_check.md` 记录问题族、检索式/审计方法、命中数、修复位置、合理例外和复查结果，重建 EPUB，并用新 seed 追加下一轮抽检。
    - 只有最近连续 N 个新 seed 抽检轮均 PASS（N 最小为 1，默认 2，高质量译本可选 3），所有已发现问题族关闭，且 `npm run review:random-validate:pass` 或等价 `--require-pass` 校验通过，才可退出抽检。
19. 抽检和修复完成后必须重新生成 EPUB。公版或授权项目运行 `npm run release:create` 或等价 release 脚本，把可发布 EPUB 输出到 `output/release/`；私人自用项目运行 `npm run private:artifact:create` 或等价 private artifact 脚本，把本地私人产物输出到 `output/private_artifacts/`，不得生成或发布公开 release。
20. 公版或授权项目的 `output/release/release_state.json.latest_status` 必须为 `PASS`；私人自用项目的 `output/private_artifacts/private_artifact_state.json.latest_status` 必须为 `PASS`。
21. 若执行中发现模板存在可复用缺陷、缺漏或歧义，必须先在本书 QA/retrospective 中记录证据，修复当前书，再把可复用规则以最小必要改动回填到正确模板层级，并重新验证建书脚本和模板引用没有破坏。
22. 最终不得提交未验证完成声明。最终报告必须包含：
    - 书籍项目路径
    - release EPUB 路径，或私人自用项目的 private artifact 路径
    - source URL 或本地来源证据
    - 验证命令与结果
    - 抽检轮次与最终 validation_report
    - 修复摘要
    - 模板回填摘要
    - `release_state.json.latest_status` 或 `private_artifact_state.json.latest_status`
    - 剩余风险
```

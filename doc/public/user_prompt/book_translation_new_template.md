# 书籍翻译执行 Prompt：没有源语言模板

适用场景：仓库里还没有对应语言方向模板，例如想做 `fr-zh-Hans`，但 `template/epub_pipeline/fr-zh-Hans/` 还不存在。

用户入口只需要包含三项内容：

- 我要翻译的书：`{书名、作者、来源线索，或本地文件路径}`
- 目标语言：`{例如 简体中文 / English / 日本語 / Español}`
- 自动选择 prompt 规则：执行本文件；若源语言模板已存在，则改用 `doc/public/user_prompt/book_translation_existing_template.md`

把上面三项内容和下面 prompt 一起发给 AI Agent。

```text
你是在 public-domain-books-translation 仓库内工作的 EPUB 翻译出版 Agent。公开项目必须使用公版或授权来源；非公版书只能在用户提供本地书源并声明个人自用、不传播、不商业使用时进入 `private_use` 模式。

用户入口只提供三项内容：
- 我要翻译的书：{用户填写}
- 目标语言：{用户填写}
- 自动选择 prompt 规则：没有源语言模板时执行本文件；已有源语言模板时改用 `doc/public/user_prompt/book_translation_existing_template.md`

除此之外，源语言、可靠公版/授权来源 URL 或私人本地书源模式、source-target 语言方向、目标语言标签、项目 slug、是否需要 profile、建书目录编号，都必须由你自动判断、自动记录。不要要求用户补充这些技术字段，除非版权状态、来源权利、目标语言规则无法确认，或用户请求非公版私人自用但没有提供本地书源文件。

任务目标：
在源语言方向模板尚不存在的情况下，先创建最小可复用的 `{source-target}` 语言方向模板，再用该模板创建并完成一本 EPUB 书籍项目。公开项目最终必须生成 `books/{target}/{number}_{slug}/output/release/` 下 latest_status=PASS 的可发布 EPUB；私人自用项目必须位于被 Git 忽略的 `books/private/{target}/{number}_{slug}/`，其版本化 EPUB 只是个人自用产物，不得发布到 GitHub。

第一阶段：读取规则与确认缺口

1. 第一件事必须读取仓库根目录 `AGENTS.md`。
2. 读取 common、目标语言框架和现有语言方向模板作为结构参考：
   - `template/epub_pipeline/README.md`
   - `template/epub_pipeline/common/README.md`
   - `template/epub_pipeline/common/preproduction/stage1/_TEMPLATE.production_spec.md`
   - `template/epub_pipeline/common/references/` 中与来源、版权、封面、book-info、图表资产、质量门禁、随机抽检、release 有关的文件
   - 匹配的 `template/epub_pipeline/targets/{target}/`
   - 至少一个现有语言方向模板，例如 `en-zh-Hans`、`ja-zh-Hans`、`grc-zh-Hans`，只用于学习目录结构，不得照搬源语言规则
   - 现有已完成书籍项目结构
3. 根据书名、作者、来源线索或本地文件，自动判断源语言和目标语言标签。
4. 确认 `template/epub_pipeline/{source-target}` 不存在。若已存在，改用“已有源语言模板”的公共 prompt 流程。
5. 若 `template/epub_pipeline/targets/{target}/` 也不存在，先停止并报告需要创建目标语言质量框架；不能把 `zh-Hans` 规则当默认规则。

第二阶段：创建最小语言方向模板

6. 在 `template/epub_pipeline/{source-target}/` 创建可复用语言方向模板。
7. 模板只放可复用规则，不得放具体书籍原文、译文、QA、EPUB、release 或 book-specific metadata。
8. 可参考现有模板的目录骨架，但必须逐项改写为当前 `{source} -> {target}` 的真实规则；不得留下其他语言方向的继承残留。
9. 最小模板至少应包含：
   - `AGENTS.md`
   - `SKILL.md`
   - `README.md`
   - `MASTER_PROMPT.md`
   - `TEMPLATE_VERSION.md`
   - `package.json`
   - `metadata/book.yaml`
   - `metadata/style_profile.md`
   - `metadata/source_text_profile.md` 或更具体的源语言 profile 模板
   - `glossary/terms.csv`
   - `glossary/style_guide.md`
   - `qa/textual/source_textual_notes.md` 或更具体的源语言文本疑难模板
   - `qa/chapter_controls/_TEMPLATE.control.md`
   - `reviews/scorecards/_TEMPLATE_scorecard.md`
   - `reviews/scorecards/_TEMPLATE_random_spotcheck_score.md`
   - `references/translation_research_universal.md`
   - `references/quality_standard.md`
   - `references/{source_language}_source_notes.md`
   - `references/{source_language}_to_{target_language}_literary_refinement.md`
   - `prompts/00` 到 `19` 的执行链，或等价的完整阶段 prompt
10. 模板重要文件必须包含该模板贡献者预期能读懂的本地语言。英文可并列用于精确说明，但重要说明不能只用英文，除非目标贡献者语言就是英文。
11. 若需要源语言专项脚本、数据或探索文件，放到 `research/{source-target}/...` 或该语言方向模板内，不得放仓库根目录。
12. 不得在脚本或 prompt 中写死 Windows 盘符、本机绝对路径或某个贡献者的工作目录。

第三阶段：验证模板可建书

13. 运行 dry-run 验证 `books/scripts/create_book_project.py` 可以使用新模板创建项目。
14. dry-run 通过后，公开项目正式创建 `books/{target}/{next_number}_{slug}/`；私人自用项目使用 `--mode private-use --local-source-file ... --private-use-declaration ...` 创建 `books/private/{target}/{next_number}_{slug}/`。slug 由你根据书名和作者自动生成。
15. create_book_project.py 必须先复制 common，再 overlay 新语言方向模板。所有后续具体书籍文件只能写入新书目录。

第四阶段：自动查找来源与版权核查

16. 若用户没有提供可靠来源 URL 且没有提供本地书源文件，必须自动查找可靠公版或授权来源，例如 Project Gutenberg、Wikisource、Internet Archive、Gallica、青空文库、国家图书馆/大学馆藏等；不得自动查找非公版全文。
17. 若用户给的是本地文件并声明个人自用、不传播、不商业使用，记录 `metadata/private_use_declaration.md`，只允许私人自用工程继续；本地文件存在不等于可发布。若既无公版/授权来源又无本地书源，必须停止。
18. 不得使用现代受版权保护译本、盗版站、来源不明 EPUB 或用户无权提交材料。
19. 翻译前必须完成：
    - `metadata/source_evidence.md`
    - `metadata/rights_checklist.md`
    - `metadata/source_text_profile.md` 或模板定义的源语言 profile
    - `qa/textual/source_textual_notes.md` 或模板定义的文本疑难记录

第五阶段：完成书籍制作

20. 完成 book-specific research、style profile、预翻译 PASS、小样本 PASS。
21. 分章翻译，完成每章译后控制、忠实度、可读性/意象、术语、章节 gate；只有 gate PASS 的章节进入 `chapters/final/`。
22. 完成 `preproduction/stage1/production_spec.md`、样章 EPUB、全书 EPUB。
23. 构建和发布前清理或重建 staging 输出，避免旧 XHTML、链接或资产污染新门禁。
24. 必须运行并通过：
    - `npm run build:epub`
    - `npm run check:epub`
    - `npm run lint:publication` 或等价 publication lint
    - `npm run lint:assets` 或等价 asset manifest check
    - `npm run preflight:template`
    - `npm run cover:check`
    - `npm run reader:check`
25. 第一版全书 EPUB 后必须执行分层随机抽检：
    - 以 reader-facing audit units 为总体。
    - 覆盖实际存在的 paragraphs、tables、figures、formulas/proof blocks、captions/notes。
    - 每轮生成 `reviews/random_spotcheck/round_XXX/` 下的样本、证据、Agent A/B 独立评审、fix_log、closure_check。
    - 任一层或任一 Agent 发现 P0/P1/P2、读者读不懂、事实/叙述关系误解、源语言句法硬搬、无依据润饰、术语/专名/译注/表格/图片/公式错误，必须修复、重建 EPUB，并用新 seed 追加下一轮抽检。
    - 只有最后N轮无未关闭问题(N最小为1, 默认2, 输出高质量译本可选3)，且 `npm run review:random-validate:pass` 或等价 `--require-pass` 校验通过，才可退出抽检。
26. 抽检和修复完成后必须重新生成 EPUB，并运行 `npm run release:create` 或等价 release 脚本，把可发布 EPUB 输出到 `output/release/`。
27. `output/release/release_state.json` 的 `latest_status` 必须为 `PASS`。`output/book.epub` 不能单独作为完成依据。

第六阶段：模板回填与最终报告

28. 如果当前书暴露新语言方向模板、common 或 target 规则的可复用缺陷，必须先在该书 QA/retrospective 中记录证据，修复当前书，再把最小必要规则回填到正确层级。
29. 回填后必须重新验证：
    - `create_book_project.py` 可创建项目
    - book-local package scripts 可运行
    - 当前书 build/check/release 不被破坏
30. 最终报告必须包含：
    - 新建语言方向模板路径
    - 书籍项目路径
    - release EPUB 路径
    - source URL 或本地来源证据
    - 验证命令与结果
    - 抽检轮次与最终 validation_report
    - 修复摘要
    - 模板回填摘要
    - `release_state.json.latest_status`
    - 剩余风险
```

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
13. 必须完成分章翻译、每章译后控制、忠实度审校、可读性/意象审校、术语审校、章节 gate。只有 gate PASS 的章节才能进入 `chapters/final/`。
14. 必须完成 `preproduction/stage1/production_spec.md`、样章检查、全书 EPUB 构建。
15. 构建和发布前必须清理或重建 staging 输出，避免旧 XHTML、链接或资产污染新门禁。
16. 必须运行并通过：
    - `npm run build:epub`
    - `npm run check:epub`
    - `npm run lint:publication` 或等价 publication lint
    - `npm run lint:assets` 或等价 asset manifest check
    - `npm run preflight:template`
    - `npm run cover:check`
    - `npm run reader:check`
17. 第一版全书 EPUB 后必须执行分层随机抽检：
    - 以 reader-facing audit units 为总体。
    - 覆盖实际存在的 paragraphs、tables、figures、formulas/proof blocks、captions/notes。
    - 每轮生成 `reviews/random_spotcheck/round_XXX/` 下的 seed、manifest、samples、evidence、Agent A/B 独立评审、fix_log、closure_check。
    - 任一层或任一 Agent 发现 P0/P1/P2、读者读不懂、事实/叙述关系误解、源语言句法硬搬、无依据润饰、术语/专名/译注/表格/图片/公式错误，必须修复、重建 EPUB，并用新 seed 追加下一轮抽检。
    - 只有最后N轮无未关闭问题(N最小为1, 默认2, 输出高质量译本可选3)，且 `npm run review:random-validate:pass` 或等价 `--require-pass` 校验通过，才可退出抽检。
18. 抽检和修复完成后必须重新生成 EPUB。公版或授权项目运行 `npm run release:create` 或等价 release 脚本，把可发布 EPUB 输出到 `output/release/`；私人自用项目运行 `npm run private:artifact:create` 或等价 private artifact 脚本，把本地私人产物输出到 `output/private_artifacts/`，不得生成或发布公开 release。
19. 公版或授权项目的 `output/release/release_state.json.latest_status` 必须为 `PASS`；私人自用项目的 `output/private_artifacts/private_artifact_state.json.latest_status` 必须为 `PASS`。
20. 若执行中发现模板存在可复用缺陷、缺漏或歧义，必须先在本书 QA/retrospective 中记录证据，修复当前书，再把可复用规则以最小必要改动回填到正确模板层级，并重新验证建书脚本和模板引用没有破坏。
21. 最终不得提交未验证完成声明。最终报告必须包含：
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

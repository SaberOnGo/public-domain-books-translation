# Language-Neutral Quality Gate Framework

This file defines quality-gate concepts that apply to every translation direction. It intentionally avoids target-language style rules.

本文件定义所有翻译方向都适用的质量门禁概念。它刻意不写入某个目标语言的文体规则。

## Universal Gates / 通用门禁

- Source and rights evidence must exist before translation starts. Public projects require public-domain or licensed evidence. Private-use projects require a user-provided local source file, a private-use declaration, and an ignored `books/private/` project path.
- 翻译开始前必须已有来源证据和版权核查记录。公开项目必须有公版或授权证据。私人自用项目必须有用户提供的本地书源文件、私人自用声明，并位于被忽略的 `books/private/` 工程路径。
- A book-level research note and style profile must exist before batch translation.
- 批量翻译前必须已有本书专项研究和文体画像。
- Trial translation must pass before full chapter production.
- 试译通过后才能进入整章批量生产。
- Every chapter must pass a post-translation full check and fix node immediately after `chapters/translated/{chapter}.md` is produced. This is a hard gate before the next chapter may be translated or promoted. The check must cover the full reader-facing chapter and its production context, including but not limited to metadata impact, nav/title/TOC implications, body text, notes, figures, formulas, tables, images, styles, terminology, reader-visible text, readability, plain-language clarity, and target-language polish. It must not limit itself to issues named by the user or by the previous failure.
- 每章生成 `chapters/translated/{chapter}.md` 后，必须立即执行“每章译后，全量检查并修复节点”。这是进入下一章翻译或送入终稿前的当前章文字硬门禁。检查对象必须覆盖该章完整读者可见文字内容及其章节级制作上下文，包括但不限于该章对 metadata/nav/标题/目录的影响、正文、注释、图表/公式/表格/图片的文字接口、样式、术语、读者可见文本、可读性、通俗化表达和目标语言润色。不得只检查用户点名项目或上一轮失败项目，也不得扩大成全书章节检查。
- 术语原词呈现必须服务读者阅读，而不是展示严谨。目标语正文默认使用目标语译名或准确意译；源语原词、定义和译名理由优先放入本章译注、章末注或术语表，并由正文注号指向。只有不保留原词会造成明显误解、原词本身是论证对象，或译名分歧必须当场交代时，才允许正文短括注原词；例外必须记录理由。无必要的大面积 `目标语译名（source term）` 是读者可见质量问题。
- `glossary/terms.csv` 必须把高风险术语的正文呈现策略机器可读地写清楚，包括 `display_policy`、`note_text`、`exception_reason` 和 `forbidden_body_renderings`。每章译后全量检查必须按 `forbidden_body_renderings` 扫描正文；若发现禁用写法、无授权正文括注原词、裸露源语词或误导性泛译，本章必须返工，不能进入下一流程。
- The chapter post-translation full check must write `qa/chapter_controls/{chapter}.control.md`. If it finds any blocking issue, any reader-confusing wording, any fact/term/text-interface error, or a score below the configured threshold, the chapter must be fixed and the same node must run again. The workflow may continue only when the latest run has no unresolved blocking issue and is either issue-free or has an overall score of at least 75, subject to any stricter project/profile rule. A score cannot override P0/P1/P2, reader confusion, factual/terminology/text-interface errors, or hard-gate failures. Failed attempts and fixes must remain recorded.
- 每章译后全量检查必须写入 `qa/chapter_controls/{chapter}.control.md`。若发现任何阻塞问题、读者难以理解的表达、事实/术语/当前章文字接口错误，或评分低于项目设定阈值，必须修复后追加执行同一节点。只有最近一次检查无未关闭阻塞问题，并且“无问题或总评分不小于 75 分”时，才可继续；若项目/profile 有更严格规则，按更严格规则。分数不能抵消 P0/P1/P2、读者难以理解、事实/术语/文字接口错误或模板硬门禁失败。失败轮次和修复点必须保留记录。
- 图表、表格、公式和图片在该节点只做当前章文字接口检查与资产分流；复杂资产问题进入 `references/epub_assets_figures_tables.md` 定义的资产/技术门禁，并阻止终稿、构建和 release，不应让译后文字门禁无限循环。
- Every chapter must pass fidelity, readability, terminology, imagery/reader-facing, post-translation control, and final gate checks before it enters `chapters/final/`. `preflight:template` must reject a project where `chapters/final/*.md` exists without matching PASS `qa/chapter_controls/*.control.md`, `allow_next_chapter: true`, and PASS `qa/gates/*.gate.md`.
- 每章进入 `chapters/final/` 前，必须通过忠实度、可读性、术语、意象/读者可见内容、译后控制和最终门禁检查。若 `chapters/final/*.md` 已存在但缺少对应 PASS 且 `allow_next_chapter: true` 的 `qa/chapter_controls/*.control.md`，或缺少 PASS 的 `qa/gates/*.gate.md`，`preflight:template` 必须拒绝继续。
- EPUB output must pass structural validation before final release or private artifact creation.
- 最终发布或创建私人产物前，EPUB 必须通过结构校验。
- After the first full-book EPUB and after each post-EPUB refinement pass, the workflow must run the stratified random spot-check module in `references/stratified_random_spotcheck.md`. At least two independent review agents must review deterministic random samples across reader-facing audit-unit strata: paragraphs, tables, figures, formula/proof blocks, captions, and notes. Both agents must pass, every discovered P0/P1/P2 must be fixed and closed, and a new-seed round must pass after rework before refinement can be considered complete.
- 第一版全书 EPUB 生成后，以及每一轮 EPUB 后精校完成后，必须执行 `references/stratified_random_spotcheck.md` 定义的分层随机抽检模块。至少两个独立评审 Agent 必须检查确定性随机样本，抽样层包括正文段落、表格、图片、公式/证明块、图注和注释。两个 Agent 都必须通过；所有发现的 P0/P1/P2 必须修复并定点关闭；返工后还必须使用新 seed 再通过一轮抽检，才可认为精校完成。
- Final public publication requires a versioned release from `references/release_versioning.md`: `output/release/{target-language-title}_vX.X.X.epub`, cumulative bilingual `release_notes.md`, `release_state.json.latest_status = PASS`, and evidence that the latest random spot-check validation used `--require-pass`. `publication_mode=private_use` requires the `modes/private_use` private artifact gate instead: `output/private_artifacts/{target-language-title}_private_vX.X.X.epub`, `private_artifact_state.json.latest_status = PASS`, and the same random spot-check evidence.
- 最终公开发布必须执行 `references/release_versioning.md` 定义的版本化发布：生成 `output/release/{目标语言书名}_vX.X.X.epub`、累计中英文 `release_notes.md`、`release_state.json.latest_status = PASS`，并证明最近一次随机抽检校验使用了 `--require-pass`。`publication_mode=private_use` 必须改走 `modes/private_use` 的私人产物门禁：生成 `output/private_artifacts/{目标语言书名}_private_vX.X.X.epub`、`private_artifact_state.json.latest_status = PASS`，并具备同等随机抽检证据。

## What Belongs Elsewhere / 哪些内容不属于这里

- Target-language prose standards belong under `template/epub_pipeline/targets/{target}/`.
- 目标语言文体标准应放在 `template/epub_pipeline/targets/{target}/`。
- Source-language interference rules belong under `template/epub_pipeline/{source-target}/`.
- 源语言干扰规则应放在 `template/epub_pipeline/{source-target}/`。
- Book-specific decisions belong inside `books/{target}/{number}_{book_id_slug}/`.
- 具体书籍判断应写入 `books/{target}/{number}_{book_id_slug}/`。

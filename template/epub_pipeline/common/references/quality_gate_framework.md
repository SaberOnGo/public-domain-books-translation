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
- The chapter post-translation full check must write `qa/chapter_controls/{chapter}.control.md`. Every round must inspect the whole current chapter, not only prior failures or sampled passages. If any round finds any blocking issue, reader-confusing wording, fact/term/text-interface error, target-language awkwardness, over-simplification, under-explained specialist term, or other translation/polish issue, the chapter must be fixed, but that round must be recorded as `FIXED_RECHECK_REQUIRED`, not `PASS`. The workflow may continue only after a new full-chapter recheck round records `scope: FULL_CHAPTER`, `issues_found: 0`, `fixes_applied: 0`, `unresolved_blocking_issues: 0`, `latest_round_status: PASS`, and `allow_next_chapter: true`. Failed attempts and fixes must remain recorded.
- 每章译后全量检查必须写入 `qa/chapter_controls/{chapter}.control.md`。每一轮都必须检查当前整章，不得只复查上一轮失败点，也不得只做抽样段落。若任一轮发现阻塞问题、读者难以理解的表达、事实/术语/当前章文字接口错误、目标语翻译腔、中文不顺、为了通俗而损害专业度、专业术语解释不足或其他翻译/润色问题，必须先修复该章；但发现并修复问题的这一轮只能记录为 `FIXED_RECHECK_REQUIRED`，不得直接 `PASS`。只有随后追加的新一轮整章复查记录 `scope: FULL_CHAPTER`、`issues_found: 0`、`fixes_applied: 0`、`unresolved_blocking_issues: 0`、`latest_round_status: PASS`、`allow_next_chapter: true` 时，才可继续。失败轮次和修复点必须保留记录。
- Plain-language readability is a quality requirement, not permission to flatten the book. A professional or scholarly book should read smoothly, clearly, and even enjoyably when the source allows it, while preserving its specialist level, terminology, evidentiary chain, and intellectual style.
- 通俗化、顺读和有趣是质量要求，不是把专业书降格改写的许可。专业/学术书也应尽量读得顺、清楚、不费劲，在原文允许时可以有趣；但必须保持本书的专业水准、术语精度、论证链条和知识风格，不能为了通俗而通俗。
- 图表、表格、公式和图片在该节点只做当前章文字接口检查与资产分流；复杂资产问题进入 `references/epub_assets_figures_tables.md` 定义的资产/技术门禁，并阻止终稿、构建和 release，不应让译后文字门禁无限循环。
- Every chapter must pass fidelity, readability, terminology, imagery/reader-facing, post-translation control, and final gate checks before it enters `chapters/final/`. `preflight:template` must also reject any `chapters/translated/*.md` chapter whose matching `qa/chapter_controls/*.control.md` is missing or whose latest full-chapter round is not closed with the zero-issue PASS fields above. For `chapters/final/*.md`, it must additionally require a PASS `qa/gates/*.gate.md`.
- 每章进入 `chapters/final/` 前，必须通过忠实度、可读性、术语、意象/读者可见内容、译后控制和最终门禁检查。`preflight:template` 还必须拒绝任何 `chapters/translated/*.md` 中已经存在、但缺少对应 `qa/chapter_controls/*.control.md`，或对应 control 最近整章轮次没有以上“零问题 PASS 字段”的章节。对 `chapters/final/*.md`，还必须额外要求 PASS 的 `qa/gates/*.gate.md`。
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

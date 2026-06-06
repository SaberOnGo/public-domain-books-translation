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
- Every chapter must pass a post-translation full check and fix node immediately after `chapters/translated/{chapter}.md` is produced. This is a hard gate before the next chapter may be translated or promoted. The check must cover the full reader-facing chapter and its production context, including but not limited to fidelity, target-language readability, teaching/explanatory rhythm when applicable, terminology, case/name/title consistency, titles/subtitles, notes, figure/table/formula text interfaces, source-language syntax residue, stiff or overly literal sentences, over-explanation, invented additions, metadata impact, nav/title/TOC implications, body text, figures, formulas, tables, images, styles, reader-visible text, readability, plain-language clarity, and target-language polish. It must not limit itself to issues named by the user or by the previous failure.
- 每章生成 `chapters/translated/{chapter}.md` 后，必须立即执行“每章译后，全量检查并修复节点”。这是进入下一章翻译或送入终稿前的当前章文字硬门禁。检查对象必须覆盖该章完整读者可见文字内容及其章节级制作上下文，包括但不限于忠实度、目标语顺读、适用时的教学/解释节奏、术语、案例/专名/题名一致性、标题/小标题、注释、图表/公式/表格/图片的文字接口、源语句法残留、过硬过直句、过度解释、擅自加戏、该章对 metadata/nav/标题/目录的影响、正文、样式、读者可见文本、可读性、通俗化表达和目标语言润色。不得只检查用户点名项目或上一轮失败项目，也不得扩大成全书章节检查。
- Expert-level translation quality is a workflow requirement, not an optional polish pass. Translation, chapter control, random spot-check, final artifact review, and reader-feedback fixes must use `skills/expert-translation-quality/SKILL.md` when source-supported prose quality, context-dependent word choice, or polysemy back-checking matters. A chapter control PASS must record `expert_translation_skill_used: true`, `expert_level_review_status: "PASS"`, `polysemy_context_review: "PASS"`, and `polysemy_unresolved_count: 0`.
- 专家级译文质量是流程要求，不是可选润色。翻译、章节 control、随机抽检、最终产物审阅和读者反馈修复中，只要涉及有原文依据的成稿质量、上下文依赖选义或多义词回看，必须使用 `skills/expert-translation-quality/SKILL.md`。章节 control 的 PASS 必须记录 `expert_translation_skill_used: true`、`expert_level_review_status: "PASS"`、`polysemy_context_review: "PASS"` 和 `polysemy_unresolved_count: 0`。
- 术语原词呈现必须服务读者阅读，而不是展示严谨。目标语正文默认使用目标语译名或准确意译；源语原词、定义和译名理由优先放入本章译注、章末注或术语表，并由正文注号指向。只有不保留原词会造成明显误解、原词本身是论证对象，或译名分歧必须当场交代时，才允许正文短括注原词；例外必须记录理由。无必要的大面积 `目标语译名（source term）` 是读者可见质量问题。
- `glossary/terms.csv` 必须把高风险术语的正文呈现策略机器可读地写清楚，包括 `display_policy`、`note_text`、`exception_reason` 和 `forbidden_body_renderings`。每章译后全量检查必须按 `forbidden_body_renderings` 扫描正文；若发现禁用写法、无授权正文括注原词、裸露源语词或误导性泛译，本章必须返工，不能进入下一流程。
- The chapter post-translation full check must write `qa/chapter_controls/{chapter}.control.md`. Every round must inspect the whole current chapter, not only prior failures or sampled passages. If any round finds any blocking issue, reader-confusing wording, fact/term/text-interface error, target-language awkwardness, over-simplification, under-explained specialist term, or other translation/polish issue, the chapter must be fixed, but that round must be recorded as `FIXED_RECHECK_REQUIRED`, not `PASS`. The workflow may continue only after a new full-chapter recheck round records `scope: FULL_CHAPTER`, `issues_found: 0`, `fixes_applied: 0`, `unresolved_blocking_issues: 0`, `latest_round_status: PASS`, and `allow_next_chapter: true`. Failed attempts and fixes must remain recorded.
- 每章译后全量检查必须写入 `qa/chapter_controls/{chapter}.control.md`。每一轮都必须检查当前整章，不得只复查上一轮失败点，也不得只做抽样段落。若任一轮发现阻塞问题、读者难以理解的表达、事实/术语/当前章文字接口错误、目标语翻译腔、中文不顺、为了通俗而损害专业度、专业术语解释不足或其他翻译/润色问题，必须先修复该章；但发现并修复问题的这一轮只能记录为 `FIXED_RECHECK_REQUIRED`，不得直接 `PASS`。只有随后追加的新一轮整章复查记录 `scope: FULL_CHAPTER`、`issues_found: 0`、`fixes_applied: 0`、`unresolved_blocking_issues: 0`、`latest_round_status: PASS`、`allow_next_chapter: true` 时，才可继续。失败轮次和修复点必须保留记录。
- When any chapter gate or review finds a recurring translation-quality defect family, use `skills/translation-quality-defect-families/SKILL.md`. The book project must preserve immediate evidence, and the reusable lesson must be merged into that skill without blind duplicate entries.
- 章节门禁或评审发现可复现的译文质量问题族时，必须使用 `skills/translation-quality-defect-families/SKILL.md`。具体书籍工程必须保存即时证据，可复用经验必须合并回填到该 skill，不能盲目重复追加。
- Plain-language readability is a quality requirement, not permission to flatten the book. A professional or scholarly book should read smoothly, clearly, and even enjoyably when the source allows it, while preserving its specialist level, terminology, evidentiary chain, and intellectual style.
- 通俗化、顺读和有趣是质量要求，不是把专业书降格改写的许可。专业/学术书也应尽量读得顺、清楚、不费劲，在原文允许时可以有趣；但必须保持本书的专业水准、术语精度、论证链条和知识风格，不能为了通俗而通俗。
- 图表、表格、公式和图片在该节点只做当前章文字接口检查与资产分流；复杂资产问题进入 `references/epub_assets_figures_tables.md` 定义的资产/技术门禁，并阻止终稿、构建和 release，不应让译后文字门禁无限循环。
- Every chapter must pass fidelity, readability, terminology, imagery/reader-facing, post-translation control, and final gate checks before it enters `chapters/final/`. `preflight:template` must also reject any `chapters/translated/*.md` chapter whose matching `qa/chapter_controls/*.control.md` is missing or whose latest full-chapter round is not closed with the zero-issue PASS fields above. For `chapters/final/*.md`, it must additionally require a PASS `qa/gates/*.gate.md`.
- 每章进入 `chapters/final/` 前，必须通过忠实度、可读性、术语、意象/读者可见内容、译后控制和最终门禁检查。`preflight:template` 还必须拒绝任何 `chapters/translated/*.md` 中已经存在、但缺少对应 `qa/chapter_controls/*.control.md`，或对应 control 最近整章轮次没有以上“零问题 PASS 字段”的章节。对 `chapters/final/*.md`，还必须额外要求 PASS 的 `qa/gates/*.gate.md`。
- EPUB output must pass structural validation before final release or private artifact creation.
- 最终发布或创建私人产物前，EPUB 必须通过结构校验。
- After the first full-book EPUB and after each post-EPUB refinement pass, the workflow must run the stratified random spot-check module in `references/stratified_random_spotcheck.md`. At least two independent review agents must review deterministic random samples across reader-facing audit-unit strata: paragraphs, tables, figures, formula/proof blocks, captions, and notes. Both agents must pass. Every discovered P0/P1/P2, unreadable unit, factual/terminology error, table/figure/formula error, or hard-gate failure must be classified as a defect family; the executor must audit the whole reader-facing book for similar cases, fix all confirmed matches, document justified exceptions, close the family in the round fix log and closure check, and only then pass a new-seed round after rework.
- 第一版全书 EPUB 生成后，以及每一轮 EPUB 后精校完成后，必须执行 `references/stratified_random_spotcheck.md` 定义的分层随机抽检模块。至少两个独立评审 Agent 必须检查确定性随机样本，抽样层包括正文段落、表格、图片、公式/证明块、图注和注释。两个 Agent 都必须通过；任一 P0/P1/P2、读不懂、事实/术语错误、图表/公式错误或模板硬门禁失败，都必须先归纳为问题族，并对整本读者可见书稿执行同类问题审计，修复所有确认命中，记录合理例外，在本轮 fix log 和 closure check 中关闭该问题族；返工后还必须使用新 seed 再通过一轮抽检，才可认为精校完成。
- Random spot-check final PASS has two score layers. `80` is only the hard minimum: below it, the round fails immediately. Final public release or private artifact creation defaults to the excellence gate: each agent must have `average_score >= 92`, `lowest_score >= 88`, `blocking_issue_count = 0`, and scored rows for every sampled unit. Results described as merely readable, stiff, dense, abstract, or over-explanatory are polish debt and must not be treated as excellent just because they exceed 80.
- 随机抽检最终 PASS 分两层计分。`80` 只是硬下限：低于 80 立即失败。最终公开 release 或私人产物默认必须走优秀出版线：每个 Agent `average_score >= 92`、`lowest_score >= 88`、`blocking_issue_count = 0`，并且每个抽中样本都有逐项评分行。评语若只是“可读”、但较硬、偏密、略抽象、解释化或仍有源语句法残留，应视为润色债务；不能因为超过 80 就当作优秀。
- For translation-quality defect families discovered by random sampling, use low-token family auditing first: `rg`, glossary rows, forbidden renderings, title maps, sample manifests, and small-context source comparison before asking agents to read broad book ranges. Reusable quality lessons belong in `skills/translation-quality-defect-families/SKILL.md`.
- 对随机抽检发现的译文质量问题族，先使用低 token 的问题族审计：`rg`、术语表行、禁用正文写法、标题映射、抽样 manifest 和小上下文原文对照，然后才让 agent 阅读较大范围。可复用质量经验应写入 `skills/translation-quality-defect-families/SKILL.md`。
- `review:random-validate:pass` must reject a current-run issue round whose `fix_log.md` does not record the translation-quality skill backfill decision. Reusable translation-quality families require `UPDATED` or `MERGED`; format-only or asset-only rounds require `NOT_APPLICABLE` with a reason.
- `review:random-validate:pass` 必须拒绝没有在 `fix_log.md` 记录译文质量 skill 回填决策的当前执行批次问题轮次。可复用译文质量问题族必须是 `UPDATED` 或 `MERGED`；纯格式或纯资产轮次必须是 `NOT_APPLICABLE` 并说明原因。
- 随机抽检 manifest、validation report、release/private artifact state、QA 证据和其他可提交产物不得记录本机绝对路径、Windows 盘符路径、`file://` 或个人工作区路径。所有可复用路径必须写成书籍工程相对路径或仓库相对路径；若校验脚本发现本机绝对路径，必须失败并修复后重跑。
- Final public publication requires a versioned release from `references/release_versioning.md`: `output/release/{target-language-title}_vX.X.X.epub`, cumulative bilingual `release_notes.md`, `release_state.json.latest_status = PASS`, and evidence that the latest random spot-check validation used `--require-pass`. `publication_mode=private_use` requires the `modes/private_use` private artifact gate instead: `output/private_artifacts/{target-language-title}_private_vX.X.X.epub`, `private_artifact_state.json.latest_status = PASS`, and the same random spot-check evidence.
- 最终公开发布必须执行 `references/release_versioning.md` 定义的版本化发布：生成 `output/release/{目标语言书名}_vX.X.X.epub`、累计中英文 `release_notes.md`、`release_state.json.latest_status = PASS`，并证明最近一次随机抽检校验使用了 `--require-pass`。`publication_mode=private_use` 必须改走 `modes/private_use` 的私人产物门禁：生成 `output/private_artifacts/{目标语言书名}_private_vX.X.X.epub`、`private_artifact_state.json.latest_status = PASS`，并具备同等随机抽检证据。

## What Belongs Elsewhere / 哪些内容不属于这里

- Target-language prose standards belong under `template/epub_pipeline/targets/{target}/`.
- 目标语言文体标准应放在 `template/epub_pipeline/targets/{target}/`。
- Source-language interference rules belong under `template/epub_pipeline/{source-target}/`.
- 源语言干扰规则应放在 `template/epub_pipeline/{source-target}/`。
- Book-specific decisions belong inside `books/{target}/{number}_{target_language_title}_{target_language_author}/`.
- 具体书籍判断应写入 `books/{target}/{number}_{目标语言书名}_{目标语言作者名}/`。

## 专家级与多义词放行条件 / Expert and Polysemy Release Condition

每章 control 最近 PASS 轮除通用字段外，还必须记录 `expert_translation_skill_used: true`、`expert_level_review_status: "PASS"`、`polysemy_context_review: "PASS"`、`polysemy_unresolved_count: 0`。发现后文推翻前文选义时，必须回到前文修订并追加新一轮整章复查；修复轮不得直接 PASS。

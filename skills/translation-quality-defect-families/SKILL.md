---
name: translation-quality-defect-families
description: Use when translating, reviewing, revising, or retrospectively improving LifeBook translations and a recurring or potentially recurring translation-quality defect is found. Trigger for fidelity, literary quality, readability, reader engagement, Chinese fluency, terminology, names, titles/subtitles, notes, figure/table/formula text interfaces, source-language syntax residue, stiff or literal sentences, over-explanation, invented additions, short-sentence fragmentation, metaphor collision, list/rhythm punctuation, unclear pronouns, or any other quality issue that may form a defect family. This skill is for translation quality, not EPUB structure, cover, rights, release, or other format-only workflow issues.
---

# 译文质量问题族 / Translation Quality Defect Families

## Boundary / 边界

Use this skill to turn recurring translation-quality problems into reusable correction knowledge.
使用本 skill，把反复出现或可能系统性复现的译文质量问题，沉淀成可复用的修正规则。

This skill focuses on the translation as a readable book: fidelity, literary force, target-language fluency, terminology, narrative rhythm, reader engagement, and source-supported expression.
本 skill 关注“译文作为一本书”的质量：忠实度、文学性、目标语顺读、术语、叙事节奏、读者吸引力，以及所有有原文依据的表达转换。

Do not use this skill for format-only issues such as EPUB manifest errors, cover policy, release metadata, local-path leaks, or CI failures unless they also expose a translation-quality pattern.
不要把本 skill 用于纯格式问题，例如 EPUB manifest、封面 policy、release metadata、本机路径泄漏或 CI 失败；除非这些问题同时暴露了译文质量模式。

## Required Workflow / 必须流程

When a review finds a defect that may recur, do the following before declaring the work closed.
评审发现可能复现的问题后，必须先完成以下步骤，才能宣布关闭。

1. Classify the defect family.
   先归纳问题族。
2. Record how it was found: chapter control, random sample, human note, `rg` scan, glossary scan, source comparison, generated XHTML inspection, or reader feedback.
   记录发现方式：章节控制、随机样本、人工意见、`rg` 扫描、术语扫描、原文对照、生成 XHTML 检查或读者反馈。
3. Define the risk: what reader misunderstanding, fidelity loss, rhythm damage, terminology drift, or unauthorized invention it causes.
   定义风险：它会造成什么误读、失真、节奏损伤、术语漂移或擅自加戏。
4. Audit similar cases with the cheapest reliable method first: glossary fields, `rg`, title maps, source-target term lists, chapter controls, or targeted small-context agent review.
   先用最低 token 且可靠的方法查同类：术语表字段、`rg`、标题映射、源语-目标语词表、章节控制，或小上下文 agent 专项复核。
5. Fix confirmed matches and record justified exceptions.
   修复确认命中，并记录合理例外。
6. Add or merge a reusable lesson in the register below.
   在下方注册表追加或合并可复用经验。
7. Recheck with the appropriate gate: full-chapter recheck for chapter-stage defects, new-seed stratified random sample for post-EPUB defects, or a targeted family audit for book-wide risks.
   用合适门禁复查：章节阶段问题做整章复查，EPUB 后抽检问题用新 seed 复抽，全书风险做问题族专项审计。

## Update Discipline / 更新纪律

Do not append repetitive notes blindly.
不要盲目重复追加。

Before adding a new entry, search this file for the family, source-language mechanism, and target-language symptom. If an entry already exists, update that entry with a sharper detection method, better fix pattern, or a concrete example.
新增条目前，先搜索本文件中的问题族、源语机制和目标语症状。已有同族条目时，应合并更新：补更准的发现方法、更好的修复模式或具体例子。

Every entry should stay reusable across books. Book-specific names may appear as examples, but the rule must be phrased as a general lesson.
每个条目都应能跨书复用。可以用具体书名或人名做例子，但规则必须写成通用经验。

Use bilingual Chinese-English wording for new major sections. Chinese may lead when the expected contributor is Chinese.
新增主要段落使用中英文双语。面向中文贡献者时，中文可置前。

## Low-Token Audit Pattern / 低 token 审计模式

- Start with machine-readable evidence: `glossary/terms.csv`, forbidden renderings, title maps, chapter controls, sample manifests, and review tables.
  先用机器可读证据：`glossary/terms.csv`、禁用正文写法、标题映射、章节控制、抽样 manifest 和评审表。
- Use `rg` to collect candidates before asking an agent to read prose.
  先用 `rg` 收集候选，再让 agent 阅读片段。
- Give the agent only the candidate passage, nearby source text, relevant glossary rows, and the current family rule.
  只给 agent 候选段、邻近原文、相关术语行和当前问题族规则。
- Treat random sampling as discovery, not as the main polishing engine.
  随机抽检用于发现盲点，不是主要润色引擎。
- Treat full-chapter review as the main place to catch fidelity, fluency, rhythm, and terminology issues.
  忠实度、顺读、节奏和术语问题，主要应在每章全量复检阶段解决。

## Defect Family Register / 问题族注册表

### Short-Sentence Fragmentation / 短句切断

- Symptom: The translation breaks a coherent source movement into clipped fragments, making the prose read like notes, commands, or a plot outline.
  症状：译文把连续动作或论述切成碎短句，读起来像提纲、指令或剧情摘要。
- Find by: Chinese-only read-aloud pass, high punctuation density, repeated comma-only action chains, or samples that feel breathless without source pressure.
  发现方式：中文独立朗读、高标点密度、连续动作清单，或原文并无强压迫感但译文读起来喘不过气。
- Fix by: Rebuild sentence groups with natural connectors, subject recovery, rhythm variation, and source-supported pacing; do not flatten tension.
  修复方式：用自然连接、主语恢复、长短变化和原文允许的节奏重组句群；不要把紧张感改平。
- Recheck: Read the revised paragraph aloud and compare with the source to ensure no action, order, or tone was changed.
  复查：朗读修订段，并对照原文确认动作、顺序和语气没有被改错。

### Metaphor Collision / 比喻自撞

- Symptom: A translated image contains mixed vehicles, incompatible physical logic, or extra imagery that sounds vivid but no longer follows the source.
  症状：译文意象混用、物理逻辑互撞，或新增了好看但原文没有支撑的比喻。
- Find by: Reviewing high-image passages, chapter openings/endings, emotional turns, and any phrase whose appeal depends on an added object, sound, motion, or psychology.
  发现方式：检查高画面段、开头结尾、情绪转折，以及任何魅力依赖新增物体、声音、动作或心理判断的表达。
- Fix by: Preserve the source effect rather than the source surface; remove unsupported added imagery and choose a target-language image grounded in source sensation, action, spatial relation, or symbol.
  修复方式：保留原文效果，不机械保留表面；删除无依据新增意象，改用扎根于原文体感、动作、空间关系或象征功能的目标语表达。
- Recheck: Ask whether the sentence remains vivid after every unsupported image is removed.
  复查：删除无依据意象后，句子是否仍然有画面；若全靠新增意象才好看，说明需要重译。

### Enumerative Punctuation Drag / 排比标点拖拽

- Symptom: Source commas, semicolons, dashes, or list rhythm are mechanically mapped into target-language punctuation, producing stiff rows of clauses.
  症状：把原文逗号、分号、破折号或列举节奏机械搬进目标语，形成僵硬的并列从句队列。
- Find by: Scanning for repeated semicolons, dash chains, parallel clauses with no rhetorical payoff, or chapter titles that preserve printed table-of-contents punctuation.
  发现方式：扫描重复分号、破折号链、没有修辞收益的排比从句，以及保留纸书目录标点的章节标题。
- Fix by: Convert lists into natural target-language hierarchy: sentence groups, short clauses, run-in explanations, subtitles, or true tables when needed.
  修复方式：按目标语习惯重组层级：句群、短分句、段内说明、副标题，必要时改为真实表格。
- Recheck: Confirm the punctuation now reflects target-language reading logic, not source punctuation inertia.
  复查：确认标点服务目标语阅读逻辑，而不是原文标点惯性。
- zh-Hans hard-gate note: In Simplified Chinese publication text, semicolons are rare. Audit them with `rg "；"` across `chapters/final/`, `frontmatter/`, and `metadata/`; most hits should be rewritten as sentence breaks, commas, or re-layered clauses unless there is a true high-level parallel structure.
  简体中文硬门禁补记：出版级简体中文里，分号应极少出现。先用 `rg "；"` 扫描 `chapters/final/`、`frontmatter/` 和 `metadata/`；除非确有高层并列关系，否则大多数命中都应改写为断句、逗号或重组层级。

### Standalone Quote Lost Source Interface / 独立引句丢失原文接口

- Symptom: In books that analyze dialogue, rhetoric, or famous literary/cinematic lines, the translation keeps only the Chinese rendering of a standalone quote block, so readers cannot inspect the source wording that is itself under discussion.
  症状：在讨论对白、修辞或经典台词的书里，独立引句块只保留中文译文，不给原文接口，导致读者无法直接核对正被分析的原句声调与措辞。
- Find by: Scan for standalone quotation blocks, attribution lines, repeated em-dash quote attributions, or isolated dialogue examples first with `rg`, then verify against nearby source context. Focus on canonical lines, famous citations, and analyzed dialogue snippets, not ordinary prose paragraphs.
  发现方式：先用 `rg` 扫描独立引句块、署名行、反复出现的破折号式引句归属或孤立台词示例，再对照邻近原文复核。重点看经典名句、著名引文和被分析的台词片段，不要把普通正文都拉进来。
- Fix by: Pair the original source line or short passage with the translation in reader-visible order, usually original first and translation second. Keep the bilingual pairing limited to places where the exact wording matters to the argument; do not bloat ordinary narrative prose into parallel text.
  修复方式：把原句或短原段与译文成对呈现，通常原文在前、译文在后。双语配对只用于“原句措辞本身就是论证对象”的位置，不要把普通叙述正文膨胀成对照文本。
- Recheck: Confirm that every added source line serves a reader-facing analytical purpose, that the translation remains primary for continuous reading, and that the chapter has not drifted into indiscriminate bilingual duplication.
  复查：确认新增原文都服务于读者可见的分析目的，译文仍然是连续阅读的主文本，章节没有滑向无差别双语堆叠。

### Unclear Pronoun Reference / 代词指代不清

- Symptom: A pronoun, demonstrative, or ellipsis that was clear in the source becomes ambiguous after translation, especially in dialogue, multi-character scenes, legal argument, or technical explanation.
  症状：原文清楚的代词、指示词或省略，在译文中变得含混；常见于对话、多人物场景、法律论证和技术说明。
- Find by: Reading only the translated paragraph and asking who/what each pronoun points to; then compare with the source chain.
  发现方式：只读译文段落，逐个确认“他/她/它/这/那”指向谁或什么，再对照原文链条。
- Fix by: Replace selected pronouns with names, roles, objects, or repeated terms when Chinese clarity requires it; avoid over-repetition that damages style.
  修复方式：中文清晰度需要时，把部分代词换成人名、身份、物体或术语；同时避免重复过密损伤文风。
- Recheck: Confirm that a reader unfamiliar with the source can follow the relation without guessing.
  复查：确认没读过原文的读者也能不猜测地跟上关系。

### Source-Syntax Residue / 源语句法残留

- Symptom: The target text is understandable but still follows source clause order, modifier stacking, passive structure, or abstract noun scaffolding.
  症状：译文能懂，但仍保留源语从句顺序、修饰堆叠、被动结构或抽象名词支架。
- Find by: Chinese-only reading, long-sentence breath checks, and source comparison for clauses that could be reordered without changing meaning.
  发现方式：中文独立阅读、长句换气检查，并对照原文找出可重排而不改义的从句。
- Fix by: Reorder information for target-language comprehension while preserving facts, emphasis, causality, and narrative viewpoint.
  修复方式：按目标语理解顺序重排信息，同时保留事实、重心、因果和叙述视角。
- Recheck: Verify the revised sentence no longer sounds translated, and that no source relation was lost.
  复查：确认修订句不再像翻译腔，同时没有丢失原文关系。

### Over-Explanation and Invented Motive / 过度解释或加戏

- Symptom: The translation explains what the source leaves implicit, supplies motives, modernizes attitudes, or adds emotional judgment not present in the source.
  症状：译文解释了原文留白，补动机，现代化人物态度，或添加原文没有的情绪判断。
- Find by: Comparing explanatory phrases, psychological verbs, moral labels, and added causal connectors against the source.
  发现方式：把解释性短语、心理动词、道德标签和新增因果连接逐项对照原文。
- Fix by: Move necessary reader help into a short note when there is real misunderstanding risk; otherwise remove the addition and let the source ambiguity stand.
  修复方式：确有误读风险时，把必要帮助移入克制短注；否则删除新增解释，保留原文暧昧或留白。
- Recheck: Ask whether the passage now lets readers infer at the same distance intended by the source.
  复查：确认读者推断距离与原文一致。

### Terminology Drift Under Readability Pressure / 顺读压力下的术语漂移

- Symptom: A translator varies terms for smoother prose, but the variation changes a concept, institution, case name, identity, ship, place, or fictional science item.
  症状：为了顺读变换术语，却改变了概念、制度、案例名、身份、船名、地名或虚构科学设定。
- Find by: `glossary/terms.csv`, `display_policy`, `forbidden_body_renderings`, source-term scans, and chapter control terminology tables.
  发现方式：检查 `glossary/terms.csv`、`display_policy`、`forbidden_body_renderings`、源语词扫描和章节控制术语表。
- Fix by: Mark terms as `locked`, `preferred`, or context-variable; keep locked terms stable and document allowed variants.
  修复方式：区分 `locked`、`preferred` 或可随上下文变化的术语；锁定术语必须稳定，允许变体必须记录。
- Recheck: Scan final chapters and generated XHTML for forbidden body renderings and unauthorized source-term parentheses.
  复查：扫描终稿章节和生成 XHTML，查禁用写法和未授权原词括注。

### Title and Subtitle Overload / 标题与小标题超载

- Symptom: The translation preserves source title chains, original names, parenthetical source terms, or explanatory subtitles in headings where target-language title design should stand alone.
  症状：标题保留原文长链、原名、括注原词或解释性副题，而目标语标题本应独立成立。
- Find by: Reviewing `nav.xhtml`, title maps, chapter headings, subtitles, and mobile wrapping risk.
  发现方式：检查 `nav.xhtml`、标题映射、章题、副题和手机换行风险。
- Fix by: Separate `nav_title`, `display_title`, `subtitle`, and optional `title_note`; put source names or first-mention notes in the first natural body occurrence, not the heading.
  修复方式：拆分 `nav_title`、`display_title`、`subtitle` 和可选 `title_note`；原名或首次出现注释放正文第一次自然出现处，不塞进标题。
- Recheck: Confirm headings carry structure and tone, not terminology explanations.
  复查：确认标题承载结构和声调，而不是术语解释。

## Retrospective Hook / 复盘要求

When a concrete book discovers a new quality family, write the immediate evidence in that book's `retrospective_lessons.md`, `qa/chapter_controls/`, or `reviews/random_spotcheck/round_XXX/fixes/fix_log.md`, then backfill the reusable lesson here.
具体书发现新的质量问题族时，先把即时证据写入该书的 `retrospective_lessons.md`、`qa/chapter_controls/` 或 `reviews/random_spotcheck/round_XXX/fixes/fix_log.md`，再把可复用经验回填到本 skill。

Backfill only the general lesson: how to find it, how to classify it, how to audit similar cases, how to fix it, and how to recheck it.
回填只写通用经验：如何发现、如何归纳、如何审计同类、如何修复、如何复查。

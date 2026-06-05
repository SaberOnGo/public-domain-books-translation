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
   This is mandatory in the same round as the fix: do not postpone skill backfill to a final summary, because later agents will otherwise rediscover the same family.
   必须在同一轮修复中完成 skill 回填：不要拖到最终总结，否则后续 agent 会反复重新发现同一问题族。
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

## Validator Fields / 校验字段

For random spot-check rounds, book-local evidence belongs in `reviews/random_spotcheck/round_XXX/fixes/fix_log.md` and `verification/closure_check.md`, but reusable translation-quality lessons must be merged here in the same round. The pass validator checks this through machine-readable fields.
随机抽检轮次中，书内证据写入 `reviews/random_spotcheck/round_XXX/fixes/fix_log.md` 和 `verification/closure_check.md`，但可复用译文质量经验必须在同一轮合并回填到本 skill。强校验会通过机器可读字段检查这件事。

When a round found translation-quality defect families, set:
发现译文质量问题族时，必须填写：

```text
defect_family_count: {total_family_count}
translation_quality_defect_family_count: {quality_family_count}
translation_quality_skill_backfill: "UPDATED" # or "MERGED"
translation_quality_skill_backfill_path: "skills/translation-quality-defect-families/SKILL.md"
translation_quality_skill_backfill_summary: "{what was added or merged: finding method, classification, low-token audit, fix pattern, recheck}"
```

And in `closure_check.md`:
并在 `closure_check.md` 写入：

```text
translation_quality_skill_backfill_verified: true
```

If the round found only format, asset, path, EPUB structure, or other non-translation-quality issues, set `translation_quality_defect_family_count: 0`, `translation_quality_skill_backfill: "NOT_APPLICABLE"`, and write a concrete `translation_quality_skill_backfill_not_applicable_reason`.
如果该轮只有格式、资产、路径、EPUB 结构或其他非译文质量问题，应写 `translation_quality_defect_family_count: 0`、`translation_quality_skill_backfill: "NOT_APPLICABLE"`，并填写具体的 `translation_quality_skill_backfill_not_applicable_reason`。

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
- Craft-analysis direction guard: When a source spatial word is metaphorical or evaluative, do not turn it into a concrete room, body, or route unless the scene is literally spatial. For example, `takes them to the basement` in a value descent should be `带到谷底` or `跌到最底层`, not `带到地下室`.
  写作分析方位防护：源语空间词若承担比喻或评价功能，不要把它译成真实房间、身体或路线，除非场景确实在写空间动作。例如价值下坠中的 `takes them to the basement` 应译为“带到谷底”或“跌到最底层”，不能写成“带到地下室”。
- Dialogue/craft-book guard: Do not intensify light source metaphors, compressed image syntax, or idioms into new physical, medical, or sound effects. `flaws fester in the subtext` should not become `缺陷在潜台词中化脓`; `dribbling basketball` should not add clock sounds such as `滴答乱响`; `fire off words` should normally become `说出狠话` or another speech action, not `发射词语`; a compressed image sequence such as `her shadow slashed rope furled sails...` should not become a false action like `影子划开缆绳`.
  对白/技法书防护：不要把原文轻比喻、压缩意象句法或惯用表达强化成新的物理、病理或声音效果。`flaws fester in the subtext` 不应译成“缺陷在潜台词中化脓”；`dribbling basketball` 不应新增“滴答乱响”这类钟表声；`fire off words` 通常应处理成“说出狠话”等话语行动，不要写成“发射词语”；`her shadow slashed rope furled sails...` 这类压缩意象序列，不应误析成“影子划开缆绳”这类虚假动作。
- Low-token audit: Search for abstract nouns near hard physical or medical verbs, and for known round-derived image collisions: `rg -n "(潜台词|缺陷|对白|词语|感知|意识|心智|内容|痛苦|反讽|兴趣).{0,12}(化脓|发射|固着|沉入|贴合|冲刷|啃噬|钉入|拖|拉|推|撞)|滴答乱响.*篮球|发射出.*词语|贴合耳朵|影子.*划开|划开.*缆绳|卷起的帆|带到地下室|slashed rope|furled sails|takes them to the basement" chapters/final chapters/translated output/epub_work/EPUB`.
  低 token 审计：扫描抽象名词附近的硬物理/病理动词，以及已由轮次发现的意象自撞：`rg -n "(潜台词|缺陷|对白|词语|感知|意识|心智|内容|痛苦|反讽|兴趣).{0,12}(化脓|发射|固着|沉入|贴合|冲刷|啃噬|钉入|拖|拉|推|撞)|滴答乱响.*篮球|发射出.*词语|贴合耳朵|影子.*划开|划开.*缆绳|卷起的帆|带到地下室|slashed rope|furled sails|takes them to the basement" chapters/final chapters/translated output/epub_work/EPUB`。
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
- Paper-like ordinal guard: In reader-facing prose, paragraph-opening `第一，第二，第三` often reads like a paper outline rather than a book. Keep explicit numbering only for true step lists, tables, notes, legal/scientific hierarchy, or places where the source argument depends on numbered order. In ordinary explanatory prose, recast as natural transitions (`先看...`, `再看...`, `最后...`) or topic leads (`形容词。`, `背景故事。`).
  论文式序号防护：面向读者的正文里，段首 `第一，第二，第三` 很容易读成论文提纲，而不是一本书。只有真正的步骤清单、表格、注释、法律/科学层级，或原文论证依赖编号顺序时才保留显性编号。普通解释性正文应改成自然过渡（如“先看……”“再看……”“最后……”）或主题句（如“形容词。”“背景故事。”）。
- Low-token audit: For zh-Hans prose, scan paragraph starts with `rg -n "^(第一|第二|第三|第四|第五|第六|第七|第八|第九|第十)[，、]" chapters/final chapters/translated output/epub_work/EPUB`, then classify notes/true step lists as exceptions and rewrite confirmed body-prose hits.
  低 token 审计：简体中文正文可先扫段首序号：`rg -n "^(第一|第二|第三|第四|第五|第六|第七|第八|第九|第十)[，、]" chapters/final chapters/translated output/epub_work/EPUB`，再把注释/真实步骤清单列为例外，确认正文提纲腔后改写。

### Standalone Quote Lost Source Interface / 独立引句丢失原文接口

- Symptom: In books that analyze dialogue, rhetoric, or famous literary/cinematic lines, the translation keeps only the Chinese rendering of a standalone quote block, so readers cannot inspect the source wording that is itself under discussion.
  症状：在讨论对白、修辞或经典台词的书里，独立引句块只保留中文译文，不给原文接口，导致读者无法直接核对正被分析的原句声调与措辞。
- Find by: Scan for standalone quotation blocks, attribution lines, repeated em-dash quote attributions, or isolated dialogue examples first with `rg`, then verify against nearby source context. Focus on canonical lines, famous citations, and analyzed dialogue snippets, not ordinary prose paragraphs.
  发现方式：先用 `rg` 扫描独立引句块、署名行、反复出现的破折号式引句归属或孤立台词示例，再对照邻近原文复核。重点看经典名句、著名引文和被分析的台词片段，不要把普通正文都拉进来。
- Fix by: Pair the original source line or short passage with the translation in reader-visible order, usually original first and translation second. Keep the bilingual pairing limited to places where the exact wording matters to the argument; do not bloat ordinary narrative prose into parallel text.
  修复方式：把原句或短原段与译文成对呈现，通常原文在前、译文在后。双语配对只用于“原句措辞本身就是论证对象”的位置，不要把普通叙述正文膨胀成对照文本。
- Retention boundary: Do not keep source text merely because it is dialogue. Ordinary scene transcripts, greetings, filler, and plot-functional lines should normally be translated into the target language only. Keep the source line only when it is a famous/canonical quotation, a named literary/cinematic line whose wording is being analyzed, or the local argument depends on source-language form, sound, word length, pun, or syntax.
  保留边界：不要因为它是对白就自动保留源文。普通场景转写、寒暄、填充语和只推动情节的台词，通常应只给目标语译文。只有名言/经典引文、明确被分析措辞的文学/影视台词，或局部论证依赖源语词形、声韵、词长、双关、句法时，才保留源句。
- Ordinary-dialogue block guard: Even when a craft paragraph briefly needs the source wording to discuss word length, repetition, or cadence, do not promote ordinary fragmentary dialogue into standalone bilingual quote blocks. Prefer target-language prose, or a minimal inline source cue such as a single word being analyzed; reserve full source block plus target block for canonical quotes or passages whose exact wording is the reader-facing evidence.
  普通对白块防护：即使技法段落需要短暂提到源语措辞来说明词长、重复或节奏，也不要把普通碎对白提升成独立双语引文块。优先使用目标语正文，或只保留正在分析的最小内联源语提示；完整“源语块在前、目标语块在后”只用于经典引文，或精确措辞本身就是读者可见证据的段落。
- Recheck: Confirm that every added source line serves a reader-facing analytical purpose, that the translation remains primary for continuous reading, and that the chapter has not drifted into indiscriminate bilingual duplication.
  复查：确认新增原文都服务于读者可见的分析目的，译文仍然是连续阅读的主文本，章节没有滑向无差别双语堆叠。
- False-positive guard: In quote-analysis books, do not classify a visible English (or other source-language) line as `untranslated residue` if it is immediately paired with a translation and the pair is clearly functioning as a reader-facing quote interface. Audit only lines that remain source-language-only with no translated partner, or quote pairs whose presentation prevents normal reading.
  误判防护：在引句分析型书中，如果一条可见英文（或其他源语）句子紧跟译文成对出现，并且明显承担读者可见的“原句接口”功能，就不要把它误判为 `untranslated residue`。真正要审计的是只有源语、没有译文配对的残留，或虽成对出现但呈现方式已经妨碍正常阅读的引句块。
- Rendering guard: When a source quote is authored with Markdown blockquote syntax, inspect the generated EPUB XHTML as well as the source Markdown. Literal `>` / `&gt;` markers, collapsed verse lines, or source quote lines joined into one paragraph are reader-facing quote-interface defects even if the translation itself is correct.
  渲染防护：如果原文引句用 Markdown blockquote 写法保留，必须同时检查生成后的 EPUB XHTML。若 `>` / `&gt;` 原样进入读者正文、诗行被压成一段，或原句行序被错误拼接，即使译文内容正确，也属于读者可见的引句接口缺陷。
- Quote-punctuation guard: When a colon introduces a standalone or long quoted passage, scan the reader-facing unit for orphan opening/closing Chinese quote marks. A closing `”` without a corresponding visible opening `“` is a quote-interface defect, unless it is a documented multi-line quote whose opening mark appears in the same continuous quoted block.
  引号标点防护：冒号引出独立引文或长引文时，要扫描读者可见单元里是否有孤立开/闭中文引号。只有闭引号 `”` 而没有对应开引号 `“`，属于引文接口缺陷；除非它是有记录的多行引文，开引号位于同一连续引文块的前文。
- Audit-unit guard: If a source quote or dialogue line is intentionally retained, keep its target-language translation immediately adjacent in normal reader-facing book layout. Do not solve sampling convenience by adding QA labels such as `原文：` / `译文：`, by joining languages with `/`, or by forcing bilingual material into one paragraph. The publishable layout is source paragraph/line first, target paragraph/line second, with the same paragraph structure on both sides when practical.
  审计单元防护：如果有意保留原文引句或对白，必须让目标语译文在正常读者版式中紧邻出现。不能为了抽样方便，在正文加入 `原文：` / `译文：` 这类 QA 标签，不能用 `/` 把两种语言串接，也不能强行把双语内容压进同一段。可出版版式应是源语段/行在前，目标语段/行在后；可行时两边保持相同的段落结构。
- Verse/dialogue layout guard: For verse, famous lines, and short analyzed dialogue, preserve the line/paragraph rhythm. If an English line is its own paragraph, the corresponding Chinese line should also be its own paragraph. Do not collapse verse into comma-separated prose, do not use Markdown `>` as the only structure, and do not leave literal `>` / `&gt;` markers in the generated EPUB.
  诗行/台词版式防护：诗行、名句和短被分析台词，要保留行/段节奏。英文若独立成段，对应中文也应独立成段。不要把诗行压成逗号串接的散文，不要只靠 Markdown `>` 表示结构，更不能让 `>` / `&gt;` 裸标记进入生成后的 EPUB。
- Complete-block guard: If several source lines together form one complete quoted unit, especially verse or a multi-line literary speech, present the complete source block first, then the complete target block. Do not interleave English line, Chinese line, English line, Chinese line unless the source itself is designed as alternating bilingual text. Preserve the source line breaks inside the source block and mirror them in the target block when practical.
  完整引文块防护：如果多行源语合起来才构成一个完整引文单元，尤其是诗段或多行文学台词，应先呈现完整源语块，再呈现完整目标语块。不要排成英文一行、中文一行、英文一行、中文一行的交错格式，除非原文自身就是交替双语文本。源语块内部保留原行分隔；可行时目标语块也对应保留行分隔。
- Consistency guard: If the same famous or analyzed line appears more than once, the target rendering must remain consistent unless the local context explicitly justifies a variant. A later occurrence of a line such as `Of all the gin joints...` must not become a syntactically incomplete variant like `走进了我的` when an earlier reader-facing quote already has a complete rendering.
  一致性防护：同一句名句或被分析台词多次出现时，译法应保持一致；除非局部上下文明示需要变体。像 `Of all the gin joints...` 这样的后续引文，不应在前文已有完整译法时变成“走进了我的”这类句法残缺变体。
- Source-form argument guard: If the source argument depends on spelling, initials, rhyme, word shape, pun, portmanteau formation, or an alphabet-constrained list, keep the source-language form in the same reader-facing unit with target-language glosses. A translated-only list can make the explanation incoherent, for example saying "phrases that begin with ba" while showing only Chinese idioms that do not begin with `ba`; a portmanteau like `narcisstick` should not become an opaque target-language coinage without the source form and morphology being visible after the target gloss.
  源语形式论证防护：如果原文论证依赖拼写、首字母、押韵、词形、双关、混成构词或按字母筛选的列表，必须在同一读者可见单元保留源语形式并配目标语释义。只给中文意译会让解释断裂，例如正文说“以 ba 开头的短语”，但列表里只有并不以 `ba` 开头的中文惯用语；像 `narcisstick` 这样的混成词，也不能只造一个中文生词，必须在目标语释义后保留源词和构词说明。
- Source-prosody argument guard: If the argument depends on source-language syllable count, word length, repeated source words, cadence, rhythm, alliteration, assonance, consonance, meter, or word counts, do not leave only the target-language line as evidence. Either keep the analyzed source line with its translation in the same reader-facing unit, or explicitly say the count/claim is "in the source/English line" when the evidence spans a long scene. A sentence such as "squeezes vast content into the fewest, simplest monosyllables" must not point only to Chinese dialogue that is not monosyllabic. If the source repeats one word such as `okay` five times, do not present several target-language variants as if they were the repeated evidence; name the source word and explain the target variants separately.
  源语声韵论证防护：如果论证依赖源语音节数、词长、同一源词反复、语势、节奏、头韵、谐元音、辅音重复、格律或词数统计，不要只给目标语台词作证据。应在同一读者可见单元保留被分析的源语台词并配译文；若证据跨越长场景，至少明确写出“按英文原文/源文统计”。例如正文说“把巨大内容压缩进最少、最简单的单音节词”时，不能只列并非单音节的中文译句。若原文反复的是 `okay` 这类同一个源词，不要把几个中文变体写成被重复的证据；应点明源词，再另行解释中文按语境如何处理。
- Source-prosody quote-block guard: If a literary quote is itself the evidence for tongue position, phoneme, stress, or alliteration, a meta note saying the analysis is "about the English" is not enough. Show the complete source quote block first, then the complete target block. Do not make the translated line carry source phonetic evidence it cannot carry.
  源语声韵引文块防护：如果文学引文正是舌位、音素、重音或头韵分析的证据，只补一句“分析针对英文”并不够。必须先给完整源语引文块，再给完整目标语译文块；不要让中文译句承担它无法承担的源语发音证据。
- Low-token audit: Collect English-only reader units with a paragraph scanner or `rg`, then inspect only those candidates and nearby translations. A practical rule is: any paragraph with Latin letters above a small threshold and zero CJK should either be metadata/code, a justified source-only exception, or be merged with its translation in the same paragraph/audit unit.
  低 token 审计：用段落扫描脚本或 `rg` 收集英文-only 读者单元，再只检查这些候选及邻近译文。实用规则是：任何拉丁字母超过少量阈值且没有 CJK 的段落，要么是 metadata/code，要么是有记录的 source-only 合理例外，要么必须与译文合并进同一段落/审计单元。
- Low-token audit: To catch over-retained ordinary dialogue, scan English-only lines and scene-transcript triggers before agent review: `rg -n "^[A-Za-z].*$|^… [A-Za-z].*$|^—[A-Za-z].*$|Hello\\.|Hi\\.|Anthony\\.|A friend of mine|Tickets|Bermuda|Elbow Beach|I turn down|Say, don.t you feel|I don.t see the point" chapters/final chapters/translated output/epub_work/EPUB`, then classify each hit as famous/analyzed source interface, ordinary dialogue to translate-only, metadata/name clutter, or code/source-form analysis. Greetings, filler, and ordinary plot-functional script fragments are confirmed defects if they remain bilingual merely because they are dialogue; source retention is justified only by fame/canonicity or a local argument about source wording, sound, length, pun, syntax, or form. Do not ask an agent to reread the whole book before this candidate pass.
  低 token 审计：追查普通对白源文过度保留时，先扫英文-only 行和场景转写触发式：`rg -n "^[A-Za-z].*$|^… [A-Za-z].*$|^—[A-Za-z].*$|Hello\\.|Hi\\.|Anthony\\.|A friend of mine|Tickets|Bermuda|Elbow Beach|I turn down|Say, don.t you feel|I don.t see the point" chapters/final chapters/translated output/epub_work/EPUB`，再把命中分为名句/被分析源语接口、应只译中文的普通对白、metadata/人名杂音、代码/源语形式分析。寒暄、填充语和普通推动情节的剧本碎片，若只是因为“它是对白”而保留双语，就是确认缺陷；只有名句/经典性，或局部论证依赖源语措辞、声韵、词长、双关、句法、形式时才保留源文。不要在候选收集前让 agent 盲读全书。
- Low-token audit: Add a quote-layout scan over final Markdown and generated XHTML for reader-visible QA labels and joiners: `rg -n "原文：|译文：| / 译文：|> >|&gt; &gt;|^> " chapters/final chapters/translated output/epub_work/EPUB`. Then inspect only the candidate quote units against nearby source and target text, distinguishing normal adjacent bilingual paragraphs from label leakage.
  低 token 审计：对终稿 Markdown 和生成 XHTML 追加引文版式扫描，查读者可见 QA 标签和拼接符：`rg -n "原文：|译文：| / 译文：|> >|&gt; &gt;|^> " chapters/final chapters/translated output/epub_work/EPUB`。随后只把候选引文单元与邻近源文/译文对照，区分正常相邻双语段落和标签泄漏。
- Low-token audit: For complete-block layout, scan repeated famous-line triggers first instead of rereading the whole book: `rg -n "Tomorrow and tomorrow|Creeps in|To the last syllable|And all our yesterdays|The way to dusty death|Towards thee|to the last I grapple|from hell|for hate|Of all the gin joints|Not that there|It was the best|I am an invisible man|Why, man|Well, I’m sure|taking a break|he’s working" chapters/final chapters/translated`. Then inspect nearby paragraphs and classify each as complete source block, complete target block, inline explanatory gloss, or reasonable exception.
  低 token 审计：完整引文块版式不要盲读全书，先扫重复名句触发式：`rg -n "Tomorrow and tomorrow|Creeps in|To the last syllable|And all our yesterdays|The way to dusty death|Towards thee|to the last I grapple|from hell|for hate|Of all the gin joints|Not that there|It was the best|I am an invisible man|Why, man|Well, I’m sure|taking a break|he’s working" chapters/final chapters/translated`。随后只检查邻近段落，把候选分为完整源语块、完整目标语块、正文内短释义或合理例外。
- Low-token audit: Add repeated famous-line scans such as `rg -n "gin joints|她偏偏走进|走进了我的|走进了我这一间|Tomorrow and tomorrow|尘土之死|Towards thee|Not that there" chapters/final chapters/translated output/epub_work/EPUB`, then compare only repeated quote units and documented variants.
  低 token 审计：追加同一名句重复扫描，例如 `rg -n "gin joints|她偏偏走进|走进了我的|走进了我这一间|Tomorrow and tomorrow|尘土之死|Towards thee|Not that there" chapters/final chapters/translated output/epub_work/EPUB`，再只复核重复引文单元和有记录的变体。
- Low-token audit: Add source-prosody scans such as `rg -n "单音节|多音节|双音节|三音节|四音节|词数|有声词语|英文原文统计|英文台词|英文短语|同一个词|重复.*(okay|行吗|好吗|没关系)|押韵|头韵|谐元音|节奏|monosyll|polysyll|syllable|word count|alliteration|assonance|consonance|cadence|rhythm|meter" chapters/src chapters/final chapters/translated output/epub_work/EPUB`; then inspect only candidates where the reader-visible evidence is translated-only, where source/translation are crammed into inline parentheses, or where target variants replace a repeated source token.
  低 token 审计：追加源语声韵扫描，例如 `rg -n "单音节|多音节|双音节|三音节|四音节|词数|有声词语|英文原文统计|英文台词|英文短语|同一个词|重复.*(okay|行吗|好吗|没关系)|押韵|头韵|谐元音|节奏|monosyll|polysyll|syllable|word count|alliteration|assonance|consonance|cadence|rhythm|meter" chapters/src chapters/final chapters/translated output/epub_work/EPUB`；随后只复核读者可见证据是译文-only、源文/译文被塞进括注混排、或目标语变体替代同一源词反复证据的候选。

### Reader-Facing Note Marker Leak / 读者可见注号裸露

- Symptom: Chapter body text exposes raw trailing digits or source-authoring note markers instead of a readable note interface, so random-sample review catches naked `3` / `9` endings or similar residue in reader-facing text.
  症状：章节正文把尾随数字或源稿注号原样暴露出来，没有形成可读的注释接口，于是随机抽检会抓到裸露的 `3` / `9` 之类尾注残留。
- Find by: Run `rg` or equivalent scans over `chapters/final/` for sentence-final digits, then compare with note inventory and built XHTML. Check whether the source markdown itself is readable, not only whether the EPUB builder later repairs it.
  发现方式：先对 `chapters/final/` 用 `rg` 或等效扫描找句末数字，再对照注释清单和生成 XHTML。不要只看 EPUB 构建后有没有自动补好，还要检查源 markdown 本身是否可读。
- Low-token audit: Start with `rg -n "。\\d+\\s|，\\d+\\s|？\\d+\\s|！\\d+\\s|[\\u4e00-\\u9fff]\\d+\\s" chapters/final chapters/translated`, then classify hits as note markers, dates, years, measurements, list numbering, or notes-section entries before editing.
  低 token 审计：先用 `rg -n "。\\d+\\s|，\\d+\\s|？\\d+\\s|！\\d+\\s|[\\u4e00-\\u9fff]\\d+\\s" chapters/final chapters/translated` 收集候选，再把命中区分为注号、日期、年份、计量、列表编号或 notes 章节条目，确认后再编辑。
- Fix by: Replace raw note digits with a controlled note-marker convention recognized by the build pipeline. If random samples or chapter controls treat source Markdown as reader-facing audit units, do not store production noteref markers in `chapters/final/`; put the injection locations in a non-reader-facing metadata map or equivalent build layer, let the EPUB builder inject noterefs in memory, and keep source Markdown clean. Use a visible note marker only when the review template explicitly accepts it.
  修复方式：把裸数字改成构建流水线识别的受控注号约定。如果随机抽检或章节控制把源 Markdown 当作读者可见审计单元，不要把制作性 noteref 标记写进 `chapters/final/`；应把注号注入位置放入非读者可见的 metadata 映射或等效构建层，由 EPUB 构建器在内存中注入 noteref，并保持源 Markdown 干净。只有评审模板明确接受时，才使用读者可见注号。
- Low-token audit: Search source chapters and built XHTML separately, for example `rg -n "<!--noteref:|〔注|见注|&lt;!--noteref" chapters/final chapters/translated output/epub_work/EPUB`. Source chapters should have zero production markers; generated XHTML should have resolved `<sup epub:type="noteref">` links and no escaped comments.
  低 token 审计：分别扫描源章节和生成 XHTML，例如 `rg -n "<!--noteref:|〔注|见注|&lt;!--noteref" chapters/final chapters/translated output/epub_work/EPUB`。源章节应没有制作标记；生成 XHTML 应呈现已解析的 `<sup epub:type="noteref">` 链接，不能残留转义注释。
- Metadata-map guard: After any body sentence carrying a note is rewritten, run a metadata-map stale-entry diagnostic before rebuilding. Compare the number of intended metadata note markers with generated XHTML `class="noteref"` count; a mismatch means a rewritten sentence no longer matches the map or a source raw digit still lacks a metadata injection point.
  metadata 映射防护：任何带注释的正文句被改写后，重建前必须运行 metadata 映射失效诊断。把 metadata 中预期注号 marker 数与生成 XHTML 的 `class="noteref"` 数量对账；若不一致，说明改写后的句子已无法匹配映射，或仍有源层裸数字缺少注入位置。
- Do not rely on builder fallback: If generated XHTML converts `。1` to a valid noteref but `chapters/final` still shows a naked `1`, the family is still open because random samples and source review are reader-facing audit units.
  不要依赖构建兜底：如果生成 XHTML 已把 `。1` 转成有效 noteref，但 `chapters/final` 仍显示裸 `1`，问题族仍未关闭，因为随机样本和源层复核同样属于读者可见审计单元。
- Recheck: Confirm `chapters/final/` random samples no longer expose raw or visible production note markers, metadata/build-layer injection count matches the intended note inventory, built XHTML renders clickable noterefs, and each note link resolves to the intended note target.
  复查：确认 `chapters/final/` 抽样文本不再暴露裸数字或可见制作注号，metadata/构建层注入数量与预期注释清单一致，生成 XHTML 呈现可点击 noteref，且每个注释链接都落到目标注释。

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
- Special check: Audit dangling contrastive or connective fragments such as isolated "相比之下。", "然而。", or similar source-led hinges. Do not stop at punctuation repair; make sure the comparison or turn has a concrete landing point in the target-language clause.
  特别检查：额外审计被截成残句的转折/连接语，例如孤立的“相比之下。”、“然而。”等源语驱动铰链。不要只修标点，要确认比较或转折关系已经在目标语主句里真正落地。
- Special check: Audit source inserted examples such as "for instance" or "for example" that land mid-clause as awkward target-language fragments, for example "但她不能比如捂住肚子". In Chinese, move the example into a natural means phrase such as "不能通过……之类的动作", "不能以……这种方式", or a full sentence with "比如说".
  特别检查：审计源语插入式例子，例如 "for instance"、"for example" 被硬塞进目标语分句中部，形成“但她不能比如捂住肚子”这类怪句。中文应把例子改成自然手段表达，例如“不能通过……之类的动作”“不能以……这种方式”，或另起完整的“比如说”句式。
- Special check: Audit English balance idioms in craft-analysis prose, especially `throw(s) ... out of balance`, `life is thrown out of balance`, and `put life back in balance`. Do not preserve the source physical verb as `把早晨/生活抛出平衡`; write the target relation directly, such as `打乱了这个早晨的平衡`, `让生活失衡`, `打乱生活平衡`, or `恢复生活平衡`. In the same pass, audit emotional mood labels such as `sour mood`, `tetchy`, and `sullen`; avoid face/body pseudo-literals like `一脸酸气`, and use context-supported Chinese such as `满心不快`, `阴沉烦躁`, `心情不佳`, or a more specific hidden pain/fear explanation.
  特别检查：审计写作分析中的英语平衡习语，尤其是 `throw(s) ... out of balance`、`life is thrown out of balance`、`put life back in balance`。不要把源语物理动词保留成“把早晨/生活抛出平衡”；应直接写目标语关系，例如“打乱了这个早晨的平衡”“让生活失衡”“打乱生活平衡”或“恢复生活平衡”。同轮审计 `sour mood`、`tetchy`、`sullen` 等情绪标签，避免“一脸酸气”这类脸部/身体伪直译，应按上下文写成“满心不快”“阴沉烦躁”“心情不佳”，或更具体的隐秘痛苦/恐惧说明。
- Special check: Audit source category examples where places, cultures, groups, and people are mechanically connected, such as `characters in low-context cultures, such as North America`. In Chinese, make the category relation explicit (`处在北美这类低语境文化中的人物`) and avoid turning `nationalistic backgrounds` into ideology (`民族主义背景`) when the source means national or national-origin backgrounds (`国族背景`).
  特别检查：审计源语分类例子中地点、文化、群体、人物被机械接上的句子，例如 `characters in low-context cultures, such as North America`。中文应显化范畴关系（如“处在北美这类低语境文化中的人物”），且不要把 `nationalistic backgrounds` 误成意识形态“民族主义背景”；若原文指 national / national-origin background，应译为“国族背景”等。
- Special check: Audit English capacity and deictic-purpose frames such as `sensitive enough to see...` and `dedicate their lives to doing exactly that`. In Chinese, do not preserve `足以看见` or `恰恰做这件事` when the clause points to awareness or a prior paradox. Prefer target-language relations such as `足够敏锐，意识到...` or `献给这件逆势而行的事`, after confirming the antecedent in nearby source context.
  特别检查：审计 `sensitive enough to see...`、`dedicate their lives to doing exactly that` 这类英语能力/指代目的结构。中文不要硬保留“足以看见”“恰恰做这件事”；若原文表达意识到后果或回指前文悖论，应按邻近原文确认后改成“足够敏锐，意识到……”或“献给这件逆势而行的事”等目标语关系。
- Special check: Audit abstract moral/legal words such as `misdeeds`, `wrongdoing`, `fault`, `blame`, `guilt`, `sin`, and `offense` for near-shape or wrong-register Chinese choices. A rendering like `错行` for `misdeeds` is a reader-facing word-choice defect; use context-appropriate words such as `过错`, `错事`, `恶行`, `责任`, `罪责`, or `罪` after source-context comparison.
  特别检查：审计 `misdeeds`、`wrongdoing`、`fault`、`blame`、`guilt`、`sin`、`offense` 等抽象道德/法律评价词，防止近形误选或语域误选。把 `misdeeds` 译成“错行”是读者可见错词；应对照上下文改为“过错”“错事”“恶行”“责任”“罪责”“罪”等合适表达。
- Special check: Audit literal body, motion, and position metaphors copied from source-language idioms, such as "glides into sentences", "in the guts", "pushed over the top", or "after interest is lost". These often look vivid in isolation but become stiff or physically odd in Chinese.
  特别检查：审计从源语习语机械搬来的身体、动作和位置隐喻，例如 "glides into sentences"、"in the guts"、"pushed over the top"、"after interest is lost" 一类表达。它们单看似乎有画面，进入中文后常变成生硬或物理感别扭的句子。
- Special check: Audit abstract-force injury metaphors copied as literal bodily harm, such as "suffered the scald of irony" becoming “被反讽烫伤”. In Chinese, preserve the cognitive/emotional effect with expressions like “尝过……的刺痛”, “感到……刺痛”, or another context-supported idiom rather than making irony, desire, truth, or memory physically burn the reader.
  特别检查：审计抽象力量造成身体伤害的硬译，例如把 "suffered the scald of irony" 译成“被反讽烫伤”。中文应保留认知/情绪效果，例如“尝过……的刺痛”“感到……刺痛”或其他有上下文支撑的习惯表达，不要让反讽、欲望、真相、记忆等抽象物在字面上烫伤读者。
- Special check: Audit throat-grab, drag-to-crawl, and concealed-hurt idioms when the source uses body language for rhythm or emotion, such as "the fear of embarrassment grabs them by the throat", "their stride shuffle to a crawl", or "concealing the hurt". Translate the effect as being stuck, slowed, stung, embarrassed, or emotionally hurt instead of importing a literal body-action chain.
  特别检查：审计源语用身体动作表达节奏或情绪的 throat-grab、drag-to-crawl、concealed-hurt 等习语，例如 "the fear of embarrassment grabs them by the throat"、"their stride shuffle to a crawl" 或 "concealing the hurt"。应译出卡住、变慢、刺痛、尴尬或受伤感等效果，不要把字面身体动作链搬进中文。
- Special check: Audit source collocations where an abstract noun, text, camera, language, or relationship is made to pour, deliver, resonate, swallow, impose a tongue, cast someone off, or call/generate danger. Phrases like "characters pour out exposition", "indirect dialogue delivers exposition", "lovers pour out their history", "poured out three pages", "resonance of a brick", "camera ... swallow", "imposing their Germanic tongue", "cast off from their marriages", and "calling on capacities / generating jeopardy" should be converted into natural target-language effects: explain too much at once, provide necessary information, recount a shared past, write at length, sound dull, take into frame, impose a language, feel excluded, force out capacity, or enter danger.
  特别检查：审计源语搭配把抽象名词、文本、摄影机、语言或关系写成倾倒、输送、共鸣、吞食、强加舌头、抛离、召唤/生成危险的句子。遇到 "characters pour out exposition"、"indirect dialogue delivers exposition"、"lovers pour out their history"、"poured out three pages"、"resonance of a brick"、"camera ... swallow"、"imposing their Germanic tongue"、"cast off from their marriages"、"calling on capacities / generating jeopardy" 等，应转成目标语自然效果：一股脑交代信息、交代必要信息、讲述共同过往、写上很长篇幅、听起来钝硬、收入画面、强加语言、被关系排除、逼出能力、进入险境。
- Special check: Audit craft-analysis idioms that look harmless in English but become literal body, camera, or space mechanics in Chinese: "conversation lubricated with alcohol descends", "value has run its course", "wraps the conversation around her little finger", "staring into the back of his head", "genius working up a sweat", "shape the scene to and around its turning point", "shape language in all the contours", or "the camera sees / moves through global storytelling space". Convert them into the target-language relation: alcohol loosens talk, a value has reached its endpoint, a character controls the conversation, someone is trapped in self-absorption, genius comes from hard labor, the scene forms around a turning point, language is shaped at multiple levels, and the camera presents or moves through narrative space.
  特别检查：审计英语里看似普通、进入中文后变成身体/摄影机/空间机械动作的写作分析习语，例如 "conversation lubricated with alcohol descends"、"value has run its course"、"wraps the conversation around her little finger"、"staring into the back of his head"、"genius working up a sweat"、"shape the scene to and around its turning point"、"shape language in all the contours"、"the camera sees / moves through global storytelling space"。应转成目标语关系：酒精让谈话松动、价值走到尽头、人物支配谈话、自我凝视、天才来自艰苦劳动、场景围绕转折点成形、从多个层面塑造语言、镜头呈现或移动于叙事空间。
- Special check: Audit parenthetical source clauses such as `influences, if not controls` when they are mechanically inserted into Chinese as `影响、即使不控制，也会影响`. Rewrite as a natural concessive relation, for example "即便没有完全控制，也影响着...", and remove duplicated verbs caused by source clause order.
  特别检查：审计 `influences, if not controls` 这类英语插入式让步结构，避免机械译成“影响、即使不控制，也会影响”。应改成中文自然让步关系，例如“即便没有完全控制，也影响着……”，并删除由源语语序造成的重复动词。
- Special check: Audit violent state contradictions where the source says someone was harmed while still alive, for example `burned and crucified while they were still alive`. Do not translate the result as "被烧死、钉死...那时还活着"; preserve the simultaneity as "还活着时，就被..." or an equivalent target-language structure.
  特别检查：审计暴力状态逻辑自撞，例如原文说 `burned and crucified while they were still alive`。不要译成“被烧死、钉死……那时还活着”；应保留“还活着时，就被……”这类同时关系。
- Special check: Audit English stage/camera/instruction wording that becomes awkward physical mechanics in Chinese, for example `a scene at a shipyard`, `looked over his shoulder`, `Forcefully utilize a big nail`, `sit back`, or `secret place from the world / teeter through life`. Translate the teaching point or emotional relation directly: a scene set in a shipyard, someone standing behind and watching, hammering a spike in, stepping back, or a private hidden corner and an unsteady life.
  特别检查：审计英语场景/镜头/说明句进入中文后变成别扭物理机械的表达，例如 `a scene at a shipyard`、`looked over his shoulder`、`Forcefully utilize a big nail`、`sit back`、`secret place from the world / teeter through life`。应直接译出教学点或情绪关系：一场设在造船厂的戏、某人站在身后看着、把长钉锤进去、退后一步、躲开世界的隐秘角落与一路踉跄的人生。
- Special check: Audit compact source grammar/history explanations before translating them as Chinese grammar labels or false language-family facts. If `-ing` is being discussed as an English form in a progressive-like phrase, do not call every instance `动名词`; prefer `-ing 形式` or `进行式结构` unless the source clearly means the grammatical gerund. Likewise, do not simplify language-history relations into false claims such as `古德语的一种方言` or `古法语，即拉丁语的一种方言`; write safer source-supported relations such as `古日耳曼语根基` or `拉丁语渊源`.
  特别检查：审计紧凑的源语语法/语言史说明，不要把它们译成误导性的中文语法标签或错误语系事实。若原文讨论的是进行式一类短语中的英语 `-ing` 形式，不要统称为“动名词”；除非原文明确指 grammatical gerund，否则优先写 `-ing 形式` 或 `进行式结构`。同样，不要把语言史关系简化成 `古德语的一种方言`、`古法语，即拉丁语的一种方言` 这类错误事实；可按源文支撑写成 `古日耳曼语根基`、`拉丁语渊源` 等更稳妥关系。
- Special check: Audit craft-analysis verbs that make scenes, values, beats, forces, or abilities perform English analytical motions, such as "arcing the scene around its value changes", "a turning point pivots", "the charge arcs toward the light", "value charge turns dark / shines", "subtextual actions echo each other", "bulldoze through beats", "moral power controls pace", "assemble abilities", or "drop her head on her arms". Prefer direct target-language relations: let values change, turn, brighten, progress along an arc, echo/correspond as actions, press through beats, pull pace back, integrate abilities, or rest/伏 the head on arms. A source term such as "value charge" may be stable in glossary/source-interface layers, but the target body should not mechanically preserve a physics term like `电荷`; use value state, direction, or change unless the local terminology policy explicitly locks a different target term.
  特别检查：审计写作分析段里让场景、价值、节拍、力量或能力执行英语分析动作的动词，例如 "arcing the scene around its value changes"、"a turning point pivots"、"the charge arcs toward the light"、"value charge turns dark / shines"、"subtextual actions echo each other"、"bulldoze through beats"、"moral power controls pace"、"assemble abilities" 或 "drop her head on her arms"。优先改为目标语直接关系：价值发生变化、转向、转亮、沿弧线推进、行动彼此呼应、压过节拍、把节奏拉回、整合能力、把头伏到手臂上。`value charge` 这类源语术语可在术语表/源语接口层稳定，但目标语正文不要机械保留 `电荷` 这类物理词；除非书内术语 policy 明确锁定，否则用价值状态、走向或变化。
- Special check: When a random sample finds craft-analysis physicalization, generalize it immediately to the whole book. High-yield English triggers include "nail the meaning", "nail characterization", "nail each action/reaction", "nails him with the truth/fact", "hammered home", "bend him farther away", "funnel their struggle", "energy explodes into", "charge erodes toward", "fear runs through", "nose is rubbed in it", "fuse burning of danger", "double-fisted punches", "flinches and withers", "rapid-fire exposition", "deliver exposition", "stubs its toe", "takes hold", "turns sharply into irony", "strikes the eyes and ears", "digging deeper into capacities", "dams emotion momentum", "flow toward", "compresses its power", "moral power controls the pace", "lurching out in defeat", "hooks/holds/pays off", "crafting words as an inner action", "confusion stifles creativity", "run its course", "working up a sweat", and "the width of all things Roman". Chinese candidates often contain suspicious pairings such as `钉住意义`, `钉住.*事实`, `事实.*锤`, `锤进耳朵`, `钉住人物塑造`, `精准钉住`, `弯折得更远`, `输送斗争`, `爆发进`, `朝负面侵蚀`, `恐惧在身上奔跑`, `鼻子被按在`, `危险引线燃烧`, `握着真相和道德的双拳`, `退缩并萎缩`, `快速发射信息`, `输送信息交代`, `脚趾撞`, `需求抓住`, `进入.*反讽`, `打进眼睛和耳朵`, `打到观众.*耳朵.*眼睛`, `挖掘.*能力`, `筑坝拦住`, `流向关键变化`, `压缩其力量`, `分量.*拉回`, `失败地冲出去`, `钩住、抓住并兑现`, `勾住兴趣`, `建立兴趣`, `回报兴趣`, `封住讲话`, `打磨成内在行动`, `落实为外在活动`, `混乱压住创造力`, `跑完自己的路程`, `天才.*出汗`, or `宽到一切...的宽度`. Repair by expressing the target relation directly: let a meaning land, force someone into silence, repeat facts until the audience goes numb, establish characterization, precisely express each action/reaction, move farther from a desire object, focus conflict through a third thing, release energy in the climactic beat, weaken/turn negative, fear surges through someone, have the issue shoved in someone's face, danger approaches, truth/morality strike rhetorically, a person loses nerve or withers in force, information is quickly delivered, provide necessary information, story pauses briefly, a need takes over, irony appears/turns, perception receives something, capacities are mobilized, momentum is held, attention concentrates, power intensifies, moral force controls rhythm, someone is defeated, suspense attracts and rewards attention, words carry inner action into outer activity, confusion blocks creativity, a value reaches its endpoint, genius comes from hard labor, or the world extends as far as an empire's reach. For `strikes the eyes and ears`, translate the sensory channel relation as "以声音和图像直接抵达观众"; for `hooks, builds, and pays off interest`, translate the suspense relation as "吸引兴趣、逐步累积、最后给出回报"; for `caps a speech with a metaphor`, use "以隐喻收束讲话".
  特别检查：随机抽检一旦发现写作分析里的抽象概念物理化，要立即归纳为全书问题族追杀。高收益英文触发式包括 "nail the meaning"、"nail characterization"、"nail each action/reaction"、"nails him with the truth/fact"、"hammered home"、"bend him farther away"、"funnel their struggle"、"energy explodes into"、"charge erodes toward"、"fear runs through"、"nose is rubbed in it"、"fuse burning of danger"、"double-fisted punches"、"flinches and withers"、"rapid-fire exposition"、"deliver exposition"、"stubs its toe"、"takes hold"、"turns sharply into irony"、"strikes the eyes and ears"、"digging deeper into capacities"、"dams emotion momentum"、"flow toward"、"compresses its power"、"moral power controls the pace"、"lurching out in defeat"、"hooks/holds/pays off"、"crafting words as an inner action"、"confusion stifles creativity"、"run its course"、"working up a sweat"、"the width of all things Roman"。中文候选常见为 `钉住意义`、`钉住.*事实`、`事实.*锤`、`锤进耳朵`、`钉住人物塑造`、`精准钉住`、`弯折得更远`、`输送斗争`、`爆发进`、`朝负面侵蚀`、`恐惧在身上奔跑`、`鼻子被按在`、`危险引线燃烧`、`握着真相和道德的双拳`、`退缩并萎缩`、`快速发射信息`、`输送信息交代`、`脚趾撞`、`需求抓住`、`进入.*反讽`、`打进眼睛和耳朵`、`打到观众.*耳朵.*眼睛`、`挖掘.*能力`、`筑坝拦住`、`流向关键变化`、`压缩其力量`、`分量.*拉回`、`失败地冲出去`、`钩住、抓住并兑现`、`勾住兴趣`、`建立兴趣`、`回报兴趣`、`封住讲话`、`打磨成内在行动`、`落实为外在活动`、`混乱压住创造力`、`跑完自己的路程`、`天才.*出汗`、`宽到一切...的宽度`。修复时直接写出目标语关系：让意义落定、把人逼到无话可说、反复强调事实直到观众麻木、确立人物塑造、准确落实每个行动/反应、离欲望对象更远、借第三物集中冲突、在高潮节拍中释放、削弱并转向负面、恐惧涌过人物、事情天天怼到脸上、危险迫近、真相/道德形成修辞出击、人物畏缩或气势枯萎、快速交代信息、交代必要信息、故事短暂停顿、需求占据主导、反讽出现/转入、感官接收事物、调动能力、动能被扣住、注意力集中、力量增强、道德力量主导节奏、人物败下阵来、悬念吸引并回报注意力、词语承载内在行动并显于外在活动、混乱妨碍创造力、价值走到尽头、天才源自艰苦劳动、世界延伸到帝国势力所及之处。`strikes the eyes and ears` 应译为“以声音和图像直接抵达观众”这类感官通道关系；`hooks, builds, and pays off interest` 应译为“吸引兴趣、逐步累积、最后给出回报”这类悬念关系；`caps a speech with a metaphor` 应译为“以隐喻收束讲话”。
- Round-derived addendum: Also watch for ordinary English analysis verbs that become unnatural Chinese mechanical actions in samples, including `comes into her head`, `seals meaning`, `let the scene go to work on you`, `voice dialogue as music`, `look into the heart of things`, `mete out exposition`, `draws an analogy ... cuisine`, `speed-building rhythm`, and `character-specific volume of culture`. Suspicious Chinese candidates include `冒进.*脑海`, `封住意义`, `自行落到.*身上`, `把对白发声`, `看进事物`, `未来事件望去`, `分配信息交代`, `一道饮食`, `饮食经验`, `断奏式.*建构速度`, `文化量`, `精准确立`, and `弹成.*跳句`. Prefer target-readable relations such as "闯进/钻进脑海", "收束意义", "让场景对读者发生作用", "用音乐唱出对白", "理解核心并期待后续", "交代信息", "同艺术作品或一道具体菜肴建立类比", "速度逐步加快的节奏", "只属于这个人物的文化积累", "准确勾勒人物形象", and "不合逻辑的跳跃句".
  轮次沉淀补充：还要警惕普通英语分析动词在样本中变成中文机械动作，例如 `comes into her head`、`seals meaning`、`let the scene go to work on you`、`voice dialogue as music`、`look into the heart of things`、`mete out exposition`、`draws an analogy ... cuisine`、`speed-building rhythm`、`character-specific volume of culture`。中文候选包括 `冒进.*脑海`、`封住意义`、`自行落到.*身上`、`把对白发声`、`看进事物`、`未来事件望去`、`分配信息交代`、`一道饮食`、`饮食经验`、`断奏式.*建构速度`、`文化量`、`精准确立`、`弹成.*跳句`。优先改成“闯进/钻进脑海”“收束意义”“让场景对读者发生作用”“用音乐唱出对白”“理解核心并期待后续”“交代信息”“同艺术作品或一道具体菜肴建立类比”“速度逐步加快的节奏”“只属于这个人物的文化积累”“准确勾勒人物形象”“不合逻辑的跳跃句”等目标语关系。
- Round-derived addendum: For craft-analysis books, do not leave analytic relations as literal physics or false technical gauges. Audit `value charge`, `charge`, `exact/specific moment`, `exact words`, `look into`, `eyes and ears`, `grips interest`, `topping/surpassing beats`, `guilt-tripping`, `Docent/Romantic [name]`, `third-person intelligence/voice`, `line design`, `character-specific`, `payoff`, `McMansion`, `fly-by-night`, `glimpse of meaning`, `column of talk`, and line-level sound analysis such as alliteration or `would`. Chinese candidates include `价值电荷`, `正电荷`, `负电荷`, `电荷`, `充电`, `精确时刻`, `精确节拍`, `精确词语`, `看进`, `抓住.*眼睛.*耳朵`, `抓住兴趣`, `超越前一个节拍`, `内疚操控`, `导览者.*凯末尔`, `浪漫主义者.*凯末尔`, `浪漫自我`, `第三人称智能`, `第三人称声音`, `人物特异性`, `人物专属性`, `缩短句行`, `拉长句行`, `爆成笑声`, `麦克豪宅`, `一夜就跑`, `被一瞥意义触发`, `她那一栏话语`, and `助动词进入`. Repair as target-readable teaching language: value state/change/direction, accurate timing/wording, study/read the subtext, attract visual/auditory attention, maintain interest, move one beat further, use guilt as a tactic, choose natural role labels, use narrative consciousness/third-person manner, line/utterance length, turn payoff into laughter, localize cultural idioms, and preserve short source-form interfaces for sound/grammar analysis.
  轮次沉淀补充：写作技法书不要把分析关系留成字面物理动作或伪技术仪表。审计 `value charge`、`charge`、`exact/specific moment`、`exact words`、`look into`、`eyes and ears`、`grips interest`、`topping/surpassing beats`、`guilt-tripping`、`Docent/Romantic [name]`、`third-person intelligence/voice`、`line design`、`character-specific`、`payoff`、`McMansion`、`fly-by-night`、`glimpse of meaning`、`column of talk`，以及头韵、`would` 等逐字音形分析。中文候选包括 `价值电荷`、`正电荷`、`负电荷`、`电荷`、`充电`、`精确时刻`、`精确节拍`、`精确词语`、`看进`、`抓住.*眼睛.*耳朵`、`抓住兴趣`、`超越前一个节拍`、`内疚操控`、`导览者.*凯末尔`、`浪漫主义者.*凯末尔`、`浪漫自我`、`第三人称智能`、`第三人称声音`、`人物特异性`、`人物专属性`、`缩短句行`、`拉长句行`、`爆成笑声`、`麦克豪宅`、`一夜就跑`、`被一瞥意义触发`、`她那一栏话语`、`助动词进入`。修复为目标语教学语言：价值状态/变化/走向、准确时机/词语、研读潜台词、吸引视听注意、维持兴趣、节拍更进一步、把内疚当策略、选择自然角色标签、叙述意识/第三人称口吻、台词长短、把包袱转化为笑声、本地化文化习语，并在音形/语法分析处保留短源语接口。
- Round-derived addendum: When samples reveal source idioms that look ordinary but become false Chinese facts or non-words, immediately audit the whole book for the exact Chinese residue and the nearby source trigger. High-yield triggers include `connects you more to life`, `build toward a loss of identity`, `conscious concern for a secure doctor/patient relationship`, `put him at the scene by name`, `taking a break from my wife`, `forgetting my son's birthday`, `endorse a whiskey`, `racing thoughts`, `mad, ticking clock`, `squeezes vast content`, `value at stake`, and `fixed desires for stability`. Chinese candidates include `更连接生命`, `连接生命`, `建向`, `意识关切`, `安全医患关系`, `按名字把.*放到现场`, `请个假`, `帮我忘掉`, `奔跑念头`, `疯狂滴答作响的钟`, `巨大内容`, `所押注`, `押注在`, `价值电荷`, and `对稳定的固定欲望`. Repair by writing the target relation directly: `更贴近生命`, `逐步走向身份丧失`, `有意识地关心关系是否安全`, `目击者可以指认他在场`, `离开妻子喘口气`, `忘了儿子的生日`, `给威士忌做代言`, `停不下来的念头`, `像一座疯狂滴答作响的钟`, `丰富含义`, `利害攸关的价值`, `价值状态`, and `维持稳定的固定欲望`.
  轮次沉淀补充：抽检一旦发现普通英语习语进入中文后变成虚假事实或不成词，要立刻用精确中文残留和邻近源语触发式全书审计。高收益触发式包括 `connects you more to life`、`build toward a loss of identity`、`conscious concern for a secure doctor/patient relationship`、`put him at the scene by name`、`taking a break from my wife`、`forgetting my son's birthday`、`endorse a whiskey`、`racing thoughts`、`mad, ticking clock`、`squeezes vast content`、`value at stake`、`fixed desires for stability`。中文候选包括 `更连接生命`、`连接生命`、`建向`、`意识关切`、`安全医患关系`、`按名字把.*放到现场`、`请个假`、`帮我忘掉`、`奔跑念头`、`疯狂滴答作响的钟`、`巨大内容`、`所押注`、`押注在`、`价值电荷`、`对稳定的固定欲望`。修复时直接写目标语关系：`更贴近生命`、`逐步走向身份丧失`、`有意识地关心关系是否安全`、`目击者可以指认他在场`、`离开妻子喘口气`、`忘了儿子的生日`、`给威士忌做代言`、`停不下来的念头`、`像一座疯狂滴答作响的钟`、`丰富含义`、`利害攸关的价值`、`价值状态`、`维持稳定的固定欲望`。
- Low-token audit: Search target text for suspicious injury verbs near abstract nouns, for example `rg -n "反讽.{0,8}(烫|灼|烧|刺伤)|被.{0,8}(反讽|欲望|真相|记忆).{0,8}(烫|灼|烧|刺)" chapters/final output/epub_work/EPUB`, then compare only the candidate sentences with nearby source.
  低 token 审计：用抽象名词附近的伤害动词收集候选，例如 `rg -n "反讽.{0,8}(烫|灼|烧|刺伤)|被.{0,8}(反讽|欲望|真相|记忆).{0,8}(烫|灼|烧|刺)" chapters/final output/epub_work/EPUB`，再只把候选句与邻近原文对照。
- Low-token audit: Search for malformed inserted-example residue with `rg -n "不能比如|可以比如|会比如|应比如|要比如|但.{0,8}比如|比如捂住|for instance|for example" chapters/final chapters/translated output/epub_work/EPUB`, then classify hits as ordinary examples, source-only evidence, or confirmed syntax residue.
  低 token 审计：用 `rg -n "不能比如|可以比如|会比如|应比如|要比如|但.{0,8}比如|比如捂住|for instance|for example" chapters/final chapters/translated output/epub_work/EPUB` 搜索插入式例子残留，再区分普通举例、源语证据和确认句法残留。
- Low-token audit: Search for balance-idiom and mood-label residue with `rg -n "抛出平衡|丢出平衡|扔出平衡|甩出平衡|掷出平衡|一脸酸气|酸气|酸溜溜|out of balance|back in balance|sour mood|tetchy|sullen" chapters/src chapters/final chapters/translated output/epub_work/EPUB`, then compare only paired source/final candidates. Treat natural target forms such as `让生活失衡`, `打乱生活平衡`, `恢复生活平衡`, or context-specific hidden pain/fear as reasonable exceptions.
  低 token 审计：用 `rg -n "抛出平衡|丢出平衡|扔出平衡|甩出平衡|掷出平衡|一脸酸气|酸气|酸溜溜|out of balance|back in balance|sour mood|tetchy|sullen" chapters/src chapters/final chapters/translated output/epub_work/EPUB` 搜索平衡习语和情绪标签残留，再只复核源文/终稿成对候选。`让生活失衡`、`打乱生活平衡`、`恢复生活平衡` 或上下文具体化的隐秘痛苦/恐惧可记为合理例外。
- Low-token audit: Search for ordinary idiom residue and craft-term hard literals with `rg -n "更连接生命|连接生命|巨大内容|建向|意识关切|安全医患关系|请个假|帮我忘掉|奔跑念头|疯狂滴答作响的钟|按名字把.*放到现场|所押注|押注在|价值电荷|对稳定的固定欲望" chapters/final chapters/translated output/epub_work/EPUB`, then compare only the candidate paragraph with nearby source. Source-side expansion, if needed: `rg -n "connects you more to life|build toward|conscious concern|put him at the scene by name|taking a break from my wife|forgetting my son|endorse a whiskey|racing thoughts|ticking clock|squeezes vast content|value at stake|fixed desires for stability" chapters/src`.
  低 token 审计：用 `rg -n "更连接生命|连接生命|巨大内容|建向|意识关切|安全医患关系|请个假|帮我忘掉|奔跑念头|疯狂滴答作响的钟|按名字把.*放到现场|所押注|押注在|价值电荷|对稳定的固定欲望" chapters/final chapters/translated output/epub_work/EPUB` 搜索普通习语残留和技法术语硬译，再只复核候选段及邻近原文。必要时用源语扩展式：`rg -n "connects you more to life|build toward|conscious concern|put him at the scene by name|taking a break from my wife|forgetting my son|endorse a whiskey|racing thoughts|ticking clock|squeezes vast content|value at stake|fixed desires for stability" chapters/src`。
- Low-token audit: Add classification and moral-word scans: `rg -n "低语境文化中的人物，例如|民族主义背景|例如北美|文化中的人物|错行|misdeed|wrongdoing|fault|blame|guilt|sin|offense|过错|恶行|错事|罪行|失误|责任" chapters/src chapters/final chapters/translated output/epub_work/EPUB`; then inspect only source/final pairs, because many `责任` or `错误` hits are reasonable exceptions.
  低 token 审计：追加分类句和道德评价词扫描：`rg -n "低语境文化中的人物，例如|民族主义背景|例如北美|文化中的人物|错行|misdeed|wrongdoing|fault|blame|guilt|sin|offense|过错|恶行|错事|罪行|失误|责任" chapters/src chapters/final chapters/translated output/epub_work/EPUB`；随后只复核源文/终稿成对候选，因为大量“责任”或“错误”命中属于合理例外。
- Special check: Audit abstract-force drag/push/pull metaphors, such as "turns sharply into the powerful irony" becoming “被一记更强的反讽拉了回去”. When the source describes a rhetorical turn, value shift, or conceptual relation, translate the turn directly instead of inventing a physical force acting on the sentence or reader.
  特别检查：审计抽象力量拖拽/推动/拉扯类硬译，例如把 "turns sharply into the powerful irony" 译成“被一记更强的反讽拉了回去”。当原文说的是修辞转折、价值转向或概念关系时，应直接译出“转向/急转/进入/形成”，不要让抽象物变成对句子或读者施力的外物。
- Low-token audit: Search target text for abstract nouns near physical force verbs, for example `rg -n "(反讽|真相|答案|兴趣|欲望|痛苦|恐惧|羞辱|冲突|价值|关系).{0,12}(拉|拖|推|拽|扯)|(被|由).{0,12}(反讽|真相|答案|兴趣|欲望|痛苦|恐惧|羞辱|冲突|价值|关系).{0,12}(拉|拖|推|拽|扯)" chapters/final chapters/translated`.
  低 token 审计：扫描抽象名词附近的物理施力动词，例如 `rg -n "(反讽|真相|答案|兴趣|欲望|痛苦|恐惧|羞辱|冲突|价值|关系).{0,12}(拉|拖|推|拽|扯)|(被|由).{0,12}(反讽|真相|答案|兴趣|欲望|痛苦|恐惧|羞辱|冲突|价值|关系).{0,12}(拉|拖|推|拽|扯)" chapters/final chapters/translated`。
- Low-token audit: For craft books, also scan concrete suspect collocations before asking an agent to reread: `rg -n "钉住|精准钉住|弯折|输送.*(斗争|信息|交代)|推动.*穿越|撞上.*真实|宽到|正电荷.*侵蚀|恐惧在.*奔跑|鼻子.*按在|爆发进|潜意识的水流|危险引线|握着.*双拳|退缩并萎缩|快速发射|脚趾撞|需求抓住|进入.*反讽|打进眼睛|挖掘.*能力|筑坝拦住|流向关键变化|压缩其力量|分量.*拉回|失败地冲出去|钩住、抓住并兑现|打磨成内在行动|落实为外在活动|混乱压住创造力|跑完自己的路程|天才.*出汗|酒精润滑|滑向.*真相|绕回自己的小指|后脑勺里面|摄影机看见|穿过整体叙事空间|所有轮廓中塑造|抓住观众的耳朵|冠军取悦|只列出以字母" chapters/final chapters/translated`, then classify each hit as confirmed fix or reasonable exception.
  低 token 审计：写作技法书还应先用具体可疑搭配收集候选，再交给 agent 小上下文复核：`rg -n "钉住|精准钉住|弯折|输送.*(斗争|信息|交代)|推动.*穿越|撞上.*真实|宽到|正电荷.*侵蚀|恐惧在.*奔跑|鼻子.*按在|爆发进|潜意识的水流|危险引线|握着.*双拳|退缩并萎缩|快速发射|脚趾撞|需求抓住|进入.*反讽|打进眼睛|挖掘.*能力|筑坝拦住|流向关键变化|压缩其力量|分量.*拉回|失败地冲出去|钩住、抓住并兑现|打磨成内在行动|落实为外在活动|混乱压住创造力|跑完自己的路程|天才.*出汗|酒精润滑|滑向.*真相|绕回自己的小指|后脑勺里面|摄影机看见|穿过整体叙事空间|所有轮廓中塑造|抓住观众的耳朵|冠军取悦|只列出以字母" chapters/final chapters/translated`，随后把每个命中归类为确认修复或合理例外。
- Low-token audit: Include round-derived source-syntax and grammar/fact residues `rg -n "敏感到足以|足以看见|恰恰做这件事|只是很不同|那是什么，好吗|称呼规范|思索.*之间的性质|从他肩后看过去|有力地使用一枚大钉子|躲避世界的秘密之处|摇摇晃晃地穿过生活|向后坐下|古德语的一种方言|古法语，即拉丁语的一种方言|动名词短语|动名词只给|使用动名词短语" chapters/final chapters/translated output/epub_work/EPUB`, then compare each candidate against nearby source before editing.
  低 token 审计：追加轮次沉淀的源语句法和语法/事实残留扫描：`rg -n "敏感到足以|足以看见|恰恰做这件事|只是很不同|那是什么，好吗|称呼规范|思索.*之间的性质|从他肩后看过去|有力地使用一枚大钉子|躲避世界的秘密之处|摇摇晃晃地穿过生活|向后坐下|古德语的一种方言|古法语，即拉丁语的一种方言|动名词短语|动名词只给|使用动名词短语" chapters/final chapters/translated output/epub_work/EPUB`，每个候选都先对照邻近原文再编辑。
- Low-token audit: Add round-derived hinge/deliver and abstract-collocation residues `rg -n "三部电影都系在|交付这条信息交代|信息交代事实|事实知识充足|狡诈策略|穿越私人生活|母亲所说的话|亚洲式形状|调谐到|现在的刀锋|同故事对抗力量挣扎|被讲出和问出|整体性的感觉|数万款项" chapters/final chapters/translated output/epub_work/EPUB`, then source-expand with `rg -n "hinge on|deliver exposition|story fact|factually informed|devious tactics|navigate his personal life|mother tongue|Asian shape|tuned to|cutting edge of the present|antagonistic forces of story|spoken and asked|feel for the whole|stolen tens of thousands" chapters/src` only for unclear candidates.
  低 token 审计：追加轮次沉淀的 hinge/deliver 和抽象搭配残留扫描：`rg -n "三部电影都系在|交付这条信息交代|信息交代事实|事实知识充足|狡诈策略|穿越私人生活|母亲所说的话|亚洲式形状|调谐到|现在的刀锋|同故事对抗力量挣扎|被讲出和问出|整体性的感觉|数万款项" chapters/final chapters/translated output/epub_work/EPUB`，只对不明确候选再用源语扩展式 `rg -n "hinge on|deliver exposition|story fact|factually informed|devious tactics|navigate his personal life|mother tongue|Asian shape|tuned to|cutting edge of the present|antagonistic forces of story|spoken and asked|feel for the whole|stolen tens of thousands" chapters/src`。
- Low-token audit: After the round-derived addendum above, include `rg -n "弹成|不合逻辑的跳句|断奏式|建构速度|一道饮食|饮食经验|文化量|精准确立|确立.*人物塑造|把对白发声|发声为音乐|看进事物|未来事件望去|分配信息交代|冒进.*脑海|封住意义|自行落到.*身上|落到你身上|终身狂热影响|即使不控制|影响、即使|被烧死、钉死|还活着.*被烧死" chapters/final chapters/translated output/epub_work/EPUB`.
  低 token 审计：对上述轮次沉淀项，还要追加 `rg -n "弹成|不合逻辑的跳句|断奏式|建构速度|一道饮食|饮食经验|文化量|精准确立|确立.*人物塑造|把对白发声|发声为音乐|看进事物|未来事件望去|分配信息交代|冒进.*脑海|封住意义|自行落到.*身上|落到你身上|终身狂热影响|即使不控制|影响、即使|被烧死、钉死|还活着.*被烧死" chapters/final chapters/translated output/epub_work/EPUB`。
- Low-token audit: For round-derived craft analysis residue, add `rg -n "价值电荷|正电荷|负电荷|电荷|充电|精确时刻|精确节拍|精确词语|看进|抓住.*眼睛.*耳朵|抓住兴趣|超越前一个节拍|内疚操控|导览者.*凯末尔|浪漫主义者.*凯末尔|浪漫自我|第三人称智能|第三人称声音|人物特异性|人物专属性|信息交代事实|缩短句行|拉长句行|爆成笑声|麦克豪宅|一夜就跑|被一瞥意义触发|她那一栏话语|助动词进入|一张又一张画布地|方法必须反向移动|烟屁股|备用胎|微波炉节目|不可说之物这一层球体|平庸炸弹|人格不可能" chapters/final chapters/translated output/epub_work/EPUB`, then classify false positives such as legitimate idioms, verse punctuation, stable target terms like `行动主线`, or source-interface quotations before editing.
  低 token 审计：对轮次沉淀的写作分析残留，追加 `rg -n "价值电荷|正电荷|负电荷|电荷|充电|精确时刻|精确节拍|精确词语|看进|抓住.*眼睛.*耳朵|抓住兴趣|超越前一个节拍|内疚操控|导览者.*凯末尔|浪漫主义者.*凯末尔|浪漫自我|第三人称智能|第三人称声音|人物特异性|人物专属性|信息交代事实|缩短句行|拉长句行|爆成笑声|麦克豪宅|一夜就跑|被一瞥意义触发|她那一栏话语|助动词进入|一张又一张画布地|方法必须反向移动|烟屁股|备用胎|微波炉节目|不可说之物这一层球体|平庸炸弹|人格不可能" chapters/final chapters/translated output/epub_work/EPUB`，编辑前先区分成语、诗歌引文标点、`行动主线` 这类稳定目标语术语、必要源语接口等合理例外。
- Low-token audit: Add the round-derived abstract/voice residue scan `rg -n "丑闻缠身地|声名狼藉地富有|富有而出名|回看合乎逻辑|合乎逻辑的感知|叙述智能|人物专属声音|人物声音这一侧|角色身份|人物身份|以角色身份|词语文本|可见的尖端|巨大内容.*沉入|孤独区域|临时冬眠|令人烦扰的迟钝" chapters/final chapters/translated output/epub_work/EPUB`, then compare only candidates with nearby source before editing.
  低 token 审计：追加本轮沉淀的抽象/声音接口残留扫描：`rg -n "丑闻缠身地|声名狼藉地富有|富有而出名|回看合乎逻辑|合乎逻辑的感知|叙述智能|人物专属声音|人物声音这一侧|角色身份|人物身份|以角色身份|词语文本|可见的尖端|巨大内容.*沉入|孤独区域|临时冬眠|令人烦扰的迟钝" chapters/final chapters/translated output/epub_work/EPUB`，只把候选与邻近原文对照后再编辑。
- Evaluative-adverb guard: Do not turn degree or social-color adverbs into unsupported facts. For example, `scandalously rich and famous` may mean rich and famous to an almost shocking or ostentatious degree; do not translate it as `丑闻缠身` unless the source explicitly asserts actual scandals.
  评价副词防护：不要把程度或社会色彩副词改成无依据事实。例如 `scandalously rich and famous` 可表示富有和出名到近乎惊人/招摇的程度；除非原文明说丑闻事实，不要译成“丑闻缠身”。
- Fix by: Reorder information for target-language comprehension while preserving facts, emphasis, causality, and narrative viewpoint.
  修复方式：按目标语理解顺序重排信息，同时保留事实、重心、因果和叙述视角。
- Recheck: Verify the revised sentence no longer sounds translated, and that no source relation was lost.
  复查：确认修订句不再像翻译腔，同时没有丢失原文关系。

### Reader-Facing Source-Name Clutter / 读者界面原名杂音

- Symptom: A target-language paragraph interrupts ordinary reading with multiple source-language names, role names, or parenthetical originals in one sentence, even though the exact source spelling is not being analyzed.
  症状：目标语正文一句里塞入多个源语人名、角色名或括注原名，打断普通阅读；而该处并不是在分析这些源语拼写本身。
- Find by: Scan sampled units and final chapters for dense Latin-script names, repeated parenthetical originals, and mixed source/target references to the same person in nearby sentences. Exempt quote-analysis lines where the source wording itself is the object of analysis.
  发现方式：扫描抽样单元和终稿章节中的密集拉丁字母人名、重复括注原名，以及邻近句里同一人物源语/目标语混用的情况。若该处正在分析原句措辞本身，应作为合理例外。
- Fix by: Keep a single useful source interface at first natural mention, then use the target-language name or role consistently. Move work titles into title parentheses if needed, but do not parenthesize every person name in explanatory prose. When the source uses role labels for contrasted selves or narrators, choose readable target-language role names and keep them stable, for example `Docent Kemal` / `Romantic Kemal` should become consistent target roles instead of awkward literal labels.
  修复方式：在第一次自然出现处保留一个有用的原名接口，之后稳定使用目标语姓名或身份。作品标题必要时可括注原名，但不要在解释性正文里给每个人名都加括注。若原文用角色标签区分叙述者、自我或人物面向，应选择目标语可读角色名并保持稳定，例如 `Docent Kemal` / `Romantic Kemal` 应处理成稳定的目标语角色称谓，而不是生硬直译标签。
- Low-token audit: Search for dense parenthetical source names and unstable role labels, for example `rg -n "（[A-Z][A-Za-z .'-]+）|Donald Hall|Robert Frost|Erwin Piscator|Thornton Wilder|讲解员凯末尔|浪漫凯末尔" chapters/final chapters/translated`, then exempt only bibliography, title interfaces, and source-form analysis.
  低 token 审计：扫描密集括注原名和不稳定角色标签，例如 `rg -n "（[A-Z][A-Za-z .'-]+）|Donald Hall|Robert Frost|Erwin Piscator|Thornton Wilder|讲解员凯末尔|浪漫凯末尔" chapters/final chapters/translated`，只豁免书目信息、作品标题接口和源语形式分析。
- Recheck: Read the paragraph without the source text and confirm the names no longer feel like production notes or terminology scaffolding.
  复查：不看原文只读该段，确认这些名字不再像制作说明或术语脚手架。

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

### Technique-Term and Idiom Interface / 技法术语与成语接口

- Symptom: A craft term, famous line, or English idiom is translated literally enough to become opaque in the target language, even though the exact source form matters for teaching or reader recognition.
  症状：写作技法术语、经典台词或英语成语被直译得不透明；而这些地方的源语形式又关系到教学说明或读者识别。
- Find by: Scan sampled low-score units plus glossary/title maps for terms such as `on-the-nose`, `action spine`, `movement`, `in-character/non-character`, `narrating intelligence`, `fits the ear`, `fix blame`, `offer he couldn't refuse`, `fly-by-night`, `flattering`, `run its course`, `okay?`, `just very different`, `codes of address`, and idiom-like phrases that appear in quoted or analytical contexts.
  发现方式：结合低分样本、术语表和标题映射，扫描 `on-the-nose`、`action spine`、`movement`、`in-character/non-character`、`narrating intelligence`、`fits the ear`、`fix blame`、`offer he couldn't refuse`、`fly-by-night`、`flattering`、`run its course`、`okay?`、`just very different`、`codes of address` 等术语/成语，以及出现在引文或分析语境中的惯用表达。
- Fix by: Use a target-readable term first, then keep the source form in parentheses only when the book-local glossary/display policy allows it or when the source phrase itself is a required quote interface. If a glossary forbids the source form in body text, put the source interface in the approved note/glossary layer instead. Render a famous line such as `offer he couldn't refuse` with the established target phrasing and, in quote-analysis contexts, pair it with the original source line. For craft terms such as `action spine` / `spine of action`, do not preserve a literal body term like `行动脊柱`; use a target-readable concept such as `行动主线`, and recast compounds like "dueling action spines" into a clear target-language relation. For dramatic-structure `movement`, avoid `运动/运动段落`; use `推进段`, `动作段`, or a context-specific equivalent. For prose-mode `in-character/non-character`, prefer readable labels such as `人物发声/非人物叙述` or `借人物声音写作`, not literal "身份声音" compounds. For `narrating intelligence`, use `叙述意识` or a context-specific narrator-awareness phrase, not `叙述智能`. For idioms and dialogue such as `fly-by-night`, `flattering`, and `fits the ear`, translate the function in the scene: `不靠谱的临时买卖`, `太抬举我了`, `听起来顺耳`, etc.; do not add fraud, excessive emotion, or anatomical literalism.
  修复方式：先给目标语可读术语；只有书内术语表/display policy 允许，或源语短语本身是必要引句接口时，才在正文括号中保留源语。若术语表禁止源词进入正文，应把源语接口放到批准的注释/术语表层。`offer he couldn't refuse` 这类经典台词应采用读者能识别的惯用译法；在引句分析语境里，还要与原句成对呈现。`action spine` / `spine of action` 这类技法术语不得硬译成正文里的 `行动脊柱`，应改为 `行动主线` 等中文可读概念；"dueling action spines" 这类组合要改成清楚的目标语关系。戏剧结构里的 `movement` 不要译成 `运动/运动段落`，应按上下文改为 `推进段`、`动作段` 等；散文模式里的 `in-character/non-character` 宜译成“人物发声/非人物叙述”或“借人物声音写作”这类可读标签，不要硬造“身份声音”。`narrating intelligence` 宜译为“叙述意识”或按上下文改写为叙述者意识，不要写“叙述智能”。`fly-by-night`、`flattering`、`fits the ear` 这类成语/台词应按场景功能处理为“不靠谱的临时买卖”“太抬举我了”“听起来顺耳”等，不要加出诈骗、过激情绪或器官直译。
- Dialogue idiom guard: In analyzed dialogue, keep the English quote interface when the source wording matters, but translate the function rather than the filler word. `okay?` inside a frantic challenge may become `行吗？` or another pressure marker, not a polite `好吗？`; `just very different` should usually become a natural understatement such as `只是不太一样`, not `只是很不同`; `codes of address` should not be narrowed to address forms only when it means broader interaction or speech norms.
  台词成语防护：被分析台词中，若源语措辞本身重要，应保留英文引句接口，但译文要译功能，不要译填充词表面。急促逼问里的 `okay?` 可译为“行吗？”等施压标记，不宜译成客气的“好吗？”；`just very different` 通常应处理成“只是不太一样”这类自然低调说法，而不是“只是很不同”；`codes of address` 若指更广的交往/话语规范，不应收窄为只关乎称谓的“称呼规范”。
- Blame/relationship-loss guard: In craft analysis, do not let compact English abstractions become false target-language actions. `fix blame` means determining or assigning where responsibility lies, not necessarily pursuing punishment; `public transportation portrait` may be a bus-side ad image rather than an abstract portrait; `mutual loss` in relationship analysis is a shared loss borne by both people, not `相互失落`.
  责任/关系损失防护：写作技法分析中，不要把紧凑英语抽象词译成错误的目标语动作。`fix blame` 指确定或归置责任，不一定是“追究责任”；`public transportation portrait` 可能是公交车身广告头像，不是抽象的“公共交通画像”；关系分析里的 `mutual loss` 是双方共同承受的损失，不是“相互失落”。
- Crowd/collective noun guard: In political or theatrical dialogue, do not translate `mob` mechanically as `暴民` when the scene means the audience, populace, crowd, or Roman people whose favor grants power. Use `民众`, `大众`, `观众`, or a context-specific collective unless the source clearly stresses riotous violence or contempt.
  群体名词防护：政治或戏剧台词中的 `mob` 不要机械译成 `暴民`。若语境指掌声、拥戴和政治权力来源中的观众/大众/罗马民众，应按上下文译为 `民众`、`大众`、`观众` 等；只有原文明示暴乱、暴力或强烈蔑称时才用 `暴民`。
- Low-token audit: Use `rg -n "顶在鼻尖|on-the-nose|行动脊柱|故事脊柱|行动主线|相互决斗|固定责任|追究责任|确定责任|无法拒绝的条件|无法拒绝的提议|受宠若惊|奉承|一个运动|两个运动|运动段落|运动段|第二个运动|解决运动|人物身份声音|非人物身份声音|角色身份声音|人物内声音|叙述智能|这个智能|人物专属声音|人物声音这一侧|以角色身份|贴合耳朵|骗一把就跑|一夜就跑|不靠谱的.*买卖|跑完自己的路程|公共交通画像|拳击家|相互失落|关系的失落|弧贯|讲解员凯末尔|浪漫凯末尔|暴民|逗暴民|mob is Rome" chapters/final chapters/translated output/epub_work/EPUB`, then classify hits as confirmed defects, established terms, famous-line interfaces, or reasonable exceptions. If source expansion is needed, search `rg -n "fix blame|share blame|place blame|public transportation portrait|pugilists|mutual loss|narrating intelligence|this intelligence" chapters/src`.
  低 token 审计：可用 `rg -n "顶在鼻尖|on-the-nose|行动脊柱|故事脊柱|行动主线|相互决斗|固定责任|追究责任|确定责任|无法拒绝的条件|无法拒绝的提议|受宠若惊|奉承|一个运动|两个运动|运动段落|运动段|第二个运动|解决运动|人物身份声音|非人物身份声音|角色身份声音|人物内声音|叙述智能|这个智能|人物专属声音|人物声音这一侧|以角色身份|贴合耳朵|骗一把就跑|一夜就跑|不靠谱的.*买卖|跑完自己的路程|公共交通画像|拳击家|相互失落|关系的失落|弧贯|讲解员凯末尔|浪漫凯末尔|暴民|逗暴民|mob is Rome" chapters/final chapters/translated output/epub_work/EPUB` 收集候选，再区分为确认问题、稳定术语、经典台词接口或合理例外。需要源语扩展时，搜索 `rg -n "fix blame|share blame|place blame|public transportation portrait|pugilists|mutual loss|narrating intelligence|this intelligence" chapters/src`。
- Rebuild guard: After repairing a literal technique term such as `行动脊柱`, scan both source Markdown and generated EPUB XHTML. If Markdown is clean but an old EPUB still contains the bad term or old quote layout, rebuild before validation; stale staging is a reader-facing regression, not a reasonable exception.
  重建防护：修复 `行动脊柱` 这类技法术语硬译后，必须同时扫描源 Markdown 和生成 EPUB XHTML。若 Markdown 已清但旧 EPUB 仍含坏术语或旧引文排版，必须先重建再验证；旧 staging 污染是读者可见回归，不是合理例外。
- Recheck: Read the revised paragraph as a target-language teaching paragraph without the source. The term should be intelligible before the source form helps it.
  复查：不看原文，只把修订段当目标语教学段阅读；术语应先能读懂，源语形式只起辅助作用。

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

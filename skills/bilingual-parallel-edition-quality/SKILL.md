---
name: bilingual-parallel-edition-quality
description: "审校双语对照 EPUB 的段落对应、译文读感、注释回链和读者可见版式。 Review bilingual EPUB paragraph alignment, translation quality, note links, and reader-facing layout."
---

# 双语对照版质量与错位排查 / Bilingual Parallel Edition Quality and Alignment Audit

## 适用范围 / When to Use

当你制作、修订、审校或重建双语对照版 EPUB，或收到读者关于段落错位、注释跳转、目录、封面及正文排版的反馈时，使用本 Skill。先读项目的 `AGENTS.md`、`template/epub_pipeline/README.md`、`template/epub_pipeline/common/README.md`、`template/epub_pipeline/common/references/bilingual_parallel_edition_policy.md` 和适用的目标语言/语言方向规则；本 Skill 是执行清单，不替代模板政策。

Use this skill when creating, revising, reviewing, or rebuilding a bilingual parallel EPUB, or when readers report paragraph misalignment, note navigation, contents, cover, or body-layout problems. First read the project `AGENTS.md`, the pipeline READMEs, the bilingual-edition policy, and applicable target-language and language-pair rules. This skill is an execution checklist, not a replacement for template policy.

## 核心阅读契约 / Core Reading Contract

- 读者必须先读一个完整源语自然段，紧接着读它完整的目标语对应段；不得先堆一大片原文，再集中放一大片译文，也不得让译文跑到前后其他段落。
- A reader must see one complete source-language paragraph immediately followed by its complete target-language counterpart. Never group a large run of source text before a large run of translation, or attach a translation to an earlier or later paragraph.

- 每个可见配对单元只对应一个源自然段。源段过长时，只能沿完整句子边界拆成连续的源语—目标语配对；不可按页面、屏幕、字数或 EPUB 文件边界切断句意。
- Each visible pair maps to one source natural paragraph. If it is too long, split it only at complete sentence boundaries into consecutive source–target pairs. Do not split by page, screen, word count, or EPUB-file boundary.

- 不得把多个源自然段合成一个译文段，也不得遗漏、重复、挪动目标语内容。标题、日期、称谓、落款、诗行、列表、图表说明和注释都要按其语义边界单独核对。
- Never merge several source paragraphs into one target paragraph, or omit, duplicate, or shift target content. Check headings, dates, salutations, signatures, verse, lists, captions, and notes at their semantic boundaries.

- 结构正确不等于语义配对正确。ID、顺序、哈希、语言标签和 XHTML 层级只能证明内容被登记和输出，不能证明这段中文翻译的就是眼前这段英文。
- Structural validity does not prove semantic alignment. IDs, order, hashes, language tags, and XHTML nesting show that content was registered and emitted; they do not prove that the Chinese translates the English immediately above it.

- 如果确认目标段串到了前一段或后一段，修复必须落在正确的 canonical target unit，并保证单语版与双语版使用同一目标文本。`qa/bilingual_parallel/alignment_map.json` 是 QA 投影；不得靠改它或生成后的 XHTML 挪动文字来伪造修复。若合同、语义审核或其他硬门禁未通过，不得绕过门禁产出正式 EPUB。
- When a target paragraph is confirmed to have shifted to a previous or next source, repair the correct canonical target unit and keep the target-only and bilingual editions on the same target text. `qa/bilingual_parallel/alignment_map.json` is a QA projection; never simulate a repair by moving text there or in generated XHTML. If the contract, semantic audit, or another hard gate has not passed, do not bypass it to produce a final EPUB.

- 对“邻段串译”复发问题族，同时使用 `skills/translation-quality-defect-families/families/bilingual-adjacent-unit-semantic-shift.md`；本 Skill 补充全书快速筛查与双语成品检查，不取代该问题族规定的 canonical 修复步骤。
- For recurring adjacent-paragraph shifts, also use `skills/translation-quality-defect-families/families/bilingual-adjacent-unit-semantic-shift.md`. This skill adds book-wide triage and bilingual-artifact checks; it does not replace that family’s canonical repair procedure.

## 全书快速排查 / Fast Whole-Book Screening

1. 先运行 `npm run check:bilingual` 和 `npm run check:bilingual:interleave`，确认映射表、中间构建和 EPUB 属于同一版。旧产物数量不符是构建版本不一致，不能当成语义结论。
1. Run `npm run check:bilingual` and `npm run check:bilingual:interleave` first. Establish that the map, staging, and EPUB describe the same build; a stale-artifact failure is a build mismatch, not a semantic verdict.

2. 从 canonical 对齐表和生成的 EPUB 读取全部可见配对，核对 ID、顺序、源文/译文哈希、配对数量和例外登记；不要依赖过期章节数或旧报告。
2. Read every visible pair from the canonical alignment map and the built EPUB. Compare IDs, order, source/target hashes, pair counts, and documented exceptions. Do not rely on stale chapter totals or old reports.

3. 用脚本或精确搜索筛查边界信号：注号与回链、标题、日期、称谓、落款、署名、引用起止、列表/表格/图片接口、异常空段、残留 Markdown、旧纸本目录条目，以及源段/目标段数量或次序突变。
3. Use scripts or exact searches for boundary signals: note markers and backlinks, headings, dates, salutations, signatures, credits, quotation boundaries, list/table/image interfaces, abnormal empty blocks, Markdown residue, print-era contents entries, and sudden changes in pair counts or order.

4. 可用多语种向量或相邻段落相似度生成候选：若当前译段与前后某个源段的相似度明显高于当前配对，标为待复核。相似度只用于召回候选；同一人物、地点或事件常造成误报。
4. If available, use multilingual embeddings or adjacent-paragraph similarity to generate candidates: flag a target whose similarity to a neighboring source is clearly higher than to its assigned source. Similarity is retrieval only; adjacent paragraphs about the same person, place, or event often trigger false positives.

5. 只把候选片段连同前后各一至两个配对单元交给人工复核；核对完整原文、译文及足够上下文。不得盲读全书，也不得仅凭孤立一句定案。
5. Send only flagged passages with one or two neighboring pairs on each side for human review. Compare the complete source and target with enough context. Do not blindly reread the whole book or decide from one isolated sentence.

6. 记录候选总数、确认问题数、误报数、未复核数及覆盖率。结构门禁或抽样通过只能报告为对应检查通过，不得宣称全书语义复核完成。
6. Record candidate totals, confirmed issues, false positives, unreviewed candidates, and coverage. Report structural or sampled success only as that check; never call it a completed whole-book semantic review.

## 注释、纸本指向与回链 / Notes, Print References, and Backlinks

- 正文注号用小号上标（或模板规定的下标），明显小于正文字号；点击注号进入注释，点击注释中的返回标记回到原文锚点。逐条核验两个方向的链接和编号，不以“链接存在”代替目标正确。
- Render body note markers as small superscripts (or template-approved subscripts), visibly smaller than body text. Link each marker to its note and each return marker to the exact body anchor. Verify both directions and every destination; link presence alone does not prove a correct target.

- 按传统书籍阅读顺序，在每章正文结束后换页列出本章注释，不把全书注释都攒到卷末或书末。章节注释应保留原编号体系，并与正文和目录导航一致。
- Follow traditional reading order: begin each chapter’s notes on a new page immediately after that chapter, rather than collecting all notes at the end of a volume or book. Preserve the source numbering and keep body links and navigation consistent.

- 原著注释与译者补充必须可辨。保留原注释原有内容和纸本交叉指向；若需要解释“见后”或纸本页码，再把有依据的译者说明补在原注之后。前置说明应告诉读者区分方式；例如原注用常规字体、译者补充用斜体。不得把补充伪装成原著内容。
- Keep original notes distinguishable from translator additions. Preserve the original note and its print cross-reference; when needed, append a supported explanation of “see below” or a print page reference after it. Tell readers in the front matter how to distinguish them—for example, regular type for original notes and italics for translator additions. Never present an addition as source-authored text.

- 纸本页码指向、`见后`、`见前`及相似注释须逐条判定：保留原有说明，再按证据补充读者需要的解释或本书定位。用规则扫描收集候选，不以正则命中数冒充确认数；维护已处理、待判断、例外和复核状态。
- Assess each print-page reference, “see below,” “see above,” and similar note individually. Preserve the original wording, then add only evidence-supported guidance the reader needs in this edition. Use rules to gather candidates, not to equate regex hits with confirmed defects; track processed items, pending judgments, exceptions, and rechecks.

## 正文、目录与封面 / Body, Contents, and Cover

- 中文单语正文不要无必要地把常见人名、机构名和普通词塞进括号英文；只在生僻专名、歧义消除或术语策略确有需要时保留原文，并保持全书一致。双语版中的完整源语段落不属于这种括号残留。
- In a Chinese-only edition, do not clutter prose with parenthetical English for familiar people, institutions, or ordinary words. Retain source forms only when an uncommon name, ambiguity, or documented terminology policy requires them, consistently throughout the book. Full source paragraphs in the bilingual edition are not parenthetical residue.

- 生成后检查读者可见 XHTML，确认没有 `**`、裸 Markdown、构建标记、内部单元 ID、旧纸本目录残留、乱码、异常空格或重复导航项。目录必须使用真实章节标题和有效链接；目录链接逐条落到正确正文位置。
- Inspect generated reader-facing XHTML for leaked `**`, raw Markdown, build markers, internal unit IDs, print-era contents residue, mojibake, abnormal spacing, and duplicate navigation entries. The contents must use actual chapter titles and valid links; verify every link lands at the right content.

- 封面检查最终渲染图而非只看源文件：核对标题、作者、署名、底部文字、边距、对齐、溢出和缩放下的可读性。书籍信息页规则与封面规则分开执行。
- Review the rendered cover, not just its source: check title, author, credit, footer, margins, alignment, overflow, and readability at reduced size. Apply book-info and cover policies separately.

## 章节标题重复 / Duplicate Chapter Headings

- 双语构建器可能同时输出目标语目录题名作为正文首个 `<h1>`，又输出首个 canonical 标题对照单元（源语标题 + 目标语标题），于是正文开头出现“目标语、源语、目标语”三连标题。应先检查生成 XHTML，确认重复来自构建器的额外 reader-title，而不是误改原文或译文造成的。
- A bilingual builder can emit the target-language navigation title as a synthetic body `<h1>` and then render the first canonical heading pair (source heading plus target heading). The result is a three-title sequence: target, source, target. Inspect generated XHTML first to confirm the extra reader-title is responsible; do not treat this as duplicated source or translation text.

- 若章节首个 canonical 单元是 `heading`，且其目标语标题去掉 Markdown 标记、合并空白后与 reader-facing title 相同，应只省略正文里的合成 reader-title。保留完整的源语/目标语标题配对单元；EPUB `<title>`、metadata 和目标语目录题名仍保留。标题文字不同、确属副标题或首单元不是标题时，不要自动合并。
- If the chapter's first canonical unit is a `heading` and its target heading matches the reader-facing title after removing Markdown markers and normalizing whitespace, omit only the synthetic body reader-title. Keep the complete source/target heading pair and retain the target-language EPUB `<title>`, metadata, and navigation label. Do not merge intentionally different titles, subtitles, or a page whose first unit is not a heading.

- 不得通过删除 canonical 标题对、改写对齐映射、在生成 XHTML 中删掉一个语言块来消重。这样会破坏单语/双语共用的目标文本或双语单元完整性。应修正生成逻辑，再从干净 staging 重建。
- Do not deduplicate by deleting the canonical heading pair, editing the alignment projection, or removing one language block from generated XHTML. Those shortcuts break the shared target text or the bilingual unit contract. Fix the build logic and rebuild from clean staging.

- 快速全书审计：对每个生成的 `bilingual_*.xhtml` 检查正文开头的 `<h1>` 和首个 `bitext-section-heading`；若 `data-lifebook-editorial="reader-title"` 与首个标题配对同时出现，逐章对照 alignment map 中的目标标题和目录题名，确认是同题重复还是刻意保留的不同标题。修复后确认配对标题只出现一次（每种语言各一个），目标语导航题名仍有效；并检查双语结构门禁、EPUBCheck 和至少一个实际阅读器页面。
- Fast book-wide audit: inspect the opening headings in every generated `bilingual_*.xhtml`. If both `data-lifebook-editorial="reader-title"` and the first `bitext-section-heading` appear, compare the alignment map's target heading with the navigation title chapter by chapter to distinguish accidental duplication from intentional title/subtitle differences. After repair, confirm one heading per language, valid target-language navigation, passing bilingual structure checks and EPUBCheck, and at least one rendered reader page.

## 译文读感与问题族闭环 / Translation Readability and Defect-Family Closure

- 对照原文时也要单独通读中文：找出直译句法、过硬过直、平板解释腔、无依据加戏、过度解释和读者可见制作痕迹。润色必须保留事实、语气、修辞功能和证据关系；不能为了“顺”而改写原意。
- Read the target text on its own as well as against the source. Look for calqued syntax, stiff or flat explanatory prose, unsupported embellishment, over-explanation, and reader-visible production residue. Preserve facts, tone, rhetorical function, and evidentiary relations while improving fluency.

- 一旦确认问题可能复发，先记录一组原文—译文证据并归纳问题族，再从该例、术语表/专名表、禁用译法、标题表和章节控制记录建立 `rg` 等低成本候选搜索；只回读命中项及必要的前后文。交给 reviewer/agent 的也只能是候选片段和小上下文，不得让其盲读全书。
- When a defect may recur, record a source–target example and classify the family first. Seed low-cost searches such as `rg` from that example, glossaries/name registers, forbidden renderings, title lists, and chapter-control records; inspect only hits with the context needed to decide. Give reviewers or agents candidate excerpts and small context windows, never a blind full-book assignment.

- 修复所有确认命中后，把可复用方法合并进 `skills/translation-quality-defect-families/SKILL.md` 或相应问题族文件；书籍特有证据留在该书 QA。修复轮标为 `FIXED_RECHECK_REQUIRED`，随后整章重查；不得直接报 PASS。
- After fixing confirmed matches, merge the reusable method into `skills/translation-quality-defect-families/SKILL.md` or its matching family file; keep book-specific evidence in book QA. Mark the repair round `FIXED_RECHECK_REQUIRED` and recheck the whole chapter before any PASS.

## 修复与通过标准 / Repair and Pass Criteria

- 每章独立闭环。任何一轮发现并修复问题，只能记录为 `FIXED_RECHECK_REQUIRED`；随后必须以新的轮次重新整章核对原文、译文和上下文。不得把修复轮写成 PASS。
- Close each chapter independently. Any round that finds and fixes an issue must be recorded as `FIXED_RECHECK_REQUIRED`; then start a new round and recheck the whole chapter against source, translation, and context. A repair round cannot be called PASS.

- 只有最新一轮同时满足 `scope: FULL_CHAPTER`、`issues_found: 0`、`fixes_applied: 0`、`unresolved_blocking_issues: 0`、`latest_round_status: PASS`、`allow_next_chapter: true`，该章才通过。
- A chapter passes only when its latest round records all of: `scope: FULL_CHAPTER`, `issues_found: 0`, `fixes_applied: 0`, `unresolved_blocking_issues: 0`, `latest_round_status: PASS`, and `allow_next_chapter: true`.

- 配对映射修改后，清理或重建 staging，再生成 EPUB；重跑映射覆盖、双语顺序/结构、回链、读者可见 lint、资产检查和可用的 EPUBCheck。抽查实际 XHTML/阅读器页面，确认修正进入成品。
- After changing alignment, clean or rebuild staging before generating the EPUB. Rerun map coverage, bilingual order/structure, backlinks, reader-facing lint, asset checks, and available EPUBCheck. Inspect actual XHTML or reader pages to confirm the repair reached the artifact.

- QA 记录必须说明如何发现、如何人工确认、如何用低成本方法查全书同类、修复了什么、复查结果和未覆盖边界。未解决项要列为后续工作；不得将候选清零、脚本通过或旧版本正确描述为本版全书通过。
- QA records must explain discovery, human confirmation, the low-cost whole-book recurrence search, repairs, recheck results, and uncovered areas. List unresolved work explicitly. Do not call a release-wide PASS based on zero remaining candidates, passing scripts, or a defect fixed in an older version.

## 最终检查清单 / Final Checklist

- [ ] 每个英文自然段后立即是其完整中文对应段；长段只按完整句子边界拆分。
- [ ] Every English paragraph is immediately followed by its complete Chinese counterpart; long paragraphs are split only at complete sentence boundaries.
- [ ] 日期、标题、称谓、落款、诗行、注释和图表文字接口的语义边界均已核验。
- [ ] Semantic boundaries for dates, headings, salutations, signatures, verse, notes, and figure/table text have been checked.
- [ ] 原注、译者补充、纸本指向、注号上标、章节末注释及双向回链都正确且易读。
- [ ] Original notes, translator additions, print references, superscript markers, chapter-end notes, and bidirectional links are correct and readable.
- [ ] 目录、封面、XHTML 中无读者可见制作痕迹，且生成物已经过对应门禁。
- [ ] Contents, cover, and XHTML are free of reader-visible production residue, and the built artifact has passed applicable gates.
- [ ] 全书候选的已确认、误报、未复核数量及覆盖范围均已如实记录。
- [ ] Confirmed, false-positive, and unreviewed candidate counts and whole-book coverage are reported honestly.

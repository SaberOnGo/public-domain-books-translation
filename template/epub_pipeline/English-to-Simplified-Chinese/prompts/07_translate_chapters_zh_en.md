# 07 分章翻译 / Translate Chapters

## 输入 / Input

- `chapters/src/*.md`
- `metadata/book_specific_translation_research.md`
- `metadata/style_profile.md`
- `glossary/terms.csv`
- `qa/pretranslation/pretranslation_report.md`

## 前置门禁 / Prerequisite Gate

只有当 `qa/pretranslation/pretranslation_report.md` 明确 `PASS` 时，才可开始。

## 任务 / Tasks

逐章翻译到：

- `chapters/translated/{same_filename}.md`

翻译调用只输出译文，不输出 QA、解释、流程记录、门禁报告或术语审计。QA 由 `08a`、`08`、`09`、`10`、`11` 等后续节点单独生成。不要在同一次调用里让模型同时当译者、审校员和流程记录员。

每章翻译前必须先在内部判断：

1. 本章原文功能。
2. 叙述声音。
3. 关键术语。
4. 关键意象。
5. 易误译/易越界发挥/易省字式翻译的段落。

翻译 prompt 必须瘦身，只给：

- 当前章节或小段落组原文。
- `metadata/style_profile.md` 中最关键的 5-8 条文体规则。
- 当前段实际命中的术语；不要把整张术语表塞入每次翻译调用。
- 必要的前后文。

不要把 release、版权、EPUB 构建、publication lint、QA 文件路径、随机抽检或版本化产物规则塞进翻译 prompt。这些规则仍然是后续门禁，但不应干扰模型先写出自然中文。

## 翻译要求 / Translation Requirements

- 保持标题和段落结构。优先按段落或小段落组翻译，避免大 chunk 导致段落合并、拆分或硬配回去。
- 自然中文是翻译阶段第一硬约束：译文必须像一本自然的中文书，普通读者能顺畅朗读。
- 忠实原意、事实、语气和叙述立场；忠实不是保留英文句法。
- 术语一致，但只有 `glossary/terms.csv.term_control = locked` 的术语必须硬性固定；`preferred` 术语可按上下文自然变体，后续术语审校再判断是否需要回收。
- 出版格式合规，但格式问题不能压倒中文可读性；后续节点处理格式门禁。
- 章节标题必须按 `references/english_chapter_title_strategy.md` 处理；不得把英文 `--` 标题链机械翻成多个中文 `——`。
- 强制规则：章节标题、副标题和 EPUB 目录题名里的人名不算“正文首次出现”。标题只使用中文译名，不得追加英文原名或括注；英文原名必须放到正文第一次自然出现该人名的位置。
- 普通名词、器物名、衣物名、材料名和动作名必须译成中文，不得写成 `source term（中文释义）`，也不得写成 `中文词（source term）`。人名首次出现保留英文原名的规则不适用于普通名词。
- 历史术语、制度名、身份称谓、专业术语和文化负载词正文默认使用中文译名或准确意译，不得批量写成 `中文译名（source term）`。需要交代原词时，优先在正文处加统一注号，如 `术语[1]` 或 `术语（1）`，并把原词、释义和译名理由写入本章译注、章末注或术语表。只有不保留原词会造成明显误解、原词本身是作者论证对象、或学界译名分歧必须当场交代时，才允许正文短括注原词，并在 control 或术语表记录理由。
- 盎格鲁-撒克逊制度身份词示例：`thegn` / `thane` 不得默认音译为“塞恩”，也不宜统一译成“支持者”。若语境强调土地、等级、服役和政治义务，正文按上下文用“王室领主”“领主近臣”“盎格鲁-撒克逊领主”等；术语注再写原文为 `thegns`，又作 `thanes`。`witenagemot` 正文用“贤人会议”，原词放术语注。
- 删除旧纸书中的可见分隔符，例如 `* * * * *`、`*****`、`----`；不得替换成 `---` 或其他可见分隔线。
- 忠实事实和语气。
- 中文必须自然，有叙述气息。
- 英文长句必须转换为中文句群，必要时拆成两句或三句；不得写成大段不断气的中文长句。
- 允许为了中文自然度调整从句顺序、合并过碎短句、重排信息焦点；但不得改变事实、情绪强度或叙述立场。
- 对话必须像中文人物说话，不得硬搬英文礼貌结构和从句骨架。
- 关键句要有画面和记忆点。
- 不接受第一版“通顺但无味”的译文。
- 不得直接写入 `chapters/final/`。

## 多候选融合 / Multi-Candidate Fusion

整章不必每段都输出多版，但以下位置必须在内部做 A/B/C/D 融合后，只把 D 写入正文：

- 章节开头和结尾。
- 高现场感、动作、危险或情绪转折段。
- 关键对话。
- 术语或文化负载重的段落。
- 上一轮 QA 或用户指出机械、不自然的段落。

A 为忠实版，B 为中文阅读版，C 为文学润色版，D 为融合终稿。正文只保留 D，不保留候选过程。

## 专家级译文与多义词主动判义及回看 / Expert Quality, Active Polysemy Handling, and Back-Check

翻译调用仍然只输出译文，不输出 QA 或流程记录；但译者必须按 `skills/expert-translation-quality/SKILL.md` 在内部建立观察清单，并在翻译阶段主动判义。遇到多义词、习语、称谓、术语或需要后文判义的语法结构，先用当前句、本段、邻近上下文、术语表、说话人身份、论证功能和可用后文线索判义；能判清的当场处理，不能判清的才用不错误收窄的目标语保留歧义并标记后文回看。不得把局部上下文已能判清的问题留给 `08a`。后文译出后，`08a` 必须回到前文位置复查并必要时修订。观察清单不得进入读者正文。

## 章节译后控制 / Post-Translation Control

每章写入 `chapters/translated/` 后，必须立即进入：

- `prompts/08a_chapter_post_translation_control_zh_en.md`

并创建：

- `qa/chapter_controls/{same_filename}.control.md`

这是“每章译后，全量检查并修复节点”，不是可选自检。该节点必须检查 metadata、nav、目录、正文、注释、图表、公式、表格、图片、样式、读者可见内容、通俗化、可读性、润色、名词术语和注释等，不得只检查用户点名项目。

如果该章 control 最近一轮不是全章零问题 PASS，AI 必须修复并追加同节点复查，不得进入下一章翻译、后续审校或 `chapters/final/`。发现并修复问题的轮次只能记为 `FIXED_RECHECK_REQUIRED`，不得直接 PASS；只有最近一轮记录 `scope: FULL_CHAPTER`、`issues_found: 0`、`fixes_applied: 0`、`unresolved_blocking_issues: 0`、`latest_round_status: PASS`、`allow_next_chapter: true` 时，流程才可继续。如果用户对该章不满意，AI 必须只回到该章重译，不得让该章继续进入后续审校。

## 状态 / State

成功后：

- `status = TRANSLATED`
- `chapters_translated = 章节数`
- `current_step = chapters_translated`

注意：`TRANSLATED` 不代表可进入终稿，必须等待每章 control PASS。

## 随机抽检同类问题全书审计 / Book-Wide Similar-Issue Audit

随机抽检一旦发现任何需要修复或可能系统性复现的问题，包括但不限于 P0/P1/P2、单项 <80、读者不可理解、事实/术语/图表/公式/注释错误，或本模板硬门禁失败，主执行 AI 不得只修被抽中的样本，也不得等到第二轮才全书检查。必须先把发现归纳为问题族，再对整本读者可见书稿执行全书同类问题审计，覆盖 `chapters/final/`、frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML；修复所有确认命中，记录合理例外，并在该轮 `fix_log.md` 与 `closure_check.md` 中关闭该问题族后，才能使用新 seed 复抽。

若该轮发现译文质量问题族，还必须在 `fix_log.md` 填写 `translation_quality_skill_backfill: "UPDATED"` 或 `"MERGED"`、`translation_quality_skill_backfill_path: "skills/translation-quality-defect-families/SKILL.md"` 和回填摘要，并在 `closure_check.md` 填写 `translation_quality_skill_backfill_verified: true`；若仅有非译文质量问题，必须填写 `NOT_APPLICABLE` 和具体理由。

If a random sample exposes any issue that needs correction or may recur systemically, treat it as a possible systemic defect family immediately in the current round. Audit the whole reader-facing book for similar cases, fix all confirmed matches, document justified exceptions, and close the family in the same round before a new-seed resample.

# 07 分章翻译 / Translate Chapters

## 输入 / Input

- `chapters/src/*.md`
- `metadata/book_specific_translation_research.md`
- `metadata/style_profile.md`
- `glossary/terms.csv`
- `glossary/proper_nouns.csv`
- `references/proper_noun_display_policy.md`
- `references/note_marker_policy.md`
- `qa/pretranslation/pretranslation_report.md`

## 前置门禁 / Prerequisite Gate

只有当 `qa/pretranslation/pretranslation_report.md` 明确 `PASS` 时，才可开始。

## 任务 / Tasks

逐章翻译 canonical unit store 中属于该章的 `target_template`，并输出 worker-owned chapter patch。patch 保存追踪用 base manifest SHA-256，并以 `base_chapter_digest`、旧 target/template hash 和章节所有权执行按章 CAS，合并为新的 immutable generation。

- 译者只写 `translation_units/patches/` 下自己的 patch，不直接改 canonical JSONL。
- `chapters/translated/` 与 `chapters/final/` 都是同一 canonical target 的干净投影，只能由 `translation_unit_pipeline.py materialize` 统一生成；两者不得分别翻译、分别润色或手工修改。

翻译调用只输出译文，不输出 QA、解释、流程记录、门禁报告或术语审计。QA 由 `08a`、`08`、`09`、`10`、`11` 等后续节点单独生成。不要在同一次调用里让模型同时当译者、审校员和流程记录员。

每章翻译前必须先在内部判断：

1. 本章原文功能。
2. 叙述声音。
3. 关键术语。
4. 关键意象。
5. 易误译/易越界发挥/易省字式翻译的段落。

翻译 prompt 必须瘦身，只给：

- 当前章内分配给该 worker 的 canonical short-paragraph units；每个 unit 都必须保持自己的完整边界。
- `metadata/style_profile.md` 中最关键的 5-8 条文体规则。
- 当前段实际命中的术语；不要把整张术语表塞入每次翻译调用。
- 必要的前后文。

不要把 release、版权、EPUB 构建、publication lint、QA 文件路径、随机抽检或版本化产物规则塞进翻译 prompt。这些规则仍然是后续门禁，但不应干扰模型先写出自然中文。

## 翻译要求 / Translation Requirements

- 每个 canonical unit 必须完全覆盖一个源自然段内的完整短段；可在过长自然段内部按完整句群拆成多个短段，但绝不能跨越两个源自然段。不得把一句拆成一个对照块，也不得把数段/数页英文合并后再集中给中文。
- 双语版的可见结构是 `完整英文短段 -> 该短段完整中文译段`。它不是逐句字幕，也不是按页面或“手机一屏”聚合多段。
- 自然中文是翻译阶段第一硬约束：译文必须像一本自然的中文书，普通读者能顺畅朗读。
- 忠实原意、事实、语气和叙述立场；忠实不是保留英文句法。
- 术语一致，但只有 `glossary/terms.csv.term_control = locked` 的术语必须硬性固定；`preferred` 术语可按上下文自然变体，后续术语审校再判断是否需要回收。
- 出版格式合规，但格式问题不能压倒中文可读性；后续节点处理格式门禁。
- 章节标题必须按 `references/english_chapter_title_strategy.md` 处理；不得把英文 `--` 标题链机械翻成多个中文 `——`。
- 重点专有名词必须使用 `{{pn:entity_id}}` 占位符；脚本根据已锁定 `glossary/proper_nouns.csv` 与 occurrence ledger 执行 display policy。译者不得自行决定首次出现、直接写已锁定名称、追加 CSV 或改变同名消歧。
- 强制规则：章节标题、副标题和 EPUB 目录题名里的人名或其他重点专名不算“正文首次出现”。标题使用锁定 CSV 的 `subsequent_rendering`：策略 `1`/`3`/`5` 通常显示中文，策略 `2`/`4` 保留原名；标题不得追加正文首次出现括注，也不得覆盖用户选择。
- 策略 `1`：直接翻译成中文；策略 `2`：保留原文不翻译；策略 `3`：首次正文自然出现 `译名（原文）`、后续用译名；策略 `4`：首次正文可按 CSV 锁定为 `译名（原文）` 或原名优先的 `原文（中文释义）`、后续用原文；策略 `5`：首次正文自然出现 `译名（原文）` 并使用合规注号、后续用译名。
- 专有名词括注和译注/脚注/尾注是两个不同功能。策略 `3` 的 `尼禄（Nero）` 不是注释；策略 `5` 才需要额外注号，例如 `尼禄（Nero）[1]`、`尼禄（Nero）（1）` 或 `尼禄（Nero）注1`。
- 首次出现后，只有当前段落正在讨论原文拼写、转写、音译差异、源语形式或学界译名分歧时，才可再次显示原文，并应回写 `glossary/proper_nouns.csv.repeat_original_allowed_when`。
- 普通名词、器物名、衣物名、材料名和动作名必须译成中文，不得写成 `source term（中文释义）`，也不得写成 `中文词（source term）`。人名首次出现保留英文原名的规则不适用于普通名词。
- 历史术语、制度名、身份称谓、专业术语和文化负载词正文默认使用中文译名或准确意译，不得批量写成 `中文译名（source term）`。需要交代原词时，优先在正文处加统一注号，如 `术语[1]` 或 `术语（1）`，并把原词、释义和译名理由写入本章译注、章末注或术语表。只有不保留原词会造成明显误解、原词本身是作者论证对象、或学界译名分歧必须当场交代时，才允许正文短括注原词，并在 control 或术语表记录理由。
- 注号只能使用 `[1]`、`(1)` / `（1）`、`注1` 三类体系。不得使用带圈数字、外面小圆圈的“注”、裸 `译注：` / `脚注：` / `尾注：` / `附注：`，或句末裸数字。
- 盎格鲁-撒克逊制度身份词示例：`thegn` / `thane` 不得默认音译为“塞恩”，也不宜统一译成“支持者”。若语境强调土地、等级、服役和政治义务，正文按上下文用“王室领主”“领主近臣”“盎格鲁-撒克逊领主”等；术语注再写原文为 `thegns`，又作 `thanes`。`witenagemot` 正文用“贤人会议”，原词放术语注。
- 删除旧纸书中的可见分隔符，例如 `* * * * *`、`*****`、`----`；不得替换成 `---` 或其他可见分隔线。
- 忠实事实和语气。
- 中文必须自然，有叙述气息。
- 英文长句必须转换为中文句群，必要时拆成两句或三句；不得写成大段不断气的中文长句。
- 允许为了中文自然度调整从句顺序、合并过碎短句、重排信息焦点；但不得改变事实、情绪强度或叙述立场。
- 对话必须像中文人物说话，不得硬搬英文礼貌结构和从句骨架。
- 关键句要有画面和记忆点。
- 不接受第一版“通顺但无味”的译文。
- 不得直接写入 `chapters/translated/` 或 `chapters/final/`。

## 并行边界 / Parallel Boundary

专名 discovery/ledger/CSV、术语表、样章与合同未锁定前禁止并行翻译。锁定后，先按 `references/adaptive_parallel_orchestration.md` 运行加权工作量和客户端能力规划：能力未知或用户未授权为 0 worker；GPT 最多派生 4 个，非 GPT 最多 8 个；首轮最多 2 个，质量达标后才扩容。translation producer 只写自己独占章节的 patch，相邻章节优先同一 owner；独立 audit consumer 不得审核自己翻译的章节；coordinator 是唯一 canonical writer/merger。不同章节从同一 base manifest 生成的 patch 可按 `base_chapter_digest` 依次合并；只有同章陈旧 patch、合同或相关 revision 变化才报 `PATCH_CONFLICT`。单目标语版和双语版必须共享这套 target，不得另派 worker 重译双语版。

## 多候选融合 / Multi-Candidate Fusion

整章不必每段都输出多版，但以下位置必须在内部做 A/B/C/D 融合后，只把 D 写入正文：

- 原作者序言、导言、开篇和首章。
- 章节开头和结尾。
- 高现场感、动作、危险或情绪转折段。
- 关键对话。
- 术语或文化负载重的段落。
- 上一轮 QA 或用户指出机械、不自然的段落。

A 为忠实版，B 为中文阅读版，C 为文学润色版，D 为融合终稿。正文只保留 D，不保留候选过程。

原作者序言、导言、开篇和首章的 D 版必须按最终读者第一印象处理：准确只是底线；语言不顺口、怪、直译感重、句子平硬或解释腔明显，都不能作为正文终稿候选。项目自加前言或书籍信息页不替代原书开篇。

## 专家级译文与多义词主动判义及回看 / Expert Quality, Active Polysemy Handling, and Back-Check

翻译调用仍然只输出译文，不输出 QA 或流程记录；但译者必须按 `skills/expert-translation-quality/SKILL.md` 在内部建立观察清单，并在翻译阶段主动判义。遇到多义词、习语、称谓、术语或需要后文判义的语法结构，先用当前句、本段、邻近上下文、术语表、说话人身份、论证功能和可用后文线索判义；能判清的当场处理，不能判清的才用不错误收窄的目标语保留歧义并标记后文回看。不得把局部上下文已能判清的问题留给 `08a`。后文译出后，`08a` 必须回到前文位置复查并必要时修订。观察清单不得进入读者正文。

## 章节译后控制 / Post-Translation Control

每章 patch 合并为新 canonical generation 后，必须立即进入：

- `prompts/08a_chapter_post_translation_control_zh_en.md`

并创建：

- `qa/chapter_controls/{same_filename}.control.md`

这是“每章译后，全量检查并修复节点”，不是可选自检。该节点必须检查 metadata、nav、目录、正文、注释、图表、公式、表格、图片、样式、读者可见内容、通俗化、可读性、润色、名词术语和注释等，不得只检查用户点名项目。

如果该章 control 最近一轮不是全章零问题 PASS，AI 必须修复并追加同节点复查；该章不得进入后续审校或 `chapters/final/`。并行模式下，其他独立 owner 的章节可继续生产，但整书不得构建或发布。发现并修复问题的轮次只能记为 `FIXED_RECHECK_REQUIRED`，不得直接 PASS；只有最近一轮记录 `scope: FULL_CHAPTER`、`issues_found: 0`、`fixes_applied: 0`、`unresolved_blocking_issues: 0`、`latest_round_status: PASS`、`allow_next_chapter: true` 时，该章流程才可继续。如果用户对该章不满意，AI 必须只回到该章重译，不得让该章继续进入后续审校。

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

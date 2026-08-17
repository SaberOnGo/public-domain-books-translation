# 07 分章翻译 / Translate Chapters

## Canonical Unit Hard Contract / Canonical 单元硬契约

本语言方向同样使用 `translation_units/` 作为唯一 source-target 事实源。正文翻译前必须完成全书专名发现、逐项裁决、`entity_id`/occurrence ledger、`glossary/proper_nouns.csv` 与术语/合同锁定；未锁定前不得并行翻译。锁定后按 `references/adaptive_parallel_orchestration.md` 规划：能力未知或用户未授权时不派生 worker；GPT 上限 4，非 GPT 上限 8，先以最多 2 个 worker 做质量 pilot。translation producer 独占章节且只写自己的 chapter patch，相邻章节优先同一 owner；audit consumer 必须独立；coordinator/CAS 合并器是唯一 canonical writer。不同章节 patch 按 `base_chapter_digest` 可从同一全书 base 依次合并，同章陈旧 patch 才冲突。不得直接写或手改 `chapters/translated`/`chapters/final`，二者只能由同一 generation 确定性物化；单目标语与双语版共享同一 target，不得分别翻译。

启用双语版时，一个可见 unit 只能来自一个原著自然段；过长自然段只可按完整句群拆成短段。每个完整源语短段后必须立即跟随它的完整目标语译段；禁止逐句字幕式交错、跨自然段合并、连续多段源文后集中译文、漏译和邻段串译。专名只能写 `{{pn:entity_id}}`，不得临场新增或直接写锁定名称。


## 输入 / Input

- `chapters/src/*.md`
- `metadata/book_specific_translation_research.md`
- `metadata/style_profile.md`
- `glossary/terms.csv`
- `metadata/japanese_source_profile.md`
- `qa/textual/japanese_textual_notes.md`
- `qa/pretranslation/pretranslation_report.md`

## 前置门禁 / Prerequisite Gate

只有当 `qa/pretranslation/pretranslation_report.md` 明确 `PASS` 时，才可开始。

## 任务 / Tasks

逐章翻译到：

- `translation_units/patches/{chapter}.{owner_run_id}.json`（worker-owned chapter patch）

每章翻译前必须先在内部判断：

1. 本章原文功能。
2. 叙述声音。
3. 关键术语。
4. 关键意象。
5. 易误译/易越界发挥/易省字式翻译的段落。
6. 本章是否涉及振假名、旧字、注记、敬语、称谓、官能/暴力/心理边界。

## 翻译要求 / Translation Requirements

- 保持标题和段落结构。
- 章节标题必须按 `references/japanese_title_strategy.md` 处理；不得把日文原题、读音、罗马字或解释性括注塞进 EPUB 目录题名。
- 强制规则：章节标题、副标题和 EPUB 目录题名里的人名不算“正文首次出现”。标题只使用中文译名或本书确定的中文呈现方式，不得追加日文原名、读音或括注；必要原文信息必须放到正文第一次自然出现处、译注、术语表或书籍信息页。
- 普通名词、器物名、衣物名、材料名和动作名必须译成中文，不得写成 `source term（中文释义）`，也不得写成 `中文词（source term）`。人名首次出现保留日文原名的规则不适用于普通名词。
- 删除旧纸书中的可见分隔符，例如 `* * * * *`、`*****`、`----`；不得替换成 `---` 或其他可见分隔线。
- 日语汉字词必须判断语义漂移，不得未经判断直接照搬。
- 日语省略关系、敬语、称谓、句末语气和暧昧心理必须转成自然中文，同时保留原文的不确定性。
- 官能、暴力、病态心理或强制关系内容不得被加重、删弱、猎奇化或道德说教化。
- 忠实事实和语气。
- 中文必须自然，有叙述气息。
- 关键句要有画面和记忆点。
- 不接受第一版“通顺但无味”的译文。
- 不得直接写入或手改 `chapters/translated/`、`chapters/final/`。

## 专家级译文与多义词主动判义及回看 / Expert Quality, Active Polysemy Handling, and Back-Check

翻译调用仍然只输出译文，不输出 QA 或流程记录；但译者必须按 `skills/expert-translation-quality/SKILL.md` 在内部建立观察清单，并在翻译阶段主动判义。遇到多义词、习语、称谓、术语或需要后文判义的语法结构，先用当前句、本段、邻近上下文、术语表、说话人身份、论证功能和可用后文线索判义；能判清的当场处理，不能判清的才用不错误收窄的目标语保留歧义并标记后文回看。不得把局部上下文已能判清的问题留给 `08a`。后文译出后，`08a` 必须回到前文位置复查并必要时修订。观察清单不得进入读者正文。

## 章节译后控制 / Post-Translation Control

每章 chapter patch 经 CAS 合并为新的 canonical generation 后，必须立即进入：

- `prompts/08a_chapter_post_translation_control_zh_ja.md`

并创建：

- `qa/chapter_controls/{same_filename}.control.md`

如果用户对该章不满意，AI 必须只回到该章重译，不得让该章继续进入后续审校。其他章节可并行继续，不必全部阻塞。

## 状态 / State

成功后：

- `status = TRANSLATED`
- `chapters_translated = 章节数`
- `current_step = chapters_translated`

注意：`TRANSLATED` 不代表可进入终稿，必须等待每章 control PASS。

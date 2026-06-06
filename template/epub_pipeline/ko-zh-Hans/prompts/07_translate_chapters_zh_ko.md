# 07 分章翻译 / Translate Chapters

## 输入 / Input

- `chapters/src/*.md`
- `metadata/book_specific_translation_research.md`
- `metadata/style_profile.md`
- `glossary/terms.csv`
- `metadata/korean_source_profile.md`
- `qa/textual/korean_textual_notes.md`
- `qa/pretranslation/pretranslation_report.md`

## 前置门禁 / Prerequisite Gate

只有当 `qa/pretranslation/pretranslation_report.md` 明确 `PASS` 时，才可开始。

## 任务 / Tasks

逐章翻译到：

- `chapters/translated/{same_filename}.md`

每章翻译前必须先在内部判断：

1. 本章原文功能。
2. 叙述声音。
3. 关键术语。
4. 关键意象。
5. 易误译/易越界发挥/易省字式翻译的段落。
6. 本章是否涉及韩文/汉字混排、旧字、注记、敬语、称谓、官能/暴力/心理边界。

## 翻译要求 / Translation Requirements

- 保持标题和段落结构。
- 章节标题必须按 `references/korean_title_strategy.md` 处理；不得把韩文/朝鲜文原题、读音、罗马字或解释性括注塞进 EPUB 目录题名。
- 强制规则：章节标题、副标题和 EPUB 目录题名里的人名不算“正文首次出现”。标题只使用中文译名或本书确定的中文呈现方式，不得追加韩文/朝鲜文原名、读音或括注；必要原文信息必须放到正文第一次自然出现处、译注、术语表或书籍信息页。
- 普通名词、器物名、衣物名、材料名和动作名必须译成中文，不得写成 `source term（中文释义）`，也不得写成 `中文词（source term）`。人名首次出现保留韩文/朝鲜文原名的规则不适用于普通名词。
- 删除旧纸书中的可见分隔符，例如 `* * * * *`、`*****`、`----`；不得替换成 `---` 或其他可见分隔线。
- 韩语/朝鲜语汉字词必须判断语义漂移，不得未经判断直接照搬。
- 韩语/朝鲜语省略关系、敬语、称谓、句末语气和暧昧心理必须转成自然中文，同时保留原文的不确定性。
- 官能、暴力、病态心理或强制关系内容不得被加重、删弱、猎奇化或道德说教化。
- 忠实事实和语气。
- 中文必须自然，有叙述气息。
- 关键句要有画面和记忆点。
- 不接受第一版“通顺但无味”的译文。
- 不得直接写入 `chapters/final/`。

## 专家级译文与多义词回看 / Expert Quality and Polysemy Back-Check

翻译调用仍然只输出译文，不输出 QA 或流程记录；但译者必须按 `skills/expert-translation-quality/SKILL.md` 在内部建立观察清单。遇到多义词、习语、称谓、术语或需要后文判义的语法结构，先避免错误收窄；后文译出后，必须在 `08a` 回到前文位置复查并必要时修订。观察清单不得进入读者正文。

## 章节译后控制 / Post-Translation Control

每章写入 `chapters/translated/` 后，必须立即进入：

- `prompts/08a_chapter_post_translation_control_zh_ko.md`

并创建：

- `qa/chapter_controls/{same_filename}.control.md`

如果用户对该章不满意，AI 必须只回到该章重译，不得让该章继续进入后续审校。其他章节可并行继续，不必全部阻塞。

## 状态 / State

成功后：

- `status = TRANSLATED`
- `chapters_translated = 章节数`
- `current_step = chapters_translated`

注意：`TRANSLATED` 不代表可进入终稿，必须等待每章 control PASS。

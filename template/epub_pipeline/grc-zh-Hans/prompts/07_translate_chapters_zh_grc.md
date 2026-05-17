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

每章翻译前必须先在内部判断：

1. 本章原文功能。
2. 叙述声音。
3. 关键术语。
4. 关键意象。
5. 易误译/易越界发挥/易省字式翻译的段落。

## 翻译要求 / Translation Requirements

- 保持标题和段落结构。
- 章节标题必须按 `references/ancient_greek_title_strategy.md` 处理；不得把现代编辑者目录或参考译本目录机械翻成中文破折号长链。
- 强制规则：章节标题、副标题和 EPUB 目录题名里的人名不算“正文首次出现”。标题只使用中文译名，不得追加古希腊文原名、拉丁化转写或外文括注；原名和转写必须放到正文第一次自然出现该人名的位置、译注或术语表。
- 普通名词、器物名、衣物名、材料名和动作名必须译成中文，不得写成 `source term（中文释义）`，也不得写成 `中文词（source term）`。人名首次出现保留原文/转写的规则不适用于普通名词。
- 删除旧纸书中的可见分隔符，例如 `* * * * *`、`*****`、`----`；不得替换成 `---` 或其他可见分隔线。
- 忠实事实和语气。
- 必须从古希腊文底本翻译；第二语言译本只能用于疑难校读，不得直接转译。
- 遇到异文、残损、OCR 不确定处或语法歧义，必须记录，不得静默修平。
- 中文必须自然，有叙述气息。
- 技术证明和作图语句也必须用现代中文读者能看懂的句子。古代术语若直译成“割某线”“超过某线”“所对弧之半所对的直线”等意义不明表达，必须改写成清楚的几何关系，例如“交某线于某点”“交于某线的延长线”“半弧对应的弦”。
- 清楚不等于啰嗦。若一个作图动作可以用一句话准确说明，不得扩写成多句解释；必要背景放入章末注释。
- 《几何原本》等依据不得裸写 `Eucl.` 缩写。正文使用“依据《几何原本》...〔n〕”这类读者可识别标记，章末集中说明对应命题、定义或系的大意。
- 关键句要有画面和记忆点。
- 不接受第一版“通顺但无味”的译文。
- 不得直接写入 `chapters/final/`。

## 章节译后控制 / Post-Translation Control

每章写入 `chapters/translated/` 后，必须立即进入：

- `prompts/08a_chapter_post_translation_control_zh_grc.md`

并创建：

- `qa/chapter_controls/{same_filename}.control.md`

如果用户对该章不满意，AI 必须只回到该章重译，不得让该章继续进入后续审校。其他章节可并行继续，不必全部阻塞。

## 状态 / State

成功后：

- `status = TRANSLATED`
- `chapters_translated = 章节数`
- `current_step = chapters_translated`

注意：`TRANSLATED` 不代表可进入终稿，必须等待每章 control PASS。

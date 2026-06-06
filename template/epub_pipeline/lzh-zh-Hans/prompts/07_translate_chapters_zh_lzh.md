# 07 分章翻译 / Translate Chapters

## 输入

- `chapters/src/*.md`
- `metadata/book_specific_translation_research.md`
- `metadata/style_profile.md`
- `glossary/terms.csv`
- `metadata/classical_chinese_source_profile.md`
- `qa/textual/classical_chinese_textual_notes.md`
- `qa/pretranslation/pretranslation_report.md`

## 前置门禁

只有当 `qa/pretranslation/pretranslation_report.md` 明确 `PASS` 时，才可开始。

## 任务

逐章翻译到：

- `chapters/translated/{same_filename}.md`

每个 passage 默认输出：

```md
<section class="parallel-passage" id="{passage_id}">

古文：
{source_text}

今译：
{modern_translation}

注释：
{必要注释，无则省略}

</section>
```

## 翻译要求

- 保持原文 passage 和今译 passage 对应。
- 不得直接写入 `chapters/final/`。
- 今译必须是现代中文，不是假古文、不是教辅串讲。
- 不得省略人物、动作、否定、因果、语气。
- 必要注释跟随 passage 或记录为章末注。
- 遇到断句、异文、人物关系疑难，先记录再翻译。

## 后续

每章写入 `chapters/translated/` 后，立即执行 `prompts/08a_chapter_post_translation_control_zh_lzh.md`。

## 专家级译文与多义词主动判义及回看 / Expert Quality, Active Polysemy Handling, and Back-Check

翻译调用仍然只输出译文，不输出 QA 或流程记录；但译者必须按 `skills/expert-translation-quality/SKILL.md` 在内部建立观察清单，并在翻译阶段主动判义。遇到多义词、习语、称谓、术语或需要后文判义的语法结构，先用当前句、本段、邻近上下文、术语表、说话人身份、论证功能和可用后文线索判义；能判清的当场处理，不能判清的才用不错误收窄的目标语保留歧义并标记后文回看。不得把局部上下文已能判清的问题留给 `08a`。后文译出后，`08a` 必须回到前文位置复查并必要时修订。观察清单不得进入读者正文。

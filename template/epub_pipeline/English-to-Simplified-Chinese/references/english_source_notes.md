# English Source To Simplified Chinese Notes

本文件只记录英语原文进入简体中文时容易出现的源语言干扰问题。更通用的简体中文译文质量规则见 `template/epub_pipeline/targets/zh-Hans/quality_framework/`。

This file records source-language interference issues that are specific to English source text translated into Simplified Chinese. General Simplified Chinese target-language quality rules live under `template/epub_pipeline/targets/zh-Hans/quality_framework/`.

## English Interference / 英语干扰

- Do not preserve English clause stacking when natural Chinese should split or reorder the sentence.
- 不要保留英文从句堆叠；自然中文需要拆分或重排时，应拆分或重排。
- Do not translate English idioms, honorific nicknames, symbolic object names, or cultural shorthand word-for-word when the result is obscure in Chinese.
- 英语习语、尊称、象征物名和文化简称不能机械逐词硬译；中文读者看不懂时，应转译功能并按需加注。
- In adventure, travel, memoir, and nonfiction prose, distinguish factual precision from English sentence shape. Preserve facts and tone, not English syntax.
- 在探险、旅行、回忆录和纪实文本中，要区分事实准确与英文句形。应保留事实和语气，而不是保留英文语法外壳。
- Watch recurring English words such as `ice`, `ship`, `wind`, `camp`, `trail`, and `flag`; they may need context-specific Chinese choices instead of one fixed translation.
- 注意 `ice`、`ship`、`wind`、`camp`、`trail`、`flag` 等高频英文词；它们往往需要按语境选择中文，而不是固定一个译法。

## Boundary / 边界

Rules about Chinese rhythm, punctuation, paragraph feel, Chinese typography, and Chinese reader experience belong to the Simplified Chinese target framework, not this source-language note.

关于中文节奏、标点、段落气息、中文排版和中文读者体验的规则，属于简体中文目标语言质量框架，不属于本文件。

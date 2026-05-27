# classical-history-zh-Hans Agent Instructions / 古代历史简体中文控制模板 Agent 指令

This file is for AI agents using the `classical-history-zh-Hans` profile overlay.

本文件供使用 `classical-history-zh-Hans` 控制模板的 AI agent 读取。

## Scope / 适用范围

- Target language: Simplified Chinese.
- 目标语言：简体中文。
- Source language: decided by the language-pair template, commonly Literary Chinese (`lzh`) for this profile.
- 原文语言：由语言方向模板决定，本 profile 常与文言文 `lzh` 模板叠加使用。
- Book type: ancient history, chronicles, biographies, statecraft, diplomacy, warfare, ritual, political persuasion, name-heavy or chronology-heavy works.
- 书籍类型：古代历史、编年、列传、政论、外交、战争、礼制、游说、人物关系或年代关系密集文本。

## Mandatory Rules / 强制规则

- Overlay order must be `common -> {source-target} -> profiles/classical-history-zh-Hans`.
- 覆盖顺序必须是 `common -> {source-target} -> profiles/classical-history-zh-Hans`。
- Do not write book-specific source text, translations, QA files, EPUB output, or metadata into this profile directory.
- 不得把具体书籍原文、译文、QA、EPUB 输出或 metadata 写入本 profile 目录。
- Before batch translation, create historical context, named-entity lock, chronology notes, and state-relations records.
- 批量翻译前必须建立历史背景、专名锁定、年代记录和国家/势力关系记录。
- Historical notes may be numerous, but reader-facing notes must solve concrete misunderstanding risks.
- 历史注释可以较多，但读者可见注释必须解决具体误读风险。
- Every chapter with historical actors must pass chapter historical audit before final chapter gate.
- 涉及历史人物的章节必须先通过章节历史审计，才能进入最终章节门禁。

## Hard Stops / 必须停止

- 人物身份、国家归属、年代或事件关系不清楚却继续批量翻译。
- 把现代百科、现代译本或现代商业校注当成隐藏底本。
- 注释缺失导致读者无法判断人物、国家、制度或事件。
- 注释堆成研究论文，压倒正文阅读。

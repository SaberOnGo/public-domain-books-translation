# Language-Neutral Quality Gate Framework

This file defines quality-gate concepts that apply to every translation direction. It intentionally avoids target-language style rules.

本文件定义所有翻译方向都适用的质量门禁概念。它刻意不写入某个目标语言的文体规则。

## Universal Gates / 通用门禁

- Source and rights evidence must exist before translation starts.
- 翻译开始前必须已有来源证据和版权核查记录。
- A book-level research note and style profile must exist before batch translation.
- 批量翻译前必须已有本书专项研究和文体画像。
- Trial translation must pass before full chapter production.
- 试译通过后才能进入整章批量生产。
- Every chapter must pass fidelity, readability, terminology, and final gate checks before it enters `chapters/final/`.
- 每章进入 `chapters/final/` 前，必须通过忠实度、可读性、术语和最终门禁检查。
- EPUB output must pass structural validation before final release.
- 最终发布前，EPUB 必须通过结构校验。
- After each post-EPUB refinement pass, at least two independent review agents must spot-check no fewer than ten random reader-facing paragraphs each; both must pass the recorded score threshold before refinement can be considered complete.
- 每一轮 EPUB 后精校完成后，必须由至少两个独立评审 Agent 各随机抽检不少于十个读者可见正文段落；两个 Agent 都达到记录的评分门槛后，才可认为精校完成。

## What Belongs Elsewhere / 哪些内容不属于这里

- Target-language prose standards belong under `template/epub_pipeline/targets/{target}/`.
- 目标语言文体标准应放在 `template/epub_pipeline/targets/{target}/`。
- Source-language interference rules belong under `template/epub_pipeline/{source-target}/`.
- 源语言干扰规则应放在 `template/epub_pipeline/{source-target}/`。
- Book-specific decisions belong inside `books/{book_id_slug}/`.
- 具体书籍判断应写入 `books/{book_id_slug}/`。

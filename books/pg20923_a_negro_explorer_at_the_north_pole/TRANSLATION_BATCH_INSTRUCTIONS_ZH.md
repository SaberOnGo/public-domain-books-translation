# 分章翻译执行要求

适用于 `chapters/src/*.md` 到 `chapters/translated/*.md`、`chapters/final/*.md` 的翻译与审校。

## 输出目录

- 初译：`chapters/translated/{same_filename}.md`
- 终稿：`chapters/final/{same_filename}.md`
- 忠实度报告：`qa/fidelity/{same_filename}`
- 可读性报告：`qa/readability/{same_filename}`
- 术语报告：`qa/terminology/{same_filename}`

## 翻译要求

- 不使用 Gemini。
- 不做机械直译，不写“AI腔”中文。
- 以中文读者自然阅读为目标，但不改写事实、不增删内容。
- 保留原文件标题层级。
- 专有名词、专业术语、行业术语按 `glossary/terms.csv` 统一。
- 涉及旧时代种族称谓、民族称谓时，尊重历史语境，避免现代误读；必要时保留译者注位置。
- 每个终稿文件必须能独立阅读，段落完整，中文标点统一。

## 审校要求

- 忠实度报告要列出：是否漏译、是否误译、是否有数字/人名/地名错误。
- 可读性报告要列出：是否有生硬直译、是否需要调整语序、是否保留叙事张力。
- 术语报告要列出：术语是否统一。


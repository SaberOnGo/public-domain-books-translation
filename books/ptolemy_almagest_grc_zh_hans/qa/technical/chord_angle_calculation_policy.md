# 《Almagest》弦表、角度与计算校验政策 / Chord, Angle, and Calculation Policy

calculation_policy_status: `PROVISIONAL_FOR_PRETRANSLATION`

## 高风险数值

- 弦表。
- 角度、度、分。
- 六十进制数值。
- 半径与比例。
- 天文观测值。
- 星表与历法表。

## 校验规则

- 保留原文数值格式；不得默认十进制化。
- 若需现代换算，另列换算值、算法和精度。
- 证明中使用的数值必须全量校验。
- 大表先抽查表头、首行、末行、关键节点和异常值；发现漂移后全量校验。
- 表格字段不得散文化。

## Book I 预翻译要求

预翻译样本如涉及弦、角度或表项，必须同时写：

- source location。
- 原文数值。
- 中文保留形式。
- 是否需要现代说明。
- 数学审校意见。

## Book I.11 弦表专项规则

- Book I.11 表格主体未在 PAL XML 中转写，必须从 Heiberg PDF viewer pages `28`-`35` 的 facsimile 影像建立结构化转录。
- 表格不得散文化，也不得用现代三角函数表回填。
- 读者版角度使用 `度/′/″` 保留六十进制含义，例如 `0°30′`，不得只给十进制小数。
- 现代校验可用 `chord = 120 * sin(arc / 2)`，但只能写入 QA 记录或注释，不能替代古代表格本身。
- EPUB 正文必须使用可检索的结构化 XHTML 表格，采用“表分段 + 横向滚动 + 简单 CSS”。
- Book I.11 读者版 EPUB 不放 facsimile crop 旁证图；facsimile crop 只保留在 `source/` 和 `qa/` 中作为转录、复核和争议项证据。

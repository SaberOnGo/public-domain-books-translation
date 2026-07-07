# 18 世纪传记中的赞助、恭维、语言政策隐喻与书信语体

## 适用场景

18 世纪英语传记写到 patronage、dedication、courtly flattery、
periodical praise、language regulation metaphor 或正式书信时，译文很容易
把社会关系、讽刺口吻和制度隐喻译成现代平面中文。

## 发现方式

- 逐章整章复查时，对照赞助人叙事、期刊评论引文和正式书信段落。
- 用 `rg` 扫描高风险译法：`伟人`、`侍候`、`坐在座位上`、
  `把自己.*好感`、`转折得.*精巧`、`被.*故事逗弄`。
- 对照 glossary 中 `patronage_*`、`language_policy`、
  `political_metaphor`、`religious_metaphor`、`document_text`
  等类型的术语行。

## 风险

- `favours from the great` 译成“伟人恩惠”，会把权贵赞助关系误读成
  道德伟大。
- `attendance` 译成“侍候”，会过度仆役化，应按赞助门庭语境译为
  “趋候”“拜候”等。
- `while in the chair` 在教皇隐喻中译成“坐在座位上”，会丢失宗座/
  教席色彩。
- `studied compliments, so finely turned` 若按句法译成“转折得精巧”，
  会误解 `turned` 的修辞雕琢义。
- `insinuate himself with the Sage` 硬译成“嵌进好感”，会留下源语句法壳。

## 修复模式

- 先判定社会关系：赞助人、权贵、题献者、候见者、门房/外间，而不是
  泛泛的“伟人”“朋友”或“服务”。
- 宫廷恭维和讽刺语气要保留手腕感，但中文需顺读：
  “以宫廷式手腕安抚……并慢慢重新讨近他的好感”。
- 语言政策隐喻应显出政治/宗教双关：
  `dictator` 可为“独裁官”，`Pope` 可为“教皇”，
  `in the chair` 可为“坐在圣座上”或按语境译为“在其教席上”。
- 正式书信中 `addressed your Lordship in publick` 应按题献/公开致献
  语境译为“公开向阁下致献”，避免泛化成普通“致意”。

## 复查方法

修复后重新不看原文通读中文，确认赞助关系、讽刺力度、隐喻链和书信尊卑
都能自然成立；再对照源文检查 facts、tone、metaphor、note markers。
若本轮有任何修复，章节 control 的该轮只能记为
`FIXED_RECHECK_REQUIRED`，必须追加整章零问题复查。


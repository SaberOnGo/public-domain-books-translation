# Boswell Unit 069: Club, Religious, and Behavioral Description Interfaces

## 中文经验

- 发现方式：第 69 单元整章译后复查，结合机器注号检查、词表 CSV 解析和源译小上下文对照。
- 问题族：十八世纪传记中的俱乐部入会术语、宗教自省、疑病症与微小行为描写，常把英语压缩表达硬译成中文壳，例如 `black-ball`、`Unelbow'd`、`spiritual improvement`、`period`、`escaped that part of your pain`。
- 风险：俱乐部投票术语会误成普通“黑球”；诗句否定关系若不顺，会反转讽刺意味；宗教语境里的 `spiritual` 若译成泛泛“精神”，会削弱灵性/虔敬层；行为描写若硬译修辞术语，读者会以为在读笔记而不是传记。
- 低 token 审计：先用 `rg -n "黑球|挤肘|精神改善|句段|你痛苦中那一部分|hypochondriack|period|Unelbow"` 扫当前译文、终稿和后续 EPUB XHTML，再只读命中附近源文。
- 修复模式：俱乐部术语译功能，如 `black-ball` 为“投黑球反对入会”；诗句先补足中文否定关系；宗教自省用“灵性增进”“圣餐”“虔敬短祷”等目标语接口；行为细节用日常可视动作重建，如 `concluded a period` 译为“把一整句说完”。
- 复查：修复轮不得 PASS；追加整章复查，确认注号、引语、诗句、祷文、病症、行为动作和信件署址全部闭环。

## English Note

- Finding method: full-chapter post-translation review with note-order checks, glossary CSV parsing, and source-target comparison.
- Family: club admission terms, religious self-accusation, hypochondria, and minute behavioral descriptions can become literal shells in Chinese.
- Fix pattern: translate the function and scene relation first, preserve source interfaces only for approved proper nouns, and recheck quotation logic plus devotional wording after each repair.

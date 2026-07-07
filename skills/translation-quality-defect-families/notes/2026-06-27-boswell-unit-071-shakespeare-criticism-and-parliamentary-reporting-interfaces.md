# Boswell Unit 071: Shakespeare Criticism and Parliamentary Reporting Interfaces

## 中文经验

- 发现方式：第 71 单元整章译后复查，结合注号检查、裸英文扫描、术语展示策略检查和附录 A 小上下文对照。
- 问题族：传记正文转入文学批评和议会出版史时，容易出现三类问题：普通情感词裸留英文；历史身份/制度术语机械括源词；遮名如 `Sir R----t W----le` 被当成普通人名括注，造成读者误以为是重复译名。
- 风险：裸英文破坏出版完成度；术语括源词会让连续中文变成词表；遮名接口处理不当会损害附录对十八世纪议会报道规避机制的说明。
- 低 token 审计：先扫 `affection|Squire）|publick|known|WHIG DOGS|Sir R----t|P--lh--m|Gent. Mag|Parl. Hist`，覆盖译稿、终稿、词表和生成 XHTML；命中后只读相邻源文。
- 修复模式：普通抽象词直接中文化，如 `affection` 为“亲爱之情”；历史身份术语如 `Squire` 正文只用“乡绅”，源词留在术语表；遮名保留源形但用“化名为 / 写作”说明功能；缩略书刊名用中文书名加源缩写接口。
- 复查：修复轮不得 PASS；追加整章复查，确认注号、遮名、书刊缩写、议会特权逻辑和文学批评比喻全部闭环。

## English Note

- Finding method: full-chapter review with note-order checks, naked-English scanning, source-display policy checks, and Appendix A source comparison.
- Family: literary criticism and parliamentary-reporting appendices often combine ordinary abstractions, historical status terms, masked names, and abbreviated citations; each needs a different Chinese interface.
- Fix pattern: translate ordinary abstractions fully, keep historical term source forms out of continuous body prose unless the form itself is under discussion, and explain masked names as disguises rather than treating them as ordinary first-mention proper nouns.

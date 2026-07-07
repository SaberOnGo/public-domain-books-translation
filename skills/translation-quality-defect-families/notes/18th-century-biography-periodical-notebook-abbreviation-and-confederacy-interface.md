# 18 世纪传记中的期刊名、札记缩写与结盟论证接口

## 中文经验

传记章节进入期刊写作和作者札记时，风险不在普通叙事，而在“半成品材料”的接口：缩写、拉丁/希腊片语、期刊题名、概率式论证都容易被译得过直或方向相反。

- 期刊名先查全书专名表，避免同一作品在相邻章节漂移成两个译名。若 `The Rambler` 已锁定为《漫游者》，`Rambler` 的短名行和术语行也要同步。
- 作者札记可保留提纲感，但不能把 `bus.`、`reflect.`、`impercept. gradat.` 等缩写裸留给读者。应译出功能性中文，必要时只在首次或正在讨论缩写形式时保留源文接口。
- 拉丁/希腊片语在札记中即使是残片，也要给中文读者一个可用接口。若源文形式本身不是讨论对象，优先译意；若必须呈现源文，应邻接中文说明。
- 概率、赔率、比较式论证要单独回看。`if two to one against two, how many against five?` 这类压缩句不是普通条件句，必须判断它是在说“可能性有利”还是“不利”。

低 token 审计方法：先用专名表查题名一致性，再扫 `Rambler|notanda|Adversaria|bus.|reflect.|gradat.|confederacies|centrifugal` 等候选；只把命中的札记小段同源文对照，重点检查缩写是否可读、外文是否有中文接口、比较/概率方向是否正确。任何修复后都要追加整章复查，修复轮不能 PASS。

## English Note

When an eighteenth-century biography quotes periodical notebooks or preparatory essay hints, treat abbreviations and foreign-language fragments as reader-interface risks. Preserve the sketch-like rhythm, but translate abbreviated functions into target-language prose. Audit title consistency across glossary rows, and recheck compressed probability or comparison logic before passing the chapter.

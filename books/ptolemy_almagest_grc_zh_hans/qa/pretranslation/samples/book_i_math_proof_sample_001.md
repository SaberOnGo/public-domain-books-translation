# Book I 小样本预翻译 001 / Book I Micro Pretranslation Sample 001

sample_status: `NEEDS_MATH_REVIEW_NOT_FORMAL_TRANSLATION`

## 范围 / Scope

- work: Ptolemy, `Mathematike Syntaxis` / `Almagest`
- book: Book I
- chapter: I.10, chord-table geometry preparation
- source_basis: Heiberg Greek text as represented in the local facsimile and checked against PAL Heiberg transcription for this micro-sample only
- publication_use: forbidden
- copied_to_translation_dirs: no

## 原文控制 / Source Control

This sample is intentionally short and exists only to test proof-language controls. Before any formal translation, the same passage must be checked against the local PDF page image or an approved transcription.

## 术语锁定 / Term Locks Used

| concept | Chinese term | lock_level |
|---|---|---|
| setup/suppose | 设 | PILOT_LOCKED |
| construct | 作 | PILOT_LOCKED |
| join | 连结 | PILOT_LOCKED |
| intersect | 交于 | PILOT_LOCKED |
| chord | 弦 | PILOT_LOCKED |
| proportion | 成比例 | PILOT_LOCKED |
| equality | 相等 | PILOT_LOCKED |

## 预翻译样本 / Trial Translation

设圆 ABCD，其直径为 AC；又设其中一条弦为 AB。连结从圆心到各端点的直线，并按图中关系作辅助线。由于半径相等，相关三角形中的对应边与对应角必须逐项保持；凡由相似三角形推出的比例，译文必须明确写出“成比例”，不得省作普通叙述。

若一条线段由构造而与另一条线段相等，译文必须说明其相等来自构造、半径或前一命题；若比例关系依赖前一相似关系，译文不得跳步。图中点名 A、B、C、D 等必须与重绘图完全一致。

## 数学/天文学校对 / Technical Audit

| check | status | note |
|---|---|---|
| proof actions preserved | PASS_FOR_SAMPLE | setup, construction, joining, equality, and proportion are explicit |
| diagram dependency visible | PASS_FOR_SAMPLE | text requires point-label match before redraw |
| numeric/table risk | N/A | sample is proof prose, not the chord table itself |
| Greek source verified from local PDF image | OPEN | requires page rendering or approved transcription |
| reference translation used as pivot | NO | no modern English translation used as base |

## 译者注释策略 / Annotation Policy

For formal translation, explanatory notes may clarify that this is chord-table geometry, but the main text must not replace Ptolemy's proof with a modern trigonometric derivation. Any modern sine/cosine explanation belongs in a translator note after the literal proof relation is preserved.

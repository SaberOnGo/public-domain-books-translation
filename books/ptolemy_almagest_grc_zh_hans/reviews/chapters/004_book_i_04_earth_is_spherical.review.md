# Book I.4 译后评审 / Post-Translation Review

review_status: `PASS_FOR_DRAFT_REVIEW__FINAL_PENDING`
chapter_id: `004_book_i_04_earth_is_spherical`
reviewer: `Codex self-review`
review_date: `2026-05-17`
translation: `chapters/translated/004_book_i_04_earth_is_spherical.md`
source: `chapters/src/004_book_i_04_earth_is_spherical.md`

## 控制结论

- 本评审只允许 Book I.4 继续进入译后技术复核和后续章节门禁。
- 本评审不允许写 `chapters/final/004_book_i_04_earth_is_spherical.md`，不允许生成正式 EPUB。
- 未发现 P0/P1 阻断问题；仍需后续技术复核和终稿前全书一致性审校。

## 综合评分

| 维度 | 满分 | 得分 | 说明 |
|---|---:|---:|---|
| 古希腊文忠实度 | 20 | 18 | 译文保留月食时刻证据、东西向升落差异、形状反证、南北星象变化和航近高地证据。 |
| 参考译本边界 | 10 | 10 | 译文说明明确英译本只作 reference witness；未出现英译转写痕迹。 |
| 术语一致性 | 15 | 14 | `感官观察所及`、`食象`、`离正午相等`、`凸曲`、`圆柱形`、`世界的两极` 与 I.4 术语预锁一致。 |
| 古今概念边界 | 15 | 14 | 正文没有改写为现代测地学、时区制度、地球椭球或大地水准面；章末注集中说明边界。 |
| 中文可读性 | 20 | 18 | 论证链分段清楚，反证句已现代化表达；少数术语仍需在后续地理章节统一。 |
| 结构与注释 | 10 | 9 | 注释覆盖感官观察、月食记录、天极、北方方位和水面凸曲。 |
| 工程/门禁 | 10 | 10 | source、formal recheck、chapter control、translation check 均已存在并接入 `quality:all`。 |
| total | 100 | 93 | PASS_FOR_DRAFT_REVIEW |

## P0/P1 检查

| issue type | result | note |
|---|---|---|
| 公版/底本边界不清 | PASS | source 文件和 metadata 已记录 Heiberg PDF + PAL Greek roles |
| 参考译本转译 | PASS | 未发现英译作为底稿的证据 |
| 整章漏译 | PASS | I.4 主要论证段落均已覆盖 |
| 严重误读 | PASS | 未发现会改变章节主旨的误读 |
| 术语系统性错误 | PASS_WITH_NOTE | `食象`、`正午`、`世界的两极` 后续需同地理/黄道章节统一 |
| 古今概念混淆 | PASS_WITH_NOTE | 注释已处理；后续技术复核需继续防止改写成现代时区或测地学说明 |

## 细节意见

- `就感官观察所及`：准确保留 `πρὸς αἴσθησιν` 的证明限定，避免把本章写成现代测地学。
- `食象` 和 `月食`：译文保留“同一食象、各地记录小时不同”的证据链；章末注说明不等同现代时区。
- 形状反证链：凹面、平面、多边形、圆柱形均已保留，未压缩为单句结论。
- `世界的两极`：保留古代天球语境；终稿可考虑统一为“天极”并注出原文。
- `水面有凸曲`：保留航海观察证据，不改写为现代光学或测量学术语。

## 下一步

1. 创建或更新 Book I.4 译后技术复核记录。
2. 检查 Book I.4 术语是否需要写入全书 glossary / terminology change log。
3. 只有技术复核、忠实度/可读性/术语门禁全部通过后，才可考虑 `chapters/final/`。

# Book I.6 译后评审 / Post-Translation Review

review_status: `PASS_FOR_DRAFT_REVIEW__FINAL_PENDING`
chapter_id: `006_book_i_06_earth_as_point_to_heavens`
reviewer: `Codex self-review`
review_date: `2026-05-17`
translation: `chapters/translated/006_book_i_06_earth_as_point_to_heavens.md`
source: `chapters/src/006_book_i_06_earth_as_point_to_heavens.md`

## 控制结论

- 本评审只允许 Book I.6 继续进入译后技术复核和后续章节门禁。
- 本评审不允许写 `chapters/final/006_book_i_06_earth_as_point_to_heavens.md`，不允许生成正式 EPUB。
- 未发现 P0/P1 阻断问题；仍需后续技术复核和终稿前全书一致性审校。

## 综合评分

| 维度 | 满分 | 得分 | 说明 |
|---|---:|---:|---|
| 古希腊文忠实度 | 20 | 18 | 译文保留“点的比例”命题、相对于恒星天球距离的可感尺度、各地观测无差异、仪器中心视同地心、地平平面二分天球。 |
| 参考译本边界 | 10 | 10 | 译文说明明确英译本只作 reference witness；未出现英译转写痕迹。 |
| 术语一致性 | 15 | 13 | `恒星天球`、`气候带`、`晷针`、`环仪`、`地平圈`、`二分` 与 I.6 术语预锁一致；`环仪` 后续需同仪器术语统一。 |
| 古今概念边界 | 15 | 14 | 正文没有改写成现代视差、现代恒星测距或现代地球半径比例；章末注集中说明边界。 |
| 中文可读性 | 20 | 18 | 原文长句已拆成五个推理段落，证明链清楚。 |
| 结构与注释 | 10 | 9 | 注释覆盖点的比例、恒星天球、气候带、晷针/环仪、地平圈。 |
| 工程/门禁 | 10 | 10 | source、formal recheck、chapter control、translation check 均已存在并接入 `quality:all`。 |
| total | 100 | 92 | PASS_FOR_DRAFT_REVIEW |

## P0/P1 检查

| issue type | result | note |
|---|---|---|
| 公版/底本边界不清 | PASS | source 文件和 metadata 已记录 Heiberg PDF + PAL Greek roles |
| 参考译本转译 | PASS | 未发现英译作为底稿的证据 |
| 整章漏译 | PASS | I.6 主要论证段落均已覆盖 |
| 严重误读 | PASS | 未发现会改变章节主旨的误读 |
| 术语系统性错误 | PASS_WITH_NOTE | `环仪` 后续需同仪器术语统一 |
| 古今概念混淆 | PASS_WITH_NOTE | 注释已处理；后续技术复核需继续防止改写成现代视差或测距说明 |

## 细节意见

- `只相当于一点`：准确处理 `σημείου λόγον ἔχει`，正文可读，注释保留字面“点的比例”。
- `恒星天球`：译文保留古代固定星天球语境，不改写为现代恒星空间。
- `各地观测无差异`：译文保留“同一时刻、不同气候带、星体大小和间距相同”的证据链。
- `晷针/环仪`：译文保留仪器中心可视同地心的观测论证；终稿前需与全书仪器术语统一。
- `地平圈二分天球`：译文保留如果地球大小可感，则地表平面会使地下部分大于地上部分的反证。

## 下一步

1. 创建或更新 Book I.6 译后技术复核记录。
2. 检查 Book I.6 术语是否需要写入全书 glossary / terminology change log。
3. 只有技术复核、忠实度/可读性/术语门禁全部通过后，才可考虑 `chapters/final/`。

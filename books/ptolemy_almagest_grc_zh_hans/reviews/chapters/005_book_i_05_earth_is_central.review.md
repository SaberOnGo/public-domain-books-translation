# Book I.5 译后评审 / Post-Translation Review

review_status: `PASS_FOR_DRAFT_REVIEW__FINAL_PENDING`
chapter_id: `005_book_i_05_earth_is_central`
reviewer: `Codex self-review`
review_date: `2026-05-17`
translation: `chapters/translated/005_book_i_05_earth_is_central.md`
source: `chapters/src/005_book_i_05_earth_is_central.md`

## 控制结论

- 本评审只允许 Book I.5 继续进入译后技术复核和后续章节门禁。
- 本评审不允许写 `chapters/final/005_book_i_05_earth_is_central.md`，不允许生成正式 EPUB。
- 未发现 P0/P1 阻断问题；仍需后续技术复核和终稿前全书一致性审校。

## 综合评分

| 维度 | 满分 | 得分 | 说明 |
|---|---:|---:|---|
| 古希腊文忠实度 | 20 | 18 | 译文保留地球居中命题、三种非居中位置、地平圈等分、二分/昼夜证据、东西地平与中天时间、月食反证。 |
| 参考译本边界 | 10 | 10 | 译文说明明确英译本只作 reference witness；未出现英译转写痕迹。 |
| 术语一致性 | 15 | 13 | `天球中央`、`球心`、`天轴`、`地平圈`、`中天`、`气候带` 与 I.5 术语预锁一致；`正球/斜球` 后续需与球面天文学章节统一。 |
| 古今概念边界 | 15 | 14 | 正文没有改写为现代物理中心、现代坐标系、牛顿力学或现代天体力学；章末注集中说明边界。 |
| 中文可读性 | 20 | 17 | 长周期句已拆分；三种反证结构可读。黄道十二分宫段仍较密，终稿前可进一步润色。 |
| 结构与注释 | 10 | 9 | 注释覆盖天球中央、正球/斜球、中天、黄道十二分宫、气候带和月食反证。 |
| 工程/门禁 | 10 | 10 | source、formal recheck、chapter control、translation check 均已存在并接入 `quality:all`。 |
| total | 100 | 91 | PASS_FOR_DRAFT_REVIEW |

## P0/P1 检查

| issue type | result | note |
|---|---|---|
| 公版/底本边界不清 | PASS | source 文件和 metadata 已记录 Heiberg PDF + PAL Greek roles |
| 参考译本转译 | PASS | 未发现英译作为底稿的证据 |
| 整章漏译 | PASS | I.5 主要论证段落均已覆盖 |
| 严重误读 | PASS | 未发现会改变章节主旨的误读 |
| 术语系统性错误 | PASS_WITH_NOTE | `正球/斜球`、`气候带`、`黄道十二分宫` 后续需同 I.12-I.16 球面天文学章节统一 |
| 古今概念混淆 | PASS_WITH_NOTE | 注释已处理；后续技术复核需继续防止改写成现代坐标系或力学说明 |

## 细节意见

- `地球位于天球中央、如同球心`：准确保留 `μέση τοῦ οὐρανοῦ` 和 `κέντρον σφαίρας` 的模型关系。
- 三种非居中位置：译文保留“不在天轴上但距两极相等 / 在天轴上偏向一极 / 既不在天轴上也不距两极相等”的反证结构。
- `地平圈`：正文保留地平圈对地上/地下部分的几何分割，不改写成现代可视地平线说明。
- `黄道十二分宫`：译文按原文保留六个可见、六个不可见的等分论证；终稿前可在注释中统一“分宫/十二分段”的术语。
- `月食`：末段保留月亮与太阳径直相对时地球遮挡的古代几何模型，不改写为现代天体力学。

## 下一步

1. 创建或更新 Book I.5 译后技术复核记录。
2. 检查 Book I.5 术语是否需要写入全书 glossary / terminology change log。
3. 只有技术复核、忠实度/可读性/术语门禁全部通过后，才可考虑 `chapters/final/`。

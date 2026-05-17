# Book I.7 译后评审 / Post-Translation Review

review_status: `PASS_FOR_DRAFT_REVIEW__FINAL_PENDING`
chapter_id: `007_book_i_07_earth_has_no_translational_motion`
reviewer: `Codex self-review`
review_date: `2026-05-17`
translation: `chapters/translated/007_book_i_07_earth_has_no_translational_motion.md`
source: `chapters/src/007_book_i_07_earth_has_no_translational_motion.md`

## 控制结论

- 本评审只允许 Book I.7 继续进入译后技术复核和后续章节门禁。
- 本评审不允许写 `chapters/final/007_book_i_07_earth_has_no_translational_motion.md`，不允许生成正式 EPUB。
- 未发现 P0/P1 阻断问题；仍需后续技术复核和终稿前全书一致性审校。

## 综合评分

| 维度 | 满分 | 得分 | 说明 |
|---|---:|---:|---|
| 古希腊文忠实度 | 20 | 18 | 译文保留地球无平移运动、重物趋向中心、切平面垂直关系、上/下方向定义、地球自转设想和空气现象反驳。 |
| 参考译本边界 | 10 | 10 | 译文说明明确英译本只作 reference witness；未出现英译转写痕迹。 |
| 术语一致性 | 15 | 13 | `平移运动`、`切平面`、`上/下`、`旋转`、`飞行物/抛射物` 与 I.7 术语预锁一致；`φορά` 的“运动/载动/趋向运动”需后续全书统一。 |
| 古今概念边界 | 15 | 14 | 正文没有改写成现代惯性、参照系、角速度、科里奥利力或真实地球自转说明；章末注集中说明边界。 |
| 中文可读性 | 20 | 17 | 长周期句已拆分，证明链可跟读；“违反自然的设想”一段仍偏密，终稿可再润色。 |
| 结构与注释 | 10 | 9 | 注释覆盖平移/旋转区别、切平面、上/下方向、自转设想和回转概念。 |
| 工程/门禁 | 10 | 10 | source、formal recheck、chapter control、translation check 均已存在；尚需接入 `quality:all`。 |
| total | 100 | 91 | PASS_FOR_DRAFT_REVIEW |

## P0/P1 检查

| issue type | result | note |
|---|---|---|
| 公版/底本边界不清 | PASS | source 文件和 metadata 已记录 Heiberg PDF + PAL Greek roles |
| 参考译本转译 | PASS | 未发现英译作为底稿的证据 |
| 整章漏译 | PASS | I.7 主要论证段落均已覆盖 |
| 严重误读 | PASS | 未发现会改变章节主旨的误读；地球每日自转设想已明确为被反驳对象 |
| 术语系统性错误 | PASS_WITH_NOTE | `φορά` 后续需在全书范围内按语境统一 |
| 古今概念混淆 | PASS_WITH_NOTE | 注释已处理；后续技术复核需继续防止现代惯性/参照系解释进入正文 |

## 细节意见

- `平移运动`：准确处理 `κίνησιν ... μεταβατικήν`，并在注释中同绕轴旋转区分。
- `切平面成直角`：译文使用现代几何中文提升可读性，没有增加原文外的证明。
- `上/下方向`：译文保留“上朝外围、下向地心”的古代球形宇宙方向定义。
- `地球每日自转设想`：译文明确这是托勒密列举并反驳的说法，避免读者误以为本章接受地球自转。
- `空气现象反驳`：译文保留云、飞行物、抛射物、滞后/不滞后的核心推理链。

## 下一步

1. 创建或更新 Book I.7 译后技术复核记录。
2. 检查 Book I.7 术语是否需要写入全书 glossary / terminology change log。
3. 只有技术复核、忠实度/可读性/术语门禁全部通过后，才可考虑 `chapters/final/`。

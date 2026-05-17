# Book I.5 章节控制 / Chapter Control

chapter_file: `005_book_i_05_earth_is_central.md`
source_path: `chapters/src/005_book_i_05_earth_is_central.md`
translated_path: `chapters/translated/005_book_i_05_earth_is_central.md`
human_required: false
human_feedback_status: `none`
control_status: `PASS_FOR_CONTROLLED_TRANSLATION_PREP__NOT_TRANSLATED`
return_to_stage: `07_translate_chapters`

## 范围

本控制只覆盖 Book I.5 的受控翻译准备。它不允许写 `chapters/final/`，不允许生成正式 EPUB，也不允许把本章的 source recheck 通过状态解释为全书可批量翻译。

## 已满足的前置条件

| check | result | evidence |
|---|---|---|
| source candidate exists | PASS | `chapters/src/005_book_i_05_earth_is_central.md` |
| source extraction check | PASS | `qa/pretranslation/005_book_i_05_source_extraction_check.md` |
| formal source recheck | PASS | `qa/pretranslation/005_book_i_05_formal_source_recheck.md` |
| PDF page evidence | PASS_FOR_PREP | `qa/technical/page_screenshots/book_i05_pages_012_014_contact_sheet.jpg` |
| technical audit | PASS_FOR_PREP | `qa/technical/005_book_i_05_earth_is_central.technical_audit.md` |
| term prelock | PASS_FOR_PREP | `qa/technical/mathematical_term_lock.md` |

## 翻译控制要求

| risk | required handling |
|---|---|
| 主命题 | 保留“地球位于天球中央/如球心”的古代天文学模型命题，不改写为现代物理中心或惯性系说明。 |
| 三种非居中位置 | 保留轴外且距两极相等、在轴上偏向一极、不在轴上且距两极不等的三分反证结构。 |
| 地平圈等分 | 保留地平圈对地上/地下部分的等分或不等分论证，不压缩为现代几何结论。 |
| 二分点/昼夜证据 | 保留二分、夏至/冬至最大日长变化与观测事实之间的推理关系。 |
| 东西地平和中天时间 | 保留从升起到中天、从中天到落下的时间对称性，以及东西地平处星体大小/距离的相同观测。 |
| 气候带与地平面 | `κλίματα` 暂译为“气候带/纬度带”；不得现代化为气候学区域。 |
| 英译本参考 | 英译本只作 reference witness，不得作为中文句子的转译底稿。 |
| 中文可读性 | 允许拆分长周期句；但不得删掉“三种非居中位置 → 观测反证 → 地球居中”的证明链。 |
| 注释策略 | 对天球中央、正球/斜球、二分、地平圈、中天和气候带，可在章末集中注释。 |

## 禁止项

- 不得写 `chapters/final/005_book_i_05_earth_is_central.md`。
- 不得生成正式 `output/book.epub`。
- 不得把英译本句式当作底稿。
- 不得把本章写成现代天体力学、现代坐标系、牛顿力学或现代地心惯性系说明。
- 不得省略三种非居中位置、地平圈等分、二分点/昼夜证据、东西地平和中天时间证据。
- 不得提前翻译 Book I.11 弦表或进入全书批量翻译。

## 自动结论

Book I.5 可以进入受控翻译准备；翻译完成后必须继续执行章节控制复核、技术审计复核、忠实度审校、可读性审校、术语审校和章节质量门禁。当前仍未翻译，不能进入终稿。

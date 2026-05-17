# Book I.6 章节控制 / Chapter Control

chapter_file: `006_book_i_06_earth_as_point_to_heavens.md`
source_path: `chapters/src/006_book_i_06_earth_as_point_to_heavens.md`
translated_path: `chapters/translated/006_book_i_06_earth_as_point_to_heavens.md`
human_required: false
human_feedback_status: `none`
control_status: `PASS_FOR_CONTROLLED_TRANSLATION_PREP__NOT_TRANSLATED`
return_to_stage: `07_translate_chapters`

## 范围

本控制只覆盖 Book I.6 的受控翻译准备。它不允许写 `chapters/final/`，不允许生成正式 EPUB，也不允许把本章的 source recheck 通过状态解释为全书可批量翻译。

## 已满足的前置条件

| check | result | evidence |
|---|---|---|
| source candidate exists | PASS | `chapters/src/006_book_i_06_earth_as_point_to_heavens.md` |
| source extraction check | PASS | `qa/pretranslation/006_book_i_06_source_extraction_check.md` |
| formal source recheck | PASS | `qa/pretranslation/006_book_i_06_formal_source_recheck.md` |
| PDF page evidence | PASS_FOR_PREP | `qa/technical/page_screenshots/book_i06_page_014_contact_sheet.jpg` |
| technical audit | PASS_FOR_PREP | `qa/technical/006_book_i_06_earth_as_point_to_heavens.technical_audit.md` |
| term prelock | PASS_FOR_PREP | `qa/technical/mathematical_term_lock.md` |

## 翻译控制要求

| risk | required handling |
|---|---|
| 主命题 | 保留“地球相对于天体只相当于一点/具有点的比例”的古代尺度命题，不改写为现代地球半径或恒星距离计算。 |
| 可感尺度限定 | `πρὸς αἴσθησιν` 应保留为“就感官观察而言/就可见现象而言”，避免写成绝对物理命题。 |
| 恒星天球距离 | `ἀπλανῶν σφαῖρα` 译为“恒星天球/固定星天球”；不得解释为现代恒星空间分布。 |
| 各地观测无差异 | 保留各地观测星体大小、间距在同一时间相同的经验证据，不压缩成一句“因为看不出差别”。 |
| 晷针与环仪中心 | 保留晷针、环仪中心可视同地心的仪器论证；不得现代化为望远镜或现代观测台几何。 |
| 地平平面 | 保留“由视线引出的平面，即所谓地平圈/地平面”的定义关系。 |
| 天球二分 | 明确地平平面总是二分整全天球；若地球大小可感，则地表处平面会使地下部分大于地上部分。 |
| 英译本参考 | 英译本只作 reference witness，不得作为中文句子的转译底稿。 |
| 中文可读性 | 可拆分长周期句；但不得删掉“观测无差异 → 仪器中心等同地心 → 地平平面二分天球 → 地球大小不可感”的证明链。 |
| 注释策略 | 对“点的比例”、恒星天球、晷针、环仪、地平平面和二分天球，可在章末集中注释。 |

## 禁止项

- 不得写 `chapters/final/006_book_i_06_earth_as_point_to_heavens.md`。
- 不得生成正式 `output/book.epub`。
- 不得把英译本句式当作底稿。
- 不得把本章写成现代视差、现代恒星测距、现代地球半径比例或近代天文学教材说明。
- 不得省略各地观测无差异、仪器中心等同地心、地平平面二分天球、地球大小不可感的证明链。
- 不得提前翻译 Book I.11 弦表或进入全书批量翻译。

## 自动结论

Book I.6 可以进入受控翻译准备；翻译完成后必须继续执行章节控制复核、技术审计复核、忠实度审校、可读性审校、术语审校和章节质量门禁。当前仍未翻译，不能进入终稿。

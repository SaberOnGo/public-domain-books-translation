# Book I.7 章节控制 / Chapter Control

chapter_file: `007_book_i_07_earth_has_no_translational_motion.md`
source_path: `chapters/src/007_book_i_07_earth_has_no_translational_motion.md`
translated_path: `chapters/translated/007_book_i_07_earth_has_no_translational_motion.md`
human_required: false
human_feedback_status: `none`
control_status: `PASS_FOR_CONTROLLED_TRANSLATION_PREP__NOT_TRANSLATED`
return_to_stage: `07_translate_chapters`

## 范围

本控制只覆盖 Book I.7 的受控翻译准备。它不允许写 `chapters/final/`，不允许生成正式 EPUB，也不允许把本章的 source recheck 通过状态解释为全书可批量翻译。

## 已满足的前置条件

| check | result | evidence |
|---|---|---|
| source candidate exists | PASS | `chapters/src/007_book_i_07_earth_has_no_translational_motion.md` |
| source extraction check | PASS | `qa/pretranslation/007_book_i_07_source_extraction_check.md` |
| formal source recheck | PASS | `qa/pretranslation/007_book_i_07_formal_source_recheck.md` |
| PDF page evidence | PASS_FOR_PREP | `qa/technical/page_screenshots/book_i07_pages_015_017_contact_sheet.jpg` |
| technical audit | PASS_FOR_PREP | `qa/technical/007_book_i_07_earth_has_no_translational_motion.technical_audit.md` |
| term prelock | PASS_FOR_PREP | `qa/technical/mathematical_term_lock.md` |

## 翻译控制要求

| risk | required handling |
|---|---|
| 主命题 | 保留“地球没有平移运动/不会离开中心处所”的命题；不得误写成只讨论地球自转。 |
| 论证连续性 | 必须接续 Book I.5-I.6 的地球居中、点的比例和地平/观测尺度论证，不可单独抽象成一段自然哲学短论。 |
| 重物趋向中心 | `τὰ βάρη` 和 `ἐπὶ τὸ κέντρον` 按古代自然运动译为“重物趋向中心/向中心运动”，不得改写为现代重力理论。 |
| 切平面垂直关系 | 可译为“落下处的切平面”“与切平面成直角”，使现代中文可读；不得增加原文没有的几何推导。 |
| 上下方向 | 保留古代球形宇宙中“上”朝外围、“下”朝地心的方向定义，必要时章末注说明。 |
| 地球整体静止 | `ἀτρεμοῦσα`、`μήτε βεβηκέναι ... μήτε φέρεσθαι` 应译清“静止/未被载动”，不得写成现代惯性静止。 |
| 地球每日自转设想 | 必须明确这是托勒密列举并反驳的设想：天不动、地球每日从西向东绕同一轴旋转，或二者以协调方式运动。 |
| 空气现象反驳 | 保留云、飞行物、抛射物应显得滞后的反证链；不得用现代大气共转或惯性系知识改写。 |
| 英译本参考 | 英译本只作 reference witness，不得作为中文句子的转译底稿。 |
| 中文可读性 | 可拆分长周期句；但不得删掉“地球居中与重物趋心 → 上下方向相对定义 → 地球若整体运动将荒谬 → 自转设想与空气现象反驳”的证明链。 |
| 注释策略 | 对“平移运动/旋转区别”“上/下方向”“重物趋向中心”“地球每日自转设想”“空气现象反驳”集中章末注释。 |

## 禁止项

- 不得写 `chapters/final/007_book_i_07_earth_has_no_translational_motion.md`。
- 不得生成正式 `output/book.epub`。
- 不得把英译本句式当作底稿。
- 不得把本章写成现代惯性、参照系、地球真实自转或科里奥利力说明。
- 不得省略地球居中、重物趋心、上/下方向定义、自转设想、空气与飞行/抛射现象反驳的证明链。
- 不得提前翻译 Book I.11 弦表或进入全书批量翻译。

## 自动结论

Book I.7 可以进入受控翻译准备；翻译完成后必须继续执行章节控制复核、技术审计复核、忠实度审校、可读性审校、术语审校和章节质量门禁。当前仍未翻译，不能进入终稿。

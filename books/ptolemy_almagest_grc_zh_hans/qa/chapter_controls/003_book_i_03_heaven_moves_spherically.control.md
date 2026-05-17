# Book I.3 章节控制 / Chapter Control

chapter_file: `003_book_i_03_heaven_moves_spherically.md`
source_path: `chapters/src/003_book_i_03_heaven_moves_spherically.md`
translated_path: `chapters/translated/003_book_i_03_heaven_moves_spherically.md`
human_required: false
human_feedback_status: `none`
control_status: `PASS_FOR_CONTROLLED_TRANSLATION_PREP__NOT_TRANSLATED`
return_to_stage: `07_translate_chapters`

## 范围

本控制只覆盖 Book I.3 的受控翻译准备。它不允许写 `chapters/final/`，不允许生成正式 EPUB，也不允许把本章的 source recheck 通过状态解释为全书可批量翻译。

## 已满足的前置条件

| check | result | evidence |
|---|---|---|
| source candidate exists | PASS | `chapters/src/003_book_i_03_heaven_moves_spherically.md` |
| source extraction check | PASS | `qa/pretranslation/003_book_i_03_source_extraction_check.md` |
| formal source recheck | PASS | `qa/pretranslation/003_book_i_03_formal_source_recheck.md` |
| PDF page evidence | PASS_FOR_PREP | `qa/technical/page_screenshots/book_i03_pages_009_011_contact_sheet.jpg` |
| technical audit | PASS_FOR_PREP | `qa/technical/003_book_i_03_heaven_moves_spherically.technical_audit.md` |
| term prelock | PASS_FOR_PREP | `qa/technical/mathematical_term_lock.md` |

## 翻译控制要求

| risk | required handling |
|---|---|
| 主命题 | 保留“天以球形方式运动”的古代数学天文学命题，不改写成现代自转/公转或物理动力学说明。 |
| 观测链 | 保留日月星从东向西、平行圆升落、恒显星绕极旋转等观测顺序。 |
| 反证链 | 保留对“星体沿直线向无穷远运动”的反证问答结构，不压缩为一句结论。 |
| 地平处视大小 | `ἀναθυμίασις` 暂译为蒸腾气/湿气蒸腾；不得直接现代化为大气折射。 |
| 几何论证 | 保留圆、球、同周长多边形、最大形体等古代几何比较。 |
| 自然学论证 | `αἰθήρ`、`ὁμοιομέρεια` 等术语必须保留古代自然学边界，不现代化为现代物理以太或材料科学。 |
| 英译本参考 | 英译本只作 reference witness，不得作为中文句子的转译底稿。 |
| 中文可读性 | 允许拆分长周期句；但不得删掉“观测 → 反证 → 几何论证 → 自然学论证”的证明链。 |
| 注释策略 | 对恒显星、天球极、地平处视大小、以太和同质性等术语，可在章末集中注释。 |

## 禁止项

- 不得写 `chapters/final/003_book_i_03_heaven_moves_spherically.md`。
- 不得生成正式 `output/book.epub`。
- 不得把英译本句式当作底稿。
- 不得把本章写成现代天体物理或大气光学说明。
- 不得省略反证链和古代自然学论证。
- 不得提前翻译 Book I.11 弦表或进入全书批量翻译。

## 自动结论

Book I.3 可以进入受控翻译准备；翻译完成后必须继续执行章节控制复核、技术审计复核、忠实度审校、可读性审校、术语审校和章节质量门禁。当前仍未翻译，不能进入终稿。

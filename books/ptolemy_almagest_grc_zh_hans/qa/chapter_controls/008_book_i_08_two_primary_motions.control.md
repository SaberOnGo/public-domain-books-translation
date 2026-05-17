# Book I.8 章节控制 / Chapter Control

chapter_file: `008_book_i_08_two_primary_motions.md`
source_path: `chapters/src/008_book_i_08_two_primary_motions.md`
translated_path: `chapters/translated/008_book_i_08_two_primary_motions.md`
human_required: false
human_feedback_status: `none`
control_status: `PASS_FOR_CONTROLLED_TRANSLATION_PREP__NOT_TRANSLATED`
return_to_stage: `07_translate_chapters`

## 范围

本控制只覆盖 Book I.8 的受控翻译准备。它不允许写 `chapters/final/`，不允许生成正式 EPUB，也不允许把本章的 source recheck 通过状态解释为 Book I 已完成或可进入 Book II。

## 已满足的前置条件

| check | result | evidence |
|---|---|---|
| source candidate exists | PASS | `chapters/src/008_book_i_08_two_primary_motions.md` |
| source extraction check | PASS | `qa/pretranslation/008_book_i_08_source_extraction_check.md` |
| formal source recheck | PASS | `qa/pretranslation/008_book_i_08_formal_source_recheck.md` |
| PDF page evidence | PASS_FOR_PREP | `qa/technical/page_screenshots/book_i08_pages_017_019_contact_sheet.jpg` |
| technical audit | PASS_FOR_PREP | `qa/technical/008_book_i_08_two_primary_motions.technical_audit.md` |
| term prelock | PASS_FOR_PREP | `qa/technical/mathematical_term_lock.md` |

## 翻译控制要求

| risk | required handling |
|---|---|
| 主命题 | 保留“天上最初运动有两类”的命题；不得改写成现代天体动力学分类。 |
| 第一运动 | 明确为全天自东向西、等速、绕赤道极的日周回转；不得解释成托勒密接受地球自转。 |
| 第二运动 | 明确为日、月、行星相对于第一运动作相反方向的迁移，且绕黄道斜圈的极；不得写成现代真实公转轨道。 |
| 观测链 | 保留每日升起、中天、落下与长期观测中行星相对恒星向东滞后并南北偏移的论证链。 |
| 赤道圈 | `ἰσημερινός` 正文译作“赤道圈”，章末注说明原文按昼夜平分命名。 |
| 黄道斜圈 | `λοξὸς κύκλος` 正文译作“黄道斜圈”或“相对于赤道倾斜的大圈”，不得引入现代黄赤交角数值。 |
| 二分二至 | 春分、秋分、冬至、夏至四点必须按原文几何定义译清，不得只列现代节气名。 |
| 子午圈 | `μεσημβρινός` 译为“子午圈”，并说明它与通过赤道极和黄道极的大圈不同。 |
| 古今概念边界 | 不得引入现代天体物理、真实地球自转、轨道力学或现代黄赤交角解释。 |
| 英译本参考 | 英译本只作 reference witness，不得作为中文句子的转译底稿。 |
| 中文可读性 | 可拆分长句；但不得删掉“第一运动日周带动 → 行星相对恒星迁移并南北偏移 → 设黄道斜圈第二运动 → 定义二分二至和子午圈”的证明链。 |
| 注释策略 | 对“第一/第二运动”“赤道圈命名”“黄道斜圈”“二分二至点”“子午圈”集中章末注释。 |

## 禁止项

- 不得写 `chapters/final/008_book_i_08_two_primary_motions.md`。
- 不得生成正式 `output/book.epub`。
- 不得把英译本句式当作底稿。
- 不得把本章写成现代地球自转、公转轨道、天体动力学或黄赤交角数值说明。
- 不得省略两类运动、每日观测、长期行星迁移、黄道斜圈、二分二至点、子午圈的论证链。
- 不得进入 Book II-XIII 翻译。

## 自动结论

Book I.8 可以进入受控翻译准备；翻译完成后必须继续执行章节控制复核、技术审计复核、忠实度审校、可读性审校、术语审校和章节质量门禁。当前仍未翻译，不能进入终稿。

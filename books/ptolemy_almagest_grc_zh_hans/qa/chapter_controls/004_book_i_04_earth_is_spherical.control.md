# Book I.4 章节控制 / Chapter Control

chapter_file: `004_book_i_04_earth_is_spherical.md`
source_path: `chapters/src/004_book_i_04_earth_is_spherical.md`
translated_path: `chapters/translated/004_book_i_04_earth_is_spherical.md`
human_required: false
human_feedback_status: `none`
control_status: `PASS_FOR_CONTROLLED_TRANSLATION_PREP__NOT_TRANSLATED`
return_to_stage: `07_translate_chapters`

## 范围

本控制只覆盖 Book I.4 的受控翻译准备。它不允许写 `chapters/final/`，不允许生成正式 EPUB，也不允许把本章的 source recheck 通过状态解释为全书可批量翻译。

## 已满足的前置条件

| check | result | evidence |
|---|---|---|
| source candidate exists | PASS | `chapters/src/004_book_i_04_earth_is_spherical.md` |
| source extraction check | PASS | `qa/pretranslation/004_book_i_04_source_extraction_check.md` |
| formal source recheck | PASS | `qa/pretranslation/004_book_i_04_formal_source_recheck.md` |
| PDF page evidence | PASS_FOR_PREP | `qa/technical/page_screenshots/book_i04_pages_011_012_contact_sheet.jpg` |
| technical audit | PASS_FOR_PREP | `qa/technical/004_book_i_04_earth_is_spherical.technical_audit.md` |
| term prelock | PASS_FOR_PREP | `qa/technical/mathematical_term_lock.md` |

## 翻译控制要求

| risk | required handling |
|---|---|
| 主命题 | 保留“地球就感官观察所及、按整体各部分看也是球形的”这一古代观测命题，不改写为现代地球椭球或测地学说明。 |
| 月食时刻证据 | 保留同一食象在不同地点记录时刻不同，尤其月食记录；不得现代化为时区制度。 |
| 东西向升落差异 | 保留东方居住者较早、西方居住者较晚的相对观测链。 |
| 形状反证链 | 保留凹面、平面、多边形、圆柱形等备选地球形状及其反证，不压缩成一句“所以地球是球形”。 |
| 南北星象变化 | 保留向北行进时南方星更多隐没、北方星显现的观测证据，并与 I.3 恒显星术语保持一致。 |
| 航近高地证据 | 保留船行接近山或高地时大小逐渐增加、仿佛从海面升出的观察；说明此前被水面凸曲遮没。 |
| 英译本参考 | 英译本只作 reference witness，不得作为中文句子的转译底稿。 |
| 中文可读性 | 允许拆分长周期句；但不得删掉“月食/升落时刻 → 形状反证 → 南北星象变化 → 航近高地”的证明链。 |
| 注释策略 | 对感官观察、月食记录、时刻差异、地球曲率和古今概念边界，可在章末集中注释。 |

## 禁止项

- 不得写 `chapters/final/004_book_i_04_earth_is_spherical.md`。
- 不得生成正式 `output/book.epub`。
- 不得把英译本句式当作底稿。
- 不得把本章写成现代测地学、现代时区制度、现代大地水准面或地球椭球说明。
- 不得省略形状反证链、南北星象变化和航近高地证据。
- 不得提前翻译 Book I.11 弦表或进入全书批量翻译。

## 自动结论

Book I.4 可以进入受控翻译准备；翻译完成后必须继续执行章节控制复核、技术审计复核、忠实度审校、可读性审校、术语审校和章节质量门禁。当前仍未翻译，不能进入终稿。

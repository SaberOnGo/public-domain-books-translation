# Book I.9 章节控制 / Chapter Control

chapter_file: `009_book_i_09_on_individual_preliminaries.md`
source_path: `chapters/src/009_book_i_09_on_individual_preliminaries.md`
translated_path: `chapters/translated/009_book_i_09_on_individual_preliminaries.md`
human_required: false
human_feedback_status: `none`
control_status: `PASS_FOR_CONTROLLED_TRANSLATION_PREP__NOT_TRANSLATED`
return_to_stage: `07_translate_chapters`

## 范围

本控制只覆盖 Book I.9 的受控翻译准备。它不允许写 `chapters/final/`，不允许生成正式 EPUB，也不允许把本章的 source recheck 通过状态解释为 Book I 已完成或可进入 Book II。

## 已满足的前置条件

| check | result | evidence |
|---|---|---|
| source candidate exists | PASS | `chapters/src/009_book_i_09_on_individual_preliminaries.md` |
| source extraction check | PASS | `qa/pretranslation/009_book_i_09_source_extraction_check.md` |
| formal source recheck | PASS | `qa/pretranslation/009_book_i_09_formal_source_recheck.md` |
| PDF page evidence | PASS_FOR_PREP | `qa/technical/page_screenshots/book_i09_page_019_contact_sheet.jpg` |
| technical audit | PASS_FOR_PREP | `qa/technical/009_book_i_09_on_individual_preliminaries.technical_audit.md` |
| term prelock | PASS_FOR_PREP | `qa/technical/mathematical_term_lock.md` |

## 翻译控制要求

| risk | required handling |
|---|---|
| 过渡章功能 | 保留“总括预设已经列出，下面将进入逐项证明”的结构，不写成简单目录提示。 |
| 具体测定 | `κατὰ μέρος καταλήψεις` 译为“各项具体测定/逐项测定”，不得硬译成抽象“把握”。 |
| I.8 衔接 | “前述两极”必须同 I.8 的赤道极、黄道斜圈极关系相衔接。 |
| 弧与大圈 | “前述两极之间、通过这些极画出的大圈上的弧”必须译清，不能省略几何对象。 |
| I.10 衔接 | “圆内直线的大小”应让读者看出将进入弦长理论，但不得提前翻译或总结 I.10 证明。 |
| 几何证明 | `γραμμικῶς ἀποδεικνύειν` 可译为“用几何方法证明/按几何线图证明”，不改写成代数计算。 |
| 英译本参考 | 英译本只作 reference witness，不得作为中文句子的转译底稿。 |
| 中文可读性 | 可将原文长句拆为两三句；但不得删掉“总括预设 → 逐项证明 → 两极间弧的大小 → 圆内直线大小”的过渡链。 |
| 注释策略 | 对“具体测定”“圆内直线/弦长”“几何方法证明”集中章末注释。 |

## 禁止项

- 不得写 `chapters/final/009_book_i_09_on_individual_preliminaries.md`。
- 不得生成正式 `output/book.epub`。
- 不得把英译本句式当作底稿。
- 不得提前翻译 Book I.10 的弦长证明或 Book I.11 弦表。
- 不得把本章改写成现代数学教材目录说明。
- 不得进入 Book II-XIII 翻译。

## 自动结论

Book I.9 可以进入受控翻译准备；翻译完成后必须继续执行章节控制复核、技术审计复核、忠实度审校、可读性审校、术语审校和章节质量门禁。当前仍未翻译，不能进入终稿。

# Book I.9 章节质量门禁 / Chapter Quality Gate

gate_status: `PASS_CHAPTER_QUALITY_GATE__FINAL_PROMOTION_PENDING`
chapter_id: `009_book_i_09_on_individual_preliminaries`

## 控制结论

- Book I.9 已完成 source extraction、formal source recheck、章节控制、受控译文、草稿评审和译后技术复核。
- 本门禁只表示 Book I.9 可进入终稿前全书一致性审校队列。
- 不允许写 `chapters/final/009_book_i_09_on_individual_preliminaries.md`。
- 不允许生成正式 `output/book.epub`。
- 不允许进入 Book II-XIII 翻译。

## 质量确认

| area | result | evidence |
|---|---|---|
| source basis | PASS | `chapters/src/009_book_i_09_on_individual_preliminaries.md` |
| chapter control | PASS | `qa/chapter_controls/009_book_i_09_on_individual_preliminaries.control.md` |
| translation | PASS | `chapters/translated/009_book_i_09_on_individual_preliminaries.md` |
| review | PASS | `reviews/chapters/009_book_i_09_on_individual_preliminaries.review.md` |
| post technical recheck | PASS | `qa/technical/009_book_i_09_on_individual_preliminaries.post_translation_technical_recheck.md` |
| term lock | PASS | `qa/technical/mathematical_term_lock.md` |
| forbidden final output | PASS | no `chapters/final/009_book_i_09_on_individual_preliminaries.md` |
| forbidden formal EPUB | PASS | no `output/book.epub` |

## 必须保留的终稿前风险

- 本章是过渡章，终稿必须同 I.8 的两极/大圈术语和 I.10 的弧/弦术语一致。
- 终稿必须保留“总括预设”转入“逐项证明”的承接关系。
- 不得将“圆内直线”改写成现代代数函数或弦表计算规则。
- 本章没有图表和数值，不得在后续 EPUB 制作中人为添加非原书图形。

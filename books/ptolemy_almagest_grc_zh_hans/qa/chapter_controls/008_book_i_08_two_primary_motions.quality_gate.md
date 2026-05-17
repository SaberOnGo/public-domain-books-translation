# Book I.8 章节质量门禁 / Chapter Quality Gate

gate_status: `PASS_CHAPTER_QUALITY_GATE__FINAL_PROMOTION_PENDING`
chapter_id: `008_book_i_08_two_primary_motions`

## 控制结论

- Book I.8 已完成 source extraction、formal source recheck、章节控制、受控译文、草稿评审和译后技术复核。
- 本门禁只表示 Book I.8 可进入终稿前全书一致性审校队列。
- 不允许写 `chapters/final/008_book_i_08_two_primary_motions.md`。
- 不允许生成正式 `output/book.epub`。
- 不允许进入 Book II-XIII 翻译。

## 质量确认

| area | result | evidence |
|---|---|---|
| source basis | PASS | `chapters/src/008_book_i_08_two_primary_motions.md` |
| chapter control | PASS | `qa/chapter_controls/008_book_i_08_two_primary_motions.control.md` |
| translation | PASS | `chapters/translated/008_book_i_08_two_primary_motions.md` |
| review | PASS | `reviews/chapters/008_book_i_08_two_primary_motions.review.md` |
| post technical recheck | PASS | `qa/technical/008_book_i_08_two_primary_motions.post_translation_technical_recheck.md` |
| term lock | PASS | `qa/technical/mathematical_term_lock.md` |
| forbidden final output | PASS | no `chapters/final/008_book_i_08_two_primary_motions.md` |
| forbidden formal EPUB | PASS | no `output/book.epub` |

## 必须保留的终稿前风险

- 第一运动和第二运动不得被现代地球自转、公转轨道或天体动力学解释替代。
- 赤道圈、黄道斜圈、二分点、二至点、子午圈需同 Book I.9-I.16 继续统一。
- 本章没有图表和数值，不得在后续 EPUB 制作中人为添加非原书图形。

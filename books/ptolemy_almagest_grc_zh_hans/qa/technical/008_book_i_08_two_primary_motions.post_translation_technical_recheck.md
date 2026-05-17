# Book I.8 译后技术复核 / Post-Translation Technical Recheck

recheck_status: `PASS_POST_TRANSLATION_TECHNICAL_RECHECK__CHAPTER_GATE_PENDING`
chapter_id: `008_book_i_08_two_primary_motions`

## 控制结论

- 本章不含几何图、表格、六十进制数值、角度或数学计算。
- 英译本只作 reference witness；译文依据古希腊文 source 文件。
- 译文保留两类最初运动、赤道圈、黄道斜圈、行星迁移、二分二至点、子午圈和古代球面天文学模型边界。
- 不得写 `chapters/final/008_book_i_08_two_primary_motions.md`；不允许生成正式 `output/book.epub`。

## 技术复核项

| item | result | evidence |
|---|---|---|
| 图表风险 | PASS | 本章无图表；无需 facsimile figure |
| 数值风险 | PASS | 本章无六十进制数值、角度和计算 |
| Euclid 依赖 | PASS | 本章无显式 Euclid 依赖 |
| 第一运动 | PASS | 译文保留“自东向西、同样方式、等速、绕赤道极” |
| 第二运动 | PASS | 译文保留“相反方向、绕黄道斜圈极” |
| 赤道圈 | PASS | 译文正文和注释均使用“赤道圈” |
| 黄道斜圈 | PASS | 译文未引入现代黄赤交角数值 |
| 行星相对恒星迁移 | PASS | 保留向东滞后与南北偏移两层观测依据 |
| 二分点/二至点 | PASS | 四点均按原文几何截点定义 |
| 子午圈 | PASS | 保留其同通过两组极的大圈的区别 |
| 古今边界 | PASS | 未出现现代地球自转、轨道力学、天体动力学替代解释 |

## 章节质量门禁输入

- 译文：`chapters/translated/008_book_i_08_two_primary_motions.md`
- 评审：`reviews/chapters/008_book_i_08_two_primary_motions.review.md`
- 术语锁：`qa/technical/mathematical_term_lock.md`
- source recheck：`qa/pretranslation/008_book_i_08_formal_source_recheck.md`

下一步只能进入 Book I.8 章节质量门禁；仍不得进入终稿、正式 EPUB 或 Book II-XIII。

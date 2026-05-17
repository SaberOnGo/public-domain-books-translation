# 预翻译报告 / Pretranslation Report

pretranslation_status: `BOOK_I_TRANSLATION_SCOPE_STARTED__FINAL_GATED`

## 2026-05-17 Book I 阶段授权记录

用户已明确收窄本轮范围：只完成 Book I，不完成 13 卷全书。本报告中旧的 `FULL_BOOK_BLOCKED` 结论不再表示“永远不得进入翻译阶段”，而是表示“不得跳过 Book I 预研究、正式 source split、术语锁定、图表/表格清单、技术 QA 后直接写终稿或 EPUB”。

新的 Book I 执行合约见：

- `goal/2026-05-17_almagest_full_book_translation_goal.md`
- `qa/pretranslation/full_book_pre_research_plan.md`
- `qa/pretranslation/full_book_pretranslation_gate.md`
- `source/full_toc_draft.json`
- `source/full_book_translation_outline.md`
- `qa/pretranslation/full_book_risk_map.md`
- `qa/technical/011_book_i_11_chord_table_strategy.md`
- `chapters/src/001_book_i_01_proem.md`

当前允许：Book I 预研究、总纲、目录抽取、风险分级、正式分章准备、术语和图表/表格 QA 升级。

当前仍禁止：未完成 Book I 章节门禁和 Book I 终稿前一致性审校前写入 `chapters/final/`、翻译 Book I.11 弦表为正式章节、生成正式 `output/book.epub`。

## 结论

已完成 Book I.10 受控试译、样书预制作和 formal source recheck；用户已授权进入 Book I 翻译阶段。当前结论不是“可以直接写终稿”，而是“可以继续建立 Book I 正式 source split、术语锁、图表/表格清单、数值控制和技术 QA 路线”。不得写入 `chapters/final/`，不得翻译 Book I.11 弦表为正式章节，且不得生成正式 `output/book.epub`。

## 阻断条件

- Book I.10 古希腊文试译底稿已从 PAL XML 抽取到 `chapters/src/010_book_i_10_chords.md`，并已通过 formal source recheck；但它仍不是终稿门禁。
- Book I.10 的 PDF 页图范围已核验到 trial/formal-recheck 级别：viewer pages `20`-`27`；viewer page `28` 开始 Book I.11。
- Book I.10 术语已完成试译级初步抽取，但未达到全书锁定。
- Book I.10 图表标签、证明引用和六十进制数值控制已完成试译级审计；最终出版重绘规格仍未完成。
- Book I 图表清单只有研究草案，未完成 PDF 页图核验。
- 全书风险图已生成，但它只是 QA 路由草案；每卷 PDF 页图抽样和正式 source split 仍待完成。
- 全书预翻译门禁已接入 `quality:all`；当前门禁状态为 `PASS_PRE_RESEARCH_ACTIVE__FORMAL_TRANSLATION_GATED`。
- Book I.11 弦表策略已通过检查，但表格逐行 source extraction 和数值校验仍未完成。
- Book I.1 已生成 source extraction candidate，但 formal PDF recheck、章节控制和技术审计仍未完成。
- Book I.1 已通过 formal source recheck 和译前技术审计；下一步仍必须先建章节控制文件，不能直接进终稿。
- Book I.1 已通过章节控制；下一步只允许写受控译文，译后仍需复核和审校，不能直接进终稿。
- Book I.1 受控译文草稿已生成并通过机械检查；下一步仍是审校和技术复核，不能直接进终稿。
- Book I.1 草稿级评审已通过；下一步仍是译后技术复核和章节质量门禁，不能直接进终稿。
- Book I.1 译后技术复核已通过；下一步仍是章节质量门禁，不能直接进终稿。
- Book I.1 章节质量门禁已通过；下一步仍是终稿前全书一致性审校，不能直接进终稿。
- Book I.2 已生成 source extraction candidate；下一步仍是 formal PDF recheck、章节控制和技术审计，不能直接翻译。
- Book I.2 已通过 formal source recheck 和译前技术审计；下一步仍必须先建章节控制文件，不能直接翻译。
- Book I.2 已通过章节控制；下一步只允许写受控译文，译后仍需复核和审校，不能直接进终稿。
- Book I.2 受控译文草稿已生成并通过机械检查；下一步仍是审校和技术复核，不能直接进终稿。
- Book I.2 草稿级评审已通过；下一步仍是译后技术复核和章节质量门禁，不能直接进终稿。
- Book I.2 译后技术复核已通过；下一步仍是章节质量门禁，不能直接进终稿。
- Book I.2 章节质量门禁已通过；下一步仍是终稿前全书一致性审校，不能直接进终稿。
- Book I.3 已生成 source extraction candidate，并通过 formal source recheck 和译前技术审计；下一步仍必须先建章节控制文件，不能直接翻译。
- Book I.3 已通过章节控制；下一步只允许写受控译文，译后仍需复核和审校，不能直接进终稿。
- Book I.3 受控译文草稿已生成并通过机械检查；下一步仍是审校和技术复核，不能直接进终稿。
- Book I.3 草稿级评审已通过；下一步仍是译后技术复核和章节质量门禁，不能直接进终稿。
- Book I.3 译后技术复核已通过；下一步仍是章节质量门禁，不能直接进终稿。
- Book I.3 章节质量门禁已通过；下一步仍是终稿前全书一致性审校，不能直接进终稿。
- Book I.4 已生成 source extraction candidate；下一步仍是 formal PDF recheck、章节控制和技术审计，不能直接翻译。
- Book I.4 已通过 formal source recheck 和译前技术审计；下一步仍必须先建章节控制文件，不能直接翻译。
- Book I.4 已通过章节控制；下一步只允许写受控译文，译后仍需复核和审校，不能直接进终稿。
- Book I.4 受控译文草稿已生成并通过机械检查；下一步仍是审校和技术复核，不能直接进终稿。
- Book I.4 草稿级评审已通过；下一步仍是译后技术复核和章节质量门禁，不能直接进终稿。
- Book I.4 译后技术复核已通过；下一步仍是章节质量门禁，不能直接进终稿。
- Book I.4 章节质量门禁已通过；下一步仍是终稿前全书一致性审校，不能直接进终稿。
- Book I.5 已生成 source extraction candidate；下一步仍是 formal PDF recheck、章节控制和技术审计，不能直接翻译。
- Book I.5 已通过 formal source recheck 和译前技术审计；下一步仍必须先建章节控制文件，不能直接翻译。
- Book I.5 已通过章节控制；下一步只允许写受控译文，译后仍需复核和审校，不能直接进终稿。
- Book I.5 受控译文草稿已生成并通过机械检查；下一步仍是审校和技术复核，不能直接进终稿。
- Book I.5 草稿级评审已通过；下一步仍是译后技术复核和章节质量门禁，不能直接进终稿。
- Book I.5 译后技术复核已通过；下一步仍是章节质量门禁，不能直接进终稿。
- Book I.5 章节质量门禁已通过；下一步仍是终稿前全书一致性审校，不能直接进终稿。
- Book I.6 已生成 source extraction candidate；下一步仍是 formal PDF recheck、章节控制和技术审计，不能直接翻译。
- Book I.6 已通过 formal source recheck 和译前技术审计；下一步仍必须先建章节控制文件，不能直接翻译。
- Book I.6 已通过章节控制；下一步只允许写受控译文，译后仍需复核和审校，不能直接进终稿。
- Book I.6 受控译文草稿已生成并通过机械检查；下一步仍是审校和技术复核，不能直接进终稿。
- Book I.6 草稿级评审已通过；下一步仍是译后技术复核和章节质量门禁，不能直接进终稿。
- Book I.6 译后技术复核已通过；下一步仍是章节质量门禁，不能直接进终稿。
- Book I.6 章节质量门禁已通过；下一步仍是终稿前全书一致性审校，不能直接进终稿。
- Book I.11 弦表/全书角度/全书数值校验未完成。
- 数学证明依赖图只完成 Book I.10 试译/正式 source recheck 级检查，未完成 Book I 全书级检查。
- 天文学/数学术语只达到 Book I 样本级 `PILOT_LOCKED`，未达到全书 `LOCKED`。
- 参考译本差异尚未逐条记录。

## 允许的下一步

继续全书预研究和 source split 准备：逐卷分章、PDF 页图核验、图表/表格清单、术语锁升级、数值控制和技术 QA 路由。Book I.10 可作为第一个 formal source recheck 已通过样本进入后续章节控制和技术复审，但不得直接转入 `chapters/final/`。

## 2026-05-17 试译底稿进展

| item | file | status |
|---|---|---|
| Book I.10 trial source | `chapters/src/010_book_i_10_chords.md` | SOURCE_EXTRACTED |
| trial toc | `source/trial_toc.json` | TRIAL_ONLY |
| PDF page/range mapping | `qa/technical/book_i_page_verification.md` | PASS_FOR_BOOK_I10_TRIAL |
| figure label/proof audit | `qa/technical/010_book_i_10_chords.diagram_table_audit.md` | PASS_FOR_BOOK_I10_TRIAL |
| pilot terminology | `qa/technical/mathematical_term_lock.md` | PARTIAL_PASS_FOR_BOOK_I10 |
| proof dependency map | `qa/technical/proof_dependency_map.md` | PASS_FOR_BOOK_I10_TRIAL |
| sexagesimal numeric control | `qa/technical/numeric_validation_log.md` | PASS_FOR_BOOK_I10_TRIAL |
| technical audit | `qa/technical/010_book_i_10_chords.technical_audit.md` | PASS_FOR_BOOK_I10_TRIAL |
| formal trial translation | `chapters/translated/010_book_i_10_chords.md` | ALLOWED_FOR_SINGLE_BOOK_I10_TRIAL_ONLY |
| formal source recheck | `qa/pretranslation/010_book_i_10_formal_source_recheck.md` | PASS_FOR_FORMAL_SOURCE_RECHECK__NOT_FINAL_GATE |
| Book I.11 chord table strategy | `qa/technical/011_book_i_11_chord_table_strategy.md` | PASS_STRATEGY_ONLY_SOURCE_EXTRACTION_PENDING |
| Book I.1 source extraction candidate | `chapters/src/001_book_i_01_proem.md` | PASS_SOURCE_ONLY |
| Book I.1 formal source recheck | `qa/pretranslation/001_book_i_01_formal_source_recheck.md` | PASS_SOURCE_PREP_CHAPTER_CONTROL_PENDING |
| Book I.1 chapter control | `qa/chapter_controls/001_book_i_01_proem.control.md` | PASS_CONTROLLED_TRANSLATION_PREP_ALLOWED |
| Book I.1 translation draft | `chapters/translated/001_book_i_01_proem.md` | PASS_DRAFT_REVIEW_PENDING |
| Book I.1 draft review | `reviews/chapters/001_book_i_01_proem.review.md` | PASS_REVIEW_TECHNICAL_RECHECK_PENDING |
| Book I.1 post-translation technical recheck | `qa/technical/001_book_i_01_proem.post_translation_technical_recheck.md` | PASS_TECHNICAL_RECHECK_CHAPTER_GATE_PENDING |
| Book I.1 chapter quality gate | `qa/chapter_controls/001_book_i_01_proem.quality_gate.md` | PASS_CHAPTER_GATE_FINAL_PROMOTION_PENDING |
| Book I.2 source extraction candidate | `chapters/src/002_book_i_02_order_of_the_theorems.md` | PASS_SOURCE_ONLY |
| Book I.2 formal source recheck | `qa/pretranslation/002_book_i_02_formal_source_recheck.md` | PASS_SOURCE_PREP_CHAPTER_CONTROL_PENDING |
| Book I.2 chapter control | `qa/chapter_controls/002_book_i_02_order_of_the_theorems.control.md` | PASS_CONTROLLED_TRANSLATION_PREP_ALLOWED |
| Book I.2 translation draft | `chapters/translated/002_book_i_02_order_of_the_theorems.md` | PASS_DRAFT_REVIEW_PENDING |
| Book I.2 draft review | `reviews/chapters/002_book_i_02_order_of_the_theorems.review.md` | PASS_REVIEW_TECHNICAL_RECHECK_PENDING |
| Book I.2 post-translation technical recheck | `qa/technical/002_book_i_02_order_of_the_theorems.post_translation_technical_recheck.md` | PASS_TECHNICAL_RECHECK_CHAPTER_GATE_PENDING |
| Book I.2 chapter quality gate | `qa/chapter_controls/002_book_i_02_order_of_the_theorems.quality_gate.md` | PASS_CHAPTER_GATE_FINAL_PROMOTION_PENDING |
| Book I.3 source extraction candidate | `chapters/src/003_book_i_03_heaven_moves_spherically.md` | PASS_SOURCE_ONLY |
| Book I.3 formal source recheck | `qa/pretranslation/003_book_i_03_formal_source_recheck.md` | PASS_SOURCE_PREP_CHAPTER_CONTROL_PENDING |
| Book I.3 chapter control | `qa/chapter_controls/003_book_i_03_heaven_moves_spherically.control.md` | PASS_CONTROLLED_TRANSLATION_PREP_ALLOWED |
| Book I.3 translation draft | `chapters/translated/003_book_i_03_heaven_moves_spherically.md` | PASS_DRAFT_REVIEW_PENDING |
| Book I.3 draft review | `reviews/chapters/003_book_i_03_heaven_moves_spherically.review.md` | PASS_REVIEW_TECHNICAL_RECHECK_PENDING |
| Book I.3 post-translation technical recheck | `qa/technical/003_book_i_03_heaven_moves_spherically.post_translation_technical_recheck.md` | PASS_TECHNICAL_RECHECK_CHAPTER_GATE_PENDING |
| Book I.3 chapter quality gate | `qa/chapter_controls/003_book_i_03_heaven_moves_spherically.quality_gate.md` | PASS_CHAPTER_GATE_FINAL_PROMOTION_PENDING |
| Book I.4 source extraction candidate | `chapters/src/004_book_i_04_earth_is_spherical.md` | PASS_SOURCE_ONLY |
| Book I.4 formal source recheck | `qa/pretranslation/004_book_i_04_formal_source_recheck.md` | PASS_SOURCE_PREP_CHAPTER_CONTROL_PENDING |
| Book I.4 chapter control | `qa/chapter_controls/004_book_i_04_earth_is_spherical.control.md` | PASS_CONTROLLED_TRANSLATION_PREP_ALLOWED |
| Book I.4 translation draft | `chapters/translated/004_book_i_04_earth_is_spherical.md` | PASS_DRAFT_REVIEW_PENDING |
| Book I.4 draft review | `reviews/chapters/004_book_i_04_earth_is_spherical.review.md` | PASS_REVIEW_TECHNICAL_RECHECK_PENDING |
| Book I.4 post-translation technical recheck | `qa/technical/004_book_i_04_earth_is_spherical.post_translation_technical_recheck.md` | PASS_TECHNICAL_RECHECK_CHAPTER_GATE_PENDING |
| Book I.4 chapter quality gate | `qa/chapter_controls/004_book_i_04_earth_is_spherical.quality_gate.md` | PASS_CHAPTER_GATE_FINAL_PROMOTION_PENDING |
| Book I.5 source extraction candidate | `chapters/src/005_book_i_05_earth_is_central.md` | PASS_SOURCE_ONLY |
| Book I.5 formal source recheck | `qa/pretranslation/005_book_i_05_formal_source_recheck.md` | PASS_SOURCE_PREP_CHAPTER_CONTROL_PENDING |
| Book I.5 chapter control | `qa/chapter_controls/005_book_i_05_earth_is_central.control.md` | PASS_CONTROLLED_TRANSLATION_PREP_ALLOWED |
| Book I.5 translation draft | `chapters/translated/005_book_i_05_earth_is_central.md` | PASS_DRAFT_REVIEW_PENDING |
| Book I.5 draft review | `reviews/chapters/005_book_i_05_earth_is_central.review.md` | PASS_REVIEW_TECHNICAL_RECHECK_PENDING |
| Book I.5 post-translation technical recheck | `qa/technical/005_book_i_05_earth_is_central.post_translation_technical_recheck.md` | PASS_TECHNICAL_RECHECK_CHAPTER_GATE_PENDING |
| Book I.5 chapter quality gate | `qa/chapter_controls/005_book_i_05_earth_is_central.quality_gate.md` | PASS_CHAPTER_GATE_FINAL_PROMOTION_PENDING |
| Book I.6 source extraction candidate | `chapters/src/006_book_i_06_earth_as_point_to_heavens.md` | PASS_SOURCE_ONLY |
| Book I.6 formal source recheck | `qa/pretranslation/006_book_i_06_formal_source_recheck.md` | PASS_SOURCE_PREP_CHAPTER_CONTROL_PENDING |
| Book I.6 chapter control | `qa/chapter_controls/006_book_i_06_earth_as_point_to_heavens.control.md` | PASS_CONTROLLED_TRANSLATION_PREP_ALLOWED |
| Book I.6 translation draft | `chapters/translated/006_book_i_06_earth_as_point_to_heavens.md` | PASS_DRAFT_REVIEW_PENDING |
| Book I.6 draft review | `reviews/chapters/006_book_i_06_earth_as_point_to_heavens.review.md` | PASS_REVIEW_TECHNICAL_RECHECK_PENDING |
| Book I.6 post-translation technical recheck | `qa/technical/006_book_i_06_earth_as_point_to_heavens.post_translation_technical_recheck.md` | PASS_TECHNICAL_RECHECK_CHAPTER_GATE_PENDING |
| Book I.6 chapter quality gate | `qa/chapter_controls/006_book_i_06_earth_as_point_to_heavens.quality_gate.md` | PASS_CHAPTER_GATE_FINAL_PROMOTION_PENDING |
| Book I.7 source extraction candidate | `chapters/src/007_book_i_07_earth_has_no_translational_motion.md` | PASS_SOURCE_ONLY |
| Book I.7 formal source recheck | `qa/pretranslation/007_book_i_07_formal_source_recheck.md` | PASS_SOURCE_PREP_CHAPTER_CONTROL_PENDING |
| Book I.7 chapter control | `qa/chapter_controls/007_book_i_07_earth_has_no_translational_motion.control.md` | PASS_CONTROLLED_TRANSLATION_PREP_ALLOWED |
| Book I.7 translation draft | `chapters/translated/007_book_i_07_earth_has_no_translational_motion.md` | PASS_DRAFT_REVIEW_PENDING |
| Book I.7 draft review | `reviews/chapters/007_book_i_07_earth_has_no_translational_motion.review.md` | PASS_REVIEW_TECHNICAL_RECHECK_PENDING |
| Book I.7 post-translation technical recheck | `qa/technical/007_book_i_07_earth_has_no_translational_motion.post_translation_technical_recheck.md` | PASS_TECHNICAL_RECHECK_CHAPTER_GATE_PENDING |
| Book I.7 chapter quality gate | `qa/chapter_controls/007_book_i_07_earth_has_no_translational_motion.quality_gate.md` | PASS_CHAPTER_GATE_FINAL_PROMOTION_PENDING |
| Book I.8 source extraction candidate | `chapters/src/008_book_i_08_two_primary_motions.md` | PASS_SOURCE_ONLY |
| Book I.8 formal source recheck | `qa/pretranslation/008_book_i_08_formal_source_recheck.md` | PASS_SOURCE_PREP_CHAPTER_CONTROL_PENDING |
| Book I.8 chapter control | `qa/chapter_controls/008_book_i_08_two_primary_motions.control.md` | PASS_CONTROLLED_TRANSLATION_PREP_ALLOWED |
| Book I.8 translation draft | `chapters/translated/008_book_i_08_two_primary_motions.md` | PASS_DRAFT_REVIEW_PENDING |
| Book I.8 draft review | `reviews/chapters/008_book_i_08_two_primary_motions.review.md` | PASS_REVIEW_TECHNICAL_RECHECK_PENDING |
| Book I.8 post-translation technical recheck | `qa/technical/008_book_i_08_two_primary_motions.post_translation_technical_recheck.md` | PASS_TECHNICAL_RECHECK_CHAPTER_GATE_PENDING |
| Book I.8 chapter quality gate | `qa/chapter_controls/008_book_i_08_two_primary_motions.quality_gate.md` | PASS_CHAPTER_GATE_FINAL_PROMOTION_PENDING |
| Book I.9 source extraction candidate | `chapters/src/009_book_i_09_on_individual_preliminaries.md` | PASS_SOURCE_ONLY |
| Book I.9 formal source recheck | `qa/pretranslation/009_book_i_09_formal_source_recheck.md` | PASS_SOURCE_PREP_CHAPTER_CONTROL_PENDING |
| Book I.9 chapter control | `qa/chapter_controls/009_book_i_09_on_individual_preliminaries.control.md` | PASS_CONTROLLED_TRANSLATION_PREP_ALLOWED |
| Book I.9 translation draft | `chapters/translated/009_book_i_09_on_individual_preliminaries.md` | PASS_DRAFT_REVIEW_PENDING |
| Book I.9 draft review | `reviews/chapters/009_book_i_09_on_individual_preliminaries.review.md` | PASS_REVIEW_TECHNICAL_RECHECK_PENDING |
| Book I.9 post-translation technical recheck | `qa/technical/009_book_i_09_on_individual_preliminaries.post_translation_technical_recheck.md` | PASS_TECHNICAL_RECHECK_CHAPTER_GATE_PENDING |
| Book I.9 chapter quality gate | `qa/chapter_controls/009_book_i_09_on_individual_preliminaries.quality_gate.md` | PASS_CHAPTER_GATE_FINAL_PROMOTION_PENDING |
| Book I.10 source extraction check | `qa/pretranslation/010_book_i_10_source_extraction_check.md` | PASS_SOURCE_ONLY |
| Book I.10 formal source recheck | `qa/pretranslation/010_book_i_10_formal_source_recheck.md` | PASS_FORMAL_SOURCE_RECHECK_NOT_FINAL |
| Book I.10 chapter control | `qa/chapter_controls/010_book_i_10_chords.control.md` | PASS_CONTROLLED_TRANSLATION_PREP_ALLOWED |
| Book I.10 translation draft | `chapters/translated/010_book_i_10_chords.md` | PASS_DRAFT_REVIEW_PENDING |
| Book I.10 draft review | `reviews/chapters/010_book_i_10_chords.review.md` | PASS_REVIEW_TECHNICAL_RECHECK_PENDING |
| Book I.10 post-translation technical recheck | `qa/technical/010_book_i_10_chords.post_translation_technical_recheck.md` | PASS_TECHNICAL_RECHECK_CHAPTER_GATE_PENDING |
| Book I.10 chapter quality gate | `qa/chapter_controls/010_book_i_10_chords.quality_gate.md` | PASS_CHAPTER_GATE_FINAL_PROMOTION_PENDING |

## 已完成样本 / Completed Samples

| sample_id | file | source_scope | status | publication_use |
|---|---|---|---|---|
| sample-001 | `qa/pretranslation/samples/book_i_math_proof_sample_001.md` | Book I.10 geometry/proof micro-sample | NEEDS_MATH_REVIEW | forbidden |

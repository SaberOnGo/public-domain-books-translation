# Book I.10 章节译后控制 / Chapter Post-Translation Control

chapter_file: `010_book_i_10_chords.md`
translated_path: `chapters/translated/010_book_i_10_chords.md`
human_required: false
human_feedback_status: `RECEIVED_AND_APPLIED_2026_05_17`
control_status: `PASS_FOR_CONTROLLED_TRANSLATION_PREP__DRAFT_EXISTS`
return_to_stage: `08_review_fidelity`

## 范围

本控制只覆盖 Book I.10 单章节受控译文。它不允许进入 `chapters/final/`，不允许翻译 Book I.11 弦表，也不允许进入 Book II-XIII。

## 自动检查

| check | result | evidence |
|---|---|---|
| 机械直译 / 古希腊文句法硬搬 | PASS_AFTER_REWORK | 已将读者版术语从难懂的“所对直线”改为“弦/某弧对应的弦”，并补章末注说明原文表达。 |
| 省字式翻译 | PASS | 证明构造、Euclid 依赖、矩形/平方关系和数值推导均有完整句子承接。 |
| 无依据发挥 | PASS | 未加入现代天文学解释；图和数值说明限于已有 QA 控制。 |
| 章节标题和层级 | PASS | 按证明依赖图拆为十边形/五边形、四边形引理、弧差、半弧、弧和、比值引理、数值夹逼、弦表引出。 |
| 专名、术语、数字 | PASS_AFTER_REWORK | 图中希腊点名保留；读者版角度写作 `0°45′`、`1°30′`，非角度六十进制弦长写作 `1p02′50″` 等；内部 `;` 记法不再裸露于正文，也不转成十进制小数。 |
| 图表处理 | PASS_AFTER_REWORK | EPUB 预制作改用 7 张 Heiberg PDF facsimile 裁图；脚本检查裁图边缘，Book I.11 弦表未纳入。 |
| 《几何原本》依据 | PASS_AFTER_REWORK | 正文依据标记改为小号“依据《几何原本》...”格式；章末集中说明本章各条依据的大意，避免读者必须另查《几何原本》。 |
| 中文可读性 | PASS_AFTER_REWORK | 已按用户反馈润色典型拗口句；作图语句采用简洁现代几何关系，不硬译、不过度解释。 |
| 脚本化门禁 | PASS_AFTER_REWORK | `scripts/check_translation_constraints.py` 已作为全书翻译门禁；Book I.10 样本构建前以 `--scope=trial-book-i10` 复用该门禁，拦截旧数值格式、裸 `Eucl.`、未注释依据和典型硬译残留。 |
| 忠实度 | PASS_FOR_TRIAL | 评分：91/100。关键风险点已写入评审记录继续复核。 |

## 用户反馈处理

- 反馈：`i10_fig02_cyclic_quadrilateral_lemma_facsimile.png` 与 `i10_fig04_half_arc_facsimile.png` 标签裁切不完整。
- 处理：更新 `scripts/extract_book_i10_facsimile_figures.py`，粗裁后允许脚本白除邻近正文、自动去白边、补固定白边，并检查原始裁框边缘是否切到墨迹。重建 7 张 facsimile 图。
- 反馈：正文存在“求它所对弧之半所对的直线”等难读直译腔。
- 处理：正文读者版优先使用“弦/某弧对应的弦”，并在章末注解释原文表达。
- 反馈：`37;4,55` 等内部六十进制记法不适合 EPUB 正文，但六十进制结构不能改成十进制小数。
- 处理：弧和角的度数使用 `°′″`；弦长、平方量等非角度六十进制值改为 `37p04′55″` 等读者版显示，并补章末注说明。
- 反馈：`Eucl. VI.33` 这类裸缩写和大字号依据标记会干扰正文阅读，读者也不易知道对应定理内容。
- 处理：正文改为小号“依据《几何原本》...”标记，并在章末注释列出本章用到的具体命题、定义或系的大意。
- 反馈：古代几何术语简短，但不能硬译成现代中文中意义不明的表达；也不能为了说明而过度啰嗦。
- 处理：典型句改为“以 `Δ` 为圆心、`ΔΕ` 为半径作圆，使它交 `ΑΔ` 于 `Η`，并在 `ΔΖ` 的延长线上交于 `Θ`”；同时把该原则写入模板、本书规范和脚本门禁。

## 结论

Book I.10 可继续作为 Book I 章节级受控草稿进入译后技术复核和章节质量门禁。不得进入终稿、Book I.11 弦表翻译或正式 EPUB 阶段。

# 11 章节最终门禁

只有章节通过译后控制、忠实度、可读性、术语和读者可见检查，且无未关闭 P0/P1/P2，才可进入 `chapters/final/`。

## 专家级与多义词硬门禁 / Expert Quality and Polysemy Hard Gate

章节进入 `chapters/final/` 前，必须确认 `qa/chapter_controls/{chapter}.control.md` 最近 PASS 轮记录 `expert_translation_skill_used: true`、`expert_level_review_status: "PASS"`、`polysemy_translation_stage_review: "PASS"`、`polysemy_context_review: "PASS"`、`polysemy_unresolved_count: 0`。若后文线索推翻前文选义，或译文只是良好但未达专家级出版质量，本章 FAIL，回到翻译、译后控制或相应审校节点。

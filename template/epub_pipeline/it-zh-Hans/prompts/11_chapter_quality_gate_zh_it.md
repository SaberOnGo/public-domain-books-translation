# 11 章节门禁

为每章写入 `qa/gates/{chapter}.gate.md`。PASS 必须同时满足：每章译后 control 最近一轮 PASS、忠实度无重大错误、中文独立阅读 >= 4/5、叙事现场感 >= 4/5、术语无阻塞漂移、20 句朗读明显拗口不超过 1 句、无生产痕迹、无裸外文。

## 专家级与多义词硬门禁 / Expert Quality and Polysemy Hard Gate

章节进入 `chapters/final/` 前，必须确认 `qa/chapter_controls/{chapter}.control.md` 最近 PASS 轮记录 `expert_translation_skill_used: true`、`expert_level_review_status: "PASS"`、`polysemy_context_review: "PASS"`、`polysemy_unresolved_count: 0`。若后文线索推翻前文选义，或译文只是良好但未达专家级出版质量，本章 FAIL，回到翻译、译后控制或相应审校节点。

# 11 章节质量门禁 / Chapter Quality Gate

## 输入

- `qa/chapter_controls/{chapter}.control.md`
- `qa/fidelity/{chapter}.fidelity.md`
- `qa/readability/{chapter}.readability.md`
- `qa/terminology/{chapter}.terminology.md`
- 叠加 profile 时的额外审计记录

## 任务

生成 `qa/gates/{chapter}.gate.md`。

PASS 条件：

- 原文-今译对照完整。
- 文义忠实，无未关闭 P0/P1/P2。
- 现代中文可读。
- 专名、术语、注释一致。
- 断句、标点、异文疑难已记录。
- 不含生产控制说明、现代版权译文或站点样板残留。

PASS 后才可把章节写入 `chapters/final/`。

## 专家级与多义词硬门禁 / Expert Quality and Polysemy Hard Gate

章节进入 `chapters/final/` 前，必须确认 `qa/chapter_controls/{chapter}.control.md` 最近 PASS 轮记录 `expert_translation_skill_used: true`、`expert_level_review_status: "PASS"`、`polysemy_context_review: "PASS"`、`polysemy_unresolved_count: 0`。若后文线索推翻前文选义，或译文只是良好但未达专家级出版质量，本章 FAIL，回到翻译、译后控制或相应审校节点。

# 17 评审回退路由 / Review-Based Revision Routing

## 目的 / Purpose

评审不是形式。评审发现问题后，必须能回到任意前置阶段修正，而不是只在最终 EPUB 上打补丁。

## 输入 / Input

- `reviews/agent_a/review.md`
- `reviews/agent_b/review.md`
- `reviews/scorecards/final_quality_score.md`

## 回退规则 / Routing Rules

按问题类型回退：

1. 版权/来源问题：回到 `01_ingest_clean` 与 `metadata/rights_checklist.md`。
2. 翻译原则问题：回到 `03_global_translation_research` 或 `04_book_specific_research`。
3. 样本翻译失败：回到 `05_pretranslation_trials`。
4. 单章翻译问题：回到 `07_translate_chapters` 和 `08a_chapter_post_translation_control`。
5. 多章共性翻译问题：回到 `04_book_specific_research`，更新规则后批量重译相关章节。
6. 术语问题：回到 `06_glossary_style` 和 `10_review_terminology`。
7. 章节门禁问题：回到 `11_chapter_quality_gate`。
8. 封面、metadata、字体、排版问题：回到 `13_preproduction_stage1_spec`。
9. 样章问题：回到 `14_preproduction_stage2_sample`。
10. EPUB 工程问题：回到 `15_full_book_production`。

## 输出 / Output

生成：

- `reviews/revision_route.md`

其中必须包含：

- 问题列表。
- 严重级别：P0/P1/P2/P3。
- 回退阶段。
- 需要修改的文件。
- 修正完成后的重新验证项。

## PASS 条件 / PASS Criteria

只有所有 P0/P1/P2 必须修复项关闭，且两个 Agent 复审或主控复审确认后，才可进入最终输出。

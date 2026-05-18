# 随机抽检返工路由 / Random Spot-Check Revision Route

status: CLOSED_FOR_ROUND_001

## round_001 结论

- seed: `aba568cbe722b3a44e5094710f58d669`
- Agent A: FAIL, `average_score=83.12`, `lowest_score=55`, `blocking_issue_count=1`
- Agent B: FAIL, `average_score=82.23`, `lowest_score=62`, `blocking_issue_count=4`
- 路由: 回到章节精修与术语一致性修复，完成后重建 EPUB，并用新 seed 执行下一轮抽检。

## 阻断项

1. P1: `chapters/final/025_chapter_24_bound_for_china.md` 有读者可见外文残留 `აღარ`。
2. P2: Saumarez 译名在 `chapters/final/028_chapter_27_landing_the_sick.md` 与 `chapters/final/035_chapter_34_capture_of_the_galleon.md` 不一致。
3. P2: `chapters/final/002_chapter_01_purpose_of_the_voyage.md` 中 `切尔西学院*`、`** 他们` 为破损脚注/Markdown 标记。
4. P1: `chapters/final/023_chapter_22_manila_trade.md` 中桑威奇群岛发现年份疑误；Project Gutenberg 原注作 1779，外部史料显示库克首次抵达并命名为 1778。

## 处理

阻断项已在 `round_001/fixes/fix_log.md` 记录并在 `round_001/verification/closure_check.md` 关闭。修复后已重新运行：

- `npm run build:epub`
- `npm run check:epub`


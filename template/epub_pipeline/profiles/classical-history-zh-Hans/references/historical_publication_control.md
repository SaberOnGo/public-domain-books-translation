# 古代历史出版控制 / Historical Publication Control

## 读者版要求

- 前置页可简短说明时代、文本性质和注释原则。
- 附录可提供人物表、国家关系表和年表，但不应压过正文。
- 正文注释必须短而有用。
- EPUB 目录题名应清楚，不写成长篇题解。

## 随机抽检重点

- 人物是否认错。
- 所属国或官爵是否错。
- 时间线是否错。
- 注释是否缺失、错误或过度。
- 今译是否把政治策略、威胁、讽刺或外交辞令翻平。

## 随机抽检同类问题全书审计 / Book-Wide Similar-Issue Audit

随机抽检一旦发现任何需要修复或可能系统性复现的问题，包括但不限于 P0/P1/P2、单项 <70、读者不可理解、事实/术语/图表/公式/注释错误，或本模板硬门禁失败，主执行 AI 不得只修被抽中的样本，也不得等到第二轮才全书检查。必须先把发现归纳为问题族，再对整本读者可见书稿执行全书同类问题审计，覆盖 `chapters/final/`、frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML；修复所有确认命中，记录合理例外，并在该轮 `fix_log.md` 与 `closure_check.md` 中关闭该问题族后，才能使用新 seed 复抽。

If a random sample exposes any issue that needs correction or may recur systemically, treat it as a possible systemic defect family immediately in the current round. Audit the whole reader-facing book for similar cases, fix all confirmed matches, document justified exceptions, and close the family in the same round before a new-seed resample.

# 文言文今译质量标准 / Literary Chinese Modern Chinese Quality Standard

本文件是 `template/epub_pipeline/targets/zh-Hans/quality_framework/` 的简体中文目标语言规则在文言文源文本场景下的应用摘要。完整中文目标语言质量规则见目标语言质量框架。

## 五维标准

1. 忠实：不误解字句、人物、事件、因果、否定和语气。
2. 可读：现代中文自然清楚，不是假古文，不是课堂串讲。
3. 可对照：古文段和今译段能逐段核对。
4. 有注释判断：必要背景解释到位，非必要注释收敛。
5. 可出版：标题、术语、专名、标点、metadata、EPUB 结构和随机抽检均通过。

## P0/P1 问题

- 人物关系、国家归属、时间顺序或事件因果翻错。
- 断句错误导致今译完全改变意思。
- 省略或新增关键事实。
- 复制现代受版权保护译文或校注表达。
- 对照正文缺失原文或今译。
- 注释缺失导致普通目标读者会形成明显误解。

## P2 问题

- 术语、官名、地名不统一。
- 注释过长、重复或位置不当。
- 现代中文可懂但无叙述气息。
- 标题过长或像题解。
- 文本疑难未同步记录。

## 随机抽检同类问题全书审计 / Book-Wide Similar-Issue Audit

随机抽检一旦发现任何需要修复或可能系统性复现的问题，包括但不限于 P0/P1/P2、单项 <70、读者不可理解、事实/术语/图表/公式/注释错误，或本模板硬门禁失败，主执行 AI 不得只修被抽中的样本，也不得等到第二轮才全书检查。必须先把发现归纳为问题族，再对整本读者可见书稿执行全书同类问题审计，覆盖 `chapters/final/`、frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML；修复所有确认命中，记录合理例外，并在该轮 `fix_log.md` 与 `closure_check.md` 中关闭该问题族后，才能使用新 seed 复抽。

If a random sample exposes any issue that needs correction or may recur systemically, treat it as a possible systemic defect family immediately in the current round. Audit the whole reader-facing book for similar cases, fix all confirmed matches, document justified exceptions, and close the family in the same round before a new-seed resample.

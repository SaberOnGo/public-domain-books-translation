# 03 文言文今译通用研究 / Global Translation Research

## 任务

读取：

- `template/epub_pipeline/targets/zh-Hans/quality_framework/README.md`
- `references/quality_standard.md`
- `references/classical_chinese_parallel_text_policy.md`
- `references/classical_chinese_annotation_policy.md`
- `references/classical_chinese_textual_criticism_policy.md`

生成 `metadata/global_translation_research.md`，说明：

1. 文言文今译的对照正文策略。
2. 现代中文文体目标。
3. 断句、标点、古今词义和省略关系风险。
4. 注释分层和注释密度控制。
5. 随机抽检如何检查原文、今译和注释。

## 门禁

没有完成通用研究，不得开始本书专项研究。

## 随机抽检同类问题全书审计 / Book-Wide Similar-Issue Audit

随机抽检一旦发现任何需要修复或可能系统性复现的问题，包括但不限于 P0/P1/P2、单项 <70、读者不可理解、事实/术语/图表/公式/注释错误，或本模板硬门禁失败，主执行 AI 不得只修被抽中的样本，也不得等到第二轮才全书检查。必须先把发现归纳为问题族，再对整本读者可见书稿执行全书同类问题审计，覆盖 `chapters/final/`、frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML；修复所有确认命中，记录合理例外，并在该轮 `fix_log.md` 与 `closure_check.md` 中关闭该问题族后，才能使用新 seed 复抽。

If a random sample exposes any issue that needs correction or may recur systemically, treat it as a possible systemic defect family immediately in the current round. Audit the whole reader-facing book for similar cases, fix all confirmed matches, document justified exceptions, and close the family in the same round before a new-seed resample.

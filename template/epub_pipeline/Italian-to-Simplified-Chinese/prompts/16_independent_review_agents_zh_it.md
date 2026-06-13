# 16 独立评审 Agent

第一版全书 EPUB 后，至少两个独立评审 Agent 按分层随机抽检样本评分。评审不得互相参考，不得跳过表格、图片、公式、图注、注释和专名高风险点。任一 P0/P1/P2、任一单项 < 80、任一读者不可理解均 FAIL。

## 随机抽检同类问题全书审计 / Book-Wide Similar-Issue Audit

随机抽检一旦发现任何需要修复或可能系统性复现的问题，包括但不限于 P0/P1/P2、单项 <80、读者不可理解、事实/术语/图表/公式/注释错误，或本模板硬门禁失败，主执行 AI 不得只修被抽中的样本，也不得等到第二轮才全书检查。必须先把发现归纳为问题族，再对整本读者可见书稿执行全书同类问题审计，覆盖 `chapters/final/`、frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML；修复所有确认命中，记录合理例外，并在该轮 `fix_log.md` 与 `closure_check.md` 中关闭该问题族后，才能使用新 seed 复抽。

若该轮发现译文质量问题族，还必须在 `fix_log.md` 填写 `translation_quality_skill_backfill: "UPDATED"` 或 `"MERGED"`、`translation_quality_skill_backfill_path: "skills/translation-quality-defect-families/SKILL.md"` 和回填摘要，并在 `closure_check.md` 填写 `translation_quality_skill_backfill_verified: true`；若仅有非译文质量问题，必须填写 `NOT_APPLICABLE` 和具体理由。

If a random sample exposes any issue that needs correction or may recur systemically, treat it as a possible systemic defect family immediately in the current round. Audit the whole reader-facing book for similar cases, fix all confirmed matches, document justified exceptions, and close the family in the same round before a new-seed resample.

## 专家级与多义词抽检 / Expert Quality and Polysemy Review

独立评审必须按 `skills/expert-translation-quality/SKILL.md` 检查样本是否达到专家级出版质量，并确认多义词、习语、语法关系、术语定义或后文线索没有推翻当前译法。发现上下文选义错误时，归入译文质量问题族，不能用“整体可读”给 PASS。

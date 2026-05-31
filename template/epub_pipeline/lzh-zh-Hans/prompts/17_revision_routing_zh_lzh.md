# 17 返工路由 / Revision Routing

## 任务

根据章节 gate、样章、EPUB 校验、随机抽检和独立评审结果，将问题路由回正确阶段：

- 底本或断句问题：回到 `01`、`02` 或文本疑难记录。
- 人物、地名、制度背景问题：回到本书研究、术语表或历史 profile。
- 今译误解：回到章节翻译和忠实度审校。
- 注释缺失或过度：回到注释策略和术语审校。
- EPUB 呈现问题：回到预制作或构建脚本。

## 输出

- `qa/revision_routing.md`
- 对应 fix log
- 必要时更新 `state/pipeline_state.json`

返工后必须重建 EPUB，并使用新 seed 复抽。

## 随机抽检同类问题全书审计 / Book-Wide Similar-Issue Audit

随机抽检一旦发现任何需要修复或可能系统性复现的问题，包括但不限于 P0/P1/P2、单项 <70、读者不可理解、事实/术语/图表/公式/注释错误，或本模板硬门禁失败，主执行 AI 不得只修被抽中的样本，也不得等到第二轮才全书检查。必须先把发现归纳为问题族，再对整本读者可见书稿执行全书同类问题审计，覆盖 `chapters/final/`、frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML；修复所有确认命中，记录合理例外，并在该轮 `fix_log.md` 与 `closure_check.md` 中关闭该问题族后，才能使用新 seed 复抽。

If a random sample exposes any issue that needs correction or may recur systemically, treat it as a possible systemic defect family immediately in the current round. Audit the whole reader-facing book for similar cases, fix all confirmed matches, document justified exceptions, and close the family in the same round before a new-seed resample.

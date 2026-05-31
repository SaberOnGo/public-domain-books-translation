# 15 全书制作 / Full Book Production

## 前置

- 全部章节 gate PASS。
- `preproduction/stage1/production_spec.md` PASS。
- 样章 EPUB PASS。

## 任务

1. 清理或重建 staging 输出。
2. 构建全书 EPUB。
3. 检查原文-今译对照正文、注释、nav、book-info、cover、metadata 和 OPF。
4. 运行 publication lint、asset lint、reader-facing policy check 和 EPUBCheck。

## 门禁

只生成 `output/book.epub` 不代表完成；第一版全书 EPUB 之后必须进入分层随机抽检。

## 随机抽检同类问题全书审计 / Book-Wide Similar-Issue Audit

随机抽检一旦发现任何需要修复或可能系统性复现的问题，包括但不限于 P0/P1/P2、单项 <70、读者不可理解、事实/术语/图表/公式/注释错误，或本模板硬门禁失败，主执行 AI 不得只修被抽中的样本，也不得等到第二轮才全书检查。必须先把发现归纳为问题族，再对整本读者可见书稿执行全书同类问题审计，覆盖 `chapters/final/`、frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML；修复所有确认命中，记录合理例外，并在该轮 `fix_log.md` 与 `closure_check.md` 中关闭该问题族后，才能使用新 seed 复抽。

If a random sample exposes any issue that needs correction or may recur systemically, treat it as a possible systemic defect family immediately in the current round. Audit the whole reader-facing book for similar cases, fix all confirmed matches, document justified exceptions, and close the family in the same round before a new-seed resample.

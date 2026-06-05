---
name: de-zh-Hans
description: Use this template when translating German public-domain or licensed source texts into Simplified Chinese EPUBs, especially literature, speculative fiction, nonfiction, social thought, and classic prose.
---

# 德语到简体中文 EPUB 模板 Skill

使用场景：用户要把德语公版或授权原文翻译成简体中文，并制作可发布 EPUB。

## 执行顺序

1. 读取仓库根目录 `AGENTS.md`。
2. 读取 `template/epub_pipeline/README.md`、`common/README.md` 和 `targets/zh-Hans/quality_framework/README.md`。
3. 读取本目录 `AGENTS.md`、`README.md` 和 `references/` 下的德语专项规则。
4. 使用 `books/scripts/create_book_project.py` 创建工程，复制顺序为 `common -> de-zh-Hans`；若书籍属于专业/学术控制对象，再叠加合适 profile。
5. 记录 `metadata/source_evidence.md` 和 `metadata/rights_checklist.md`，权利不清楚则停止。
6. 完成本书专项研究、文体画像、术语表、预翻译试译和小样本测试。
7. 分章翻译，每章立即生成 `qa/chapter_controls/{chapter}.control.md`，再做忠实度、可读性、术语、意象/读者可见内容和章节门禁。
8. 生成 EPUB，运行出版 lint、资源检查、EPUBCheck；完成首轮发布前执行 `12_build_validate_zh_de.md`、`16a_stratified_random_spotcheck.md`、`16_independent_review_agents_zh_de.md`。
9. 写入 `references/stratified_random_spotcheck.md` 所在流程的验收证据：问题族关闭、`fix_log`、`closure_check`、`validation_report`，通过 `--require-pass` 后进入版本化 release。
10. 将可复用经验写回本模板的 `retrospective_lessons.md` 或对应 reference；书籍专属经验留在具体书籍工程。

## 德语翻译重点

- 先判断句法骨架，再翻译修辞。
- 把德语框架结构、长定语链和复合词改成中文读者能跟上的动作、因果和承接。
- 核对可分动词、情态动词、否定作用域、虚拟式和代词回指。
- 保留德语散文的节奏，但不保留让中文拗口的逗号串联。
- 科学技术词、天文学词、政治/社会词和虚构文明设定必须稳定，不能为了文采随意换词。
- 原词呈现从严控制；正文不默认写 `中文译名（deutscher Begriff）`。

## 随机抽检同类问题全书审计 / Book-Wide Similar-Issue Audit

随机抽检一旦发现任何需要修复或可能系统性复现的问题，包括但不限于 P0/P1/P2、单项 <80、读者不可理解、事实/术语/图表/公式/注释错误，或本模板硬门禁失败，主执行 AI 不得只修被抽中的样本，也不得等到第二轮才全书检查。必须先把发现归纳为问题族，再对整本读者可见书稿执行全书同类问题审计，覆盖 `chapters/final/`、frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML；修复所有确认命中，记录合理例外，并在该轮 `fix_log.md` 与 `closure_check.md` 中关闭该问题族后，才能使用新 seed 复抽。

若该轮发现译文质量问题族，还必须在 `fix_log.md` 填写 `translation_quality_skill_backfill: "UPDATED"` 或 `"MERGED"`、`translation_quality_skill_backfill_path: "skills/translation-quality-defect-families/SKILL.md"` 和回填摘要，并在 `closure_check.md` 填写 `translation_quality_skill_backfill_verified: true`；若仅有非译文质量问题，必须填写 `NOT_APPLICABLE` 和具体理由。

If a random sample exposes any issue that needs correction or may recur systemically, treat it as a possible systemic defect family immediately in the current round. Audit the whole reader-facing book for similar cases, fix all confirmed matches, document justified exceptions, and close the family in the same round before a new-seed resample.

## 译文质量问题族沉淀 / Translation-Quality Defect Family Backfill

凡发现可复现的译文质量问题族，包括忠实度、中文顺读、术语、标题/小标题、注释、图表文字接口、源语句法残留、过硬过直句、短句切断、比喻自撞、排比标点拖拽、代词指代不清、过度解释或加戏等，必须使用 `skills/translation-quality-defect-families/SKILL.md`。先在具体书籍工程完成证据记录、同类审计、修复和复查；再把可复用经验合并回填到该 skill，已有同族条目时更新归纳，不盲目重复追加。

When a recurring translation-quality defect family is found, use `skills/translation-quality-defect-families/SKILL.md`. Close the evidence, similar-case audit, fixes, and recheck in the book project first; then merge only reusable lessons into the skill.

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

随机抽检一旦发现任何需要修复或可能系统性复现的问题，包括但不限于 P0/P1/P2、单项 <80、读者不可理解、事实/术语/图表/公式/注释错误，或本模板硬门禁失败，主执行 AI 不得只修被抽中的样本，也不得等到第二轮才全书检查。必须先把发现归纳为问题族，再对整本读者可见书稿执行全书同类问题审计，覆盖 `chapters/final/`、frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML；修复所有确认命中，记录合理例外，并在该轮 `fix_log.md` 与 `closure_check.md` 中关闭该问题族后，才能使用新 seed 复抽。

若该轮发现译文质量问题族，还必须在 `fix_log.md` 填写 `translation_quality_skill_backfill: "UPDATED"` 或 `"MERGED"`、`translation_quality_skill_backfill_path: "skills/translation-quality-defect-families/SKILL.md"` 和回填摘要，并在 `closure_check.md` 填写 `translation_quality_skill_backfill_verified: true`；若仅有非译文质量问题，必须填写 `NOT_APPLICABLE` 和具体理由。

If a random sample exposes any issue that needs correction or may recur systemically, treat it as a possible systemic defect family immediately in the current round. Audit the whole reader-facing book for similar cases, fix all confirmed matches, document justified exceptions, and close the family in the same round before a new-seed resample.
## 随机抽检优秀出版线 / Random Review Excellence Gate

`80` 分只是硬失败线，不是优秀线。低于 80 必须 FAIL；80-87 代表基本可读但仍需精修；88-91 代表较好但未达到最终优秀门槛。

最终 release/private artifact 默认要求每个独立 Agent `average_score >= 92`、`lowest_score >= 88`、`blocking_issue_count = 0`，并且每个抽中样本都有逐项评分行。只写总评、缺少逐样本表格，或把“可读但略硬/偏密/略抽象/解释化/翻译腔”当作优秀分，均不得作为最终 PASS 证据。

反复出现的“可读但不顺”必须归入 `style_debt` 或相应译文质量问题族，回到目标语独立润色、源语句法重组或本书专项精修。随机抽检用于发现盲点和验证闭环，不应成为主要润色引擎。

## 专家级译文与上下文选义 / Expert Quality and Context Disambiguation

专家级译文不是“意思正确且大体顺”。翻译、审校和最终抽检必须按 `skills/expert-translation-quality/SKILL.md` 执行目标语独立阅读、原文忠实复核、多义词后文回看和句法重建。多义词、习语、称谓、术语和依赖后文判义的语法结构若被后文推翻，前文译法必须修订；保留未决歧义只能发生在原文本身有意暧昧，且译文保留了同等暧昧时。

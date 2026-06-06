# 日语到简体中文译文质量标准 / Japanese To Simplified Chinese Quality Standard

本文件是 `template/epub_pipeline/targets/zh-Hans/quality_framework/` 的简体中文目标语言规则在日语源文本场景下的应用摘要。更完整的中文目标语言质量规则见目标语言质量框架；日语源语言干扰问题见 `references/japanese_source_notes.md`；题名策略见 `references/japanese_title_strategy.md`。

## 核心标准

译文要像优秀中文译者写出来的书，而不是日文文本的中文影子。

必须同时满足：

- 忠实：事实、人物关系、视角、语气、叙述距离和暧昧程度不偏离原文。
- 可读：中文读者不被日语修饰链、省略和语序绊住。
- 有声调：叙述有节奏，关键句有力度，沉默和停顿也有功能。
- 有判断：汉字词、敬语、称谓、时代词、官能或心理描写都经过译者判断。
- 可验收：每章有控制、审校、门禁和抽检证据。

## 不合格模式

- 日语汉字词机械照搬，造成现代中文误读。
- 把日语省略关系译成中文断裂句，读者不知道谁在做什么。
- 把暧昧心理解释得过度明确。
- 把官能描写加重成色情化表达，或删弱成空泛心理说明。
- 为了“文雅”抹掉身体动作、羞耻、压迫、不适或病态心理。
- 为了“通顺”删掉原文重复、停顿、犹疑和视角限制。
- 译注太多，正文像研究笔记。
- 章节标题、目录或正文混入日文原题、读音、罗马字或长括注。
- 底本说明、青空文库工作说明、OCR 注记或现代编者注混入作者正文。

## PASS 条件

- `metadata/source_evidence.md` 和 `metadata/rights_checklist.md` 已记录来源与版权。
- `metadata/japanese_source_profile.md` 已记录底本文字形态。
- `qa/textual/japanese_textual_notes.md` 已记录文本疑难或明确无疑难。
- `metadata/book_specific_translation_research.md` 已说明作者、时代、文体、题材边界和参考材料使用边界。
- `metadata/style_profile.md` 已建立中文文体画像。
- 预翻译试译为 `PASS`。
- 每章译后控制、忠实度审校、可读性/意象审校、术语审校和章节门禁均为 `PASS`。
- EPUB 构建、publication lint、asset manifest check、reader-facing policy check、随机抽检和 release gate 均通过。

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

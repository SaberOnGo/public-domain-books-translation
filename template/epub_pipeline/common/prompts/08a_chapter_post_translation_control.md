# 08a Per-Chapter Post-Translation Full Check / 每章译后全量检查

Run this node immediately after one chapter patch is merged into the current immutable canonical generation. `chapters/translated/{chapter}.md` and `chapters/final/{chapter}.md` are read-only projections, never independent review sources.

每章 patch 合并到当前 immutable canonical generation 后，必须立即执行本节点。`chapters/translated/{chapter}.md` 与 `chapters/final/{chapter}.md` 只是同一目标文本的只读投影，不得分别审校或手改。

After proper-noun discovery, terminology, and the translation contract are locked, different chapters may be translated and audited under `references/adaptive_parallel_orchestration.md`. A translation producer owns only its chapter patch; an independent audit consumer owns the chapter audit run; the reviewer must not be a recorded translation owner for that chapter. Follow the queue's batch ID, per-unit token budget, and maximum-attempt fields; every retry after attempt 1 must preserve the prior failure evidence. A unit audit must bind the current source/target hashes, translation owner, contract, terminology, proper-noun register, occurrence ledger, reviewer/model, rubric, timestamp, and batch. Scalar `PASS` values are invalid: omission, addition, neighbor-boundary contamination, and numbers/names/negation/notes each require structured evidence. A full-chapter PASS must bind the exact ordered unit IDs and current chapter digest. Validation seals evidence per chapter; never edit a sealed run. An unrelated chapter merge must not invalidate this chapter, but any change to this chapter's source, target, owner, or locked revisions does.

A failed or just-fixed chapter may not enter downstream review, projection, build, or release. This is not a global producer stop: after the book-level locks, other independently owned chapters may continue. Treat `allow_next_chapter` as a legacy field meaning only that the current chapter may advance.

专名发现、术语和翻译合同锁定后，不同章节可按 `references/adaptive_parallel_orchestration.md` 并行翻译、并行审计。translation producer 只拥有自己的 chapter patch；独立 audit consumer 拥有该章 audit run；reviewer 不得与该章记录的 translation owner 相同。必须遵守 queue 的 batch ID、逐 unit token 预算和最大尝试次数；第 2 次起的重试必须保留前次失败证据。unit audit 必须绑定当前 source/target hash、translation owner、合同、术语、专名表、occurrence ledger、reviewer/model、rubric、时间戳和 batch。单独字符串 `PASS` 无效；遗漏、增译、邻段串译、数字/专名/否定/注释四类检查均须提供结构化 evidence。全章 PASS 必须绑定精确有序 unit ID 与当前 chapter digest。校验器按章封存证据；封存轮不得再编辑。无关章节合并不得使本章失效，但本章 source、target、owner 或锁定 revision 变化必须使其失效。

失败或刚修复的章节不得进入后续审校、投影、构建或发布。这不是全局 producer 停止信号：全书合同锁定后，其他独立 owner 的章节可继续。`allow_next_chapter` 仅表示当前章可向下游流转的旧兼容字段。

## Scope / 范围

This is a current-chapter text-quality closure gate. It must inspect the whole current chapter against the whole source chapter and the reader-facing target text. It is not a whole-book gate and not a spot check.

这是“当前章节文字质量闭环”门禁。必须对照当前整章原文和当前整章读者可见译文；不得扩大成全书门禁，也不得缩小成抽样检查。

Check at least:

- fidelity, omissions, mistranslations, unsupported additions;
- target-language readability, naturalness, polish, rhythm, and sentence breathing;
- whether the chapter reads clearly, smoothly, and, where the source permits, engagingly;
- expert-level publication quality using `skills/expert-translation-quality/SKILL.md`;
- whether the translation stage actively resolved locally decidable polysemy instead of deferring it to review;
- polysemous or context-dependent source words after downstream context has been translated;
- whether plain-language revision has damaged specialist terms, concepts, evidence chains, or the professional level of the book;
- terminology, source-term display, forbidden body renderings, and note density;
- important proper-noun display against `glossary/proper_nouns.csv`, including the user's setting value and the default strategy `3` when unset;
- note marker format against `references/note_marker_policy.md`;
- title/nav/TOC/metadata effects;
- notes, captions, alt text, figure/table/formula/image text interfaces;
- reader-visible production traces, naked source text, URLs, prompts, QA notes, TODO/FIXME, code fences, and stale template text.

至少检查：

- 忠实度、漏译、误译、无依据增译；
- 目标语可读性、自然度、成稿润色、节奏和句子呼吸；
- 本章是否尽量读得清楚、顺畅、不费劲，并在原文允许时有趣；
- 使用 `skills/expert-translation-quality/SKILL.md` 检查专家级出版质量；
- 翻译阶段是否已主动处理局部上下文可判清的多义词，而不是推给审校；
- 后文已译出后，回看复查多义词或依赖上下文判义的源语结构；
- 通俗化是否损害了专业术语、概念层级、证据链或本书应有的专业水准；
- 术语、原词呈现、正文禁用写法和注释密度；
- 重点专有名词是否符合 `glossary/proper_nouns.csv`、用户设置值，以及未设置时默认策略 `3`；
- 注号格式是否符合 `references/note_marker_policy.md`；
- 标题、nav、TOC、metadata 影响；
- 注释、图注、alt text、图表/表格/公式/图片文字接口；
- 读者可见生产痕迹、裸源语/外文、URL、prompt、QA 记录、TODO/FIXME、代码块和陈旧模板文本。

## 专家级与多义词回看 / Expert Quality and Polysemy Back-Check

本节点必须使用 `skills/expert-translation-quality/SKILL.md`。翻译阶段是多义词处理的第一责任节点；08a 负责审计该责任是否已经执行，并在后文已译出后回看当前章前文的多义词、习语、称谓、术语和依赖上下文判义的语法结构。若发现译文把局部上下文已能判清的选义推给后续审校，该轮不能 PASS。`qa/chapter_controls/{chapter}.control.md` 的最近 PASS 轮必须记录：

```text
expert_translation_skill_used: true
expert_translation_skill_path: "skills/expert-translation-quality/SKILL.md"
expert_level_review_status: "PASS"
polysemy_translation_stage_review: "PASS"
polysemy_context_review: "PASS"
polysemy_watchlist_count: {number_checked}
polysemy_revisited_count: {number_revisited}
polysemy_unresolved_count: 0
```

若回看后修正了前文选义，该轮只能记为 `FIXED_RECHECK_REQUIRED`，必须追加新的整章复查轮才可 PASS。

## Round Closure / 轮次闭环

Write the result to `qa/chapter_controls/{chapter}.control.md`.

结果写入 `qa/chapter_controls/{chapter}.control.md`。

Every round must be a full-chapter check. If any issue is found, fix it, but that round cannot pass. Record:

```text
scope: "FULL_CHAPTER"
expert_translation_skill_used: true
expert_translation_skill_path: "skills/expert-translation-quality/SKILL.md"
expert_level_review_status: "FIXED_RECHECK_REQUIRED"
polysemy_translation_stage_review: "FIXED_RECHECK_REQUIRED"
polysemy_context_review: "FIXED_RECHECK_REQUIRED"
polysemy_watchlist_count: {number_found}
polysemy_revisited_count: {number_revisited}
polysemy_unresolved_count: {number_unresolved}
issues_found: {number_found}
fixes_applied: {number_fixed}
unresolved_blocking_issues: {number_unresolved}
latest_round_status: "FIXED_RECHECK_REQUIRED"
allow_next_chapter: false
```

每一轮都必须是整章检查。只要发现任何问题，就先修复；但该轮不能 PASS，必须记录：

```text
scope: "FULL_CHAPTER"
expert_translation_skill_used: true
expert_translation_skill_path: "skills/expert-translation-quality/SKILL.md"
expert_level_review_status: "FIXED_RECHECK_REQUIRED"
polysemy_translation_stage_review: "FIXED_RECHECK_REQUIRED"
polysemy_context_review: "FIXED_RECHECK_REQUIRED"
polysemy_watchlist_count: {观察项数量}
polysemy_revisited_count: {已回看数量}
polysemy_unresolved_count: {未关闭数量}
issues_found: {发现数量}
fixes_applied: {修复数量}
unresolved_blocking_issues: {未关闭阻塞数量}
latest_round_status: "FIXED_RECHECK_REQUIRED"
allow_next_chapter: false
```

Then append a new full-chapter recheck. The workflow may continue only when the latest round records:

```text
scope: "FULL_CHAPTER"
expert_translation_skill_used: true
expert_translation_skill_path: "skills/expert-translation-quality/SKILL.md"
expert_level_review_status: "PASS"
polysemy_translation_stage_review: "PASS"
polysemy_context_review: "PASS"
polysemy_watchlist_count: {number_checked}
polysemy_revisited_count: {number_revisited}
polysemy_unresolved_count: 0
issues_found: 0
fixes_applied: 0
unresolved_blocking_issues: 0
latest_round_status: "PASS"
allow_next_chapter: true
```

然后追加新一轮整章复查。只有最近一轮记录如下字段时，流程才可继续：

```text
scope: "FULL_CHAPTER"
expert_translation_skill_used: true
expert_translation_skill_path: "skills/expert-translation-quality/SKILL.md"
expert_level_review_status: "PASS"
polysemy_translation_stage_review: "PASS"
polysemy_context_review: "PASS"
polysemy_watchlist_count: {已检查观察项数量}
polysemy_revisited_count: {已回看数量}
polysemy_unresolved_count: 0
issues_found: 0
fixes_applied: 0
unresolved_blocking_issues: 0
latest_round_status: "PASS"
allow_next_chapter: true
```

Run `npm run check:chapter-controls` or `npm run preflight:template` before moving on when tooling is available. The gate must fail if any translated chapter lacks a closed zero-issue control file.

如果工具可用，在本章进入下游投影/终稿前运行 `npm run check:chapter-controls` 或 `npm run preflight:template`。并行模式下，其他独立 owner 的章节可以继续生产；本章及依赖本章上下文的工作不得越过失败门禁。任何已译章节缺少零问题闭环 control 文件时，整书构建和发布门禁必须失败。

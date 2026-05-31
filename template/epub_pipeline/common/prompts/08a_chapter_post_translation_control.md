# 08a Per-Chapter Post-Translation Full Check / 每章译后全量检查

Run this node immediately after one chapter is written to `chapters/translated/{chapter}.md`. Do not translate the next chapter first.

每章写入 `chapters/translated/{chapter}.md` 后，必须立即执行本节点。不得先翻译下一章。

## Scope / 范围

This is a current-chapter text-quality closure gate. It must inspect the whole current chapter against the whole source chapter and the reader-facing target text. It is not a whole-book gate and not a spot check.

这是“当前章节文字质量闭环”门禁。必须对照当前整章原文和当前整章读者可见译文；不得扩大成全书门禁，也不得缩小成抽样检查。

Check at least:

- fidelity, omissions, mistranslations, unsupported additions;
- target-language readability, naturalness, polish, rhythm, and sentence breathing;
- whether the chapter reads clearly, smoothly, and, where the source permits, engagingly;
- whether plain-language revision has damaged specialist terms, concepts, evidence chains, or the professional level of the book;
- terminology, source-term display, forbidden body renderings, and note density;
- title/nav/TOC/metadata effects;
- notes, captions, alt text, figure/table/formula/image text interfaces;
- reader-visible production traces, naked source text, URLs, prompts, QA notes, TODO/FIXME, code fences, and stale template text.

至少检查：

- 忠实度、漏译、误译、无依据增译；
- 目标语可读性、自然度、成稿润色、节奏和句子呼吸；
- 本章是否尽量读得清楚、顺畅、不费劲，并在原文允许时有趣；
- 通俗化是否损害了专业术语、概念层级、证据链或本书应有的专业水准；
- 术语、原词呈现、正文禁用写法和注释密度；
- 标题、nav、TOC、metadata 影响；
- 注释、图注、alt text、图表/表格/公式/图片文字接口；
- 读者可见生产痕迹、裸源语/外文、URL、prompt、QA 记录、TODO/FIXME、代码块和陈旧模板文本。

## Round Closure / 轮次闭环

Write the result to `qa/chapter_controls/{chapter}.control.md`.

结果写入 `qa/chapter_controls/{chapter}.control.md`。

Every round must be a full-chapter check. If any issue is found, fix it, but that round cannot pass. Record:

```text
scope: "FULL_CHAPTER"
issues_found: {number_found}
fixes_applied: {number_fixed}
unresolved_blocking_issues: {number_unresolved}
latest_round_status: "FIXED_RECHECK_REQUIRED"
allow_next_chapter: false
```

每一轮都必须是整章检查。只要发现任何问题，就先修复；但该轮不能 PASS，必须记录：

```text
scope: "FULL_CHAPTER"
issues_found: {发现数量}
fixes_applied: {修复数量}
unresolved_blocking_issues: {未关闭阻塞数量}
latest_round_status: "FIXED_RECHECK_REQUIRED"
allow_next_chapter: false
```

Then append a new full-chapter recheck. The workflow may continue only when the latest round records:

```text
scope: "FULL_CHAPTER"
issues_found: 0
fixes_applied: 0
unresolved_blocking_issues: 0
latest_round_status: "PASS"
allow_next_chapter: true
```

然后追加新一轮整章复查。只有最近一轮记录如下字段时，流程才可继续：

```text
scope: "FULL_CHAPTER"
issues_found: 0
fixes_applied: 0
unresolved_blocking_issues: 0
latest_round_status: "PASS"
allow_next_chapter: true
```

Run `npm run check:chapter-controls` or `npm run preflight:template` before moving on when tooling is available. The gate must fail if any translated chapter lacks a closed zero-issue control file.

如果工具可用，进入下一章前运行 `npm run check:chapter-controls` 或 `npm run preflight:template`。任何已译章节缺少零问题闭环 control 文件时，门禁必须失败。

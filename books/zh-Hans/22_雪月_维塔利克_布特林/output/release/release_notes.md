# Release Notes / 发布说明

## Release v0.0.4 / 版本 v0.0.4

status: PASS
main_version: 0
sub_version: 0
patch_version: 4
created_at: 2026-11-10T05:49:32Z
epubs:
- target_only: `雪月_v0.0.4.epub` sha256=`49549556155dcd902011cbe7c04802f76ef075f37e0c1b6b8e301e2114b7db19` size_bytes=`2117254`
- bilingual_parallel: `雪月_中英双语_v0.0.4.epub` sha256=`8f2b1e9365a882123b20fc75afd8d5909c22717c882ab1394d39030e64267b25` size_bytes=`2482821`
- source_original: `雪月_英文原文_v0.0.4.epub` sha256=`0eeff2944c54c8f7acddc6a2dc714519c3751a2f052510ddd2ec4783d9bbc9d8` size_bytes=`1077819`

## Release Reason / 发布原因

v0.0.4：全书成品质检与抽检后的修订版 / Whole-book finished-artifact QA and spot-check revision

## Changes / 修改内容

- 移除书中 GPL v3 全文页，仅在书籍简介用一句话写明授权；中文版封面去掉图下多余文字；双语版 dc:identifier 与中文版区分 / GPL v3 full-text page removed, licence stated in one sentence in the introduction; zh cover text removed; bilingual edition has its own dc:identifier
- 按抽检修订 13 处译文（漏译补回、术语统一：伤亡比、公共汽车、参议员，图26.3 题注补“无人机”等）/ 13 translation fixes from spot-checks (omissions restored, term unification, figure 26.3 caption)
- 原文版与双语版英文栏把作者原文的 _强调_ 渲染为真正的斜体；第1章相邻中文按钮标签不再含半角空格 / Author's _emphasis_ rendered as real italics in source-original and bilingual editions; no ASCII space between adjacent CJK labels in chapter 1

## Issues / 问题点

- 审校与阅读由AI完成，无人工或有声朗读；未变更单元沿用此前封存复核结果；文学门禁判定逐条沿用，未新增阅读员判断 / AI-only review; unchanged units carry forward earlier sealed reviews; literary judgments carried forward

## Fixes / 修复方式

- 成品 EPUB 检查器识别带命名空间前缀的 XHTML，消除误报 / Final-EPUB checker understands namespace-prefixed XHTML

## QA And Evidence / QA 与证据

- source_epub_target_only: `output/book.epub`
- source_epub_bilingual_parallel: `output/book_bilingual_parallel.epub`
- source_epub_source_original: `output/book_english.epub`
- random_spotcheck_round: `reviews/random_spotcheck/round_018`
- random_spotcheck_validation: `reviews/random_spotcheck/round_018/validation_report.json`
- random_spotcheck_status: `PASS`
- random_spotcheck_require_pass: `True`
- current_review_run_id: `a1bdcdc96f1f3e18d2433a9f`
- current_run_pass_rounds: `2/2`
- release_confidence: `1.0`
- epubcheck: `output/epubcheck.json`
- epubcheck_fatal: `0`
- epubcheck_error: `0`
- epubcheck_warning: `0`
- epubcheck_target_only: `output/epubcheck.json` artifact_sha256=`49549556155dcd902011cbe7c04802f76ef075f37e0c1b6b8e301e2114b7db19` hash_match=`True`
- epubcheck_bilingual_parallel: `output/epubcheck_bilingual_parallel.json` artifact_sha256=`8f2b1e9365a882123b20fc75afd8d5909c22717c882ab1394d39030e64267b25` hash_match=`True`
- epubcheck_source_original: `output/epubcheck_source_original.json` artifact_sha256=`0eeff2944c54c8f7acddc6a2dc714519c3751a2f052510ddd2ec4783d9bbc9d8` hash_match=`True`
- translation_artifact_gate: `output/translation_unit_artifact_check.json`
- translation_artifact_gate_status: `PASS`
- real_reader_validation_status: `PASS`
- publication_lint: `output/publication_lint.json`
- publication_lint_issue_count: `0`
- translation_metrics: `output/release/translation_metrics.json`
- translation_metrics_estimate_status: `PASS`
- translation_metrics_actual_status: `PASS`
- translation_metrics_primary_book_type: `fiction`
- translation_metrics_difficulty_level: `high`
- translation_metrics_actual_difficulty_level: `high`
- translation_metrics_actual_active_hours: `MISSING`
- translation_metrics_total_tokens: `3307476482`
- literary_style_review: `qa/literary_style/literary_style_review.md`
- literary_style_status: `PASS`
- literary_target_only_reading_score: `5.0`
- literary_read_aloud_awkward_sentence_count: `0.0`
- literary_unresolved_style_debt_count: `0.0`
- literary_literal_explanatory_style_debt_count: `0.0`
- literary_high_impact_sections_reviewed: `True`
- literary_author_preface_and_first_chapter_reviewed: `True`

## Risks / 风险

- 阅读器证据为 Calibre 自动探测，无人工目视复核；在线书库图表与表格显示依赖 LifeBook 后台净化修复上线 / Reader evidence is automated; online-library table and figure display depends on the LifeBook sanitizer fix

## Next Iteration / 下一轮迭代

- Reader feedback, review comments, or automated QA findings should create the next patch release. / 后续读者反馈、审校意见或自动化 QA 发现的问题应进入下一个小版本发布。
- Patch version increases by 1 for every release artifact created by this script. / 本脚本每创建一次发布产物，小版本号递增 1。


## Release v0.0.3 / 版本 v0.0.3

status: PASS
main_version: 0
sub_version: 0
patch_version: 3
created_at: 2026-11-09T23:51:27Z
epubs:
- target_only: `雪月_v0.0.3.epub` sha256=`80f52e1e7c540ca6cfdc8fd6dda66268bfb545c171bb495e8df7283b2b1c3ebb` size_bytes=`2130259`
- bilingual_parallel: `雪月_中英双语_v0.0.3.epub` sha256=`64fe611dce93ae9fcf15e9bbb088554880a1111063f951303fd036eb033fbf5f` size_bytes=`2495775`
- source_original: `雪月_英文原文_v0.0.3.epub` sha256=`98835a26661d6e8fdfc2b3a02b3aac3143e0a846f27fac22ac19564c62565186` size_bytes=`1090350`

## Release Reason / 发布原因

v0.0.3：全书逐单元语义复核、文学门禁与随机抽检重做后的修订版 / Full per-unit semantic re-review, literary gate and random spot-check revision

## Changes / 修改内容

- 全书译文按评审与抽检意见逐处精修，术语、人名与标点统一 / Translation refined per review and spot-check findings; terms, names and punctuation unified
- 三版EPUB（中文、中英双语、原文）重建，EPUBCheck 0/0/0 / Three EPUBs rebuilt, EPUBCheck 0/0/0

## Issues / 问题点

- 审校与阅读由AI完成，无人工或有声朗读；未变更单元沿用此前封存的复核结果 / Review and reading by AI only, no human or audio reading; unchanged units carry forward earlier sealed reviews

## Fixes / 修复方式

- 修复截断句、专名标记、分号例外与阅读器证据过期 / Fixed truncated sentences, entity markers, semicolon exceptions and stale reader evidence

## QA And Evidence / QA 与证据

- source_epub_target_only: `output/book.epub`
- source_epub_bilingual_parallel: `output/book_bilingual_parallel.epub`
- source_epub_source_original: `output/book_english.epub`
- random_spotcheck_round: `reviews/random_spotcheck/round_013`
- random_spotcheck_validation: `reviews/random_spotcheck/round_013/validation_report.json`
- random_spotcheck_status: `PASS`
- random_spotcheck_require_pass: `True`
- current_review_run_id: `a1bdcdc96f1f3e18d2433a9f`
- current_run_pass_rounds: `2/2`
- release_confidence: `1.0`
- epubcheck: `output/epubcheck.json`
- epubcheck_fatal: `0`
- epubcheck_error: `0`
- epubcheck_warning: `0`
- epubcheck_target_only: `output/epubcheck.json` artifact_sha256=`80f52e1e7c540ca6cfdc8fd6dda66268bfb545c171bb495e8df7283b2b1c3ebb` hash_match=`True`
- epubcheck_bilingual_parallel: `output/epubcheck_bilingual_parallel.json` artifact_sha256=`64fe611dce93ae9fcf15e9bbb088554880a1111063f951303fd036eb033fbf5f` hash_match=`True`
- epubcheck_source_original: `output/epubcheck_source_original.json` artifact_sha256=`98835a26661d6e8fdfc2b3a02b3aac3143e0a846f27fac22ac19564c62565186` hash_match=`True`
- translation_artifact_gate: `output/translation_unit_artifact_check.json`
- translation_artifact_gate_status: `PASS`
- real_reader_validation_status: `PASS`
- publication_lint: `output/publication_lint.json`
- publication_lint_issue_count: `0`
- translation_metrics: `output/release/translation_metrics.json`
- translation_metrics_estimate_status: `PASS`
- translation_metrics_actual_status: `PASS`
- translation_metrics_primary_book_type: `fiction`
- translation_metrics_difficulty_level: `high`
- translation_metrics_actual_difficulty_level: `high`
- translation_metrics_actual_active_hours: `MISSING`
- translation_metrics_total_tokens: `3307476482`
- literary_style_review: `qa/literary_style/literary_style_review.md`
- literary_style_status: `PASS`
- literary_target_only_reading_score: `5.0`
- literary_read_aloud_awkward_sentence_count: `0.0`
- literary_unresolved_style_debt_count: `0.0`
- literary_literal_explanatory_style_debt_count: `0.0`
- literary_high_impact_sections_reviewed: `True`
- literary_author_preface_and_first_chapter_reviewed: `True`

## Risks / 风险

- 阅读器证据为Calibre自动化探测，无人工目视复核 / Reader evidence is automated Calibre probing without human visual review

## Next Iteration / 下一轮迭代

- Reader feedback, review comments, or automated QA findings should create the next patch release. / 后续读者反馈、审校意见或自动化 QA 发现的问题应进入下一个小版本发布。
- Patch version increases by 1 for every release artifact created by this script. / 本脚本每创建一次发布产物，小版本号递增 1。


## Release v0.0.2 / 版本 v0.0.2

status: PASS
main_version: 0
sub_version: 0
patch_version: 2
created_at: 2026-10-05T05:07:45Z
epubs:
- target_only: `雪月_v0.0.2.epub` sha256=`76cfc68cf625c619d83678f786b41b7b602d2de66e77d275e35462b2dc72068d` size_bytes=`2129654`
- bilingual_parallel: `雪月_中英双语_v0.0.2.epub` sha256=`c94d48ad7b7921b160483faed6fbde591581b58e96db08745633ce1590a3315a` size_bytes=`2495045`
- source_original: `雪月_英文原文_v0.0.2.epub` sha256=`68bb6e0667eb52d583281fbf319efc3b2fe6e856d59e131278419255a7e166e1` size_bytes=`1090504`

## Release Reason / 发布原因

完成《雪月》英文、简体中文与中英双语首个正式版本；GPL 对应源码及三 EPUB、两网页完整隔离重建通过。 / First validated Snowmoon release with three EPUBs and a reproducible GPL corresponding-source package.

## Changes / 修改内容

- 33/33 部分、4373 单元独立全量审校；32 正文章节门禁、问题族闭环及当前连续两轮 A/B 优秀分层抽检通过。 / Independent full-section reviews, defect-family closure and two consecutive current A/B random-review rounds passed.
- 保留原文图片与样式，完成中文及双语静态网页、三 EPUBCheck 零错误零警告和实际原生阅读器验证；不含 LifeBook Digest。 / Source assets and style retained; both static web editions, all three EPUBChecks and native-reader evidence validated; no LifeBook Digest.

## Issues / 问题点

- No new issue entry was declared for this release note. / 本发布说明未声明新的问题条目。

## Fixes / 修复方式

- 旧源码 v0.0.1 的 OPF 时间比较漏认 namespace 前缀；修复后 38 项回归及 v0.0.2 六步全五版重建通过，旧包及失败记录保留。 / Namespace-aware modification-time comparison repaired, with 38 regression cases and the full v0.0.2 rebuild; prior evidence preserved.

## QA And Evidence / QA 与证据

- source_epub_target_only: `output/book.epub`
- source_epub_bilingual_parallel: `output/book_bilingual_parallel.epub`
- source_epub_source_original: `output/book_english.epub`
- random_spotcheck_round: `reviews/random_spotcheck/round_005`
- random_spotcheck_validation: `reviews/random_spotcheck/round_005/validation_report.json`
- random_spotcheck_status: `PASS`
- random_spotcheck_require_pass: `True`
- current_review_run_id: `7990b5d2a643ff7a86d8e8fd`
- current_run_pass_rounds: `2/2`
- release_confidence: `1.0`
- epubcheck: `output/epubcheck.json`
- epubcheck_fatal: `0`
- epubcheck_error: `0`
- epubcheck_warning: `0`
- epubcheck_target_only: `output/epubcheck.json` artifact_sha256=`76cfc68cf625c619d83678f786b41b7b602d2de66e77d275e35462b2dc72068d` hash_match=`True`
- epubcheck_bilingual_parallel: `output/epubcheck_bilingual_parallel.json` artifact_sha256=`c94d48ad7b7921b160483faed6fbde591581b58e96db08745633ce1590a3315a` hash_match=`True`
- epubcheck_source_original: `output/epubcheck_source_original.json` artifact_sha256=`68bb6e0667eb52d583281fbf319efc3b2fe6e856d59e131278419255a7e166e1` hash_match=`True`
- translation_artifact_gate: `output/translation_unit_artifact_check.json`
- translation_artifact_gate_status: `PASS`
- real_reader_validation_status: `PASS`
- publication_lint: `output/publication_lint.json`
- publication_lint_issue_count: `0`
- translation_metrics: `output/release/translation_metrics.json`
- translation_metrics_estimate_status: `PASS`
- translation_metrics_actual_status: `PASS`
- translation_metrics_primary_book_type: `fiction`
- translation_metrics_difficulty_level: `high`
- translation_metrics_actual_difficulty_level: `high`
- translation_metrics_actual_active_hours: `MISSING`
- translation_metrics_total_tokens: `3307476482`
- literary_style_review: `qa/literary_style/literary_style_review.md`
- literary_style_status: `PASS`
- literary_target_only_reading_score: `5.0`
- literary_read_aloud_awkward_sentence_count: `0.0`
- literary_unresolved_style_debt_count: `0.0`
- literary_literal_explanatory_style_debt_count: `0.0`
- literary_high_impact_sections_reviewed: `True`
- literary_author_preface_and_first_chapter_reviewed: `True`

## Risks / 风险

- 预估记录在开工后补齐，保留历史流程偏差；有效工时不可测量；宿主 token 截止质量封版，排除后续分发与更新。 / Estimate timing deviation retained; active hours unavailable; usage is bounded at the quality cutoff.
- LifeBook 书库接入尚未配置，交付可部署中文及双语网页，不声称线上已更新。 / LifeBook integration is not configured; deployable web editions are supplied.

## Next Iteration / 下一轮迭代

- Reader feedback, review comments, or automated QA findings should create the next patch release. / 后续读者反馈、审校意见或自动化 QA 发现的问题应进入下一个小版本发布。
- Patch version increases by 1 for every release artifact created by this script. / 本脚本每创建一次发布产物，小版本号递增 1。

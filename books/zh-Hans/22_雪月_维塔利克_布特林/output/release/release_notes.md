# Release Notes / 发布说明

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

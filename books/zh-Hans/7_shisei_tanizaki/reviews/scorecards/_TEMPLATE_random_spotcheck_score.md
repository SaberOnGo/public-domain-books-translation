# 分层随机抽检评分表模板 / Stratified Random Spot-Check Scorecard Template

review_round: "round_001"
sample_manifest: "reviews/random_spotcheck/round_001/random_sample_manifest.json"
latest_manifest: "reviews/random_spotcheck/random_sample_manifest.json"
source_scope: "chapters/final + reader-facing assets"
status: "DRAFT" # PASS | FAIL

## Strata / 抽样层

| stratum | candidate_count | sample_count | full_scan | estimated_confidence | status |
| --- | ---: | ---: | --- | ---: | --- |
| paragraph | 0 | 0 | false | 0 | DRAFT |
| table | 0 | 0 | false | 0 | DRAFT |
| figure | 0 | 0 | false | 0 | DRAFT |
| formula | 0 | 0 | false | 0 | DRAFT |
| caption_note | 0 | 0 | false | 0 | DRAFT |

## Agent A

review_file: "reviews/random_spotcheck/round_001/reviews/agent_a_review.md"
compat_review_file: "reviews/agent_a/random_spotcheck_review.md"
sample_count: 0
average_score: 0
lowest_score: 0
blocking_issue_count: 0
status: "DRAFT" # PASS | FAIL

## Agent B

review_file: "reviews/random_spotcheck/round_001/reviews/agent_b_review.md"
compat_review_file: "reviews/agent_b/random_spotcheck_review.md"
sample_count: 0
average_score: 0
lowest_score: 0
blocking_issue_count: 0
status: "DRAFT" # PASS | FAIL

## Fix Closure / 修复闭环

fix_log: "reviews/random_spotcheck/round_001/fixes/fix_log.md"
closure_check: "reviews/random_spotcheck/round_001/verification/closure_check.md"
fix_log_status: "DRAFT" # PASS | FAIL
closure_status: "DRAFT" # PASS | FAIL
new_seed_round_after_rework: "required_if_failed"
validator: "npm run review:random-validate:pass"
validator_status: "DRAFT" # PASS | FAIL
validation_report: "reviews/random_spotcheck/round_001/validation_report.json"
release_confidence: 0
target_confidence: 0.80
release_confidence_status: "DRAFT" # PASS | FAIL

## PASS 条件 / PASS Criteria

- 两个 Agent 必须独立完成，不得互相参考。
- 抽样必须覆盖 `paragraph`、`table`、`figure`、`formula`、`caption_note` 中实际存在的层。
- 表格、图片、公式、图注/注释不得被普通段落样本替代。
- 每个样本必须逐项评分；不得只写总评。
- 每个 Agent 平均分必须 >= 75。
- 任一单项 < 70，则本轮 FAIL。
- 任一 P0/P1/P2、读不懂、事实误解、术语/专名/译注错误、表格错误、图片裁剪/标签错误、公式/证明错误，则本轮 FAIL。
- FAIL 后必须写入 `reviews/revision_route.md`，回到精校或更早阶段修复；修复后旧问题必须在 `fix_log.md` 和 `closure_check.md` 定点关闭，并使用新 seed 重新抽样。
- `npm run review:random-validate:pass` 必须通过。
- `validation_report.json.release_confidence` 必须 >= 0.80。

## 结论 / Conclusion

final_status: "DRAFT"
revision_route_required: true
notes: ""

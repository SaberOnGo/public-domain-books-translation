# 随机段落抽检评分表模板 / Random Spot-Check Scorecard Template

review_round: "YYYY-MM-DD-round-1"
sample_manifest: "reviews/random_spotcheck/random_sample_manifest.json"
source_scope: "chapters/final"
status: "DRAFT" # PASS | FAIL

## Agent A

review_file: "reviews/agent_a/random_spotcheck_review.md"
sample_count: 10
average_score: 0
lowest_score: 0
blocking_issue_count: 0
status: "DRAFT" # PASS | FAIL

## Agent B

review_file: "reviews/agent_b/random_spotcheck_review.md"
sample_count: 10
average_score: 0
lowest_score: 0
blocking_issue_count: 0
status: "DRAFT" # PASS | FAIL

## PASS 条件 / PASS Criteria

- 两个 Agent 必须独立完成，不得互相参考。
- 每个 Agent 至少抽检 10 个随机正文段落。
- 每个 Agent 平均分必须 >= 75。
- 任一单段 < 70，则本轮 FAIL。
- 任一段存在读不懂、事实误解、英文句法硬搬、无依据润饰、术语/专名/译注错误，则本轮 FAIL。
- FAIL 后必须写入 `reviews/revision_route.md`，回到精校或更早阶段修复；修复后重新生成随机样本。

## 结论 / Conclusion

final_status: "DRAFT"
revision_route_required: true
notes: ""

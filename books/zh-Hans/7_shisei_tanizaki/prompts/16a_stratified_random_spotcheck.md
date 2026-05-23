# 16a 分层随机抽检与修复闭环 / Stratified Random Spot-Check and Fix Closure

## 触发条件 / Trigger

第一版全书 EPUB 已生成后立即执行本步骤。只要存在 `output/book.epub`，主执行 AI 就不得跳过本模块进入最终输出、复盘或 `DONE`。

Run this step immediately after the first full-book `output/book.epub` exists. The main executor must not skip this gate.

## 必读 / Must Read

- `references/stratified_random_spotcheck.md`
- `PIPELINE_SPEC.md`
- `automation_contract.md`
- `preproduction/stage1/production_spec.md`
- `preproduction/stage2_sample/sample_review.md`
- `output/publication_lint.json`
- `output/asset_manifest_check.json`
- `output/epubcheck.json` 或 `output/epubcheck.log`

若启用科学、数学、天文、图表密集 profile，还必须读取：

- `qa/technical/diagram_table_inventory.md`
- `qa/technical/verification_plan.md`
- `qa/technical/table_validation_log.md`
- `qa/technical/numeric_validation_log.md`
- `qa/technical/proof_dependency_map.md`
- `qa/technical/diagram_redraw_workflow.md`

## 执行 / Execution

运行确定性抽样脚本：

```powershell
npm run review:random-samples
```

如果 npm 脚本不可用，运行：

```powershell
python scripts/select_random_review_passages.py --source-dir chapters/final --agents 2 --samples-per-agent 60 --rounds-planned 4 --target-confidence 0.80 --defect-rate 0.10 --profile auto
```

默认预算解释：

```text
T = 4
agents = 2
paragraph/text = 每 agent 每轮 60
table = N<=80 全检，否则每轮总抽 20
figure = N<=80 全检，否则每轮总抽 20
formula/proof = N<=100 全检，否则每轮总抽 20
caption/note = N<=120 全检，否则每轮总抽 20
```

这是发布前高质量但控制 token 预算的默认值。若任一层发现 P0/P1/P2，下一轮随机抽样量保持不变；若同层连续两轮发现 P0/P1/P2，必须进入定向专项审计和闭环复查，默认不强制全检。

脚本会读取最近 `round_XXX/reviews/*_review.md` 中带样本单元编号的 P0/P1/P2 行，并自动把该层写入 manifest 的风险和专项审计字段；主执行 AI 不得手动删除这些结果。

随后运行：

```powershell
npm run review:random-validate
```

## Agent 派生 / Independent Agents

主执行 AI 必须派生至少 2 个独立评审 Agent。每个 Agent 只读取自己的样本目录和必要模板，不得互相参考：

- `reviews/random_spotcheck/round_XXX/samples/agent_a/`
- `reviews/random_spotcheck/round_XXX/samples/agent_b/`

每个 Agent 必须输出到：

- `reviews/random_spotcheck/round_XXX/reviews/agent_a_review.md`
- `reviews/random_spotcheck/round_XXX/reviews/agent_b_review.md`

并同步更新兼容路径：

- `reviews/agent_a/random_spotcheck_review.md`
- `reviews/agent_b/random_spotcheck_review.md`

## 评审要求 / Review Requirements

每个样本必须逐项评分并判断是否返工。不得只写总评。

必须检查：

- 正文段落：忠实度、目标语言可读性、术语、专名、叙述关系、AI 味。
- 表格：行列、表头、数值、单位、caption、XHTML 结构、与来源表对应关系。
- 图片：裁剪是否过大或过小、标签是否缺失、是否带入周边无关文字、插入点、caption、alt、分辨率。
- 公式/证明块：符号、前后依赖、数学/科学关系、读者可理解性。
- 图注/表注/注释：是否与正文和图表一致，是否误导读者。

任一 P0/P1/P2、任一单项 < 70、任一读不懂、任一事实/术语/数值/图表/公式错误，均判为本轮 FAIL。

## 修复 / Fix

如果本轮 FAIL，主执行 AI 必须：

1. 更新 `reviews/revision_route.md`。
2. 修复对应章节、资源、表格、图片、公式、metadata 或构建脚本。
3. 在 `reviews/random_spotcheck/round_XXX/fixes/fix_log.md` 记录修复。
4. 在 `reviews/random_spotcheck/round_XXX/verification/closure_check.md` 定点复查旧问题。
5. 使用新 seed 再运行一轮抽样，生成 `round_YYY/`。

修复后 OK 概率可按 75% 作为迭代估计，但不能作为退出依据。退出依据是旧问题定点关闭、新 seed 抽检通过、校验脚本通过。

## PASS 条件 / PASS Criteria

本步骤 PASS 必须同时满足：

- 至少 2 个独立 Agent 评审为 `PASS`。
- `fix_log.md` 为 `PASS`。
- `closure_check.md` 为 `PASS`。
- `validation_report.json` 为 `PASS`，且 `release_confidence >= 0.80`。
- `reviews/scorecards/random_spotcheck_score.md` 记录本轮 PASS。
- `npm run review:random-validate:pass` 通过。
- 若本轮前发生返工，当前通过轮次必须使用新 seed。

未 PASS 时，`state/pipeline_state.json.status` 必须设为 `RANDOM_SPOTCHECK_FAILED` 或 `REVISION_ROUTING_REQUIRED`，不得进入最终输出。

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
python scripts/select_random_review_passages.py --source-dir chapters/final --agents 2 --samples-per-agent 120 --rounds-planned 4 --target-confidence 0.80 --defect-rate 0.10 --profile auto
```

用户可以指定当前执行批次所需的连续无问题 PASS 轮次数，取值必须 `>=1`；未指定时默认 `2`。等效默认命令应使用：

```powershell
python scripts/select_random_review_passages.py --source-dir chapters/final --agents 2 --samples-per-agent 120 --rounds-planned 4 --min-current-run-pass-rounds 2 --target-confidence 0.80 --defect-rate 0.10 --profile auto
```

严禁把旧 Agent、旧 release、旧 private artifact 之前已经 PASS 的轮次算作本次执行的最后 PASS 轮次。那些记录只能说明历史状态，不能替当前 AI 完成本次抽检。当前执行者必须生成带 `review_run_id` 与 `generated_at` 的新轮次，并让本次运行的最新连续 PASS 轮次达到用户指定数量；用户未指定时按 2 轮执行。

默认预算解释：

```text
T = 4
agents = 2
paragraph/text = 每 agent 每轮 120
table = N<=80 全检，否则每轮总抽 20
figure = N<=80 全检，否则每轮总抽 20
formula/proof = N<=100 全检，否则每轮总抽 20
caption/note = N<=120 全检，否则每轮总抽 20
```

这是发布前高质量但控制 token 预算的默认值。若任一层、任一样本发现任何需要修复或可能系统性复现的问题，本轮立即把发现归纳为问题族，并执行全书同类问题审计和闭环；不得只修被抽中的样本，也不得等到第二轮才全书检查。同层可被标记为高风险，用于后续抽样和人工复核，但不能替代本轮全书同类问题审计。

若发现的是译文质量问题族，必须读取并使用 `skills/translation-quality-defect-families/SKILL.md`。质量问题族包括但不限于忠实度偏移、中文不顺、术语漂移、标题/小标题超载、注释误导、图表文字接口错误、英文句法残留、过硬过直句、短句切断、比喻自撞、排比标点拖拽、代词指代不清、过度解释或加戏。先用 `rg`、术语表、禁用正文写法、标题映射、抽样 manifest 和小上下文原文对照收集候选，再把候选片段交给 agent 复核。书内闭环后，必须把可复用经验合并回填到该 skill，不能盲目重复追加。

每个发现问题的抽检轮次都必须在 `fix_log.md` 和 `closure_check.md` 写入机器可读的 skill 回填决策。若发现译文质量问题族，`translation_quality_skill_backfill` 必须是 `UPDATED` 或 `MERGED`，`translation_quality_skill_backfill_path` 必须是 `skills/translation-quality-defect-families/SKILL.md`，并用 `translation_quality_skill_backfill_summary` 说明本次合并了什么发现方法、归纳口径、低 token 审计式、修复模式和复查模式；`closure_check.md` 必须写 `translation_quality_skill_backfill_verified: true`。若本轮只有格式、资产、路径、EPUB 结构等非译文质量问题，也必须写 `translation_quality_skill_backfill: "NOT_APPLICABLE"` 和具体理由。

脚本会读取最近 `round_XXX/reviews/*_review.md` 中带样本单元编号的 P0/P1/P2 行，并自动把该层写入 manifest 的风险字段；主执行 AI 不得手动删除这些结果。风险字段只用于后续抽样和复核，不能替代本轮问题族全书同类审计。

随后运行：

```powershell
npm run review:random-validate
```

最终退出或创建 release/private artifact 前必须运行：

```powershell
npm run review:random-validate:pass
```

`validation_report.json` 必须显示 `current_run_pass_rounds_required >= 1` 且 `current_run_pass_rounds_count >= current_run_pass_rounds_required`；用户未指定时默认要求 2。如果只看到旧轮次 PASS，或报告缺少 `current_review_run_id` / `current_run_pass_rounds_count`，本步骤未完成。

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

任一 P0/P1/P2、任一单项 < 80、任一读不懂、任一事实/术语/数值/图表/公式错误，均判为本轮 FAIL。

## 修复 / Fix

如果本轮 FAIL，主执行 AI 必须：

1. 更新 `reviews/revision_route.md`。
2. 把每个发现归纳为问题族，例如专名误译、术语硬译、短句切断、比喻自撞、排比标点拖拽、代词指代不清、英文句法、过度解释、加戏、脚注裸露、图表标签错误、公式符号错误、注释/metadata 不一致。
3. 对每个问题族执行全书同类问题审计，至少覆盖 `chapters/final/`、frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML；不得只修改被抽中的样本。译文质量问题族必须按 `skills/translation-quality-defect-families/SKILL.md` 先用低 token 方法收集候选，再做小上下文 agent 复核。
4. 修复对应章节、资源、表格、图片、公式、metadata 或构建脚本中的全部确认命中；合理例外必须记录原因。
5. 在 `reviews/random_spotcheck/round_XXX/fixes/fix_log.md` 记录问题族、检索式或审计方法、范围、命中数、修复位置和例外。可复用的译文质量经验必须合并回填到 `skills/translation-quality-defect-families/SKILL.md`，并填写 `defect_family_count`、`translation_quality_defect_family_count`、`translation_quality_skill_backfill`、`translation_quality_skill_backfill_path`、`translation_quality_skill_backfill_summary` 或 `translation_quality_skill_backfill_not_applicable_reason`。
6. 在 `reviews/random_spotcheck/round_XXX/verification/closure_check.md` 定点复查旧问题，确认全书同类问题审计已关闭；若有译文质量问题族，还必须确认 `translation_quality_skill_backfill_verified: true`。
7. 使用新 seed 再运行一轮抽样，生成 `round_YYY/`。

If a sample reveals a defect, treat it as evidence of a possible systemic issue. Classify the defect family, audit the whole reader-facing book for similar cases, fix all confirmed matches, document exceptions, and only then proceed to a new-seed round.

修复后 OK 概率可按 75% 作为迭代估计，但不能作为退出依据。退出依据是旧问题定点关闭、新 seed 抽检通过、校验脚本通过。

## PASS 条件 / PASS Criteria

本步骤 PASS 必须同时满足：

- 至少 2 个独立 Agent 评审为 `PASS`。
- `fix_log.md` 为 `PASS`。
- `closure_check.md` 为 `PASS`。
- `fix_log.md` 和 `closure_check.md` 明确记录每个问题族的全书同类问题审计已经关闭。
- 若当前执行批次任一问题轮次发现译文质量问题族，`fix_log.md` 证明 skill 已 `UPDATED` 或 `MERGED`，`closure_check.md` 记录 `translation_quality_skill_backfill_verified: true`；若无译文质量问题族，必须有 `NOT_APPLICABLE` 和具体理由。
- `validation_report.json` 为 `PASS`，且 `release_confidence >= 0.80`。
- `reviews/scorecards/random_spotcheck_score.md` 记录本轮 PASS。
- `npm run review:random-validate:pass` 通过。
- `validation_report.json.current_run_pass_rounds_required >= 1`，且 `validation_report.json.current_run_pass_rounds_count >= validation_report.json.current_run_pass_rounds_required`；用户未指定时默认要求 2；旧 PASS 轮次不得计入本次执行。
- 若本轮前发生返工，当前通过轮次必须使用新 seed。

未 PASS 时，`state/pipeline_state.json.status` 必须设为 `RANDOM_SPOTCHECK_FAILED` 或 `REVISION_ROUTING_REQUIRED`，不得进入最终输出。

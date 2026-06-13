# 分层随机抽检门禁 / Stratified Random Spot-Check Gate

本文件定义第一版全书 EPUB 生成后必须执行的强制质量门禁。它适用于所有语言方向；具体目标语言风格规则由 `targets/{target}/` 和 `{language-pair-template}/` 模板追加。

This file defines the mandatory post-EPUB quality gate. It applies to every language direction; target-language and source-to-target rules add their own review criteria.

## 核心定义 / Core Definition

`N` 不是正文段落数，也不是 EPUB 页数。`N` 是读者可见审计单元总数：

`N = reader-visible audit units`

审计单元至少包括：

- `paragraph`：正文段落。
- `table`：Markdown/XHTML 表格、数值表、星表、术语表等读者可见表格。
- `figure`：图片、图版、示意图、扫描裁剪图、几何图、天文图、地图。
- `formula`：公式块、证明块、符号推导块。
- `caption_note`：图注、表注、脚注、注释、读者可见说明段。

表格、图片和公式不得被普通段落抽样覆盖。含图表、公式、科学或数学内容的书籍必须对这些层单独抽样。

Tables, figures, and formula/proof blocks are separate strata. They must not be hidden inside ordinary paragraph sampling.

## 概率目标 / Probability Target

每一层单独计算漏检风险。若某层仍有至少 `q` 比例的问题单元，抽样目标是让发现该系统性问题的概率达到 `target_confidence`。

Per stratum, if at least `q` of units are defective, sampling should discover that systematic problem with at least `target_confidence`.

近似公式：

```text
required_total_samples >= ln(1 - target_confidence) / ln(1 - q)
```

默认参数：

```text
target_confidence = 0.80
q = 0.10
T = 4 planned rounds
agents = 2
```

这表示：如果某一层仍有至少 10% 的系统性问题，计划抽检轮次合计应有至少 80% 概率发现。

全书发布置信度按实际存在的抽样层取最小值：

```text
release_confidence = min_h confidence_h
confidence_h = 1 - (1 - q) ** planned_samples_h
```

若某层全检，`confidence_h = 1.0`。最终退出条件是 `release_confidence >= 0.80`，且所有硬门禁通过。概率分只处理抽样覆盖风险；未关闭 P0/P1/P2、Agent FAIL、EPUBCheck fatal/error、版权/来源不清楚均直接失败。

## 强制脚本 / Mandatory Scripts

第一版 `output/book.epub` 生成后，主执行 AI 必须运行：

```powershell
npm run review:random-samples
```

等效命令：

```powershell
python scripts/select_random_review_passages.py --source-dir chapters/final --agents 2 --samples-per-agent 120 --rounds-planned 4 --target-confidence 0.80 --defect-rate 0.10 --profile auto
```

用户可以指定当前执行批次所需的连续无问题 PASS 轮次数，取值必须 `>=1`；未指定时默认 `2`。等效默认命令应包含：

```powershell
python scripts/select_random_review_passages.py --source-dir chapters/final --agents 2 --samples-per-agent 120 --rounds-planned 4 --min-current-run-pass-rounds 2 --target-confidence 0.80 --defect-rate 0.10 --profile auto
```

The user may specify any current-run consecutive PASS requirement of `>=1`; when unspecified, the default is 2. Historical PASS rounds from earlier agents, earlier release artifacts, or earlier private artifacts are not part of the current run and must not be counted.

旧 Agent 做过的 PASS 轮次、旧 release 之前的 PASS 轮次、旧 private artifact 之前的 PASS 轮次，都只能作为历史证据；它们与当前 AI 执行的退出条件无关，不得拿来凑本次连续 PASS 轮次。

## 默认抽样预算 / Default Sampling Budget

发布前默认配置兼顾质量和 AI token 预算：

```text
T = 4
agents = 2

paragraph/text:
  each agent samples 120 units per round
  total planned text samples = 2 * 120 * 4 = 960

table:
  if N <= 80, full scan
  otherwise sample 20 units per round total

figure:
  if N <= 80, full scan
  otherwise sample 20 units per round total

formula/proof:
  if N <= 100, full scan
  otherwise sample 20 units per round total

caption/note:
  if N <= 120, full scan
  otherwise sample 20 units per round total
```

对于只有文本的长书，`960` 个文本样本可把“若真实问题文本比例至少 1%”的大总体近似漏检概率压到约 `0.99^960 ~= 0.0065%`。若书很短，实际抽样受 `N` 限制，有限总体下应接近全检。

非文本层通常数量较少，优先使用小规模全检。若表格、图片、公式或注释层很大，默认每轮总抽 20 个，以控制 token 成本。该配置主要防系统性图表/公式问题；若要防 1% 以下的极稀疏错误，应人工上调该层抽样量或触发专项审计。

风险升级规则：

```text
if any stratum or sampled unit exposes an issue needing correction or likely to recur systemically:
  classify it as a defect family in the current round
  if it is a translation-quality family, consult skills/translation-quality-defect-families/SKILL.md
  if it concerns expert-level prose or context-dependent word sense, consult skills/expert-translation-quality/SKILL.md
  audit the whole reader-facing book for similar cases in the current round
  prefer machine-readable candidate collection before broad agent reading
  fix confirmed matches and document justified exceptions
  backfill reusable translation-quality lessons into the skill after book-local closure
  close the family in fix_log.md and closure_check.md before any new-seed resample
  optionally mark the stratum as higher risk for later sampling or human review, but never use that flag as a substitute for the current-round book-wide audit
```

The deterministic sampler reads recent `round_XXX/reviews/*_review.md` files, detects P0/P1/P2 rows that include sampled unit ids such as `::paragraph::`, `::table::`, `::figure::`, `::formula::`, or `::caption_note::`, and records the resulting risk flags in the next manifest. The main AI executor is not allowed to delete these script-produced flags.

脚本默认预算是发布前高质量门禁，不是最高强度门禁。用户可通过 `--samples-per-agent`、`--rounds-planned` 或后续专项脚本提高抽样强度。

抽样产物校验：

```powershell
npm run review:random-validate
```

最终退出前必须执行：

```powershell
npm run review:random-validate:pass
```

`review:random-validate:pass` 失败时，不得标记 `DONE`，不得宣布任务完成。

`review:random-validate:pass` 必须只统计同一 `review_run_id` 下、带 `generated_at`、且晚于最近 release/private artifact 的最新连续 PASS 轮次。用户可以通过 `--min-current-run-pass-rounds N` 指定 `N>=1`；未指定时默认 `N=2`。报告必须满足 `current_run_pass_rounds_required >= 1` 且 `current_run_pass_rounds_count >= current_run_pass_rounds_required`。缺少这些字段的旧 `validation_report.json` 不可作为完成证据。

`review:random-validate:pass` must count only latest consecutive PASS rounds that share the same `review_run_id`, carry `generated_at`, and are newer than the latest release/private artifact. The user may pass `--min-current-run-pass-rounds N` for any `N>=1`; when unspecified, `N=2`. The report must satisfy `current_run_pass_rounds_required >= 1` and `current_run_pass_rounds_count >= current_run_pass_rounds_required`. Old validation reports without these fields are not completion evidence.

该命令会写入：

```text
reviews/random_spotcheck/round_XXX/validation_report.json
```

其中必须满足 `release_confidence >= target_confidence`。
启用 `review:random-validate:pass` 时，`80` 只作为出版硬失败线：每个 Agent 评审文件中 `average_score >= 80`、`lowest_score >= 80`、`blocking_issue_count = 0`，且闭环文件中 `open_p0_p1_p2_count = 0`。最终 release/private artifact 默认还必须满足优秀出版线：每个 Agent `average_score >= 92`、`lowest_score >= 88`，并且评审文件必须为每个抽中样本保留逐项评分行。只写总评、缺少逐样本表格、或只有“可读但略硬/偏密/解释化/抽象腔”的 80 多分结果，不能作为最终优秀 PASS。

若维护者只需要诊断硬下限，可显式运行 `--skip-excellence-gate` 或 `npm run review:random-validate:hard-minimum`；该结果不得替代正式 `review:random-validate:pass` 的最终发布证据。

如果同一 `review_run_id` 下任何较早轮次发现过问题，`review:random-validate:pass` 还会回看这些问题轮次的 `fix_log.md` 与 `closure_check.md`。问题轮次必须填写机器可读字段：`defect_family_count`、`translation_quality_defect_family_count`、`translation_quality_skill_backfill`、`translation_quality_skill_backfill_path`、`translation_quality_skill_backfill_summary` 或不适用理由，以及 `translation_quality_skill_backfill_verified`。只要发现译文质量问题族，`translation_quality_skill_backfill` 必须是 `UPDATED` 或 `MERGED`，路径必须是 `skills/translation-quality-defect-families/SKILL.md`；否则最终 PASS 校验失败。若本轮没有译文质量问题族，必须填 `NOT_APPLICABLE` 并说明原因。

## 轮次目录 / Round Directory

每次抽检必须生成独立轮次目录：

```text
reviews/random_spotcheck/
  round_001/
    seed.txt
    random_sample_manifest.json
    strata_summary.json
    samples/
      agent_a/
        all_samples.md
        paragraph.md
        table.md
        figure.md
        formula.md
        caption_note.md
      agent_b/
        all_samples.md
        ...
    evidence/
      figures/
      tables/
      formulas/
    reviews/
      agent_a_review.md
      agent_b_review.md
    fixes/
      fix_log.md
    verification/
      closure_check.md
```

根目录下的 `reviews/random_spotcheck/random_sample_manifest.json`、`agent_a_samples.md`、`agent_b_samples.md` 是最近一轮兼容入口；人工核查应优先进入对应 `round_XXX/` 子目录。

## Agent 独立性 / Agent Independence

至少 2 个独立 Agent 必须分别评审样本：

- 不得互相参考评审结论。
- 不得复述主执行 AI 的结论。
- 不得把表格、图片、公式、图注当作普通段落略过。
- 每个样本必须给出 0-100 分、问题类型、优先级、是否返工和理由。
- 任一 P0/P1/P2、任一单项 < 80、任一读者不可理解、任一事实/术语/图表/公式错误，均判为本轮 FAIL。
- 正文样本必须检查多义词、习语、语法关系、术语定义或后文线索是否推翻当前译法；发现上下文选义错误时，按译文质量问题族处理。
- 80-87 是“硬门槛以上但需要精修”，88-91 是“较好但未达最终优秀门槛”。若样本只是“可读”但明显较硬、偏密、略抽象、解释化或仍有源语句法残留，应计入 `style_debt` 或相应问题族，不能用高分掩盖。

At least two independent agents must review the samples. The main executor cannot self-certify this gate.

## 修复闭环 / Fix Closure

发现问题后，主执行 AI 必须：

1. 在 `reviews/random_spotcheck/round_XXX/reviews/` 保留 Agent 原始评审。
2. 在 `reviews/revision_route.md` 写明回退阶段。
3. 将每个发现归纳为问题族，例如专名误译、术语硬译、上下文选义漂移、短句切断、比喻自撞、排比标点拖拽、代词指代不清、英文句法、过度解释、加戏、脚注裸露、图表标签错误、公式符号错误、metadata 不一致等。
4. 对每个问题族执行全书同类问题审计，范围至少覆盖 `chapters/final/`、读者可见 frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML；不得只修改被抽中的单个样本。译文质量问题族必须先按 `skills/translation-quality-defect-families/SKILL.md` 使用 `rg`、术语表、禁用正文写法、标题映射和小上下文原文对照等低 token 方法收集候选，再把候选片段交给 agent 复核。
5. 修复对应章节、表格、图片、公式、metadata 或构建脚本中的所有同类问题；若某个疑似命中被判定为合理例外，必须记录理由。
6. 在 `round_XXX/fixes/fix_log.md` 记录每个问题族的检索式或审计方法、审计范围、命中数、修复位置、例外和复查结果。可复用的译文质量经验必须回填到 `skills/translation-quality-defect-families/SKILL.md`，已有同族条目时合并改进，不盲目重复追加；同时必须填写 `translation_quality_skill_backfill` 相关机器可读字段，供 `review:random-validate:pass` 强制校验。
7. 在 `round_XXX/verification/closure_check.md` 定点复查旧问题，并确认同类问题全书审计已关闭。
8. 使用新 seed 生成下一轮 `round_YYY/` 抽检，不得复用旧样本自证通过。

If a sampled unit exposes a defect, the fix must be upgraded to a book-wide similar-issue audit. The executor must classify the defect family, search or otherwise inspect the whole reader-facing book for the same family, fix all confirmed matches, document justified exceptions, and close that systemic audit before the next new-seed round.

假设单次修复 OK 概率为 75%，它只能作为迭代效率假设，不能作为发布条件。发布条件是：已发现的 P0/P1/P2 必须定点复查关闭，且修复后新 seed 抽检通过。

If a single fix has a 75% chance of success, that is only an iteration-efficiency assumption. Release requires closed findings plus a new-seed sampling round.

## 完成条件 / Completion Criteria

随机抽检模块通过必须同时满足：

- `reviews/random_spotcheck/round_XXX/random_sample_manifest.json` 存在。
- `strata_summary.json` 记录每层候选数、抽样数、是否全检和置信度。
- `validation_report.json` 记录 `release_confidence >= 0.80`，且 `status=PASS`。
- `validation_report.json` 记录 `current_review_run_id`、`current_run_pass_rounds_required >= 1`，且 `current_run_pass_rounds_count >= current_run_pass_rounds_required`；用户未指定时默认要求 2。
- `validation_report.json.excellence_gate_required = true`，并记录每个 Agent `average_score >= 92`、`lowest_score >= 88`，以及 `agent_review_checks.*.all_samples_scored = true`。
- 至少 2 个 Agent 的样本、评审文件存在。
- `reviews/random_spotcheck/round_XXX/fixes/fix_log.md` 为 `PASS`。
- `reviews/random_spotcheck/round_XXX/verification/closure_check.md` 为 `PASS`。
- 每个已发现问题族都已完成全书同类问题审计，`fix_log.md` 记录审计范围、检索式或复查方法、同类命中、修复和例外。
- 若当前执行批次任何轮次发现过译文质量问题族，`fix_log.md` 证明 skill 已 `UPDATED` 或 `MERGED`，`closure_check.md` 记录 `translation_quality_skill_backfill_verified: true`；若无译文质量问题族，必须有 `NOT_APPLICABLE` 和具体理由。
- `npm run review:random-validate:pass` 通过。
- 若发生返工，后续至少还有一轮新 seed 抽检通过。

未满足以上任一条件时，`state/pipeline_state.json.status` 不得进入 `FINAL_OUTPUT_PASS`、`RELEASE_PASS`、`RETROSPECTIVE_DONE` 或 `DONE`。随机抽检通过后还必须进入 `references/release_versioning.md` 定义的版本化发布步骤；只有 `DRAFT` release 不能退出任务。

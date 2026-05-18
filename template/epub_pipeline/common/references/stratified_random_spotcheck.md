# 分层随机抽检门禁 / Stratified Random Spot-Check Gate

本文件定义第一版全书 EPUB 生成后必须执行的强制质量门禁。它适用于所有语言方向；具体目标语言风格规则由 `targets/{target}/` 和 `{source-target}/` 模板追加。

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
python scripts/select_random_review_passages.py --source-dir chapters/final --agents 2 --samples-per-agent 60 --rounds-planned 4 --target-confidence 0.80 --defect-rate 0.10 --profile auto
```

## 默认抽样预算 / Default Sampling Budget

发布前默认配置兼顾质量和 AI token 预算：

```text
T = 4
agents = 2

paragraph/text:
  each agent samples 60 units per round
  total planned text samples = 2 * 60 * 4 = 480

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

对于只有文本的长书，`480` 个文本样本可把“若真实问题文本比例至少 1%”的大总体近似漏检概率压到约 `0.99^480 ~= 0.8%`。若书很短，实际抽样受 `N` 限制，有限总体下应接近全检。

非文本层通常数量较少，优先使用小规模全检。若表格、图片、公式或注释层很大，默认每轮总抽 20 个，以控制 token 成本。该配置主要防系统性图表/公式问题；若要防 1% 以下的极稀疏错误，应人工上调该层抽样量或触发专项审计。

风险升级规则：

```text
if any stratum finds P0/P1/P2:
  keep the next-round random sample budget unchanged
  mark that stratum as higher risk

if the same stratum finds P0/P1/P2 in two consecutive rounds:
  require a dedicated targeted audit and closure review
  do not force a full scan by default
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

该命令会写入：

```text
reviews/random_spotcheck/round_XXX/validation_report.json
```

其中必须满足 `release_confidence >= target_confidence`。
启用 `review:random-validate:pass` 时，还必须满足每个 Agent 评审文件中 `average_score >= 75`、`lowest_score >= 70`、`blocking_issue_count = 0`，且闭环文件中 `open_p0_p1_p2_count = 0`。

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
- 任一 P0/P1/P2、任一单项 < 70、任一读者不可理解、任一事实/术语/图表/公式错误，均判为本轮 FAIL。

At least two independent agents must review the samples. The main executor cannot self-certify this gate.

## 修复闭环 / Fix Closure

发现问题后，主执行 AI 必须：

1. 在 `reviews/random_spotcheck/round_XXX/reviews/` 保留 Agent 原始评审。
2. 在 `reviews/revision_route.md` 写明回退阶段。
3. 修复对应章节、表格、图片、公式、metadata 或构建脚本。
4. 在 `round_XXX/fixes/fix_log.md` 记录每个问题的修复位置。
5. 在 `round_XXX/verification/closure_check.md` 定点复查旧问题。
6. 使用新 seed 生成下一轮 `round_YYY/` 抽检，不得复用旧样本自证通过。

假设单次修复 OK 概率为 75%，它只能作为迭代效率假设，不能作为发布条件。发布条件是：已发现的 P0/P1/P2 必须定点复查关闭，且修复后新 seed 抽检通过。

If a single fix has a 75% chance of success, that is only an iteration-efficiency assumption. Release requires closed findings plus a new-seed sampling round.

## 完成条件 / Completion Criteria

随机抽检模块通过必须同时满足：

- `reviews/random_spotcheck/round_XXX/random_sample_manifest.json` 存在。
- `strata_summary.json` 记录每层候选数、抽样数、是否全检和置信度。
- `validation_report.json` 记录 `release_confidence >= 0.80`，且 `status=PASS`。
- 至少 2 个 Agent 的样本、评审文件存在。
- `reviews/random_spotcheck/round_XXX/fixes/fix_log.md` 为 `PASS`。
- `reviews/random_spotcheck/round_XXX/verification/closure_check.md` 为 `PASS`。
- `npm run review:random-validate:pass` 通过。
- 若发生返工，后续至少还有一轮新 seed 抽检通过。

未满足以上任一条件时，`state/pipeline_state.json.status` 不得进入 `FINAL_OUTPUT_PASS`、`RELEASE_PASS`、`RETROSPECTIVE_DONE` 或 `DONE`。随机抽检通过后还必须进入 `references/release_versioning.md` 定义的版本化发布步骤；只有 `DRAFT` release 不能退出任务。

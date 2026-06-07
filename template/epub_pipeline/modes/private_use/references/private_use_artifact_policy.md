# Private-Use Artifact Policy / 私人自用产物规则

policy_status: "ACTIVE"
scope: "publication_mode=private_use only / 仅私人自用模式"

## Artifact Semantics / 产物语义

Private-use EPUB files are local personal-study artifacts. They are not public releases, not licensed releases, and not repository deliverables.

私人自用 EPUB 是本地个人学习产物，不是公开 release，不是授权发布物，也不是仓库交付物。

## Output Directory / 输出目录

Use:

```text
output/private_artifacts/
```

Do not use private EPUB artifacts as GitHub release assets. Do not commit them.

不要把私人 EPUB 产物作为 GitHub release 资产，也不要提交到 Git。

## Required Files / 必备文件

- `{target_title}_private_vX.X.X.epub`
- `private_artifact_notes.md`
- `private_artifact_state.json`
- `private_artifact_index.md`

## Random Spot-Check Evidence / 随机抽检证据

Before creating a PASS private artifact, run `npm run review:random-validate:pass`. The validation report must include `current_review_run_id` and must show `current_run_pass_rounds_required >= 1` plus `current_run_pass_rounds_count >= current_run_pass_rounds_required`. The user may specify any current-run consecutive PASS requirement of `>=1`; when unspecified, the default is 2. PASS rounds from earlier agents, earlier public releases, or earlier private artifacts are historical records only and must not be counted as the current executor's final PASS rounds.

创建 `PASS` 私人产物前，必须运行 `npm run review:random-validate:pass`。校验报告必须包含 `current_review_run_id`，且必须显示 `current_run_pass_rounds_required >= 1`、`current_run_pass_rounds_count >= current_run_pass_rounds_required`。用户可以指定任意 `>=1` 的当前运行连续 PASS 轮次要求；未指定时默认 2。旧 Agent、旧公开 release 或旧私人产物之前的 PASS 轮次只能作为历史记录，不得计入当前执行者的最后 PASS 轮次。

## Expert Translation Closure / 专家级译文闭环

Before creating a PASS private artifact, translation QA must use `skills/expert-translation-quality/SKILL.md` when expert-level prose, context-dependent word choice, translation-stage polysemy handling, or downstream polysemy back-checking matters. A valid current-run random review PASS must show `polysemy_context_issue_count: 0`; chapter controls must record `expert_translation_skill_used: true`, `expert_level_review_status: "PASS"`, `polysemy_translation_stage_review: "PASS"`, `polysemy_context_review: "PASS"`, and `polysemy_unresolved_count: 0`.

创建 `PASS` 私人产物前，只要涉及专家级译文、上下文依赖选义、翻译阶段多义词处理或多义词回看，译文 QA 必须使用 `skills/expert-translation-quality/SKILL.md`。有效的当前运行随机抽检 PASS 必须显示 `polysemy_context_issue_count: 0`；章节 control 必须记录 `expert_translation_skill_used: true`、`expert_level_review_status: "PASS"`、`polysemy_translation_stage_review: "PASS"`、`polysemy_context_review: "PASS"` 和 `polysemy_unresolved_count: 0`。

## Required Note Wording / 必备说明

Every private artifact note must include:

- `仅供个人自用，不传播，不商业使用`
- 风险由个人承担。
- public-domain-books-translation 开源项目仅用于公版书翻译发布，不承担其他个人翻译、保存、传播或使用非公版内容导致的版权风险及责任。

每份私人产物说明必须包含上述使用边界、个人风险和 public-domain-books-translation 开源项目责任边界。

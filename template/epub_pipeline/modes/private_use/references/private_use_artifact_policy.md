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

## Required Note Wording / 必备说明

Every private artifact note must include:

- `仅供个人自用，不传播，不商业使用`
- 风险由个人承担。
- LifeBook书坊仅发布 LifeBook 翻译发布系统，不承担任何因其他个人翻译、保存、传播或使用非公版内容导致的版权风险及责任。

每份私人产物说明必须包含上述使用边界、个人风险和 LifeBook 书坊责任边界。

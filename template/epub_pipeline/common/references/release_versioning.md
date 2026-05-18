# EPUB 版本发布规则 / EPUB Release Versioning

EPUB 成书应按软件发布方式管理。`output/book.epub` 是当前构建产物；正式或候选交付物必须写入 `output/release/`，并带版本号、发布说明和校验证据。

EPUB books should be managed like software releases. `output/book.epub` is the current build artifact; release or candidate artifacts must be written under `output/release/` with a version, release note, and validation evidence.

## 版本号 / Version Number

版本号格式：

```text
v{main_version}.{sub_version}.{patch_version}
```

默认初始版本：

```text
v0.0.1
```

规则：

- `main_version`：重大结构、底本或出版策略变更。
- `sub_version`：章节范围、译文策略、版式体系或重要审校批次变更。
- `patch_version`：每次迭代修改、读者反馈修复、抽检修复或小范围 QA 修复后递增 1。

若没有明确要求，脚本每次创建 release 都递增 `patch_version`。

旧版本 EPUB 和旧 release note 不得被覆盖。若已经存在同版本产物，必须创建下一个 patch version；只有在明确重建同一候选版本时，才允许使用脚本的 `--overwrite` 参数。

## 目录 / Directory

所有 release 文件写入：

```text
output/release/
```

必须包含：

- `book_vX.X.X.epub`
- `release_note_vX.X.X.md`
- `release_state.json`
- `release_index.md`

`output/` 根目录可以保留 `book.epub`、`epubcheck.json`、`publication_lint.json` 等当前构建产物，但不得把多个版本 EPUB 平铺在 `output/` 根目录。

## 发布说明 / Release Note

每个版本必须有中英文 release note，像软件版本说明一样记录：

- 发布原因 / Release reason
- 修改内容 / Changes
- 问题点 / Issues
- 修复方式 / Fixes
- QA 与证据 / QA and evidence
- 风险 / Risks
- 下一轮迭代 / Next iteration

读者评论、人工审校、阅读行为分析和自动化 QA 发现的问题，都应进入后续版本的 release note。

## 脚本 / Script

候选发布：

```powershell
npm run release:draft
```

正式发布：

```powershell
npm run release:create
```

等效命令：

```powershell
python scripts/create_release.py --status DRAFT
python scripts/create_release.py --status PASS --require-pass
```

`PASS` release 必须满足随机抽检闭环、`validation_report.json.require_pass = true`、`release_confidence >= 0.80`、EPUBCheck fatal/error 为 0、publication lint 无未解决问题，以及其他最终门禁。`DRAFT` release 可以用于人工核查或候选版本，但不得作为 `DONE` 的依据。

`PASS` release cannot be created from a structural-only random spot-check validation. The latest `validation_report.json` must come from `npm run review:random-validate:pass` or the equivalent `python scripts/validate_random_spotcheck.py --require-pass`.

## Done Gate / 完成门禁

一本书不得标记 `DONE`，除非：

- 至少存在一个 `output/release/book_vX.X.X.epub`。
- 对应 `release_note_vX.X.X.md` 存在。
- `release_state.json.latest_status = PASS`。
- release note 记录抽检、修复、风险和校验证据。

这让 EPUB 可以像软件一样持续迭代：每次读者反馈或自动化检查产生修改，就发布一个新的 patch version。

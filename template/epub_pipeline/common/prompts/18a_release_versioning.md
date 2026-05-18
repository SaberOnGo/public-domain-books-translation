# 18a EPUB 版本化发布 / EPUB Release Versioning

## 目标 / Purpose

把当前 `output/book.epub` 固化为带版本号的发布产物，并写入双语 release note。EPUB 必须像软件版本一样持续迭代：读者评论、人工审校、阅读行为分析、自动化 QA 和随机抽检修复都进入后续 patch version。

Freeze the current `output/book.epub` into a versioned release artifact with a bilingual release note. The EPUB is managed like software: reader feedback, human review, reading-behavior analysis, automated QA, and random spot-check fixes all feed later patch releases.

## 必读 / Must Read

- `references/release_versioning.md`
- `references/stratified_random_spotcheck.md`
- `PIPELINE_SPEC.md`
- `automation_contract.md`
- `reviews/random_spotcheck/round_XXX/validation_report.json`
- `output/epubcheck.json`
- `output/publication_lint.json`

## 触发时机 / Trigger

第一版 `output/book.epub` 生成后，且分层随机抽检模块已经执行后，必须进入本步骤。后续每次根据读者反馈、人工审校或自动化 QA 修改 EPUB 后，也必须重新执行本步骤并产生新的 patch version。

Run this step after the first `output/book.epub` is built and the stratified random spot-check module has run. Re-run it after every EPUB modification caused by reader feedback, human review, or automated QA, producing a new patch version.

## 版本规则 / Version Rule

版本号格式：

```text
v{main_version}.{sub_version}.{patch_version}
```

默认首版是 `v0.0.1`。没有明确人工指令时：

- `main_version` 不变。
- `sub_version` 不变。
- 每次生成发布产物，`patch_version += 1`。

Default first version is `v0.0.1`. Unless the human explicitly changes major or minor version, every release artifact increments the patch version by 1.

## 目录 / Directory

禁止把多个版本的 EPUB 平铺在 `output/` 根目录。发布产物必须写入：

```text
output/release/
```

必须包含：

- `book_vX.X.X.epub`
- `release_note_vX.X.X.md`
- `release_state.json`
- `release_index.md`

`output/book.epub` 只是当前构建产物；`output/release/book_vX.X.X.epub` 才是可追踪发布产物。

## 命令 / Commands

候选发布：

```powershell
npm run release:draft
```

正式发布：

```powershell
npm run review:random-validate:pass
npm run release:create
```

等效脚本命令：

```powershell
python scripts/create_release.py --status DRAFT
python scripts/create_release.py --status PASS --require-pass
```

## Release Note 要求 / Release Note Requirements

每个版本必须用中文和英文记录：

- 发布原因 / release reason
- 修改内容 / changes
- 问题点 / issues
- 修复方式 / fixes
- QA 与证据 / QA and evidence
- 风险 / risks
- 下一轮迭代 / next iteration

如果是 `DRAFT`，release note 必须明确说明不能作为 `DONE` 依据。若是 `PASS`，release note 必须引用随机抽检轮次、`release_confidence >= 0.80`、EPUBCheck、publication lint 和所有关闭记录。

## 硬门禁 / Hard Gates

不得创建 `PASS` release，除非同时满足：

- `npm run review:random-validate:pass` 通过，且 `validation_report.json.require_pass = true`。
- `validation_report.json.release_confidence >= 0.80`。
- 至少 2 个独立 Agent PASS，无单项 `< 70`，无 blocking issue。
- `fixes/fix_log.md` 和 `verification/closure_check.md` 为 PASS，且 `open_p0_p1_p2_count = 0`。
- `output/epubcheck.json` 存在，且 fatal/error 为 0。
- `output/publication_lint.json` 存在，且 unresolved issues 为 0。

`DRAFT` release 可以给人工核查，但不得把 `state/pipeline_state.json.status` 标为 `DONE`。

## 状态 / State

候选发布：

```text
state/pipeline_state.json.status = RELEASE_DRAFT
```

正式发布：

```text
state/pipeline_state.json.status = RELEASE_PASS
```

只有 `output/release/release_state.json.latest_status = PASS` 时，流水线才允许进入最终 `DONE` 判断。


# EPUB 版本发布规则 / EPUB Release Versioning

EPUB 成书应按软件发布方式管理。`output/book.epub` 是当前单目标语构建产物；公版或授权项目的正式或候选交付物必须写入 `output/release/`，并带版本号、发布说明和校验证据。`edition_type: bilingual_parallel` 项目还必须把双语对照构建产物写入 `output/book_bilingual_parallel.epub`，并在 release 中保留对应版本化产物。是否输出双语对照版与 `publication_mode` 解耦；`publication_mode=private_use` 项目不创建公开 release，但同样可以按 `output_editions` 生成单目标语和双语对照 EPUB，并改用 `template/epub_pipeline/modes/private_use/references/private_use_artifact_policy.md` 把本地私人产物写入 `output/private_artifacts/`。

EPUB books should be managed like software releases. `output/book.epub` is the current target-only build artifact. Public-domain or licensed release or candidate artifacts must be written under `output/release/` with a version, release note, and validation evidence. `edition_type: bilingual_parallel` projects must also write the bilingual parallel build artifact to `output/book_bilingual_parallel.epub` and preserve a matching versioned release artifact. Bilingual output is independent from `publication_mode`; `publication_mode=private_use` projects do not create public releases, but they can still generate both target-only and bilingual EPUBs according to `output_editions` and must instead follow `template/epub_pipeline/modes/private_use/references/private_use_artifact_policy.md` to write local private artifacts under `output/private_artifacts/`.

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

旧版本 EPUB 不得被覆盖。Release note 使用累计文件 `release_notes.md`，每次发布必须把最新版本说明追加到文件顶部，保留旧版本记录；不得为每次修改散落新建多个 release note 文件。若已经存在同版本 EPUB，必须创建下一个 patch version；只有在明确重建同一候选版本时，才允许使用脚本的 `--overwrite` 参数。

## 目录 / Directory

公版或授权项目的所有 release 文件写入：

```text
output/release/
```

必须包含：

- `{目标语言书名}_vX.X.X.epub`，例如 `金属巨兽_v0.0.4.epub`
- 当 `edition_type: bilingual_parallel` 时，还必须包含 `{目标语言书名}_{目标语言简称}{源语言简称}双语_vX.X.X.epub`，例如英译简中为 `林伯洛斯特的女孩_中英双语_v0.0.4.epub`。语言简称顺序必须是目标语言在前、源语言在后；不得把内部枚举名 `_bilingual_parallel` 暴露为读者文件名。
- 作者名属于书籍工程目录、metadata、book-info 和 release note 记录；release EPUB 文件名默认不包含作者名，避免文件名过长。若同一 release 目录内存在同名书冲突，必须先在书名中加入读者可识别的短区分项，再生成版本文件。
- Release/private artifact scripts must read `state/pipeline_state.json.output_editions` and copy every enabled EPUB artifact. They must not decide bilingual output from public/private publication mode.
- release/private artifact 脚本必须读取 `state/pipeline_state.json.output_editions`，并固化每个已启用的 EPUB 产物。不得根据公开/私人发布模式决定是否输出双语版。
- `release_notes.md`
- `release_state.json`
- `release_index.md`

`output/` 根目录可以保留 `book.epub`、`book_bilingual_parallel.epub`、`epubcheck.json`、`publication_lint.json` 等当前构建产物，但不得把多个版本 EPUB 平铺在 `output/` 根目录。

私人自用项目不使用 `output/release/` 表达公开发布，必须使用：

```text
output/private_artifacts/
```

具体规则见 `template/epub_pipeline/modes/private_use/references/private_use_artifact_policy.md`。

## 发布说明 / Release Note

每个版本必须在同一个 `release_notes.md` 中有中英文 release note 条目，像软件版本说明一样记录；最新版本条目必须位于文件最上方：

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

私人自用项目使用：

```powershell
npm run private:artifact:draft
npm run private:artifact:create
```

等效命令：

```powershell
python scripts/create_release.py --status DRAFT
python scripts/create_release.py --status PASS --require-pass
```

`PASS` release 必须满足文学顺读复审、随机抽检闭环、所有已发现问题族的全书同类问题审计与关闭记录、当前执行批次问题轮次的译文质量 skill backfill 字段校验、`validation_report.json.require_pass = true`、`release_confidence >= 0.80`、EPUBCheck fatal/error 为 0、publication lint 无未解决问题，以及其他最终门禁。`DRAFT` release 可以用于人工核查或候选版本，但不得作为 `DONE` 的依据。

文学顺读复审由 `npm run literary:validate` 执行，要求 `qa/literary_style/literary_style_review.md` 明确 PASS。原作者/原书序言、导言、开篇和首章必须作为高影响区域复审；这些部分不得带着未关闭的直译腔、解释腔、平硬句、怪句或朗读拗口问题进入正式 PASS release。

`PASS` release 还必须来自当前执行批次的新随机抽检证据：`validation_report.json` 必须包含 `current_review_run_id`，且必须满足 `current_run_pass_rounds_required >= 1`、`current_run_pass_rounds_count >= current_run_pass_rounds_required`。用户可以指定任意 `>=1` 的当前运行连续 PASS 轮次要求；未指定时默认 2。旧 Agent、旧 release 之前已经 PASS 的轮次不得计入本次 release；release 脚本必须拒绝缺少这些字段的旧报告。

`PASS` release cannot be created from a structural-only random spot-check validation. The latest `validation_report.json` must come from `npm run review:random-validate:pass` or the equivalent `python scripts/validate_random_spotcheck.py --require-pass --min-current-run-pass-rounds N`, where `N>=1` and defaults to 2 when unspecified. The round fix log and closure check must prove that each discovered defect family was audited book-wide, fixed where confirmed, closed, and, for reusable translation-quality families, merged or updated in `skills/translation-quality-defect-families/SKILL.md`. Historical PASS rounds from earlier agents or earlier releases do not count toward the current release.

## Done Gate / 完成门禁

一本书不得标记 `DONE`，除非：

公版或授权项目：

- 至少存在一个 `output/release/{目标语言书名}_vX.X.X.epub`。
- 若 `state/pipeline_state.json.edition_type = bilingual_parallel`，还必须存在同版本 `output/release/{目标语言书名}_{目标语言简称}{源语言简称}双语_vX.X.X.epub`，例如 `output/release/林伯洛斯特的女孩_中英双语_v0.0.4.epub`，或 release_state 中记录的等效双语对照 EPUB。
- `output/release/release_notes.md` 存在，且最新版本条目位于最上方。
- `release_state.json.latest_status = PASS`。
- release note 记录抽检、问题族全书同类审计、修复、风险、校验证据；双语对照版还必须记录对齐完整性、源文出版权利和双语 EPUB 校验结果。
- `qa/literary_style/literary_style_review.md` 记录最终文学顺读复审 PASS，且高影响开篇区域已关闭文学债务。

私人自用项目：

- 至少存在一个 `output/private_artifacts/{目标语言书名}_private_vX.X.X.epub`。
- `output/private_artifacts/private_artifact_notes.md` 存在，且最新版本条目位于最上方。
- `private_artifact_state.json.latest_status = PASS`。
- private artifact note 记录抽检、问题族全书同类审计、修复、风险和校验证据，并明确该产物仅供个人自用、不传播、不商业使用、不得发布到 GitHub。

这让 EPUB 可以像软件一样持续迭代：每次读者反馈或自动化检查产生修改，就发布一个新的 patch version。

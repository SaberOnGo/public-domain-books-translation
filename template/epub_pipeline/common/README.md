# Common EPUB Pipeline / EPUB 通用流水线

This directory contains shared workflow files for all language-pair templates.

本目录包含所有语言方向模板共享的工作流文件。

## Contents / 内容

- `PIPELINE_SPEC.md`: state machine, project directory contract, naming rules, and done definition.
- `automation_contract.md`: automation and template-protection rules.
- `metadata/rights_checklist.md`, `metadata/source_evidence.md`, and `metadata/private_use_declaration.md`: source, rights, public-domain/licensed publication, and private-use evidence templates.
- `preproduction/`: shared EPUB preproduction templates.
- `references/`: language-neutral title, literary refinement, quality gate, EPUB asset, benchmark, and stratified random spot-check policies.
- `assets/`: default EPUB resource directories for figures, images, styles, and table resources.
- `source/tables/`: source CSV/TSV tables used to generate reader-facing XHTML tables.
- `scripts/`: reusable chapter splitting, Markdown normalization, publication lint, refinement-check, stratified random sampling, and random-gate validation helpers.
- `package.json`: book-local npm script template only; shared dependencies are installed once under `books/`.
- `state/`: initial pipeline state and human-feedback control files.
- `Makefile`: generic EPUB build/check entry points.

`common` is a shared base layer. Non-public-domain personal-use projects must receive the separate `template/epub_pipeline/modes/private_use/` overlay after common, language-pair, and profile layers. Do not copy private-use cover, frontmatter, artifact, or gate rules into public-domain projects.

`common` 是共享基础层。非公版个人自用项目必须在 common、语言方向和 profile 层之后，再叠加独立的 `template/epub_pipeline/modes/private_use/`。不要把私人自用封面、首页/前置页、私人产物或门禁规则复制进公版项目。

目标语言质量框架放在 `template/epub_pipeline/targets/{target}/`。源语言到目标语言的专用模板只应在确实需要不同翻译、排版或评审规则时覆盖或扩展 common 文件。

Target-language quality frameworks live under `template/epub_pipeline/targets/{target}/`. Source-to-target-specific templates should override or extend common files only when the direction needs different translation, typography, or review rules.

## Shared Tooling / 共享工具

Node.js dependencies for EPUB building and validation are repository-level book tooling. Install them once from `books/`:

```powershell
cd books
npm install
```

Do not install a duplicate `node_modules/` inside every `books/{target}/{number}_{target_language_title}_{target_language_author}/` directory. Book-local `package.json` files keep only scripts; scripts such as `scripts/run_epubcheck.js` must resolve tools by walking up to the shared `books/node_modules/`.

Node.js 依赖属于书籍区共享工具，应在 `books/` 下统一安装一次：

```powershell
cd books
npm install
```

不要在每个 `books/{target}/{number}_{目标语言书名}_{目标语言作者名}/` 目录里重复安装 `node_modules/`。具体书籍的 `package.json` 只保留脚本；`scripts/run_epubcheck.js` 等脚本必须向上查找共享的 `books/node_modules/`。

Private-use projects live under ignored `books/private/{target}/{number}_{target_language_title}_{target_language_author}/`. They use the same shared tooling and the private-use mode overlay, but their source text, translations, QA records, EPUB artifacts, private artifacts, and book-specific metadata must remain local and must not be published to GitHub.

私人自用工程位于被忽略的 `books/private/{target}/{number}_{目标语言书名}_{目标语言作者名}/`。它们使用同一套共享工具和 private-use 模式覆盖层，但其中的原文、译文、QA 记录、EPUB 产物、私人产物和具体书籍 metadata 必须留在本地，不得发布到 GitHub。

## Publication Lint / 出版文本检查

Before building a final EPUB, run:

```powershell
python scripts/check_no_local_absolute_paths.py --write-report
python scripts/check_template_workflow_gate.py --write-report
node scripts/publication_lint.js --target={target-language} --write-report
node scripts/asset_manifest_check.js --write-report
python scripts/check_cover_output_assets.py --write-report
python scripts/check_reader_facing_policy.py --write-report
```

在构建最终 EPUB 前必须运行：

```powershell
python scripts/check_no_local_absolute_paths.py --write-report
python scripts/check_template_workflow_gate.py --write-report
node scripts/publication_lint.js --target={target-language} --write-report
node scripts/asset_manifest_check.js --write-report
python scripts/check_cover_output_assets.py --write-report
python scripts/check_reader_facing_policy.py --write-report
```

Private-use projects must additionally run the private-use gates copied from `modes/private_use/`:

```powershell
python scripts/check_private_use_gate.py --write-report
python scripts/check_private_reader_facing_policy.py --write-report
```

私人自用项目还必须额外运行从 `modes/private_use/` 复制来的私人门禁：

```powershell
python scripts/check_private_use_gate.py --write-report
python scripts/check_private_reader_facing_policy.py --write-report
```

`npm run preflight:template` runs the local absolute-path gate first. The gate rejects contributor-specific Windows drive paths, personal home-directory paths, and file URLs in book production artifacts, public prompt examples, and reusable template documentation; use repository-relative paths, script-relative paths, or explicit user-provided arguments instead.

`npm run preflight:template` 会先运行本机绝对路径门禁。该门禁会拒绝在书籍生产产物、公共 prompt 示例和可复用模板文档中出现 Windows 盘符路径、个人 home 目录路径和 file URL 等贡献者本机路径；应改用仓库相对路径、脚本相对路径，或由用户显式传入的参数。

These checks are common because template drift, unnumbered book paths, encoding damage, legacy print tables of contents, repeated spacing, missing image resources, missing output cover assets, reader-facing production notes, unmanifested SVG/PNG/CSS files, and path portability problems can affect any language.

这些检查属于通用层，因为模板漂移、未编号书籍路径、编码污染、旧纸书页码目录、连续空格、图片资源丢失、output 封面资产缺失、读者可见制作说明、SVG/PNG/CSS 未登记到 OPF manifest、路径可移植性问题可能影响任何语言方向。

`check_reader_facing_policy.py` 会拦截进入读者版 EPUB 的生产痕迹，例如章节开头的 `译文说明` / `章节控制说明`、书籍信息页里的项目宣传语、制作日志、QA/prompt 记录，以及同一前置页内反复出现的版权/权利说明。

## Figures, Images, and Tables / 图表、图片与表格

Markdown files under `chapters/final/` are authoring sources only. The EPUB build must convert them to XHTML, copy assets into the EPUB package, and register every used resource in OPF manifest.

`chapters/final/` 下的 Markdown 只是编辑源。EPUB 构建必须把它们转换成 XHTML，把资源复制进 EPUB 包，并把所有实际使用的资源登记到 OPF manifest。

Recommended defaults:

- `assets/figures/*.svg` for diagrams and line art.
- `assets/images/*.jpg|png|webp` for cover images, scans, and bitmap illustrations.
- `source/tables/*.csv|tsv` for table source data.
- XHTML `<table>` for reader-facing numeric or technical tables.

具体规则见 `references/epub_assets_figures_tables.md`。

## Refinement Check / 精修复查

After a full EPUB has been built, run the reusable refinement scan from the book project root:

```powershell
node scripts/refinement_check.js
```

整本 EPUB 构建后，应在书籍工程根目录运行可复用精修扫描：

```powershell
node scripts/refinement_check.js
```

The report is written to `qa/refinement/refinement_check.json`. It separates reader-facing publication files from raw source evidence, so original downloaded source files can be preserved while EPUB-facing text stays clean.

报告会写入 `qa/refinement/refinement_check.json`。它会区分面向读者的出版文本和原始来源证据，因此既能保留下载原文的原貌，也能保证进入 EPUB 的文本干净。

## Per-Chapter Full Check Gate / 每章译后全量检查门禁

After each chapter is translated into `chapters/translated/{NNN_slug}.md`, the workflow must immediately run a full check and fix node for that chapter only before translating the next chapter or promoting the chapter. The result belongs in `qa/chapter_controls/{NNN_slug}.control.md`.

每章译入 `chapters/translated/{NNN_slug}.md` 后，必须立即只针对该章执行“每章译后，全量检查并修复节点”，并在进入下一章翻译或送入终稿前完成。结果写入 `qa/chapter_controls/{NNN_slug}.control.md`。

This gate must check the whole chapter and its reader-facing production context, including but not limited to fidelity, target-language readability, teaching/explanatory rhythm when applicable, terminology, case/name/title consistency, titles/subtitles, notes, figure/table/formula text interfaces, source-language syntax residue, stiff or overly literal sentences, over-explanation, invented additions, metadata impact, nav/title/TOC implications, body text, figures, formulas, tables, images, styles, reader-visible wording, readability, plain-language clarity, and polish. It is not enough to check only items named by the user.

该门禁必须检查当前章整章及其读者可见文字上下文，包括但不限于忠实度、目标语顺读、适用时的教学/解释节奏、术语、案例/专名/题名一致性、标题/小标题、注释、图表/公式/表格/图片的文字接口、源语句法残留、过硬过直句、过度解释、擅自加戏、本章对 metadata/nav/标题/目录的影响、正文、样式、读者可见文字、可读性、通俗化和润色。不得只检查用户点名项目，也不得把它扩大成全书门禁。

Terminology must not clutter the body with source terms by default. Use the target-language term in the body, and move source terms, definitions, and translation rationale to chapter notes, endnotes, or the glossary with a clear note marker. Body parenthetical source terms are allowed only when omitting the source term would confuse readers, the source term itself is being discussed, or competing translations must be disclosed immediately; record the reason.

术语呈现不得默认用原词挤占正文。正文使用目标语译名或准确意译；原词、定义和译名理由放入本章译注、章末注或术语表，并用清楚注号指向。只有不保留原词会让读者误解、原词本身正在被讨论，或译名分歧必须当场交代时，才允许正文括注原词；必须记录理由。

`glossary/terms.csv` must carry term-display fields such as `display_policy`, `exception_reason`, and `forbidden_body_renderings`. High-risk historical, institutional, status, technical, and culture-loaded terms must list forbidden body renderings before chapter translation proceeds. `preflight:template` may reject final chapters whose body still contains a forbidden rendering listed in the glossary.

`glossary/terms.csv` 必须包含 `display_policy`、`exception_reason`、`forbidden_body_renderings` 等术语呈现字段。历史术语、制度名、身份称谓、专业术语和文化负载词等高风险术语，必须在分章翻译前列出正文禁用写法。若终稿正文仍出现术语表列出的禁用写法，`preflight:template` 可以拒绝继续。

If any round finds any issue that requires a fix, including fidelity, terminology, reader confusion, text-interface errors, target-language awkwardness, weak polish, or over-simplification that damages specialist quality, fix the chapter but mark that round as `FIXED_RECHECK_REQUIRED`. It cannot be the PASS round. Append a new full-chapter recheck in the same control file. The workflow may continue only when the latest round records `scope: FULL_CHAPTER`, `issues_found: 0`, `fixes_applied: 0`, `unresolved_blocking_issues: 0`, `latest_round_status: PASS`, and `allow_next_chapter: true`. A failed or just-fixed chapter may not enter the next chapter translation, `chapters/final/`, or proceed as if the chapter were complete.

若任一轮发现需要修复的问题，包括忠实度、术语、读者理解、文字接口、目标语翻译腔、润色不足，或为了通俗而损害专业质量，都必须先修复该章；但该轮只能记为 `FIXED_RECHECK_REQUIRED`，不能作为 PASS 轮。必须在同一 control 文件追加新一轮整章复查。只有最近一轮记录 `scope: FULL_CHAPTER`、`issues_found: 0`、`fixes_applied: 0`、`unresolved_blocking_issues: 0`、`latest_round_status: PASS`、`allow_next_chapter: true` 时，流程才可继续。失败或刚修复的章节不得进入下一章翻译、`chapters/final/`，流程也不得把该章当作完成。

If a chapter check exposes a recurring translation-quality defect family, use `skills/translation-quality-defect-families/SKILL.md`. Examples include short-sentence fragmentation, metaphor collision, enumerative punctuation drag, unclear pronoun reference, source-syntax residue, terminology drift, title overload, over-explanation, and invented motive. Record immediate evidence in the book project, audit similar cases with low-token methods first, and backfill only reusable lessons into the skill.

若章节检查暴露可复现的译文质量问题族，必须使用 `skills/translation-quality-defect-families/SKILL.md`。示例包括短句切断、比喻自撞、排比标点拖拽、代词指代不清、源语句法残留、术语漂移、标题超载、过度解释和加戏。即时证据写入书籍工程；先用低 token 方法审计同类；只把可复用经验回填到该 skill。

Plain-language readability and professional quality are not opposites. A specialist book should be as clear, smooth, and engaging as the source permits, while preserving its specialist terms, concepts, evidence chain, and intellectual level.

通俗、顺读、有趣与专业质量不是对立关系。专业书应在原文允许范围内尽量清楚、顺畅、不费劲，同时保持术语、概念层级、证据链和知识水准；不得为了通俗而把专业内容改扁或改错。

Figures, tables, formulas, and images are handled here as a text-interface and routing check, not as an unbounded asset-production loop. Fix captions, labels, references, alt text, variables, units, and reader explanations in this node when they affect the current chapter's readability. Route redraw, OCR, cropping, numeric validation, formula layout, resource-path, or manifest issues to the asset/technical gate; routed asset issues block final/build/release, but they do not turn the chapter text gate into an endless asset-production loop once the current chapter text has a latest full-chapter zero-issue PASS.

图表、表格、公式和图片在本节点只做“文字接口与风险分流”检查，不作为无限资产制作循环。影响当前章可读性的图题、表题、正文引用、alt text、变量、单位和读者说明必须在本节点修复。重绘、OCR、裁剪、数值校验、公式排版、资源路径或 manifest 问题应路由到资产/技术门禁；已路由的资产问题会阻止终稿/构建/release，但在当前章文字最近一轮已经达到全章零问题 PASS 后，不应把译后文字门禁变成无限资产制作循环。

`preflight:template` must reject translated chapters whose matching control file is missing or whose latest full-chapter round is not a zero-issue PASS. For final chapters, it must also reject missing or non-PASS chapter gates.

`preflight:template` 必须拒绝缺少对应 control 文件，或最近整章轮次不是零问题 PASS 的已译章节。对终稿章节，还必须拒绝缺少章节门禁或章节门禁未 PASS 的情况。

## Stratified Random Spot Check / 分层随机抽检

After the first full-book EPUB is built, the workflow must run the post-EPUB stratified random spot-check gate:

```powershell
npm run review:random-samples
npm run review:random-validate
```

第一版全书 EPUB 生成后，必须执行 EPUB 后分层随机抽检门禁：

```powershell
npm run review:random-samples
npm run review:random-validate
```

The sampling unit is not an EPUB page and not only a paragraph. It is a reader-visible audit unit: paragraph, table, figure, formula/proof block, caption, or note. Samples, copied figure evidence, table/formula snippets, agent reviews, fix logs, and closure checks are written under `reviews/random_spotcheck/round_XXX/` so humans can inspect exactly what was sampled and what was fixed.

抽样单位不是 EPUB 页，也不只是正文段落，而是读者可见审计单元：正文段落、表格、图片、公式/证明块、图注或注释。样本、图片证据、表格/公式片段、Agent 评审、修复记录和闭环验证都会写入 `reviews/random_spotcheck/round_XXX/`，方便人工核查到底抽了什么、修了什么。

Every new executor run must create new random spot-check rounds for that run. Historical PASS rounds from earlier agents, earlier releases, or earlier private artifacts are audit history only; they must not be counted as the current executor's final PASS rounds. The sampler records `review_run_id` and `generated_at`. The user may specify any current-run consecutive PASS requirement of `>=1`; if not specified, `npm run review:random-validate:pass` defaults to the latest consecutive 2 PASS rounds from the same current `review_run_id`, newer than the latest release/private artifact.

每次新的 AI 执行随机抽检时，必须生成本次运行的新轮次。之前 Agent、之前 release 或之前 private artifact 已经 PASS 的轮次只能作为历史审计记录，不得计入当前执行者的最后 PASS 轮次。抽样脚本会写入 `review_run_id` 和 `generated_at`。用户可以指定任意 `>=1` 的当前运行连续 PASS 轮次要求；未指定时，`npm run review:random-validate:pass` 默认只接受同一当前 `review_run_id` 下、晚于最近 release/private artifact 的最新连续 2 个 PASS 轮次。

Default release sampling is intentionally stronger than a smoke test while still respecting AI token budgets: `T=4`, `agents=2`, paragraph/text samples are `120` per agent per round. Tables and figures are fully scanned when `N<=80`; formula/proof blocks when `N<=100`; captions/notes when `N<=120`. Larger non-text strata sample `20` units per round total by default.

默认发布前抽检强度高于快速 smoke test，但仍控制 AI token 成本：`T=4`，`agents=2`，正文层每个 Agent 每轮 120 个。表格和图片 `N<=80` 全检；公式/证明块 `N<=100` 全检；图注/表注/注释 `N<=120` 全检。超过阈值的非文本层默认每轮总抽 20 个。

If any stratum or sampled unit exposes any issue that needs correction or may recur systemically, the current round must immediately classify it as a defect family and complete a book-wide similar-issue audit and closure. Do not fix only the sampled unit, and do not wait for a second failed round before checking the whole book. The stratum may be marked as higher risk for later sampling and human review, but that risk flag cannot replace the current-round book-wide audit.

The sampling script enforces this deterministically by reading recent `round_XXX/reviews/*_review.md` files for P0/P1/P2 rows that include sampled unit ids such as `::table::` or `::figure::`.

若任一层、任一样本发现任何需要修复或可能系统性复现的问题，本轮必须立即归纳为问题族，并完成全书同类问题审计和闭环；不得只修被抽中的样本，也不得等到第二轮才全书检查。同层可被标记为高风险，用于后续抽样和人工复核，但风险标记不能替代本轮全书同类问题审计。

Any defect found by random sampling is treated as a possible defect family, not as an isolated sample-only fix. The executor must classify the family, audit the whole reader-facing book for similar cases across `chapters/final/`, frontmatter, metadata, nav, tables, figures, formulas, captions, notes, and the generated EPUB XHTML, fix all confirmed matches, document justified exceptions, and close the family in the same round's fix log and closure check before using a new seed.

随机抽检一旦发现问题，不得只修被抽中的样本。主执行 AI 必须先归纳问题族，再对整本读者可见书稿执行全书同类问题审计，覆盖 `chapters/final/`、frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML；修复所有确认命中、记录合理例外，并在同一轮 `fix_log.md` 与 `closure_check.md` 中关闭该问题族后，才能使用新 seed 复抽。

For translation-quality families, the whole-book audit should first use machine-readable candidates (`glossary/terms.csv`, forbidden renderings, title maps, `rg` scans, sample manifests, and review tables), then send only candidate passages and nearby source context to agents. If the family is reusable, update `skills/translation-quality-defect-families/SKILL.md` after book-local closure.

对译文质量问题族，全书审计应先使用机器可读候选（`glossary/terms.csv`、禁用正文写法、标题映射、`rg` 扫描、抽样 manifest 和评审表），再把候选片段与邻近原文交给 agent。若该问题族可复用，书内闭环后必须更新 `skills/translation-quality-defect-families/SKILL.md`。

The pass validator makes this a hard gate. If any current-run random spot-check round found an issue, its `fix_log.md` must declare the defect-family counts and the translation-quality skill backfill decision. Translation-quality families require `translation_quality_skill_backfill: "UPDATED"` or `"MERGED"` plus `translation_quality_skill_backfill_verified: true` in `closure_check.md`; non-translation-quality-only rounds must use `"NOT_APPLICABLE"` with a reason.

强校验会把这件事作为硬门禁。若当前执行批次任何随机抽检轮次发现过问题，该轮 `fix_log.md` 必须声明问题族数量和译文质量 skill 回填决策。发现译文质量问题族时，必须填写 `translation_quality_skill_backfill: "UPDATED"` 或 `"MERGED"`，并在 `closure_check.md` 写入 `translation_quality_skill_backfill_verified: true`；仅有非译文质量问题时，必须填写 `"NOT_APPLICABLE"` 和原因。

Before final output, the stronger pass validator must succeed:

```powershell
npm run review:random-validate:pass
```

最终输出前，强校验必须通过：

```powershell
npm run review:random-validate:pass
```

`review:random-validate:pass` 默认执行优秀出版线：两个 Agent 必须逐样本评分，`average_score >= 92`、`lowest_score >= 88`，且无阻塞问题。`80` 只是硬失败线，用来判定“低于此分必须失败”；80 多分的“可读但略硬/偏密/解释化”不能作为最终优秀出版证据。若只需诊断硬下限，可显式运行 `npm run review:random-validate:hard-minimum`，但该结果不得替代最终 release/private artifact 的 PASS 证据。

The pass report must include `current_review_run_id`, `current_run_pass_rounds_required`, `current_run_pass_rounds_count`, and `current_run_pass_rounds`. If the count is below the required value, the workflow is still not closed even when older rounds are PASS.

强校验报告必须包含 `current_review_run_id`、`current_run_pass_rounds_required`、`current_run_pass_rounds_count` 和 `current_run_pass_rounds`。只要本次运行计数不足，即使旧轮次都是 PASS，也不得关闭流程。

See `references/stratified_random_spotcheck.md` and `prompts/16a_stratified_random_spotcheck.md`.

## Versioned Release / 版本化发布

`output/book.epub` is only the current build artifact. After random spot-check closure, public-domain and licensed publication projects must create a versioned release under `output/release/`. Release scripts must run the template workflow gate and cover output asset gate first:

```powershell
npm run release:create
```

`PASS` release creation requires the latest random spot-check validation to come from `npm run review:random-validate:pass`; a structural-only validation, missing output cover assets, or `DRAFT` release is not enough for `DONE`.

`output/book.epub` 只是当前构建产物。随机抽检闭环通过后，公版和授权发布项目必须在 `output/release/` 下创建带版本号的发布产物。发布脚本必须先运行模板流程门禁和封面 output 资产门禁：

```powershell
npm run release:create
```

正式 `PASS` release 要求最近一次随机抽检校验来自 `npm run review:random-validate:pass`；只做结构校验、缺少 output 封面资产或只生成 `DRAFT` release，不能作为 `DONE` 依据。

Release artifacts are named with the target-language title plus version, for example `金属巨兽_v0.0.4.epub`, with `v0.0.1` as the default first version. Every release also needs the cumulative `release_notes.md`, `release_state.json`, and `release_index.md`. New release-note entries are inserted at the top of `release_notes.md`, like software changelogs. See `references/release_versioning.md` and `prompts/18a_release_versioning.md`.

Private-use projects are different: they must create local-only versioned artifacts under `output/private_artifacts/` by running:

```powershell
npm run private:artifact:create
```

Private-use artifacts are not public releases and must not be submitted to GitHub.

私人自用项目不同：它们必须通过以下命令在 `output/private_artifacts/` 下创建仅限本地的版本化产物：

```powershell
npm run private:artifact:create
```

私人自用产物不是公开 release，不得提交到 GitHub。

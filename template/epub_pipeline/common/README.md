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

Do not install a duplicate `node_modules/` inside every `books/{target}/{number}_{book_id_slug}/` directory. Book-local `package.json` files keep only scripts; scripts such as `scripts/run_epubcheck.js` must resolve tools by walking up to the shared `books/node_modules/`.

Node.js 依赖属于书籍区共享工具，应在 `books/` 下统一安装一次：

```powershell
cd books
npm install
```

不要在每个 `books/{target}/{number}_{book_id_slug}/` 目录里重复安装 `node_modules/`。具体书籍的 `package.json` 只保留脚本；`scripts/run_epubcheck.js` 等脚本必须向上查找共享的 `books/node_modules/`。

Private-use projects live under ignored `books/private/{target}/{number}_{book_id_slug}/`. They use the same shared tooling and the private-use mode overlay, but their source text, translations, QA records, EPUB artifacts, private artifacts, and book-specific metadata must remain local and must not be published to GitHub.

私人自用工程位于被忽略的 `books/private/{target}/{number}_{book_id_slug}/`。它们使用同一套共享工具和 private-use 模式覆盖层，但其中的原文、译文、QA 记录、EPUB 产物、私人产物和具体书籍 metadata 必须留在本地，不得发布到 GitHub。

## Publication Lint / 出版文本检查

Before building a final EPUB, run:

```powershell
python scripts/check_template_workflow_gate.py --write-report
node scripts/publication_lint.js --target={target-language} --write-report
node scripts/asset_manifest_check.js --write-report
python scripts/check_cover_output_assets.py --write-report
python scripts/check_reader_facing_policy.py --write-report
```

在构建最终 EPUB 前必须运行：

```powershell
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

Default release sampling is intentionally stronger than a smoke test while still respecting AI token budgets: `T=4`, `agents=2`, paragraph/text samples are `60` per agent per round. Tables and figures are fully scanned when `N<=80`; formula/proof blocks when `N<=100`; captions/notes when `N<=120`. Larger non-text strata sample `20` units per round total by default.

默认发布前抽检强度高于快速 smoke test，但仍控制 AI token 成本：`T=4`，`agents=2`，正文层每个 Agent 每轮 60 个。表格和图片 `N<=80` 全检；公式/证明块 `N<=100` 全检；图注/表注/注释 `N<=120` 全检。超过阈值的非文本层默认每轮总抽 20 个。

If any stratum finds P0/P1/P2, keep the next-round random sample budget unchanged to control AI token cost, but mark that stratum as higher risk. If the same stratum finds P0/P1/P2 in two consecutive rounds, require a dedicated targeted audit and closure review; do not force a full scan by default.

The sampling script enforces this deterministically by reading recent `round_XXX/reviews/*_review.md` files for P0/P1/P2 rows that include sampled unit ids such as `::table::` or `::figure::`.

若任一层发现 P0/P1/P2，下一轮随机抽样量保持不变，以控制 AI token 成本，但该层会被标记为高风险。若同层连续两轮发现 P0/P1/P2，必须进入定向专项审计和闭环复查；默认不强制全检。

Before final output, the stronger pass validator must succeed:

```powershell
npm run review:random-validate:pass
```

最终输出前，强校验必须通过：

```powershell
npm run review:random-validate:pass
```

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

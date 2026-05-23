# 《刺青》生产规格 / Production Spec

status: "PASS"

## Template Basis

- template/epub_pipeline/common/preproduction/stage1/_TEMPLATE.production_spec.md
- template/epub_pipeline/common/references/cover_design_policy.md
- template/epub_pipeline/common/references/book_info_frontmatter_policy.md
- template/epub_pipeline/common/references/epub_assets_figures_tables.md
- template/epub_pipeline/common/references/quality_gate_framework.md
- template/epub_pipeline/common/references/release_versioning.md
- template/epub_pipeline/common/references/stratified_random_spotcheck.md
- template/epub_pipeline/targets/zh-Hans/quality_framework/README.md
- template/epub_pipeline/ja-zh-Hans/README.md

## Book Scope

- 书名：刺青
- 作者：谷崎润一郎
- source-target: ja-zh-Hans
- target: zh-Hans
- 创建方式：`books/scripts/create_book_project.py shisei_tanizaki --source-target ja-zh-Hans --source-url ...`

## Cover

- cover_source: `assets/cover_source.png`
- output_source: `output/cover_source.png`
- cover_epub_source: `assets/cover.jpg`
- output_cover: `output/cover.jpg`
- EPUB internal image: `EPUB/images/cover.jpg`
- cover page: `cover.xhtml`
- OPF requirement: manifest item for `images/cover.jpg` must include `properties="cover-image"`.
- size target: 1600 x 2400 px, 2:3 ratio, final JPG below 800KB.
- visual basis: needle-line and spider composition from the central tattoo image in the story.
- typography: deterministic image rendering; title, author, producer line and source note are placed by script, not by a generative image model.
- cover producer line: `LifeBook 书坊 译制`.
- book-info and metadata contributor: `LifeBook 书坊 SaberOnGo`.
- rights: self-made deterministic cover art for this trial EPUB; no modern copyrighted cover or still image is used.

## Book Info and Frontmatter

- frontmatter order: `cover.xhtml`, then `book_info.xhtml`, then translator/preface pages, then body.
- `book_info.md` must build into reader-visible `book_info.xhtml` and be reachable from `nav.xhtml`.
- `book_info.md` must include target title, original title, author, `LifeBook 书坊 SaberOnGo`, production date, source URL, concise rights note, book description, author background, and composition background.
- `book_info.md` must not contain QA logs, prompt logs, project workflow notes, repeated rights sections, or long raw URLs except the required source URL.
- `translator_note.md` is allowed only as concise reader-facing translation note.

## Metadata and EPUB Structure

- OPF must include `dc:title`, `dc:creator`, `dc:contributor`, `dc:publisher`, `dc:language`, `dc:date`, `dc:source`, `dc:description`, `dc:rights`, and `meta property="dcterms:modified"`.
- `nav.xhtml` must include TOC and landmarks for cover and book info.
- `cover.xhtml` and `book_info.xhtml` must be in OPF manifest and spine.
- `output/book.epub` is only the current build artifact; release must be under `output/release/`.

## Figures and Tables

- figures_and_tables: none in the source text body.
- cover image is the only reader-visible image asset.
- formula/proof blocks: none.
- table layer: none.
- caption/note layer: only generated cover figure caption if present; random spot-check script records actual candidate counts.

## Required Gates

- source evidence: PASS
- rights checklist: PASS
- Japanese textual notes: PASS
- pretranslation: PASS
- chapter gate: PASS
- publication lint: must PASS
- asset lint: must PASS
- template workflow gate: must PASS
- cover output assets: must PASS
- reader-facing policy: must PASS
- EPUBCheck: must report fatal=0,error=0
- stratified random spot-check: latest round must PASS with `--require-pass`

## Release Rule

Only `output/release/*.epub` created by `npm run release:create` can be treated as a release artifact. `output/book.epub` is an intermediate build only.

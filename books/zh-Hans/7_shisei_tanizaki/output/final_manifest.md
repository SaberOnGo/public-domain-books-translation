# Final Manifest / 最终产物清单

book: 刺青
original_title: 刺青
author: 谷崎润一郎
contributor: LifeBook 书坊 SaberOnGo
publisher: LifeBook 书坊
language: zh-CN
release_version: v0.0.3
release_status: PASS

## Source / 来源

- source_card: https://www.aozora-renewal.cloud/cards/001383/card56641.html
- source_text_zip: https://www.aozora-renewal.cloud/cards/001383/files/56641_ruby_59456.zip
- source_evidence: `metadata/source_evidence.md`
- rights_checklist: `metadata/rights_checklist.md`

## Release Artifact / 发布产物

- current_epub: `output/book.epub`
- release_epub: `output/release/刺青_v0.0.3.epub`
- size_bytes: 296935
- sha256: `24F7A87C491EF1F62F321216D64D1457159A0F0E0DBFBB814A63119D65DC3B03`

## Cover Assets / 封面资产

- cover_jpg: `output/cover.jpg`
- cover_jpg_size_bytes: 372730
- cover_jpg_sha256: `A7FE8CD517456C43079230697A452A0DDC3854E6434F949D1F4DB22CB5577DCA`
- cover_source_png: `output/cover_source.png`
- cover_source_png_size_bytes: 126299
- cover_source_png_sha256: `4E649C8A14FC8B0E3E09EC3F1EAD51BD04FFD545552F65EEE541EABDF90041DB`

## QA / 校验证据

- template_preflight: PASS
- publication_lint: PASS, unresolved issue count 0
- asset_manifest_check: PASS, issue count 0
- cover_output_assets_check: PASS
- reader_facing_policy: PASS
- epubcheck: fatal 0, error 0, warning 0
- random_spotcheck_round: `reviews/random_spotcheck/round_004`
- random_spotcheck_validation: `reviews/random_spotcheck/round_004/validation_report.json`
- random_spotcheck_status: PASS
- random_spotcheck_require_pass: true
- release_confidence: 1.0

## EPUB Structure / EPUB 结构

- spine_order: `cover.xhtml`, `book_info.xhtml`, `translator_note.xhtml`, `preface.xhtml`, `001_shisei.xhtml`
- OPF includes: `dc:title`, `dc:creator`, `dc:contributor`, `dc:publisher`, `dc:language`, `dc:date`, `dc:source`, `dc:description`, `dc:rights`
- nav includes TOC and landmarks for cover and frontmatter.

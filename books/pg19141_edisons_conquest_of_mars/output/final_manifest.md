# Final Manifest / 最终产物清单

status: "PASS"

## EPUB Output

- `output/book.epub`
- `output/爱迪生征服火星.epub`
- `preproduction/stage2_sample/sample_book.epub`
- 主标题：`爱迪生征服火星`
- 译者：`LifeBook 书坊 SaberOnGo`

## Validation

- `output/publication_lint.json`: PASS，硬错误 0。
- `output/epubcheck.json`: PASS，fatal 0，error 0，warning 0。
- `qa/refinement/refinement_check.json`: PASS，出版范围 BOM 0，mojibake 0，中文异常空格 0。
- `qa/refinement/full_book_literary_review_2026-05-13.md`: PASS，已覆盖全书信达雅和重点高潮段落复查。
- `qa/refinement/2026-05-13_publication_grade_title_terms_paragraphs.md`: PASS，已覆盖标题工程、术语/译注统一、章节精修和长段落处理。
- 长段落复扫：普通叙述段 `gt300=0`，`gt500=0`，最长 300 字。

## Source And Rights

- Source: Project Gutenberg #19141, https://www.gutenberg.org/ebooks/19141
- Source text: `source/source_text_raw.txt`
- Clean source: `source/source_text.txt`
- Rights checklist: `metadata/rights_checklist.md`

## Translation Artifacts

- Source chapters: 19
- Translated chapters: 19
- Final chapters: 19
- Chapter gates: 19

## Decision

DONE-ready.

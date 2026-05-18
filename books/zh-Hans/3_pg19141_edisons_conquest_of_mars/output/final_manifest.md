# Final Manifest / 最终产物清单

status: "PASS"

## EPUB Output

- `output/book.epub`
- `output/爱迪生征服火星.epub`
- `preproduction/stage2_sample/sample_book.epub`
- 封面源图：`assets/cover_source_gpt_image.png`
- 封面生成 prompt：`assets/cover_source_gpt_image_prompt.txt`
- EPUB 封面图：`assets/cover.jpg` / `output/cover.jpg`
- EPUB 文件体积：620034 bytes
- EPUB 封面体积：456011 bytes
- EPUB SHA256：`815780A768B5BDB7ED5B86F4A41A45458BD6EC81996BBEE148C76885F9A1C876`
- 封面 SHA256：`4D9C5D8C2A9AB8561B08C99ADB186EC440A2B95FE4E74A5FCC671FF2F922912F`
- 主标题：`爱迪生征服火星`
- 译者：`LifeBook 书坊 SaberOnGo`

## Validation

- `output/publication_lint.json`: PASS，硬错误 0。
- `output/epubcheck.json`: PASS，fatal 0，error 0，warning 0。
- `qa/refinement/refinement_check.json`: PASS，出版范围 BOM 0，mojibake 0，中文异常空格 0。
- `qa/refinement/full_book_literary_review_2026-05-13.md`: PASS，已覆盖全书信达雅和重点高潮段落复查。
- `qa/refinement/2026-05-14_cover_policy_rebuild_review.md`: PASS，已按最新封面规则重做 GPT-IMAGE-2 封面，并补齐书籍信息页作者简介与创作背景。
- `qa/refinement/2026-05-13_gpt_image_cover_and_book_info_review.md`: PASS，已覆盖 GPT-IMAGE 封面、书籍信息页、EPUB 内 cover-image 和最终体积复核。
- `qa/refinement/2026-05-13_publication_grade_title_terms_paragraphs.md`: PASS，已覆盖标题工程、术语/译注统一、章节精修和长段落处理。
- EPUB 解包抽查：`EPUB/images/cover.jpg` 为 456011 bytes，OPF `cover-image` 指向 `images/cover.jpg`，EPUB 内无 `cover.svg`，书籍首页为“书籍信息”。
- 书籍信息页抽查：含 `LifeBook 书坊 SaberOnGo`、作者简介、创作背景和关于本书的简短阅读背景。
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

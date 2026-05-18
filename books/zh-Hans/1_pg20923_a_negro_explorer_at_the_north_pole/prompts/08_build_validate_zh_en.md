# 08 构建与校验 EPUB / Build & Validate EPUB

【中文命令】
pandoc frontmatter/preface.md frontmatter/translator_note.md chapters/final/*.md --metadata-file=metadata/book.yaml --toc --toc-depth=2 --split-level=1 -o output/book.epub
node scripts/publication_lint.js --target=zh-Hans --write-report
epubcheck output/book.epub > output/epubcheck.log
`publication_lint.json` 必须无硬错误，且 `targetTitleLatinResidue=0`。无 ERROR 则状态= DONE。

[EN Commands]
pandoc frontmatter/preface.md frontmatter/translator_note.md chapters/final/*.md --metadata-file=metadata/book.yaml --toc --toc-depth=2 --split-level=1 -o output/book.epub
node scripts/publication_lint.js --target=zh-Hans --write-report
epubcheck output/book.epub > output/epubcheck.log
Set state.status=DONE only when publication lint has no hard errors, `targetTitleLatinResidue=0`, and EPUBCheck has no ERROR.

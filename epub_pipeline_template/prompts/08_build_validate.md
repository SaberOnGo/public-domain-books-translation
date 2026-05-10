# Step 08 Build + Validate EPUB
Build command:
pandoc frontmatter/preface.md frontmatter/translator_note.md chapters/final/*.md --metadata-file=metadata/book.yaml --toc --toc-depth=2 --split-level=1 -o output/book.epub
Validate command:
epubcheck output/book.epub > output/epubcheck.log
If no ERROR, set state.status=DONE

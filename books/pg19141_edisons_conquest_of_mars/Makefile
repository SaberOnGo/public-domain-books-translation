BOOK=output/book.epub

epub:
	pandoc frontmatter/preface.md frontmatter/translator_note.md chapters/final/*.md \
	  --metadata-file=metadata/book.yaml \
	  --toc --toc-depth=2 --split-level=1 \
	  -o $(BOOK)

check:
	epubcheck $(BOOK) > output/epubcheck.log

all: epub check

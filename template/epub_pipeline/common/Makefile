BOOK=output/book.epub

.PHONY: lint epub check all

lint:
	npm run lint:publication
	npm run lint:assets

epub:
	npm run build:epub

check:
	npm run check:epub

all:
	npm run build:epub
	npm run check:epub

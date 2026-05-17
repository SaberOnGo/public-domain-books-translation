BOOK=output/book.epub

.PHONY: lint epub check all trial

lint:
	npm run quality:all

epub:
	npm run build:epub

check:
	npm run check:epub

trial:
	npm run trial:epub

all:
	npm run build:epub
	npm run check:epub

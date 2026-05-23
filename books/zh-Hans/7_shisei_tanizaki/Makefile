BOOK=output/book.epub

.PHONY: lint epub check random-review random-validate release release-draft all

lint:
	npm run lint:publication
	npm run lint:assets

epub:
	npm run build:epub

check:
	npm run check:epub

random-review:
	npm run review:random-samples

random-validate:
	npm run review:random-validate:pass

release:
	npm run release:create

release-draft:
	npm run release:draft

all:
	npm run build:epub
	npm run check:epub

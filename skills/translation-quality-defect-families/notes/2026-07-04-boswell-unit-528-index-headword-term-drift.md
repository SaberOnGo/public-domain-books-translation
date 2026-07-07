# Boswell Unit 528: Index Headword Term Drift

## Finding

Dense index units can hide proper-noun drift because entries are short and look like ordinary topical labels. Unit 528 initially rendered `Goldsmith`, `Johnson's Court`, `King's evil`, and `Temple Bar` with locally plausible Chinese forms that did not all match the book glossary or prior index/body usage.

## Low-token audit

Before closing an index unit, scan high-risk headwords and place/event/medical terms against:

- `glossary/proper_nouns.csv`
- `glossary/terms.csv`
- neighboring completed index files under `chapters/final/5*.md`
- body occurrences in `chapters/final/`

Useful triggers: personal names, London places, historic events, folk-medical terms, work titles, and capitalized quoted phrases.

## Fix pattern

Prefer the locked or established reader-facing Chinese form in index entries:

- `Goldsmith` -> `哥尔德史密斯`
- `Johnson's Court` -> `约翰生院`
- `King's evil` -> `王疮`
- `Temple Bar` -> `坦普尔关`

If source spelling is the point of the entry, keep the source form only where the existing proper-noun policy or prior index format requires it.

## Recheck

After any index terminology fix, the fix round is not PASS. Rerun a fresh whole-unit source/target review and repeat the low-token scans for both the rejected and accepted renderings.

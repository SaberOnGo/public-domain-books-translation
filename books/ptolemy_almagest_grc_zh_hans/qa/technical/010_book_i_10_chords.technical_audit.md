# Book I.10 技术审计 / Technical Audit

audit_status: `BOOK_I10_PRE_TRANSLATION_CONTROL_PASS_FOR_TRIAL`

## Scope

- chapter_id: `010_book_i_10_chords`
- source_file: `chapters/src/010_book_i_10_chords.md`
- PAL range: `I_31_7` through before `I_48`
- PDF viewer range: pages `19` through `27`
- diagram audit: `qa/technical/010_book_i_10_chords.diagram_table_audit.md`
- term lock: `qa/technical/mathematical_term_lock.md`

## Current Control Result

Book I.10 is approved for one controlled trial translation only. This does not approve full-book translation, final chapter promotion, publication diagrams, or Book I.11 chord-table work.

## Required Checks Before Trial Translation

| id | check | status | evidence / next action |
|---|---|---|---|
| TECH-001 | Greek source extracted and marked | PASS_FOR_TRIAL | `chapters/src/010_book_i_10_chords.md` |
| TECH-002 | PDF page range mapped | PASS_FOR_TRIAL | viewer pages `19`-`27`, boundary page `28` |
| TECH-003 | figure pages identified | PASS_FOR_RANGE | figures visible on pages `20`, `22`, `23`, `24`, `25`, `26` |
| TECH-004 | figure labels transcribed and checked | PASS_FOR_TRIAL | `qa/technical/010_book_i_10_chords.diagram_table_audit.md` records labels for 7 figures and maps them to source lines |
| TECH-005 | proof dependency map created | PASS_FOR_TRIAL | `qa/technical/proof_dependency_map.md` maps Book I.10 constructions, Euclid citations, internal lemmas, and numerical proof dependencies |
| TECH-006 | sexagesimal number policy applied | PASS_FOR_TRIAL | `qa/technical/numeric_validation_log.md` records Book I.10 sexagesimal scale, chord values, approximation policy, and Book I.11 table boundary |
| TECH-007 | terminology pilot lock updated from Greek | PARTIAL | `mathematical_term_lock.md` now contains Book I.10 source terms, but not full lock |
| TECH-008 | reference witness diff policy applied | DEFERRED_TO_TRIAL_REVIEW | English witness may be consulted only after Greek-first draft segments exist; not required for the pre-translation technical-control gate |

## Known Technical Risks

- The chapter uses `εὐθεῖα` and `ὑποτείνουσα εὐθεῖα` for chord-like lines; translating every instance as `弦` may obscure the proof wording.
- The phrase `ἄκρον καὶ μέσον λόγον` needs a stable Chinese convention before final translation.
- The proof repeatedly uses Euclid references; omitted dependencies would make the Chinese translation mathematically misleading.
- Several numerical values are sexagesimal or Greek numeral expressions; they must be transcribed and checked, not silently normalized.
- The figure labels in the scan are small; GPT-image-2 redraw cannot be used until labels are manually or visually confirmed.

## Trial Translation Gate

`chapters/translated/010_book_i_10_chords.md` is now allowed for a single controlled Book I.10 trial translation. The permission is narrow:

- translate only from `chapters/src/010_book_i_10_chords.md`;
- keep Greek point labels and sexagesimal values controlled by the QA files above;
- do not write `chapters/final/`;
- do not translate Book I.11 chord table or any other chapter;
- do not enter full-book translation.

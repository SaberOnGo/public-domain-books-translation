# 18th-Century Biography Latin Poem and Parliamentary Report Interface

## Trigger

Biographical chapters may embed Latin poems, classical mythic names, political
reporting devices, and publication letters in one unit. These passages mix
quoted poetry, note markers, pseudonymous institutions, and bookseller terms.

## Risk

Latin or classical names can be translated smoothly but lose the required
first-mention source interface. Note markers attached to language names,
quotation tags, or publication terms may drift onto the next Markdown line and
become hard to audit. Parliamentary reporting terms can also flatten into
generic political prose if the pseudonymous or press-history function is missed.

## Low-Token Audit

- Compare source and target note-number lists first.
- Scan for Latin or mythic proper names in the source, then verify
  `glossary/proper_nouns.csv` rows and first target occurrences.
- Search source terms such as `anagram`, `The Senate of Lilliput`,
  `regular coadjutor`, `Parliamentary Journals`, `pension`, and
  `mercenary bookseller`, then confirm the target uses controlled Chinese terms.
- Inspect line breaks around note markers such as `[333]`, `[340]`, and `[344]`
  so the marker stays visibly attached to the word or quote it annotates.

## Fix Pattern

Translate the reader-facing meaning in Chinese, while preserving source forms
only for controlled first-mention proper nouns or explicitly named foreign
phrases. For Latin poems, provide a readable Chinese rendering and keep mythic
name interfaces such as `伊里斯（Iris）` when first introduced. For parliamentary
reports, keep the institutional disguise visible, for example `小人国元老院
（The Senate of Lilliput）`.

## Recheck

After any repair, rerun CSV-width checks, source-string scans, note-marker
comparison, and target-only reading. A repaired round remains
`FIXED_RECHECK_REQUIRED`; only the following zero-issue full-chapter review can
PASS.

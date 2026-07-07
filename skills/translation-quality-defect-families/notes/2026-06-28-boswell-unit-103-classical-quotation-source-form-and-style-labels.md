# Boswell Unit 103: classical quotation source forms and style labels

## Trigger

Biographical notes often quote Latin, Greek transliteration, or older printed
forms as evidence. A translator may silently normalize a source form to a more
familiar spelling, but that changes the edition witness visible to readers.

## Defect Family

- Classical or foreign-language quotation lines must preserve the printed
  source form when the note is citing the line as evidence. Do not silently
  correct a strange or likely erroneous form such as `ilia` to a more familiar
  `illa`.
- Rare coined words and style labels such as `peregrinity`, `depeditation`, and
  `Brownism` need a compact target-language interface. If the source form is
  being discussed, preserve it once with a Chinese gloss.
- Names that are not yet in the proper-noun register still need the user's
  display policy: first natural body mention should provide a source interface
  unless the source form is irrelevant or already supplied elsewhere.

## Find

- Scan source and target for classical quotation blocks and source-form labels:
  `Greek:|Diligat|Quam juvat|peregrinity|depeditation|Brownism|Raleigh's`.
- Compare quoted source lines character-for-character when they are copied
  into the translation.
- Scan new proper names that are absent from `glossary/proper_nouns.csv`, then
  check first-body display against the book's user setting.

## Fix

- Preserve the printed source form in the quote, then add a target-language
  rendering nearby.
- For coined or style words, use a readable Chinese gloss while keeping the
  source form only where the source form is the evidence.
- For an unregistered but important name, use a compact first interface such as
  `珀森（Person）`, then continue in Chinese.

## Recheck

- Rerun source/target quotation scans after each fix.
- Confirm the Chinese gloss has not replaced the source evidence.
- Confirm the latest chapter-control round after any fix is a separate
  full-chapter zero-issue PASS round.

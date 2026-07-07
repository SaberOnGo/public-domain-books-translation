# Boswell Unit 104: source-word glosses and historical household labels

## Trigger

Eighteenth-century biographical notes often combine source-word corrections,
loaded social labels, and later moral testimony. Small wording choices can add
modern judgment or hide the note's textual evidence.

## Defect Family

- A source word cited as the original reading, such as `retrospection`, should
  not be left as a bare foreign word. Keep the source form and add a compact
  Chinese gloss.
- Historical identity labels such as `black servant` should be rendered clearly
  without adding contempt or anachronistic euphemism. Avoid abrupt compounds
  that feel like a slur or production shorthand when a plain phrase such as
  `黑人仆人` is accurate.
- Locked work titles should be checked before translating advertisements or
  short-title notices; a descriptive title may drift from the book's register.

## Find

- Scan source and target for source-word correction triggers:
  `In the original|original|retrospection|Detector|Inopem`.
- Scan translated text for abrupt household or status labels:
  `黑仆|黑人仆人|仆人|servant`.
- Compare advertised or variant title mentions against `glossary/proper_nouns.csv`.

## Fix

- Use `source（Chinese gloss）` for brief source-word correction points when the
  source form itself matters.
- Recast historical household labels into plain, accurate Chinese that does not
  add contempt.
- Use the registered work title unless the local note is explicitly analyzing
  the variant title wording.

## Recheck

- Confirm the source evidence remains visible and immediately understandable.
- Confirm the Chinese wording has not softened or intensified the historical
  fact beyond the source.
- Confirm any fix round is followed by a separate full-chapter zero-issue PASS
  round.

# 18th-Century Biography: Character Sketch and Glossary Interface

## Trigger Context

Use this note when a Boswell/Johnson unit shifts from conversation into a
compressed character sketch, especially when the passage introduces a writer,
lists early employments, quotes foreign phrases, and records book titles in
glossaries.

## Defect Family

- **Moral-character abstraction drift**: Phrases such as `no settled system`
  often judge fixed principles or conduct, not a theoretical "system." In
  Chinese, prefer a concrete moral/intellectual phrase when the paragraph is
  describing a person's reliability.
- **Biographical wordplay flattening**: Puns like Goldsmith having `disputed`
  his passage through Europe carry both literal debate and travel survival.
  Preserve the double function in a compact reader-facing phrase.
- **Foreign social-label interface**: Short French or Latin phrases can be kept
  in parentheses when the source phrase is being cited, but the Chinese must
  first give a usable meaning such as "冒失鬼" or "凡他触及之物，无不经他装点".
- **Comma-bearing title rows**: Work titles such as `Telemachus, a Mask` must
  be CSV-quoted in glossary files. Otherwise the row may parse into the wrong
  fields and later proper-noun checks become unreliable.
- **Performance names need scene function**: A term like `Fantoccini` is not
  only a foreign proper noun; in a scene it may need a class word such as
  "木偶戏演出" so the reader understands why a puppet's dexterity is being
  judged.

## Review Moves

1. In character sketches, test abstract nouns against the paragraph's moral
   argument before accepting a literal rendering.
2. For foreign phrases, make the Chinese meaning readable before the source
   form appears.
3. Search the book glossary for every new source name that contains a comma,
   then verify with `csv.DictReader` that the row still maps to the expected
   columns.
4. If a glossary-interface issue is repaired after a chapter review, record it
   as a fix round and run a new full-chapter recheck before PASS.

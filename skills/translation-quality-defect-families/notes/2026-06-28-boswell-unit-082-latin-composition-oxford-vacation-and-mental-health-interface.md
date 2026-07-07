# Boswell Unit 082: Latin composition, Oxford vacation, and mental-health interfaces

## Context

Unit 082 combines Johnson's Latin college work, Oxford institutional terms,
vacation attendance records, and Boswell/Johnson mental-health language. The
main risks were not single unknown words, but small source interfaces that look
ordinary until the whole note is read.

## Defect Family

- Latin composition interface drift: a Latin poem or prose exercise may be
  accurately summarized but still read as awkward Chinese if the image,
  quotation function, and classical wine/place references are not rebuilt.
- Oxford institution drift: `gaudy`, `Demy`, `Fellow`, `A.M.`, college
  printers, and vacation account tables need reader-facing Chinese before the
  source term helps.
- OCR-like source anomaly drift: a suspicious phrase such as `with seventy`
  must be tested against nearby sense and likely source corruption; do not
  translate the surface if it breaks the sentence logic.
- Mental-health idiom drift: phrases such as `hypochondria`, `not sober`,
  `mad`, and `disorders of body and disturbances of mind` must follow the
  historical psychological context, not modern colloquial illness shortcuts or
  alcohol senses.
- Dense citation-name gaps: notes packed with diary titles, college records,
  biographies, works, and abbreviations still need setting-3 source interfaces.

## Audit Pattern

1. Scan source triggers:
   `gaudy|Demy|A.M.|Fellow|MDCCXXXI|with seventy|not sober|hypochondria|disorders of body|Mea nec Falernae|Formiani Pocula|Southey's Wesley|Morris, Aeneids`.
2. Scan target residues:
   `七十岁|不清醒|盛大的 gaudy|Demy［奖学生］|也不能如此|MDCCXXXI 年|A.M.|Pr. and Med|deficience`.
3. Compare all new people, works, institutions, and source books against
   `glossary/proper_nouns.csv`, especially note-heavy paragraphs.
4. For tables copied from old editions, check row count, column labels,
   numerical values, and whether the prose explains what the table measures.

## Fix Pattern

- Rebuild Latin or classical quotations into readable Chinese images, and keep
  source form only when a local policy or note interface requires it.
- Translate institution terms by function first: `学院宴会（gaudy）`,
  `Demy（奖学生）`, `研究员`, `文学硕士`, then record exceptions when a body
  source parenthesis is necessary.
- Treat suspected OCR/source anomalies as source-critical watchlist items:
  check grammar, neighboring sentences, and the argument before translating.
- Render mental-health language by historical function: `不算神志安宁` is safer
  than alcohol-coded `不清醒` when the surrounding note discusses melancholy,
  madness, and disturbances of mind.
- Pair Roman numerals and antiquarian abbreviations with target-readable forms:
  `1731年（MDCCXXXI）`, not a bare Roman date.

## Recheck

The latest PASS round should have matching note numbers, complete table rows,
no stale source abbreviations, no target residues from the audit list, and a
target-only reading score high enough that the Latin and Oxford passages read
as finished Chinese notes rather than source-facing crib text.

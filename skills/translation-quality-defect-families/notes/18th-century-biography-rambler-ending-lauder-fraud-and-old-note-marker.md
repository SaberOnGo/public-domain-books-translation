# 18th-Century Biography Rambler Ending, Lauder Fraud, and Old Note Marker

## Trigger

When Boswell moves from periodical criticism into letters, charity theatre,
and literary fraud, one unit may contain several fragile interfaces at once:
old editorial markers such as `[*]`, motto or verse endings, benefit
performances, subscription appeals, and pamphlet titles in a plagiarism dispute.

## Risk

Old edition markers can survive even when numeric notes are correct, because
they are not counted by the numeric note audit. Social idioms such as `hung
loose upon society` can be translated too literally, leaving source syntax in
Chinese. Fraud terms such as `plagiary`, `interpolated fragments`, and
`archetype` may also drift if they are handled as ordinary descriptive prose.

## Low-Token Audit

- Search each translated unit for `\[\*\]`, `原卷范围`, page headers, `A.D.`,
  `Ætat`, URLs, and other old-edition residue in addition to numeric notes.
- For periodical endings, check whether motto, Greek verse, English couplet,
  and religious-conformity wording are all retained without moving note markers
  inside quoted phrases unnecessarily.
- For charity theatre passages, confirm that `benefit`, `living remains`,
  `Masque`, and `dramatic satire` are translated as performance and relief
  terms, not flattened into generic kindness language.
- For literary fraud passages, audit `plagiary`, `forgery and imposition`,
  `interpolated fragments`, `archetype`, `Preface`, `Postscript`, and pamphlet
  titles against the glossary before promotion.

## Fix Pattern

Delete nonnumeric old-edition markers from reader text unless the production
spec explicitly routes them to notes. Rebuild social idioms into idiomatic
Chinese that preserves the social relation, for example `与社会松散相依` rather
than a literal physical image. Keep first-occurrence title and person
interfaces compact as `译名（source）`, especially in fraud narratives where
source titles are evidence.

## Recheck

After repairs, rerun note equality, old-marker scan including `\[\*\]`, CSV
width checks, coverage checks, and a target-only read. Because any repair round
cannot PASS, append a fresh full-chapter review round and promote only after the
latest round reports zero issues.

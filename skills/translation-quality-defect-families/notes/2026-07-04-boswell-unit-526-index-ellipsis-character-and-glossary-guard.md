# Boswell Unit 526: Index Ellipsis, Character-Writing, and Glossary Guard

## Evidence

- Unit: `books/zh-Hans/19_约翰生传_詹姆斯_鲍斯威尔/chapters/translated/526_vol06_unit_45.md`
- Discovery method: full-unit source-to-target chapter control, glossary scan, and low-token `rg`/pattern audit for source index headwords.
- Immediate fixes: repaired glossary-sensitive terms (`apology`, `_Armiger_`, `beadle within him`, `_bow-wow_ way`), historical/social senses (`consequence`, `attendance`, `outcast woman`, `buck`), and the `character` subentry family.

## Reusable Lesson

Dense eighteenth-century indexes often omit the governing noun after a headword. When a block headed `character` later says `Bayle's of Menage`, `Dryden's`, or `Savage's`, the target should normally carry the implied "character-writing / portrait" relation, not translate the possessive as the person's own moral character. Use `性格描写`, `人物性格`, or `人物画像` according to the local relation.

For index units, do not treat short headwords as isolated dictionary entries. First recover the governing headword and the prior subentry relation, then translate the elliptical line. This is especially important for:

- possessive ellipsis after character/portrait/letter/work headwords;
- passive index formulas such as `felt by`, `described by`, and `drawn by`;
- old-sense abstract nouns such as `apology`, `consequence`, and `attendance`;
- social labels such as `buck`, where the glossary may prefer a period social type over a modern generic word.

## Low-Token Audit Pattern

Before closing similar index units, scan the current unit and nearby final chapters for source triggers and target candidates:

```text
character|characters|portrait|drawn by|described by|felt by|apology|consequence|attendance|buck|beadle|bow-wow
```

Then compare only the candidate lines against the neighboring source headword. Confirmed repairs require a fresh whole-unit recheck; the repair round itself cannot PASS.

## Recheck

Unit 526 fresh recheck after repair found zero residual raw `ib.`, `n.`, `n,`, `see`, OCR-like `l`+digit page anchors, TODO/FIXME markers, or line/note parity mismatches. The latest control round is PASS.

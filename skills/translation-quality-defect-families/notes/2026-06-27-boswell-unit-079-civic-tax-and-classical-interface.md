# Boswell Unit 079: Civic offices, tax terms, and classical interfaces

## Context

Unit 079 is a dense note block about Johnson's family, Michael Johnson's civic
offices and trade, excise records, local registers, and several Latin or Greek
interfaces. The risk is not one large omission, but many small terms that look
ordinary and become misleading if translated from surface form.

## Defect Family

- Racing allusion drift: `Eclipse` in Macaulay is a racehorse, not the
  astronomical event alone.
- Tax-term drift: `Excise` must follow the locked book term `消费税`; do not
  introduce `国产税`.
- Source spelling regularization: printed forms such as `Pharmako-Basauos`
  should not be silently corrected.
- Civic and church offices: `Riding`, `churchwarden`, `sheriff`, `bailiff`,
  `perpetual curate`, and `living` require historical office senses.
- Proper-name interface gaps: dense title pages and letters still need
  setting-3 source interfaces for important new names.

## Audit Pattern

For family-history or antiquarian note clusters:

1. Scan for historical office and tax terms:
   `Excise|exciseable|Riding|churchwarden|sheriff|bailiff|perpetual curate|living`.
2. Scan for source-interface forms:
   `Populus Armigerorum|in agro Varvicensi|sine directione Michaelis|Pharmako`.
3. Scan target residues:
   `国产税|应纳国产税|永久助理牧师|Pharmako-Basanos|进城途中|日蚀”第一`.
4. Compare every name in a quoted title page or letter against
   `glossary/proper_nouns.csv`, even if the sentence is otherwise a citation.

## Fix Pattern

- Translate `Eclipse` with the racehorse signal on first use:
  `赛马“日蚀”（Eclipse）`.
- Use `消费税` and `应纳消费税` for `Excise` and `exciseable`.
- Preserve printed source forms in foreign-script or transliterated title
  interfaces, with a Chinese title beside them.
- Use historical office terms consistently: `骑巡`, `教区委员`, `郡长`,
  `执达官`, `常任助理牧师`, `圣俸`.
- Add source forms for important names in letters and title pages:
  `Rev. George Plaxton`, `Lord Gower`, `Allen`, `John Evans`,
  `Sir John Floyer`, `Queen's College, Oxford`.

## Recheck

After fixes, run a fresh full-chapter pass. The latest PASS round must have
zero residue for the target drift list and no newly added CSV bad fields.

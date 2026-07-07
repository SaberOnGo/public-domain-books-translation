# Boswell unit 122: pension politics title and court/place interface

## Family

Biographical notes about Johnson's pension often combine political pamphlet
titles, pension patronage, London legal geography, and periodical/work-title
cross references. If the translator relies on memory instead of the book
glossary, established Chinese titles and institutional names drift within a
single note unit.

## How it was found

- Full source-vs-translation review after unit 122 draft.
- Glossary scan for `The Idler`, `Lord Bute`, `Taxation no Tyranny`, `The False
  Alarm`, `The Patriot`, `Falkland's Islands`, and related names.
- Exact-string scan of the translated unit for prior or competing renderings.

## Risk

- Periodical and pamphlet title drift (`《闲散者》` vs `《闲谈者》`,
  `《征税非暴政》` vs `《征税并非暴政》`) breaks full-book consistency and later
  title-map audits.
- Patron names such as `Lord Bute` can drift by transliteration (`比尤特` vs
  `布特`), which weakens cross-chapter reference.
- London legal-place phrases (`Old Bailey`, `Fetter Lane`, `Wine Office Court`)
  are easy to leave under-registered, making later searches miss court and
  lodging references.
- Compact legal/social actions such as `picking pockets` should be rendered by
  target-language function (`扒窃`), not literal object handling.

## Low-token audit pattern

```powershell
rg -n "闲散者|征税非暴政|比尤特|偷窃口袋|它于一七五九年|Wine Office Court|Old Bailey|Fetter Lane|Life of Young" chapters/translated chapters/final glossary
rg -n "The Idler|Taxation no Tyranny|Lord Bute|picking pockets|Wine Office Court|Old Bailey|Fetter Lane|Life of Young|Prophecy of Famine" chapters/src glossary
```

Then classify each hit as a confirmed drift, a glossary-approved form, or a
documented source-title/source-form exception.

## Fix pattern

- Check `proper_nouns.csv` before finalizing recurring Johnson works,
  pamphlets, patrons, and places.
- Add missing place/work rows immediately when a note introduces a reusable
  legal, lodging, court, or political-title interface.
- Translate legal/social actions by their target-language legal/social function:
  `picking pockets` -> `扒窃`.
- If a pronoun note such as `It was taken...` points to a place named only in
  adjacent context, make the Chinese note self-contained when it prevents reader
  confusion.

## Recheck

After fixes, rerun exact-string scans, glossary parse-width checks, note-id
equality, and target-only/source-fidelity rereading. The repair round remains
`FIXED_RECHECK_REQUIRED`; only the next zero-issue full-unit recheck may PASS.

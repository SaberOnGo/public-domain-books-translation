# Boswell Unit 101: periodical units, manuscript misreadings, and source-form evidence

## Trigger

In eighteenth-century biography notes, periodical format labels, manuscript
misreadings, and foreign-language fragments may be the evidence being argued
about, not decorative source residue.

## Defect Family

- Periodical format units can become false quantities if smoothed into modern
  Chinese. `three half sheets` is three items of the `half sheet` unit, not
  necessarily `three and a half sheets`.
- Manuscript-correction notes require both the wrong reading and the corrected
  reading. Omitting either side weakens the editor's argument.
- Latin, Greek-transliteration, and French fragments in correction notes need
  a source-form interface plus a compact Chinese gloss. They should not stand
  alone, but they also should not be flattened away.
- Cross-references with odd typography such as `3 Post` should be checked
  against local function before treating the initial mark as a volume number.

## Find

- Scan source units for correction language and quoted forms:
  `misread|read the manuscript|instead of|whereas|decyphers|printed|Corrections|for .* read`.
- Scan translated/final text for ambiguous measurement phrases:
  `三个半印张|三张半|三页半|半张纸`.
- Scan source and target for foreign source forms that need paired renderings:
  `Greek:|fami non|fatui non|Dégouté|renommée|In Tuccam|Multa ferunt`.
- For cross references, compare the local note with surrounding `See post` and
  `See ante` conventions before translating isolated numbers.

## Fix

- Name the source unit clearly when quantity is ambiguous, e.g. `三份“半印张”`.
- Preserve wrong and right readings side by side, then add the Chinese meaning
  only after the source-form contrast is visible.
- Give concise glosses for foreign fragments, especially when the point is a
  spelling, old word, or editorial correction.
- Recast cross-references by function, e.g. `见后文1753年1月1日条`, when the
  mark is not a real volume reference.

## Recheck

- Confirm the reader can see what the editor is correcting.
- Confirm the Chinese gloss has not replaced the source evidence.
- Confirm no smooth Chinese quantity now states a different material format.
- If any fix was made in a chapter control round, that round is
  `FIXED_RECHECK_REQUIRED`; only a later full-chapter zero-issue round can PASS.

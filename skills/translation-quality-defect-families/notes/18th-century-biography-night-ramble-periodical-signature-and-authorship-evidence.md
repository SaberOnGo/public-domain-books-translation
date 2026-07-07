# 18th-Century Biography Night Ramble, Periodical Signature, and Authorship Evidence

## Trigger

When Boswell shifts from comic nocturnal anecdotes into periodical authorship,
the same unit may contain market scenes, Shakespeare or Hogarth allusions,
dated prayers, signatures, pseudonyms, and arguments about who actually wrote
or dictated an essay.

## Risk

Compact English modifiers can attach to the wrong noun in Chinese. In a market
scene, `hampers, just come in from the country` refers to the baskets or goods,
not necessarily to the sellers. Periodical evidence can also be flattened if
letter signatures such as `T`, pseudonyms such as `Mysargyrus`, or initials
such as `C. B.` are translated away without showing why they matter.

## Low-Token Audit

- In comic action scenes, check every trailing participial phrase and nearby
  noun: ask whether the source modifies people, objects, places, or actions.
- Scan the translated chapter for source-interface residues and classify them
  as names, periodical signatures, foreign quotations, or accidental English.
- For periodical authorship passages, audit `signature`, `pseudonym`, `marked`,
  `ascribed`, `dictated`, and `wrote` against the source so the attribution
  chain remains visible.
- Check that dated prayers preserve calendar markers such as `N. S.` in target
  language rather than leaving unexplained abbreviations.

## Fix Pattern

Rebuild compact modifier chains into explicit Chinese relations: `正开始摆放他们刚从乡下运来的大篮筐`
rather than wording that makes the sellers themselves newly arrived. Preserve
periodical signatures when the source is arguing from them, but pair them with
Chinese function words such as `署名`, `标有`, or `归于`, so the reader sees why
the letters matter.

## Recheck

After repairs, rerun note equality, old-marker scans, CSV width checks,
coverage checks, and English-residue classification. If the fix touched a
source-interface or authorship chain, perform a source-fidelity pass before the
latest PASS round.

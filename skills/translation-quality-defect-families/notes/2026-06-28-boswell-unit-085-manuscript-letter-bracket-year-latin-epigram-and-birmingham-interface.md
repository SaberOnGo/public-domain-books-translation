# Boswell Unit 085: Manuscript letters, bracket years, Latin epigrams, and Birmingham interfaces

## Context

Unit 085 combines a residence chronology puzzle, manuscript debt letters,
Latin epitaph and epigram material, family-name variants, and Birmingham
newspaper evidence. The recurring risk is that editorial or source-evidence
interfaces look like ordinary body text but are actually part of the proof
chain.

## Defect Family

- Non-note bracket drift: source brackets such as `[1850]` may be years or
  editorial additions rather than note markers, but the reader-facing bracket
  sequence still must be preserved when the source uses square brackets.
- Manuscript-letter normalization drift: old spelling in quoted letters may be
  translated into readable Chinese, but names, money, addressees, and payment
  endorsements need faithful evidence handling.
- Latin epigram interface loss: when a passage discusses translation of a
  Latin couplet, keep the Latin source interface and then provide the Chinese
  sense, so later proposed translations have an anchor.
- Name-variant residue: `Jarvis or Jervis` and similar variants should not
  remain bare English; render both variants with target-language names and
  source forms.
- Local newspaper/source interface drift: Birmingham newspapers, surviving
  issue numbers, addresses, and later bracketed corrections must remain
  checkable as evidence, not generalized into prose.

## Audit Pattern

1. Scan source triggers:
   `[1850]|Good Sr.|truble|desiurs|Mr. Wumsley|Pd.|£5|Jarvis or Jervis|Liber ut esse|pulchra Maria|Birmingham Journal|Birmingham Daily Post|Swan Tavern|High Street`.
2. Scan target residues:
   `〔1850〕|Jarvis or Jervis|Good Sr.|truble|desiurs|oportunity|reat|freund|Pd.|tête-à-tête|adieu`.
3. Compare all bracketed numbers in source and target; do not assume every
   bracketed number is a note marker.
4. For manuscript letters, verify money amounts, names, addresses, addressee
   lines, and endorsements separately from the prose translation.

## Fix Pattern

- Preserve non-note square brackets when they are source-visible editorial
  evidence: `[1850]`, not `〔1850〕`, unless the project has an explicit
  conversion rule.
- Translate old-spelling manuscript prose into readable Chinese while keeping
  source names and amounts exact enough for audit.
- For Latin epigrams followed by translation discussion, use a source-plus-
  target interface:
  `Liber ut esse...` followed by a Chinese rendering.
- Convert name variants into target-language paired forms:
  `贾维斯（Jarvis）或杰维斯（Jervis）`.
- Preserve newspaper titles and issue evidence with source interfaces.

## Recheck

The latest PASS round should have equal ordered bracket-number lists, no old
letter spelling residue, no target residues from the audit list, and a
target-only reading that keeps the evidence chain clear without turning the
notes into commentary.

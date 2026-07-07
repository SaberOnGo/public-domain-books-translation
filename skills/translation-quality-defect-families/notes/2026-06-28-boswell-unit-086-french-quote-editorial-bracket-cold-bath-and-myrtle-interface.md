# Boswell Unit 086: French quote, editorial bracket, cold bath, and Myrtle interfaces

## Context

Unit 086 combines Johnson's adaptation of Lobo, curiosity passages in The
Rambler, modern Latin poetry, medical claims about cold bathing, and the
contested attribution of the Myrtle verses. Several issues came from source
interfaces that are small but evidentiary.

## Defect Family

- Foreign-language quote loss: French or Latin phrases that are themselves
  cited as wording evidence need both target-language sense and source form.
- Editorial bracket drift: compact source references such as `[lv. 3]` are
  evidence and should not be silently converted into looser Chinese brackets.
- Name-contraction interface loss: contractions such as `Mund` matter when
  the note itself discusses Johnson's habit of shortening names.
- Medical-practice drift: cold bath, bleeding, purging, rickets, font, and
  baptismal dipping must stay historically medical/religious, not modern
  wellness phrasing.
- Attribution-letter residue: old spellings such as `cloaths` or `publick`
  can be normalized in Chinese, but quoted letters still require names,
  dates, titles, and manuscript labels to remain auditable.

## Audit Pattern

1. Scan source triggers:
   `qu'il abusait|de la permission|[lv. 3]|Mund|Myrtle|cold bath|bleeding and purging|rickets|font|cloaths|publick|breakfast law|sermoms|Segued|Zeila`.
2. Scan target residues:
   `〔第五十五卷第3页〕|亲爱的蒙德，|without religion|sermoms|breakfast law|cloaths|publick|Sit still`.
3. Check that source-only spellings explicitly discussed by the note, such as
   `Segued` and `Zeila`, remain visible as source forms.
4. For medical passages, verify the historical treatment chain rather than
   modernizing it.

## Fix Pattern

- Pair foreign quotation with target sense:
  `滥用了男人可以丑的许可（qu'il abusait...）`.
- Preserve editorial source brackets where they are evidence: `[lv. 3]`.
- Add source form for meaningful contractions: `蒙德（Mund）`.
- Translate historical medical practice literally enough to keep the evidence:
  `放血和导泻`, `冷水浴`, `洗礼池`.
- Normalize old spelling only after preserving names, dates, and manuscript
  provenance.

## Recheck

The latest PASS round should have matching note numbers, no old-spelling
residue from quoted letters, no target residues from the audit list, and a
target-only reading that preserves both the argument and the evidence trail.

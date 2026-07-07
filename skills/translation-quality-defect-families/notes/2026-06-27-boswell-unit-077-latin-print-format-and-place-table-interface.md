# Boswell Unit 077: Latin tags, print formats, and place-table interfaces

## Context

In Boswell unit 077, the source combines eighteenth-century editorial notes,
Latin or Latinized tags, bibliographic format words, and a compressed table of
dates and places. These elements are easy to leave either too raw for Chinese
readers or too loosely normalized.

## Defect Family

- Foreign tag without reader interface: `pars magna` and `Johnsonianissimum`
  should not stand alone without a Chinese sense.
- Bibliographic format drift: `quarto` and `octavo` are book formats, not
  volume counts.
- Place table over-literalization: place names inside compressed tables should
  be checked against the glossary before being translated semantically.
- Social or moral abstract drift: `egotism` and `sober` need local context;
  they should not become vague `自我` or generic `清醒` when the scene is about
  self-display and temperance.

## Audit Pattern

When a translated chapter contains editorial notes or tables:

1. Scan source and target for Latin-like tags and bibliographic format words:
   `pars magna|Johnsonianissimum|magnum opus|quarto|octavo`.
2. Scan target residues and forbidden candidates:
   `四卷本|八卷本|药片|碑板|清醒而有规律|自己的自我`.
3. For tables, compare every place cell against `glossary/proper_nouns.csv`.
4. If any issue is fixed in the first pass, record the round as
   `FIXED_RECHECK_REQUIRED` and run a fresh full-chapter recheck.

## Fix Pattern

- Pair foreign tags with concise Chinese meaning in the body when the source
  phrase itself matters: `其中重要的一部分（pars magna）`,
  `最具约翰生气质（Johnsonianissimum）`.
- Render bibliographic formats as `四开本` and `八开本`.
- Use locked place-name entries for table cells, for example `Southill` as
  `索思希尔`.
- In quoted self-characterization and reform vows, translate the social
  function rather than the dictionary surface: `自我表现欲`, `节制而有规律的人`.

## Recheck

After fixes, reread the complete chapter without the source. The foreign tags
must be intelligible to a Chinese reader before the source form helps them, and
the date/place table must not contain semantic translations of proper names.

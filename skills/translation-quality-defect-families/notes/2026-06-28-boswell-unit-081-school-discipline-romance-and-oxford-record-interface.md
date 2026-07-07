# Boswell Unit 081: School discipline, old romance, and Oxford record interfaces

## Context

Unit 081 combines child-discipline debates, old romance titles, Johnson family
notes, poetic quotations, and Oxford college finance records. Several defects
came from ordinary-looking English words that had specialized institutional or
literary meanings.

## Defect Family

- Discipline phrase drift: `blow or whipping`, `rod`, and `force or fear`
  should be rendered as corporal-discipline terms, not abstract force words.
- Social phrase hardening: `common mould` and `philosophy and softness` need
  readable Chinese rather than material or body-like literalism.
- Old-romance title drift: `Don Bellianis` / `Don Belianis of Greece` should
  preserve the romance-title interface and the `Don` signal.
- Oxford record drift: `Commr.`, `Caution`, `Battells`, `servitor`,
  `commoner`, `sconce`, and `theme` need college-account senses.
- Dense citation-name gaps: quoted letters and college records still require
  setting-3 source interfaces for new people, institutions, works, and records.

## Audit Pattern

For education, discipline, and university-record notes:

1. Scan source triggers:
   `force or fear|blow or whipping|rod|common mould|Don Bellianis|Don Belianis|Caution|Commr.|Battells|servitor|commoner|sconce|theme`.
2. Scan target residues:
   `打击或鞭笞|普通材料做成|普通生|勤工生，是错误的|贝利亚尼斯爵士|哲学和柔软`.
3. Compare known work titles against `glossary/proper_nouns.csv`; especially
   `The Distressed Mother`, old romances, and Oxford source books.
4. Re-run CSV parsing after glossary updates, especially rows containing
   apostrophes or commas.

## Fix Pattern

- Use corporal-discipline terms: `挨打或鞭笞`, `戒尺`, `强力或恐惧`.
- Rebuild social abstractions as idiomatic Chinese: `寻常性情`,
  `哲学和温软风气`.
- Use romance title forms such as `《唐·贝利亚尼斯史》（Don Bellianis）` and
  `《希腊的唐·贝利亚尼斯》（Don Belianis of Greece）`.
- Translate Oxford records by function and preserve source terms when the
  entry itself is quoted: `自费生（Commr.）`, `保证金（Caution）`,
  `食宿账未清（Battells not discharg'd）`, `罚金（sconce）`.
- Follow existing locked glossary rows: `The Distressed Mother` as
  `《苦恼的母亲》`, `commoner` as `自费生`, and `servitor` as `勤工学生`.

## Recheck

The latest PASS round should have no residues from the target drift list, no
new CSV bad fields, and all quoted record terms should be intelligible before
their source form helps the reader.

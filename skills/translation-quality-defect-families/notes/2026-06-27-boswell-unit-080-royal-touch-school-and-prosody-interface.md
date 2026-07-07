# Boswell Unit 080: Royal touch, school discipline, and prosody interfaces

## Context

Unit 080 includes notes on Johnson's childhood, the royal-touch ceremony,
grammar-school exercises, Latin prosody, school discipline, and antiquarian
citations. The defects found here were mostly small but high-impact term
misreadings.

## Defect Family

- Civic body drift: `Court of Common Council` is a London municipal body, not
  a court of law.
- Records office drift: `Master of the Rolls` should not become a generic
  archive director.
- Prosody drift: `quantity` in Latin verse is syllable length, not volume or
  amount.
- School-discipline rhetoric: harsh phrases such as `inexorable blockhead`,
  `liberally educated`, and `illiberal sauciness` must be rebuilt for Chinese.
- Field-sports term drift: `sportsman` in a partridge context means a hunter,
  not a modern athlete.
- Dense note-name interfaces: citation-heavy school notes still require
  setting-3 source interfaces for important names and institutions.

## Audit Pattern

For childhood, education, or civic-history note clusters:

1. Scan source triggers:
   `Court of Common Council|Master of the Rolls|quantity|inexorable blockhead|liberally educated|illiberal sauciness|sportsman|barring out`.
2. Scan target residues:
   `共同议会法院|档案长官|音量|不可宽恕的笨蛋|自由教育|不自由的冒失无礼|运动家的气味`.
3. Check every new author, quoted official, and institutional name against
   `glossary/proper_nouns.csv`.
4. Re-run CSV parsing after appending any row containing commas or quotes.

## Fix Pattern

- Use `伦敦市共同议会（Court of Common Council）`.
- Use `案卷主事官（Master of the Rolls）`.
- Translate Latin prosody `quantity` as `音长`.
- Rebuild school rhetoric as readable Chinese:
  `铁石心肠的蠢材`, `受过文雅教育`, `鄙陋的粗鲁无礼`.
- Translate field-sports `sportsman` as `猎人` when the local evidence is
  partridges or hunting.
- Add setting-3 interfaces for dense note names such as `Hester Lynch Piozzi`,
  `Sir John Hawkins`, `Accidence`, `Hunter`, `Andrew Corbet`, `Tom Davies`,
  and `Lord Campbell`.

## Recheck

The final recheck should find zero target residues for the drift list and no
increase in `bad_extra_fields` for glossary CSV files.

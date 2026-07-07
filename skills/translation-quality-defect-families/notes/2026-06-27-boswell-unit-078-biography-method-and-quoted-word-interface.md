# Boswell Unit 078: Biography-method wording and quoted word interfaces

## Context

Unit 078 contains Boswell's final dictated letter, long editorial notes about
biography, Piozzi/Hawkins testimony, a French sentence from Voltaire, and a
word-choice dispute over `cast`, `malignancy`, and `disposition`.

## Defect Family

- Existing glossary drift: established work and character names such as
  `Female Quixote` and `Griffith` can drift when translated from memory.
- Quoted wording debate: when the source discusses exact English words, the
  target text needs both a Chinese meaning and the source word interface.
- Foreign sentence interface: French quotations should not be replaced by only
  a Chinese paraphrase when the source form is part of the note.
- Moral-character phrases can become stiff if translated abstractly, as with
  `outward sanctity` or `industry and activity`.

## Audit Pattern

For biography/editorial notes:

1. Scan source for disputed terms and foreign quotations:
   `cast|malignancy|disposition|unclubable|Des Maizeaux|visible progress`.
2. Scan target for stale or over-literal residues:
   `女堂吉诃德|格里菲斯|外在圣洁|勤勉和活动力|性情上低伏`.
3. Compare all work titles and character names against
   `glossary/proper_nouns.csv`, even if they look familiar.
4. If a revision is made during review, mark that round
   `FIXED_RECHECK_REQUIRED` and run a fresh full-chapter pass.

## Fix Pattern

- Use locked glossary forms: `《女吉诃德》`, `格里菲思`.
- For word-choice debate, write the Chinese sense first and keep the source
  word in parentheses or inline quote: `气质（cast）`,
  `malignancy（恶意）`, `disposition（倾向）`.
- Preserve the French source sentence with an immediate Chinese rendering.
- Recast moral-character abstractions into readable Chinese:
  `摆出极其虔敬的外表`, `勤奋好动`.

## Recheck

Read the final Chinese without the source. The exact source words should aid a
wording debate, not interrupt comprehension; all foreign sentences must have an
immediate Chinese interface.

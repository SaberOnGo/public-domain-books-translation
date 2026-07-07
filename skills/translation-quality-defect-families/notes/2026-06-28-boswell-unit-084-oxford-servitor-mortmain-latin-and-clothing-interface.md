# Boswell Unit 084: Oxford servitor, Mortmain, Latin, and clothing interfaces

## Context

Unit 084 combines Oxford college discipline, legal restrictions on charitable
devises, lists of Pembroke figures, Latin and Juvenal quotations, Savage's
clothing episode, and residence evidence from college books. The recurring
risk is that short institutional or material nouns look easy but carry a
specific historical interface.

## Defect Family

- Oxford discipline drift: `servitor`, room knocking, college hunting jokes,
  and "buttery books" need institutional senses rather than generic student
  or dining words.
- Legal-property drift: `freehold` and `Statute of Mortmain` should not be
  flattened into generic real estate or vague "permanent ownership" wording.
- Signature-interface drift: editorial signatures such as `J. BOSWELL, JUN.`
  need readable identity plus source form, not casual initials in Chinese.
- Latin and classical quote drift: Latin or Juvenal passages may be translated
  into Chinese verse/prose, but scans must ensure no naked source residue or
  line-order loss remains.
- Clothing/material residue: `clothes and linen` should become reader-facing
  garment terms; half-translated strings such as `衬 linen` are blockers.

## Audit Pattern

1. Scan source triggers:
   `servitor|Chevy Chase|freehold|Statute of Mortmain|J. BOSWELL, JUN|Si toga|Pelle patet|Haud facile|Res angusta|clothes and linen|buttery books|fivepence|Croker|Hickman`.
2. Scan target residues:
   `衬 linen|永久管业法|不动产|小 J.|Subito ad Batavos|Haud facile|Pelle patet|virtutibus|Pr. and Med`.
3. For legal words, check whether the target term identifies the historical
   legal barrier before the source form helps the reader.
4. For residence evidence, check college books, buttery books, dates, and money
   amounts together; do not translate them as generic school records.

## Fix Pattern

- Render Oxford institutional terms by function with source interface when
  needed: `勤工学生（servitor）`, `食堂账簿`, `五便士`.
- Use legal terms that expose the historical barrier: `自由保有地产` and
  `《死手法令》（Statute of Mortmain）`.
- Render editorial signatures as readable names plus source interface:
  `小詹姆斯·鲍斯威尔（J. Boswell, Jun.）`.
- Translate clothing/material terms fully into Chinese: `衣服和衬衣`, never
  half-source strings such as `衬 linen`.
- After Latin/classical quote handling, scan both source residues and target
  line order before PASS.

## Recheck

The latest PASS round should have matching note numbers, no naked Latin or
English material residue, no target residues from the audit list, and a
target-only reading that keeps college discipline, legal restriction, and
residence evidence clear to Chinese readers.

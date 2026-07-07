# 18th-century biography: lexicography, patronage, and amanuensis interface

## Problem family

Eighteenth-century literary biography often compresses publishing contracts,
patronage language, classical tags, Dictionary-making terms, and lists of
assistants into long narrative sentences. A translation can look fluent while
dropping one note marker, turning patronage terms into modern bureaucracy, or
leaving the workroom vocabulary too literal.

## Find by

- Compare source and target note-marker sequences after any prose polish,
  especially around named visitors or list items.
- Scan the current unit for lexicography and printing terms: `Plan`,
  `specimen`, `authorities`, `etymologies`, `definitions`, `significations`,
  `amanuenses`, `copyists`, `copy-right`, and `compositor`.
- Scan patronage/judicial rhetoric: `patron`, `province`, `suffrages`,
  `vicarious jurisdiction`, `Principal Secretaries of State`, and classical
  tags quoted inside prose.

## Risk

- Missing a note marker breaks source traceability even when the sentence still
  reads smoothly.
- Literal legal or bureaucratic wording can make patronage rhetoric sound like
  modern office procedure rather than Johnson's elevated appeal to a noble
  patron.
- Barely translated workshop terms make the Dictionary process opaque:
  `authorities` should read as lexical citation evidence, `amanuenses` as
  copyist-assistants, and `copy-right` as the book-trade payment object.

## Fix pattern

- Keep source note markers as an exact ordered sequence and do a second sequence
  check after every manual edit.
- Translate body terms into readable Chinese first; reserve source forms for
  policy-3 proper names, classical quotations, or a term row that explicitly
  requires a source interface.
- For Dictionary-making workflow, map terms by function:
  `authorities` -> citation authorities / evidence examples,
  `significations` -> senses or meanings, `amanuenses` -> copyist-assistants,
  `compositor` -> typesetter, and `copy-right` -> copyright in the book-trade
  payment context.
- For patronage rhetoric, preserve the formal register without making it stiff:
  `vicarious jurisdiction` can be `代行的裁断权`, and `province` can be
  `职分范围` or `权限` depending on the sentence.

## Recheck

After fixes, rerun the full source-target pass, exact note sequence comparison,
CSV structure check, and residue scans for old page headings, source-language
term shells, and punctuation-heavy English syntax.

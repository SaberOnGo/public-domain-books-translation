# 18th-Century Biography Periodical and Theatre Name Interface

## Trigger

When an eighteenth-century biography moves through periodicals, theatres,
taverns, street addresses, royal libraries, or dramatic personae, the prose often
contains short institutional names whose source form is useful at first mention.
Examples include magazine pseudonyms, theatre patentees, tavern names, and
dramatic character headings.

## Risk

If `target (source)` interfaces are split across Markdown lines or treated as
ordinary prose, low-token audits may miss them, and readers may see a broken
name interface in generated XHTML. If periodical or theatre terms are translated
too generically, the passage loses the publication or performance-history
evidence carried by the source.

## Low-Token Audit

- Scan the translated chapter for required source strings from
  `glossary/proper_nouns.csv`, especially names with `display_policy=3`.
- Check that first body occurrences remain visibly connected as
  `译名（source）`, not as a detached parenthetical on the next visual unit when
  that can be avoided.
- Search theatre and periodical terms such as `patentee`, `miscellany`,
  `adventurer in literature`, `gave the wall`, and `took the wall` in the source,
  then confirm the target uses book-level term rows rather than ad hoc wording.

## Fix Pattern

Keep first-mention interfaces compact and machine-searchable. For institutions
or periodical history, use target-readable nouns such as `专利经营人`,
`杂志性汇编`, and `投身文学谋生的冒险者`, while preserving the source form only
where the proper-noun policy requires it.

## Recheck

After repairs, rerun the note-marker scan, source-string scan, CSV-width check,
and a target-only reading pass. A fix round is not a PASS round; append a new
full-chapter review with zero issues before promotion to `chapters/final/`.

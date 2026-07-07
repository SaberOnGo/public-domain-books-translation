# 18th-Century Biography Friend Catalogue, Social Custom, and Title Interface

## Trigger

When an eighteenth-century biography gives a dense catalogue of friends,
booksellers, physicians, nobles, addresses, and household companions, the prose
often introduces many names before turning to one or two major relationships.
The same unit may also use social-custom words such as `levee`, Latin praise
phrases, medieval legal privileges, and title changes such as `Mr. (now Sir
Joshua) Reynolds`.

## Risk

Long lists make it easy to miss the first reader-facing source interface for an
important person, especially when the source itself nests a later title inside a
parenthesis. Social terms can drift the other way: an ordinary or already
translated custom word may get an unnecessary source parenthesis even when the
glossary says body Chinese only. Latin tags such as `dulce decus` should not be
treated like ordinary forbidden English residue when the source phrase is the
evidence.

## Low-Token Audit

- Scan the chapter's English residue after translation and classify every hit:
  proper-name first interface, Latin/foreign quotation, or accidental residue.
- For dense friend lists, compare the first visible occurrence of major names
  against `glossary/proper_nouns.csv`, including awkward source strings such as
  `Mr. (now Sir Joshua) Reynolds`.
- For social and legal terms, scan the target for source terms listed as
  forbidden renderings in `glossary/terms.csv`, especially `levee`,
  `mechanicks`, `free warren`, `Round-house`, and trade names.
- Check whether Latin tags intentionally preserved in the body have immediate
  Chinese glosses and no conflicting forbidden-rendering row.

## Fix Pattern

In friend catalogues, give the first important body occurrence a compact
`译名（source）` interface, even if the source string is typographically awkward.
After that, use the Chinese name only. For social customs, prefer a target
phrase such as `晨间接待`, `普通工匠`, or `自由猎苑权`; keep the source form only
when the text itself is discussing the foreign word or when a glossary row
records a source-plus-translation exception.

## Recheck

After repairs, rerun note equality, CSV-width checks, old-marker scans,
coverage checks, and a full English-residue classification. A fix round remains
`FIXED_RECHECK_REQUIRED`; only a new full-chapter round with zero issues may
promote the chapter.

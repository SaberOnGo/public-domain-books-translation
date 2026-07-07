# Boswell unit 123: pension-record and naval-slang interface

## Family

Johnson pension notes combine dictionary headwords, parliamentary metonymy,
Treasury/Exchequer record language, and rare naval slang. Literal guessing can
produce false etymology, inconsistent title forms, or wrong institutional
interfaces.

## How it was found

- Full source-vs-translation review after drafting unit 123.
- Residue scan for raw source forms such as `pension`, `pensioner`,
  `Loplolly`, `Loblolly`, and institutional names.
- Glossary scan for `Lord Loughborough`, `St. Stephen`, `Moral Essays`,
  `Exchequer`, `Grenville Papers`, and `Roderick Random`.

## Risk

- `Lord Loughborough` can drift by transliteration; follow the book glossary
  (`洛伯勒勋爵`) rather than a plausible alternate form.
- `St. Stephen` in Pope's couplet is parliamentary metonymy, not a saint in
  ordinary religious prose; use `圣斯蒂芬堂` so the House of Commons setting is
  visible.
- `loblolly/loplolly` is naval medical slang for gruel/thick porridge and the
  surgeon's assistant role; do not infer a vegetable meaning such as `萝卜粥`.
- `pension/pensioner` may retain source forms only when the note discusses
  Johnson's dictionary headwords; ordinary body text should use `年金` and
  `领年金者`.

## Low-token audit pattern

```powershell
rg -n "拉夫伯勒|圣斯蒂芬又|萝卜粥|Loplolly|Loblolly|Lobolly|Docker|pensioner|pension|Exchequer|Treasury|Civil List" chapters/translated chapters/final glossary
rg -n "Lord Loughborough|St\\. Stephen|Loplolly|Loblolly|Lobolly Boy|Docker|pensioner|pension|Exchequer|Treasury|Civil List" chapters/src glossary
```

Classify source forms as definition/slang-discussion exceptions or as forbidden
body residue.

## Fix pattern

- Resolve institution and political metonymy from historical function before
  translating.
- For rare slang, verify the domain through nearby source explanation and known
  cited work context; translate the function in Chinese and retain the source
  form only because the note discusses the word itself.
- Add terms rows with forbidden renderings for false-etymology risks, e.g.
  `loblolly/loplolly` forbids `萝卜粥`.
- After changing a glossary form, scan translated and final chapters for the
  drifted form.

## Recheck

Run exact residue scans, CSV parse-width checks, note-id equality, and a full
target-only/source-fidelity reread. A repair round is
`FIXED_RECHECK_REQUIRED`; only a subsequent zero-issue full-unit check may PASS.

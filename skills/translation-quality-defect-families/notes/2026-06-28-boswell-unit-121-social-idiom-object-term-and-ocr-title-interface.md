# Boswell unit 121: social idiom, object-term, and OCR-title interface

## Family

18th-century biographical notes often compress social judgement, technical
object names, and bibliographic evidence into short anecdotes. A literal Chinese
rendering can make a social idiom false, turn a historical object into the wrong
kind of thing, or silently preserve an OCR-damaged title.

## How it was found

- Full unit source-vs-translation review after drafting unit 121.
- Targeted scan for suspicious literal residues in `chapters/translated`.
- Glossary check against `proper_nouns.csv` for `The Man of Feeling`,
  `Royal Academy`, `Rambler`, and related Johnson-circle names.

## Risk

- `told a million of stories` is hyperbolic praise; literal quantity makes the
  Chinese sound childish and distracts from Burney's social portrait.
- `eaten himself out of every tavern` describes exhausting credit/welcome by
  eating on account; translating it as emptying taverns changes the joke.
- `a thousand tun of copper` in Thrale's brewing context means copper brewing
  vessels or vats; translating it as a weight of copper breaks the anecdote.
- OCR-damaged bibliographic text such as `Life of me` can hide a real title
  (`Life of Hume`) if not checked against context.

## Low-token audit pattern

Use exact and near-string scans before asking for long prose review:

```powershell
rg -n "一百万个故事|吃空|一千吨铜|低层街头语言|泰伯恩的路|有情人|皇家美术院|格雷旅馆|漫步者|Life of me|我的生平" chapters/translated chapters/final glossary
rg -n "million of stories|eaten himself out|tun of copper|Life of me|Man of Feeling|Royal Academy|Grays Inn|Rambler" chapters/src
```

Classify hits as confirmed defects, glossary-approved earlier forms, or
documented exceptions.

## Fix pattern

- Rebuild social idioms by function: `told a million of stories` -> `讲了无数故事`;
  `eaten himself out of every tavern` -> `把沿途每家酒馆都吃到再赊不下账`.
- Resolve technical object nouns from the immediate material context before
  translating: brewing context makes `tun` an equipment/vessel interface, not a
  weight.
- Check apparent title oddities against author/person context; if source OCR is
  damaged, translate the intended title and record the correction in QA.
- Align recurring work and institution titles with `proper_nouns.csv`, e.g.
  `The Man of Feeling` -> `《感伤人》`, `Royal Academy` -> `皇家艺术院`.

## Recheck

After fixing, rerun note-marker equality, exact residue scans, glossary CSV
parse-width checks, and a full target-only/source-fidelity recheck. The fixed
round is `FIXED_RECHECK_REQUIRED`; only the subsequent zero-issue full-unit
round may PASS.

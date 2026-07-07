# Boswell Unit 527: Index Headword Context Reuse

## Family

Dense index entries can reintroduce mistranslations when a short headword or quotation is translated from the index line alone instead of reusing the full-body context already translated earlier.

密集索引条目若只按索引短行判断，容易把正文中已经定性的短词、引语或讥称重新误译。

## Found In

- Book: `books/zh-Hans/19_约翰生传_詹姆斯_鲍斯威尔`
- Unit: `527_vol06_unit_46`
- Stage: chapter post-translation full check, Round 1

## Concrete Triggers

- Source index line: `'runts, would learn to talk of,' iii. 337;`
  - Risky draft: `“矮牛，也会学着谈论”`
  - Corrected with body context from unit 308: `“小母牛，也会学着谈论”`
- Source index line: `'an auld dominie,' v. 382, n. 2;`
  - Risky draft: `“一位老校长”`
  - Corrected with body context from unit 087: `“一位老学究”`
- Source index line: `Court mourning, at a, iv. 325;`
  - Risky draft: over-explicit clothing/action wording
  - Corrected as an index-compatible context marker: `在一次宫廷服丧场合`

## Low-Token Audit

Before finalizing an index unit, scan the earlier source and final chapters for exact rare headwords or quoted fragments:

```powershell
rg -n "runts|auld dominie|Court mourning" books/zh-Hans/*/chapters/src books/zh-Hans/*/chapters/final
```

For Chinese output, also scan the current translated/final unit for rejected draft renderings:

```powershell
rg -n "矮牛|老校长|宫廷丧服" books/zh-Hans/*/chapters/translated books/zh-Hans/*/chapters/final
```

## Fix Pattern

Treat index quotations and rare nouns as pointers back to body evidence, not as fresh standalone translation tasks. Reuse the established body rendering when the source passage has already defined the sense; keep the index line concise after repair.

索引中的短引语、罕见名词和讥称要先当作“正文回指”，不要当作新的孤立翻译题。正文已有释义或定译时，应复用正文译法，并保持索引条目的短促形态。

## Recheck

A round that repairs these context-reuse misses cannot PASS. Record it as `FIXED_RECHECK_REQUIRED`, then run a fresh full-unit review with:

- line count and blank-line parity;
- raw `ib.`, `n.`, `see` residue scan;
- exact rejected-rendering scan;
- spot checks against the body passages that supplied the final wording.

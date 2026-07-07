# Boswell Unit 102: periodical title collisions and anecdote-phrase drift

## Trigger

Long biographical note sequences often cite several periodicals, excerpt
collections, and retrospective anecdotes close together. Smooth translation can
accidentally collapse distinct titles or turn compact anecdote phrases into
false social facts.

## Defect Family

- Periodical titles with similar Chinese candidates must be checked against the
  glossary before use. `The Tatler` and `The Idler` can otherwise collide as
  the same target title.
- Excerpt collection titles should not be shortened in body text when the
  glossary has locked a fuller reader-facing title, e.g. `The Beauties of Dr.
  Johnson`.
- Compact English phrasing in anecdotes can be causal rather than literal:
  `owes it to me` means `is due to me`, not `owes me a debt`.
- Social-success phrases such as `lucky project`, `sudden shoot of success`,
  and `power of drinking such tea` should be translated as eighteenth-century
  social circumstance, not modern project-management or abstract ability.

## Find

- Compare source title triggers against `glossary/proper_nouns.csv` and
  `glossary/terms.csv`: `Tatler|Idler|Beauties|Rambler|Spectator`.
- Scan translated/final text for title drift: `《闲谈者》|《闲散者》|《名句选》|《约翰生博士名句选》`.
- Scan anecdote-risk phrases in source and target:
  `owes it to me|lucky project|sudden shoot|power of drinking` and
  `欠我的|幸运项目|成功的突然跃升|有能力喝到`.

## Fix

- Use the locked title and, on first useful mention, keep a compact source
  interface if the display policy requires it.
- Restore the full collection title when a generic Chinese short title would
  hide the work identity.
- Translate `owes it to me` as causation or responsibility.
- Rebuild social anecdotes into readable period language: `靠一项侥幸成功的计划致富`,
  `成功的骤然窜升`, and `能喝到这样的茶`.

## Recheck

- Confirm each periodical/excerpt collection is still distinct in Chinese.
- Confirm no target phrase makes a modern or literal claim absent from the
  source.
- If fixes are applied in a chapter control round, mark that round
  `FIXED_RECHECK_REQUIRED` and run a new full-chapter zero-issue PASS round.

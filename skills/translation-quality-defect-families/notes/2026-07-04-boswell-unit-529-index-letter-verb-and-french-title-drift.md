# Boswell Unit 529: Index Letter-Verb and French Title Drift

## 中文

- 发现方式：第529单元整章译后复查，对照书信索引行与 `glossary/proper_nouns.csv`。
- 问题族：索引式短语中，普通动词或称谓容易被孤立字面化；例如书信语境的 `_returns not answers_` 不能译作“退还”，应译为“回信而非作答”。法语称谓 `Mme. de Boufflers` 也不能按临时音译漂移，应遵循术语表“布弗莱尔夫人”。
- 低 token 审计：先用 `rg -n "returns not answers|Boufflers|布夫莱|布弗莱"` 扫 `chapters/translated`、`chapters/final` 和术语表，再只复核命中小上下文。
- 修复规则：索引头词要看其所在语义域，不可只按词典第一义处理；法语/贵族称谓优先用已有 `proper_nouns.csv` 的本书译名。
- 复查规则：任何此类修复轮不能 PASS；必须追加一轮整章零问题复查，并确认旧误译和漂移译名零命中。

## English

- Finding method: Unit 529 post-translation full-chapter review, comparing letter-index lines against `glossary/proper_nouns.csv`.
- Defect family: compact index phrases can literalize a context-specific verb or drift on a titled French name. In a letter-index context, `_returns not answers_` means replying without truly answering, not physically returning a letter. `Mme. de Boufflers` must follow the established book glossary form, not a fresh ad hoc transliteration.
- Low-token audit: scan `chapters/translated`, `chapters/final`, and glossary files with `rg -n "returns not answers|Boufflers|布夫莱|布弗莱"`, then inspect only matched local contexts.
- Fix pattern: resolve index headwords by semantic field first; use `proper_nouns.csv` for French titles and recurring names.
- Recheck: a repair round for this family cannot pass. Add a fresh full-unit zero-issue recheck, and verify zero hits for the rejected rendering and drifted name.

# Boswell Unit 530: Index Page-Number and Greek Motto Interface

## 中文

- 发现方式：第530单元整章译后复查，对照原文索引行、Gutenberg 原文与已完成索引条目。
- 问题族：索引行里孤立数字可能是页码，不一定是 OCR 损坏的脚注；例如 `i. 363, 72; v. 219, n. 3` 中的 `72` 应保留为页码，不应补译成 `注2`。同时，短希腊/拉丁格言即使是索引短语，也不能裸露成 `[Greek: ...]` 这类制作接口；应保留源形并给出简短中文含义。
- 低 token 审计：对索引单元先扫 `\\b[0-9]{1,3}\\.`、`\\b[0-9]{1,3};`、`\\[Greek:`、`\\[Latin:`，再只复核命中行是否为页码、注号或源语接口。
- 修复规则：页码只在原文明示 `n.` 或可靠来源可证为注号时译为 `注`；希腊/拉丁短语用“源形 + 中文含义 + 原文语种说明”的最小接口。
- 复查规则：修复轮不能 PASS；必须追加整章零问题复查，并确认 `注` 计数、页码保留和源语接口均无残留问题。

## English

- Finding method: Unit 530 post-translation full-chapter review against the source index line, the Gutenberg source, and completed index entries.
- Defect family: In index lines, a bare number may be a page number rather than a damaged note marker. For example, `i. 363, 72; v. 219, n. 3` must keep `72` as a page reference, not silently convert it to `n. 2`. Also, short Greek or Latin mottoes should not expose production-style tags such as `[Greek: ...]`; retain the source form with a concise target-language meaning.
- Low-token audit: scan index units for `\\b[0-9]{1,3}\\.`, `\\b[0-9]{1,3};`, `\\[Greek:`, and `\\[Latin:`, then inspect only matched lines.
- Fix pattern: translate as `注` only when the source explicitly has `n.` or reliable source evidence proves a note marker. For Greek/Latin mottoes, use a minimal source-form plus Chinese-meaning interface.
- Recheck: a repair round cannot pass. Add a fresh whole-unit zero-issue recheck and verify note counts, page-number retention, and source-language interfaces.

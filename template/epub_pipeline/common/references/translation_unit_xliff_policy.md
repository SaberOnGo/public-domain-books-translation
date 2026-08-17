# Canonical Translation Units And XLIFF Exchange / 统一翻译单元与 XLIFF 交换政策

## 中文

- `translation_units/units.jsonl` 是正文翻译唯一事实源；`chapters/translated/`、`chapters/final/`、双语 alignment map 和 EPUB 都是投影。
- 翻译前必须锁定 `state/translation_contract.json`。优先采用用户显式选择；用户未选择时使用并显式记录默认策略 `3`，`selection_source=default`。两条路径都必须完成全书发现、逐项裁决和 CSV 锁定。
- 原著自然段不可跨越；短段只在完整句子边界切分。内部句 ID 只用于覆盖审计，不得导致逐句字幕式显示。
- XLIFF 2.1 是可选交换格式，默认构建路径不经过 XLIFF，也不依赖外部 CAT/TMS。
- XLIFF 导入不得修改 source、ID、顺序、哈希或受保护 inline token，只能更新已知单元的 target 和受支持状态。Markdown inline 使用 `<ph>`、`<pc>`、`<originalData>` 映射，导入导出必须通过 schema 和往返 fixture。
- 并行 producer 只写独占章节 patch；唯一 merger 使用 `base_chapter_digest` 做按章 CAS。不同章节从同一全书 base 产生的 patch 可依次合并，同章陈旧 patch 必须失败。
- 结构 PASS 只证明结构；翻译质量 PASS 还必须有当前章节 hash、translation owner 和独立 reviewer 绑定的逐单元语义审计及逐章全量复核。审计按章密封和局部失效；所有当前章节均 PASS 后才生成全书 completion manifest。

## English

- `translation_units/units.jsonl` is the sole source of truth for translated body content. `chapters/translated/`, `chapters/final/`, the bilingual alignment map, and EPUBs are projections.
- `state/translation_contract.json` must be locked before translation. Prefer an explicit user choice; when none is supplied, record policy `3` with `selection_source=default`. Both paths still require book-wide discovery, per-candidate decisions, and a locked CSV.
- Source natural-paragraph boundaries are non-crossable. Short units may split only at complete sentence boundaries. Internal sentence IDs exist for coverage audits and must not cause subtitle-style sentence alternation.
- XLIFF 2.1 is an optional exchange format. The default build path does not pass through XLIFF and does not require an external CAT/TMS.
- XLIFF import must not change source text, IDs, order, hashes, or protected inline tokens. Markdown inline content maps through `<ph>`, `<pc>`, and `<originalData>` and must pass schema and round-trip fixtures.
- Parallel producers write only owned chapter patches. The single merger performs chapter-scoped CAS using `base_chapter_digest`; disjoint patches from one full-book base may merge sequentially, while stale same-chapter patches fail.
- A structural PASS proves structure only. Translation-quality PASS additionally requires per-unit semantic audits and full-chapter reviews bound to the current chapter hash, translation owner, and independent reviewer. Evidence is sealed and invalidated per chapter; the book completion manifest exists only after all current chapters pass.

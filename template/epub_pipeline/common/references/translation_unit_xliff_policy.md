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

## Contextual Source-Form Exclusions / 依语境排除普通描述

CSV 的 `source_aliases` / `target_aliases` 使用分号或竖线分隔别名；完整字符实体（例如 `&#x27;`、`&#39;`、`&amp;`）内部的终止分号不作为分隔符。别名按源文本的实际编码保留，不在匹配前解码，否则精确源位置与哈希会失配。添加转义写法仍须逐处核验实体归属及正文/索引角色，不能仅凭解码后的相似文字自动合并身份。

CSV `source_aliases` / `target_aliases` use semicolons or vertical bars as separators. The terminating semicolon inside a complete character reference such as `&#x27;`, `&#39;`, or `&amp;` is part of the alias. Preserve the actual source encoding rather than decoding before matching, so source offsets and hashes remain exact. Adding an encoded form still requires contextual identity and body/index-role review; decoded text similarity alone does not establish identity.

A registered name's spelling may also occur as an ordinary description. Such a use needs an explicit, reviewed source-span exclusion; it must not be assigned to the named entity solely because the text matches. Configure an optional CSV through `proper_nouns.occurrence_exclusions`, with a book-relative `path` and locked `sha256`. Each row requires `unit_id`, `source_sha256`, `start_offset`, `end_offset`, `source_form`, `rationale`, and `reviewer`. Offsets are zero-based Unicode character positions, with an exclusive end.

已登记专名的词形也可能出现在普通描述中。此时必须逐处记录并审阅原文跨度排除证据，不能仅凭字面命中就归入该实体。可在 `proper_nouns.occurrence_exclusions` 配置 CSV 的书内相对 `path` 和锁定的 `sha256`；每行须包含上述七个字段。位置使用从零开始的 Unicode 字符索引，结束位置不包含在跨度内。

An exclusion must match the exact current source unit, source hash, and registered source-form span, with a substantive rationale and reviewer identity. Missing or changed proof, unknown units, invalid spans, duplicates, and overlapping exclusions fail the gate. Excluded spans do not enter the proper-name occurrence ledger, require no target marker, and do not consume the first body occurrence. They remain ordinary source content that must be translated completely. Blanket substring skips, false heading/body classifications, fabricated generic entities, and source deletion are forbidden. Without configured exclusions, the existing complete registered-form coverage rule still applies.

排除项必须精确绑定当前原文单元、原文 hash 和已登记词形跨度，并提供具体理由与审核者身份。证据缺失或改变、未知单元、无效跨度、重复或重叠排除均须阻断门禁。排除跨度不进入专名出现账本、不要求目标语 marker，也不消耗正文首次出现；它仍是必须完整翻译的普通原文内容。禁止整词批量跳过、把正文伪装成标题、虚构普通描述实体，或删除源文。未配置排除项时，继续执行原有已登记词形全量覆盖规则。

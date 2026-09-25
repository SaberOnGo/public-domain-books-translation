# Bilingual Adjacent-Unit Semantic Shift / 双语相邻单元语义串位

## Symptom and risk / 表现与风险

A target paragraph may start with a sentence that translates the previous source paragraph, even though the EPUB renders each unit with correct IDs, hashes, and source-then-target order. This shifts dialogue, action, clue order, or a referent and can make a reader think the whole bilingual pairing is wrong.

即使 EPUB 的 ID、hash 和英文后接中文顺序完全正确，某个译文段落仍可能以翻译前一段英文的句子开头。它会挪动对话、动作、线索顺序或指代关系，让读者感觉整组双语配对错位。

## Find efficiently / 快速发现

1. Run `npm run check:bilingual` and `npm run check:bilingual:interleave` to rule out stale projections, missing units, hash drift, DOM order errors, and rendered-text substitution.
2. If the optional `audit_bilingual_neighbor_alignment.py` is present in the project, run it on every reader-facing pair, including headings and registered HTML blocks that contain both languages. If it is absent, use the exact-hash embedding-cache neighbor screen documented in `skills/bilingual-parallel-edition-quality/SKILL.md`, or build a boundary-trigger candidate list with deterministic searches. Compare each candidate’s full target block to its mapped, previous, and next source units; state exact embedding coverage and leave uncovered pairs explicitly unverified.
3. Read every ranked candidate with the previous/current/next source-target pairs. Use `rg` on a confirmed English anchor and Chinese phrase to locate same-family occurrences elsewhere in the book; search canonical units and chapter projections, not just the EPUB.

1. 运行两个双语门禁，先排除旧投影、漏单元、hash 漂移、DOM 顺序错误和渲染文本替换。
2. 若项目中存在可选脚本 `audit_bilingual_neighbor_alignment.py`，就对全书每个读者可见配对运行候选排序，包括标题和登记过的双语 HTML 块。若脚本不存在，按 `skills/bilingual-parallel-edition-quality/SKILL.md` 使用精确哈希句向量缓存筛查，或以确定性搜索建立边界候选；把完整译文与当前、前一和后一源单元对照，并报告实际向量覆盖率，未覆盖部分必须明确保留为未核实。
3. 连同前后英中配对逐条阅读候选。确认某项后，用 `rg` 搜索原文锚点和中文短语，审计全书同类；检索 canonical units 与章节投影，不要只搜 EPUB。

Embedding scores are triage only. Adjacent paragraphs in the same scene often share meaning; a short first sentence may also be hard to distinguish automatically. Confirm with source context before editing, and record false positives and unresolved cases.

句向量分数只用于排序。相邻段落常处于同一场景，短句也难由模型区分；编辑前必须对照原文上下文确认，并记录假阳性与未决项。

## Fix and recheck / 修复与复查

Repair the canonical target sentence in its proper unit; do not move text by editing the reader map or generated XHTML. Keep the triggering review round failed, recheck the entire affected chapter after repair, regenerate both EPUBs, and rerun structural plus semantic-alignment review. If the issue came from a post-EPUB random sample, close the book-wide family audit and take a new-seed sample.

在正确的 canonical unit 中修复译文；不要通过改 reader map 或生成后的 XHTML 来挪文字。触发问题的评审轮次保持 FAIL，修后整章复查，重建两版 EPUB，并重跑结构门禁和语义对齐复核。若问题来自 EPUB 后随机抽检，还要闭合全书问题族审计并用新 seed 复抽。

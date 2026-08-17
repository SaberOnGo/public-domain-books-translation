# Adaptive Parallel Translation Orchestration / 自适应并行翻译编排

## 1. Purpose / 目的

LifeBook uses a quality-first producer-consumer design for long books. Parallelism may shorten elapsed time, but it must not bypass pre-translation research, the locked proper-noun and terminology registers, chapter ownership, semantic audit, or release gates.

LifeBook 对长书采用“质量优先”的生产者—消费者架构。并行可以缩短日历时间，但不得绕过译前研究、已锁定专名/术语表、章节所有权、语义审计或发布门禁。

The policy is global and language-neutral. It applies equally to French-to-English, Japanese-to-Spanish, Chinese-to-English, English-to-Spanish, German-to-Traditional-Chinese, and Arabic-to-Indonesian projects.

本规则是全球化、语言方向无关的规则，同样适用于法语到英语、日语到西班牙语、中文到英语、英语到西班牙语、德语到繁体中文、阿拉伯语到印尼语等项目。

## 2. Scheme B roles / 方案 B 角色

- The coordinator is the only merger and the only writer of the canonical store. It locks global policy, issues context capsules, merges chapter patches serially, materializes editions, and controls release.
- Translation producers own disjoint chapters. A chapter has exactly one translation owner at a time. Adjacent chapters should remain with the same producer when workload balance permits.
- Audit consumers independently compare complete source and target units and complete chapters. A reviewer identity must differ from every translation owner recorded for that chapter.
- The target-only and bilingual editions share one canonical target. They are two projections, not two translation jobs.

- coordinator 是唯一合并者，也是 canonical store 的唯一写入者；负责锁定全局规则、发放上下文 capsule、串行合并章节 patch、物化版本和控制发布。
- translation producer 只拥有互不重叠的章节；同一时刻每章只能有一个翻译 owner。在工作量允许时，相邻章节应交给同一 producer。
- audit consumer 独立执行完整 source-target 单元和完整章节复核；reviewer 身份不得与该章任何 translation owner 相同。
- 单目标语版和双语版共用同一 canonical target；它们是两个投影，不是两次翻译。

## 3. Capability declaration and hard caps / 能力声明与硬上限

The common core does not guess the active client, launch workers by itself, or hard-code a vendor model. The active client adapter must write `state/orchestration_capabilities.json` from live, verified capabilities and user authorization. Unknown, missing, stale, unsupported, or unauthorized capability means zero spawned workers.

通用核心不猜测当前客户端，不自行启动 worker，也不写死厂商模型。活动客户端适配器必须根据实时验证的能力和用户授权写入 `state/orchestration_capabilities.json`。能力未知、缺失、陈旧、不支持或未经用户授权时，派生 worker 数一律为 0。

Required fields are provider family, parallel-worker support, advertised maximum, user maximum, rate-limit maximum, budget maximum, quality maximum, user authorization, UTC `verified_at` and `valid_until`, and an optional client-local worker profile. The planner rejects missing, malformed, future-dated, or expired verification evidence. The effective maximum is the minimum of all applicable limits and the workload limit.

必填信息包括 provider family、是否支持并行 worker、客户端上限、用户上限、速率上限、预算上限、质量上限、用户授权、UTC `verified_at` 与 `valid_until`，以及可选的客户端本地 worker profile。缺失、格式错误、来自未来或已过期的验证证据必须被规划器拒绝。有效上限取所有适用上限和书籍工作量上限的最小值。

- GPT-family clients: at most 4 spawned workers.
- Non-GPT clients: at most 8 spawned workers.
- The coordinator is not counted as a spawned worker.
- A user prohibition always wins and produces 0 workers.

- GPT 家族客户端：最多派生 4 个 worker。
- 非 GPT 客户端：最多派生 8 个 worker。
- coordinator 不计入派生 worker 数。
- 用户禁止子代理时，任何其他检测结果都必须让位，结果为 0。

The active AI executes this finite static plan with the host's verified capabilities; LifeBook does not implement a runtime task queue or worker launcher. Model-selection precedence, including the GPT-family `SHOULD` default and user override, is defined in `ai_parallel_execution_guidance.md`. The actual coordinator/worker models, reasoning levels, and any justified deviation must remain in run evidence.

活动 AI 使用宿主已验证的能力执行这份有限静态计划；LifeBook 不实现运行时任务队列或 worker 启动器。模型选择优先级（包括 GPT 系列的 `SHOULD` 默认规则和用户覆盖规则）见 `ai_parallel_execution_guidance.md`。实际 coordinator/worker 模型、推理等级及任何有理由的偏离必须保留在执行证据中。

## 4. Workload model / 工作量模型

Page count is only a fallback signal because PDF pages vary by trim size, font, images, OCR quality, and layout. The planner prefers canonical source units and computes a weighted workload from source length, chapter count, named-entity density, notes, tables, figures, formulas/code, and structural unit type. `metrics:evaluate` records an aggregate estimate; after canonical units exist, `translation:orchestration:plan` uses their chapter-level weights.

页数只能作为后备信号，因为 PDF 页面会受开本、字体、图片、OCR 质量和排版影响。规划器优先使用 canonical source units，并综合原文规模、章节数、专名密度、注释、表格、图片、公式/代码和结构单元类型计算加权工作量。`metrics:evaluate` 记录聚合估计；canonical units 建立后，`translation:orchestration:plan` 使用逐章权重。

Books below the parallel threshold remain coordinator-only. Larger books receive a workload cap from 2 upward; GPT plans stop at 4 and non-GPT plans stop at 8. This is a ceiling, not a promise to fill every slot.

低于并行阈值的书只由 coordinator 执行。更大的书从 2 个 worker 起获得书籍工作量上限；GPT 最高 4，非 GPT 最高 8。该数字是上限，不是必须占满的配额。

## 5. Pilot, scale-up, and scale-down / 试运行、扩容与降容

The first representative pilot uses no more than two spawned workers. Scaling up requires all of the following on current evidence: zero structural violations, zero proper-noun policy violations, first-pass semantic rate at least 90%, rework rate at most 10%, and patch-conflict rate at most 1%.

首轮代表性试运行最多使用两个派生 worker。只有当前证据同时满足以下条件才可扩容：结构违规为 0、专名策略违规为 0、语义首过率至少 90%、返工率不超过 10%、patch 冲突率不超过 1%。

Rate limiting, repeated conflicts, terminology/name drift, incomplete translations, semantic omissions/additions, or excessive rework immediately reduce concurrency. More workers are never the response to a failing quality signal.

出现限流、重复冲突、术语/专名漂移、少译、漏译、增译或过高返工率时必须立即降低并发。质量信号失败时不得用“增加 worker”作为解决办法。

## 6. Context and ownership / 上下文与所有权

Each producer receives a compact immutable context capsule: contract hash, proper-noun revision, occurrence-ledger revision, terminology revision, chapter ID, neighboring chapter summaries, style constraints, and patch base chapter digest. Full preceding chapters need not be copied into every prompt; cross-chapter continuity is preserved by adjacent-chapter affinity, locked global resources, and short boundary summaries.

每个 producer 获得一份紧凑且不可变的上下文 capsule：合同 hash、专名 revision、出现账本 revision、术语 revision、chapter ID、相邻章节摘要、文体约束和 patch 的 base chapter digest。无需把所有前文章节复制进每个 prompt；跨章连续性由相邻章节归属、锁定的全局资源和简短边界摘要共同维持。

Workers write only their owned patch or immutable audit evidence. They never edit `translation_units/units.jsonl`, `chapters/translated`, `chapters/final`, global glossaries, contracts, or another worker's evidence.

worker 只能写自己拥有的 patch 或不可变审计证据；不得编辑 `translation_units/units.jsonl`、`chapters/translated`、`chapters/final`、全局 glossary、合同或其他 worker 的证据。

## 7. Validation and completion / 验收与完成

Disjoint chapter patches from one base manifest may merge sequentially because CAS binds the current chapter digest. Same-chapter stale patches still fail. Semantic evidence is sealed per chapter; an unrelated chapter merge does not invalidate it, while any change to that chapter's source, target, translation owner, or locked revisions does. The book completes only when all current chapters have sealed independent PASS evidence and `book_completion_manifest.json` is generated.

同一 base manifest 产生的不同章节 patch 可以依次合并，因为 CAS 绑定当前章节 digest；同章陈旧 patch 仍必须失败。语义证据按章密封；无关章节合并不会使其失效，但本章 source、target、translation owner 或锁定 revision 的任何变化都会使其失效。只有所有当前章节都有独立密封的 PASS 证据并生成 `book_completion_manifest.json`，全书才算完成。

Structural PASS, EPUBCheck, or a fluent-looking sample never substitutes for complete semantic review. Real-reader smoke testing remains a final-candidate, non-blocking-if-unavailable boundary as defined by the quality policy.

结构 PASS、EPUBCheck 或看起来流畅的抽样都不能替代完整语义复核。真实阅读器 smoke test 仍只用于最终候选；阅读器不可用时不阻塞发布，但必须按质量政策披露该边界。

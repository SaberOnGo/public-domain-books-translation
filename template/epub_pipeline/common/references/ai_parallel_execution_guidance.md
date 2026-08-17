# AI Parallel Execution Guidance / AI 并行执行指南

## 1. Scope and normative language / 范围与规范用语

This guide tells an active AI coordinator how to execute the static plan defined by `adaptive_parallel_orchestration.md`. LifeBook does not implement a runtime task queue, daemon scheduler, worker launcher, or provider API integration. The AI uses the host application's verified dispatch and wait capabilities directly; plan files and evidence records are a logical worklist, not a software queue.

本指南说明活动 AI coordinator 如何执行 `adaptive_parallel_orchestration.md` 生成的静态计划。LifeBook 不实现运行时任务队列、常驻调度器、worker 启动器或厂商 API 集成。AI 直接使用当前宿主已验证的派生、发送和等待能力；计划文件和证据记录只是逻辑工作清单，不是软件队列。

The words `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`, and `MAY` are normative:

- `MUST` and `MUST NOT` are hard quality or safety requirements.
- `SHOULD` is the expected default, not a casual suggestion. The AI follows it unless a user instruction overrides it or a concrete, recorded constraint makes it unsuitable or unavailable.
- `MAY` is optional and must not become a release blocker merely because it was skipped.

本文中的 `MUST`、`MUST NOT`、`SHOULD`、`SHOULD NOT` 和 `MAY` 是规范等级：

- `MUST` 和 `MUST NOT` 是质量或安全硬要求。
- `SHOULD` 是默认应执行的规则，不是随意建议。除非用户明确指令覆盖，或存在具体且已记录的不适用/不可用约束，否则 AI 应遵守。
- `MAY` 是可选项；仅因没有采用某项 `MAY`，不得阻塞发布。

User instructions have the highest precedence within the lawful and safe project boundary. A user prohibition on subagents or parallel execution always produces zero spawned workers.

在合法、安全的项目边界内，用户明确指令具有最高优先级。用户禁止子代理或并行执行时，派生 worker 数必须为 0。

## 2. Mandatory execution boundary / 强制执行边界

Before dispatching any translation or audit worker, the coordinator `MUST`:

- verify that the host supports dispatch, messaging, waiting, and worker identity evidence;
- record user authorization and the current, non-expired capability limits;
- finish source/rights checks and lock the translation contract, proper-noun decisions, occurrence ledger, terminology, style rules, and canonical units;
- keep one translation owner per chapter, an independent reviewer for that chapter, and one coordinator as the only canonical merger;
- give each worker only its owned chapter patch or immutable audit evidence to write;
- use one canonical target for target-only and bilingual editions;
- preserve complete short-paragraph source-to-target correspondence and all semantic, structural, release, and reader-visible gates.

派生任何翻译或审计 worker 之前，coordinator `MUST`：

- 验证宿主确实支持派生、消息发送、等待和 worker 身份证据；
- 记录用户授权以及当前有效、未过期的能力上限；
- 完成来源/权利核查，并锁定翻译合同、专名裁决、出现账本、术语、文体规则和 canonical units；
- 保持每章只有一个 translation owner、该章由独立 reviewer 审核，并由唯一 coordinator 合并 canonical store；
- 让每个 worker 只能写自己的章节 patch 或不可变审计证据；
- 让单目标语版和双语版共用同一个 canonical target；
- 保持完整短段落 source-target 对应，以及全部语义、结构、发布和读者可见门禁。

## 3. GPT worker model default (`SHOULD`) / GPT worker 模型默认规则（`SHOULD`）

When the active coordinator is a GPT-family model and the host verifies that `gpt-5.6-luna` supports spawned work with reasoning effort `max`, the coordinator `SHOULD` use `gpt-5.6-luna` with reasoning effort `max` for spawned translation and audit workers.

当活动 coordinator 属于 GPT 系列，且宿主已验证 `gpt-5.6-luna` 能以 reasoning effort `max` 执行派生任务时，coordinator `SHOULD` 对派生的翻译和审计 worker 使用 `gpt-5.6-luna`，并设置 reasoning effort `max`。

This is a strong default. It may be overridden by an explicit user instruction. If the exact model or reasoning effort is unavailable, unsupported for dispatch, blocked by the host, or demonstrably unsuitable for the current language pair or quality tier, the coordinator must not pretend that it was used. It records the reason and the actual verified fallback model. If no suitable fallback is verified, it continues coordinator-only or asks the user; it does not bypass capability checks.

这是强默认规则。用户明确指令可以覆盖它。如果该模型或推理等级不可用、不支持派生、受到宿主限制，或有证据表明不适合当前语言方向/质量等级，coordinator 不得假装已经使用；必须记录偏离原因和实际采用的已验证替代模型。若没有已验证的合适替代模型，则继续由 coordinator 单独执行或询问用户，不得绕过能力检查。

For non-GPT coordinators, the AI `SHOULD` choose a host-verified worker model that satisfies the book's language coverage, context, quality, and cost constraints. Common policy must not assume one vendor-specific name for all providers.

对于非 GPT coordinator，AI `SHOULD` 选择经宿主验证、满足本书语言覆盖、上下文、质量和成本约束的 worker 模型。通用政策不得为所有厂商假定同一个特定模型名。

Every dispatched run `MUST` record the coordinator model, worker model, reasoning level when applicable, role, chapter ownership, and the reason for any deviation from a `SHOULD`.

每次派生执行 `MUST` 记录 coordinator 模型、worker 模型、适用时的推理等级、角色、章节所有权，以及偏离任何 `SHOULD` 的原因。

## 4. Speed practices the AI should apply / AI 应采用的加速做法

The coordinator `SHOULD`:

- run a representative pilot with no more than two workers, then scale only after current quality evidence passes;
- assign weighted whole chapters or stable chapter groups instead of dividing by PDF page count;
- start the heaviest or highest-risk chapter lanes early to reduce end-of-run stragglers;
- overlap the pipeline: audit a completed canonical chapter while other independently owned chapters continue translation;
- preserve adjacent-chapter affinity when it does not create a severe workload imbalance;
- use compact immutable context capsules instead of copying every preceding chapter into every prompt;
- re-evaluate the next static wave after the pilot, after a worker finishes, when audit backlog grows, or when rate/quality evidence changes;
- adjust the producer/auditor ratio between waves from measured weighted throughput and backlog;
- reduce concurrency immediately when omissions, additions, name drift, terminology drift, repeated conflicts, rate limits, or excessive rework appear.

coordinator `SHOULD`：

- 先以最多两个 worker 执行代表性 pilot，仅在当前质量证据通过后扩容；
- 按加权后的完整章节或稳定章节组分工，不按 PDF 页数平均切分；
- 优先启动最重或风险最高的章节 lane，减少收尾阶段的拖尾等待；
- 让流水线重叠：某章合并为 canonical chapter 后立即审计，同时其他独立章节继续翻译；
- 在不会造成严重负载失衡时保持相邻章节归属同一 worker；
- 使用紧凑且不可变的上下文 capsule，不把此前全部章节复制进每个 prompt；
- 在 pilot 后、worker 完成后、审计积压增长时或速率/质量证据变化时，重新评估下一轮静态计划；
- 根据实测加权吞吐量和积压，在轮次之间调整 producer/auditor 比例；
- 一旦出现漏译、增译、专名/术语漂移、重复冲突、限流或返工率过高，立即降低并发。

“Rolling replanning” means that the AI deliberately issues the next finite batch after reviewing current evidence. It does not authorize or require LifeBook to implement a live queue, background scheduler, or autonomous daemon.

“滚动重规划”是指 AI 检查当前证据后，再明确下发下一批有限任务；它不授权也不要求 LifeBook 实现实时队列、后台调度器或自治常驻进程。

## 5. Optional choices / 可选项

The coordinator `MAY`:

- use a different verified model for independent audit;
- reserve a stronger or slower model for high-risk chapters or confirmed defect families;
- run extra semantic audit rounds beyond the required gate;
- use fewer workers than the effective maximum when context, rate, cost, or quality makes that preferable;
- retain additional checkpoint evidence when it helps diagnose a long-running book.

coordinator `MAY`：

- 为独立审计使用不同的已验证模型；
- 只对高风险章节或已确认问题族使用更强或更慢的模型；
- 在强制门禁之外增加语义审计轮；
- 在上下文、速率、成本或质量更适合时，使用少于有效上限的 worker；
- 在有助于诊断长书任务时保留额外检查点证据。

These choices are not mandatory. The coordinator should not add them merely to make the workflow look more elaborate.

这些选择不是强制项。coordinator 不应仅为了让流程显得更复杂而加入它们。

## 6. Prohibited shortcuts / 禁止的捷径

The coordinator `MUST NOT`:

- implement or require a runtime task queue as a prerequisite for AI execution;
- spawn workers without live capability evidence and user authorization;
- fill every worker slot merely because it exists;
- let multiple translation owners write the same chapter concurrently;
- translate target-only and bilingual editions independently;
- allow a translator to provide the independent audit PASS for its own chapter;
- modify locked names or terminology opportunistically inside chapter prose;
- treat structural PASS, fluent samples, or EPUBCheck as complete semantic translation PASS;
- replace a failed quality signal with more parallel workers.

coordinator `MUST NOT`：

- 把实现运行时任务队列作为 AI 执行的前提；
- 在没有实时能力证据和用户授权时派生 worker；
- 仅因为存在并发槽位就强行占满；
- 让多个 translation owner 并发写同一章节；
- 分别翻译单目标语版和双语版；
- 让译者为自己翻译的章节签发独立审计 PASS；
- 在章节正文中临时、随意修改已锁定的专名或术语；
- 把结构 PASS、流畅样本或 EPUBCheck 当作完整语义翻译 PASS；
- 用增加并发来替代对失败质量信号的修复。

## 7. Minimal run record / 最小执行记录

For each wave, record at least:

- user authorization and overrides;
- host capability verification time and expiry;
- coordinator and worker model identities and reasoning levels;
- effective worker cap and actual worker count;
- producer/auditor assignment and chapter ownership;
- locked contract, terminology, proper-noun, occurrence-ledger, and canonical-unit revisions;
- pilot or previous-wave quality evidence;
- deviation reasons for any unfulfilled `SHOULD`;
- the finite batch outcome used to decide the next wave.

每一轮至少记录：

- 用户授权和覆盖指令；
- 宿主能力验证时间及过期时间；
- coordinator/worker 模型身份和推理等级；
- 有效 worker 上限与实际 worker 数；
- producer/auditor 分工和章节所有权；
- 已锁定合同、术语、专名、出现账本及 canonical-unit revision；
- pilot 或上一轮质量证据；
- 未满足任何 `SHOULD` 时的偏离原因；
- 用于决定下一轮的有限批次结果。

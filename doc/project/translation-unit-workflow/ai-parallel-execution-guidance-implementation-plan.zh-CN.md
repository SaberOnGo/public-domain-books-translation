# AI Parallel Execution Guidance Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add provider-neutral instructions that tell AI executors how to apply LifeBook's static parallel plan without implementing a runtime task queue, including a user-overridable GPT `gpt-5.6-luna` plus `max` SHOULD rule.

**Architecture:** Keep the existing static planner and canonical translation pipeline unchanged. Add one human-facing bilingual execution guide, reference it from the repository and EPUB-pipeline agent entry points, and replace the Codex-specific paragraph in the orchestration policy with the generic precedence rule. A focused repository test prevents the guide, references, SHOULD semantics, and no-runtime-queue boundary from drifting.

**Tech Stack:** Markdown policy documents, Python `unittest`, repository local-path gate.

## Global Constraints

- Do not implement a runtime task queue, scheduler, worker launcher, or provider API integration.
- Keep LifeBook provider-neutral; product-specific adapters may live outside the common workflow.
- For a GPT-family coordinator, `gpt-5.6-luna` with reasoning effort `max` is a `SHOULD`, not a `MUST` or `MAY`.
- The user instruction overrides the model SHOULD; verified unavailability, host restrictions, or a recorded quality/cost reason may also justify deviation.
- Quality invariants, locks, canonical ownership, independent audit, CAS merge, and release gates remain mandatory.
- Nonessential acceleration choices remain `SHOULD` or `MAY`; do not turn them into release blockers.
- Do not dispatch subagents while implementing this documentation-only change.

---

### Task 1: Add a documentation contract test

**Files:**
- Modify: `tests/test_language_pair_template_names.py`
- Test: `tests/test_language_pair_template_names.py`

**Interfaces:**
- Consumes: repository paths rooted at `REPO_ROOT` and `TEMPLATE_ROOT`.
- Produces: `test_ai_parallel_execution_guidance_is_referenced_and_provider_neutral`, which validates guide existence, entry-point references, normative model wording, override semantics, and the runtime-queue prohibition.

- [x] **Step 1: Write the failing test**

Add a test that reads `AGENTS.md`, both pipeline README files, `adaptive_parallel_orchestration.md`, and the new `ai_parallel_execution_guidance.md`. Assert the guide is referenced by all entry points, contains `gpt-5.6-luna`, `max`, `SHOULD`, and user-override wording, says that no runtime queue is implemented, and contains no Codex-only `luna_worker` profile.

- [x] **Step 2: Run the focused test to verify it fails**

Run: `python tests/test_language_pair_template_names.py LanguagePairTemplateNameTests.test_ai_parallel_execution_guidance_is_referenced_and_provider_neutral -v`

Expected: `FAIL` because the guide and references do not yet exist.

- [x] **Step 3: Commit with Task 2 after the test passes**

This test and its documentation implementation form one reviewable policy change and are committed together after Task 2.

### Task 2: Write and link the generic AI execution guide

**Files:**
- Create: `template/epub_pipeline/common/references/ai_parallel_execution_guidance.md`
- Modify: `AGENTS.md`
- Modify: `template/epub_pipeline/README.md`
- Modify: `template/epub_pipeline/common/README.md`
- Modify: `template/epub_pipeline/common/references/adaptive_parallel_orchestration.md`
- Test: `tests/test_language_pair_template_names.py`

**Interfaces:**
- Consumes: the static plan and quality invariants defined by `adaptive_parallel_orchestration.md`.
- Produces: a provider-neutral AI execution contract organized into `MUST`, `SHOULD`, `MAY`, and `MUST NOT` sections.

- [x] **Step 1: Add the minimal guide and references**

Write bilingual guidance that:

- separates planning from execution and states that LifeBook does not implement a runtime queue;
- requires the active AI to verify user authorization and host capabilities before dispatch;
- makes `gpt-5.6-luna` plus `max` the GPT-family default SHOULD;
- defines the allowed reasons to deviate and requires recording the actual model and reason;
- recommends pilot-first scaling, weighted chapter allocation, translation/audit overlap, rolling replanning by the AI, adjacent-chapter affinity, and scaling down on defects;
- leaves optional model diversity, stronger models for difficult chapters, and additional audit rounds as MAY choices;
- preserves mandatory canonical-store, ownership, audit, CAS, terminology, proper-noun, semantic, bilingual, and release boundaries.

Reference the guide from `AGENTS.md`, the pipeline README, and the common README. Replace the Codex-specific paragraph in the orchestration policy with a generic pointer and precedence rule.

- [x] **Step 2: Run the focused test to verify it passes**

Run: `python tests/test_language_pair_template_names.py LanguagePairTemplateNameTests.test_ai_parallel_execution_guidance_is_referenced_and_provider_neutral -v`

Expected: `PASS`.

- [x] **Step 3: Run the surrounding test module**

Run: `python tests/test_language_pair_template_names.py -v`

Expected: all tests pass.

- [x] **Step 4: Run reusable-template path validation**

Run: `npm --prefix books run check:local-paths`

Expected: exit code `0` with no local absolute-path leak.

- [x] **Step 5: Review the diff and commit**

Run: `git diff --check` and inspect `git diff -- AGENTS.md template/epub_pipeline tests docs/superpowers/plans`.

Commit with a concise title and separated multiline `ZH:`, `EN:`, and `JA:` body sections, as required by `AGENTS.md`.

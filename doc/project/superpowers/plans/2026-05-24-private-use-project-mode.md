# Private Use Project Mode Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a separate private-use workflow where publishable scripts and templates can be tracked, while non-public-domain book source, translation, QA, and EPUB output under `books/private/` stay out of GitHub.

**Architecture:** Keep the existing public-domain workflow unchanged by default. Add an explicit `private_use` publication mode that creates projects under `books/private/{target}/{number}_{slug}`, records local-source evidence and the user declaration, and lets the workflow gate accept private paths only when `state/pipeline_state.json.publication_mode` is `private_use`.

**Tech Stack:** Python scripts, unittest regression tests, Markdown template policy files, `.gitignore`.

---

### Task 1: Private Project Creation

**Files:**
- Modify: `books/scripts/create_book_project.py`
- Test: `tests/test_private_use_mode.py`

- [ ] Add a failing unittest that runs `create_book_project.py --mode private-use --local-source-file <file> --private-use-declaration <text>` in a temporary repo and expects `books/private/{target}/{number}_{slug}`.
- [ ] Implement parser options for `--mode public-domain|private-use`, `--local-source-file`, and `--private-use-declaration`.
- [ ] Make public mode keep the existing `books/{target}/{number}_{slug}` path.
- [ ] Make private mode create `books/private/{target}/{number}_{slug}` and update copied state with `publication_mode`, `private_use`, and local-source metadata.

### Task 2: Private Workflow Gate

**Files:**
- Modify: `template/epub_pipeline/common/scripts/check_template_workflow_gate.py`
- Test: `tests/test_private_use_mode.py`

- [ ] Add a failing unittest that builds a temporary private book project with `publication_mode=private_use` and expects the workflow gate to pass.
- [ ] Update the gate so normal books must remain under `books/{target}/{number}_{slug}`.
- [ ] Update the gate so private books may live under `books/private/{target}/{number}_{slug}` only when `publication_mode` is `private_use`.

### Task 3: Policy And Documentation

**Files:**
- Modify: `.gitignore`
- Modify: `AGENTS.md`
- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Modify: `template/epub_pipeline/README.md`
- Modify: `template/epub_pipeline/common/PIPELINE_SPEC.md`
- Modify: `template/epub_pipeline/common/metadata/rights_checklist.md`
- Modify: `template/epub_pipeline/common/metadata/source_evidence.md`
- Add: `template/epub_pipeline/common/metadata/private_use_declaration.md`
- Modify: `template/epub_pipeline/common/references/book_info_frontmatter_policy.md`
- Modify: `template/epub_pipeline/common/references/quality_gate_framework.md`

- [ ] Ignore `books/private/` so private source, translation, QA, and EPUB output do not go to GitHub.
- [ ] Document that scripts/templates/config are publishable but non-public-domain book projects must live under ignored private paths.
- [ ] Split public-domain, licensed, and private-use rights decisions.
- [ ] State that a user prompt saying "do not care about copyright" does not remove the boundary; it only selects private-use mode when a local source file is provided.

### Task 4: Verification

**Files:**
- Test: `tests/test_private_use_mode.py`

- [ ] Run `python -m unittest tests.test_private_use_mode`.
- [ ] Run focused syntax checks for the changed Python scripts.
- [ ] Check `git diff --check`.

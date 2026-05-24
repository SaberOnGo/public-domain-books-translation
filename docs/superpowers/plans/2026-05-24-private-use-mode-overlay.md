# Private-Use Mode Overlay Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Separate non-public-domain personal-use book production from public-domain publication by adding a `private_use` template mode overlay with dedicated policies, scripts, and hard gates.

**Architecture:** Keep `template/epub_pipeline/common/` as the shared EPUB infrastructure layer. Add `template/epub_pipeline/modes/private_use/` as a mode overlay copied only by `books/scripts/create_book_project.py --mode private-use`, after common, language-pair, and profile overlays. Public projects must not receive private-use scripts or policies; private projects must receive them and use private artifact terminology rather than public release terminology.

**Tech Stack:** Python standard library, Node.js package scripts, Markdown template documents, `unittest`.

---

### Task 1: Lock Overlay Behavior With Tests

**Files:**
- Modify: `tests/test_private_use_mode.py`

- [ ] Add a test proving `--mode private-use` copies `template/epub_pipeline/modes/private_use/` files into the private project.
- [ ] Assert the private project has private scripts, private references, private preproduction spec, and package scripts such as `private:artifact:create`.
- [ ] Assert a public project created without `--mode private-use` does not contain private-use overlay files.
- [ ] Add gate tests proving private projects without the overlay fail, and public projects contaminated with private overlay files fail.

### Task 2: Add Private-Use Mode Overlay

**Files:**
- Create: `template/epub_pipeline/modes/private_use/README.md`
- Create: `template/epub_pipeline/modes/private_use/package.json`
- Create: `template/epub_pipeline/modes/private_use/preproduction/stage1/_TEMPLATE.private_use_production_spec.md`
- Create: `template/epub_pipeline/modes/private_use/references/private_use_cover_policy.md`
- Create: `template/epub_pipeline/modes/private_use/references/private_use_frontmatter_policy.md`
- Create: `template/epub_pipeline/modes/private_use/references/private_use_artifact_policy.md`
- Create: `template/epub_pipeline/modes/private_use/scripts/check_private_use_gate.py`
- Create: `template/epub_pipeline/modes/private_use/scripts/check_private_reader_facing_policy.py`
- Create: `template/epub_pipeline/modes/private_use/scripts/create_private_artifact.py`

- [ ] Define private-use cover text: title, author, and bottom line `个人学习版`; do not require the long no-redistribution sentence on the cover.
- [ ] Define private-use frontmatter: no public-domain notice, no public license, no public release language, producer wording `参考LifeBook书坊 个人自制`.
- [ ] Define rights wording: `仅供个人自用，不传播，不商业使用` plus personal risk responsibility and LifeBook Shufang system-provider limitation.
- [ ] Provide private scripts that reject public wording and create private versioned artifacts under `output/private_artifacts/`.

### Task 3: Wire Overlay Into Project Creation And Gates

**Files:**
- Modify: `books/scripts/create_book_project.py`
- Modify: `template/epub_pipeline/common/scripts/check_template_workflow_gate.py`

- [ ] In private-use mode, copy common, language-pair, profiles, then `modes/private_use`.
- [ ] Reject missing private mode overlay at creation time.
- [ ] In the workflow gate, reject public projects that contain private-use overlay files.
- [ ] In the workflow gate, require private-use projects to contain the private-use policy and script files.
- [ ] Require private-use production specs to cite `template/epub_pipeline/modes/private_use/preproduction/stage1/_TEMPLATE.private_use_production_spec.md`.

### Task 4: Update Docs And Prompts

**Files:**
- Modify: `AGENTS.md`
- Modify: `README.md`
- Modify: `README.zh-CN.md`
- Modify: `template/epub_pipeline/README.md`
- Modify: `template/epub_pipeline/common/README.md`
- Modify: `template/epub_pipeline/common/PIPELINE_SPEC.md`
- Modify: `template/epub_pipeline/common/metadata/private_use_declaration.md`
- Modify: `doc/public/user_prompt/book_translation_private_existing_template.md`
- Modify: `doc/public/user_prompt/book_translation_private_new_template.md`
- Modify: `doc/public/user_prompt/book_translation_existing_template.md`
- Modify: `doc/public/user_prompt/book_translation_new_template.md`

- [ ] Public prompts should remain public-domain/licensed first and mention private-use only as a mode branch.
- [ ] Private prompts must instruct agents to read `template/epub_pipeline/modes/private_use/` and use private commands.
- [ ] Replace private-use `npm run release:create` wording with `npm run private:artifact:create` or explicit private artifact terminology.

### Task 5: Verify

**Commands:**
- `python -m unittest tests.test_private_use_mode`
- `python -m py_compile books/scripts/create_book_project.py template/epub_pipeline/common/scripts/check_template_workflow_gate.py template/epub_pipeline/modes/private_use/scripts/check_private_use_gate.py template/epub_pipeline/modes/private_use/scripts/check_private_reader_facing_policy.py template/epub_pipeline/modes/private_use/scripts/create_private_artifact.py tests/test_private_use_mode.py`
- `git diff --check`
- `rg -n "private:artifact:create|template/epub_pipeline/modes/private_use|参考LifeBook书坊 个人自制|个人学习版" AGENTS.md README.md README.zh-CN.md doc/public template/epub_pipeline books/scripts/create_book_project.py tests/test_private_use_mode.py`

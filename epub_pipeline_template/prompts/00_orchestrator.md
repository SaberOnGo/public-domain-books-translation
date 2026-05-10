# Orchestrator Prompt (Autonomous)
Inputs:
- TEMPLATE_ROOT={{TEMPLATE_ROOT}}
- SOURCE_URL={{SOURCE_URL}}

Read and obey:
1. PIPELINE_SPEC.md
2. README.md
3. metadata/rights_checklist.md

Rules:
- Execute end-to-end without asking user for file/folder decisions.
- Update state/pipeline_state.json and append state/run.log after each step.
- On failure set status=FAILED and write last_error.

Deliverables:
- output/book.epub
- output/epubcheck.log
- state/pipeline_state.json status DONE

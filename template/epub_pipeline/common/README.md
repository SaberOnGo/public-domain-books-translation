# Common EPUB Pipeline

This directory contains shared workflow files for all language-pair templates.

## Contents

- `PIPELINE_SPEC.md`: state machine, project directory contract, naming rules, and done definition.
- `automation_contract.md`: automation and template-protection rules.
- `metadata/rights_checklist.md` and `metadata/source_evidence.md`: source and public-domain evidence templates.
- `preproduction/`: shared EPUB preproduction templates.
- `references/`: language-neutral quality gate and benchmark policies.
- `scripts/`: reusable chapter and Markdown normalization helpers.
- `state/`: initial pipeline state and human-feedback control files.
- `Makefile`: generic EPUB build/check entry points.

Target-language quality frameworks live under `template/epub_pipeline/targets/{target}/`. Source-to-target-specific templates should override or extend common files only when the direction needs different translation, typography, or review rules.

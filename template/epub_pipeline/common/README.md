# Common EPUB Pipeline

This directory contains shared workflow files for all language-pair templates.

## Contents

- `PIPELINE_SPEC.md`: state machine, project directory contract, naming rules, and done definition.
- `automation_contract.md`: automation and template-protection rules.
- `metadata/rights_checklist.md` and `metadata/source_evidence.md`: source and public-domain evidence templates.
- `preproduction/`: shared EPUB preproduction templates.
- `scripts/`: reusable chapter and Markdown normalization helpers.
- `state/`: initial pipeline state and human-feedback control files.
- `Makefile`: generic EPUB build/check entry points.

Language-specific templates should override or extend these files only when the target language needs different translation, typography, or review rules.

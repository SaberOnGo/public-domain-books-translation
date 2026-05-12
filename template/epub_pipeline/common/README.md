# Common EPUB Pipeline

This directory contains shared workflow files for all language-pair templates.

## Contents

- `PIPELINE_SPEC.md`: state machine, project directory contract, naming rules, and done definition.
- `automation_contract.md`: automation and template-protection rules.
- `metadata/rights_checklist.md` and `metadata/source_evidence.md`: source and public-domain evidence templates.
- `preproduction/`: shared EPUB preproduction templates.
- `references/`: language-neutral quality gate and benchmark policies.
- `scripts/`: reusable chapter, Markdown normalization, and publication lint helpers.
- `state/`: initial pipeline state and human-feedback control files.
- `Makefile`: generic EPUB build/check entry points.

Target-language quality frameworks live under `template/epub_pipeline/targets/{target}/`. Source-to-target-specific templates should override or extend common files only when the direction needs different translation, typography, or review rules.

## Publication Lint / 出版文本检查

Before building a final EPUB, run:

```powershell
node scripts/publication_lint.js --target={target-language} --write-report
```

在构建最终 EPUB 前必须运行：

```powershell
node scripts/publication_lint.js --target={target-language} --write-report
```

This check is common because encoding damage, legacy print tables of contents, repeated spacing, and path portability problems can affect any language.

这项检查属于通用层，因为编码污染、旧纸书页码目录、连续空格和路径可移植性问题可能影响任何语言方向。

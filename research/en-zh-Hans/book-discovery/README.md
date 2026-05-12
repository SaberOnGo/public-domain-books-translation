# English to Simplified Chinese Book Discovery Research

本目录保存英语到简体中文方向的候选书调研、版权初筛和已有中文译本检索材料。

This directory stores candidate-book research, initial rights screening, and existing Chinese-translation checks for the English to Simplified Chinese direction.

## Scope / 范围

- These files are language-pair-specific research artifacts, not global project tools.
- 这些文件是特定语言方向的调研产物，不是项目全局通用工具。
- Future language pairs should create their own research directories, for example `research/fr-en/`, `research/ja-es/`, or `research/ar-id/`.
- 后续其他语言方向应建立自己的调研目录，例如 `research/fr-en/`、`research/ja-es/`、`research/ar-id/`。

## Files / 文件

- `public_domain_book_audit.csv`: candidate-book audit table with English source metadata, Chinese-title suggestions, rights screening, translation-gap notes, and priority scores.
- `public_domain_book_audit.csv`：候选书审计表，包含英文书源信息、中文题名建议、版权初筛、中文译本缺口和优先级评分。
- `search_results.json`: historical search output for checking whether selected English books already had likely Chinese translations.
- `search_results.json`：历史搜索结果，用于初步判断部分英文书是否已有中文译本。
- `check_translation.py`: historical script for checking likely Chinese translation status.
- `check_translation.py`：用于初步检索中文译本状态的历史脚本。
- `generate_doc.py`: historical script for generating Chinese-facing candidate-book documentation.
- `generate_doc.py`：用于生成中文候选书说明文档的历史脚本。

## Maintenance Rule / 维护规则

Do not move these files back to the repository root. If a script or dataset becomes truly language-neutral, refactor it first and move it to a shared `tools/` or `data/` area with multilingual documentation.

不要把这些文件移回仓库根目录。如果某个脚本或数据集未来真的变成语言无关的通用资产，应先重构参数和字段，再移动到共享的 `tools/` 或 `data/` 区域，并补充多语言说明。

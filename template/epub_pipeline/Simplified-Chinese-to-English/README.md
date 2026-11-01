# Simplified Chinese to English / 简体中文到英文

This overlay combines language-neutral common infrastructure with English reader-quality rules and Chinese-specific source interpretation. It contains reusable rules only. The English framework lives under `template/epub_pipeline/targets/en/quality_framework/`.

Create a numbered project using `books/scripts/create_book_project.py` with `--source-target Simplified-Chinese-to-English --target en`. Add the private-use arguments for a user-provided non-public source. Read MASTER_PROMPT.md for the full route. Bilingual output is enabled only when requested; then retain both English-only and Chinese-English editions from one canonical target.

本目录只保存可复用规则；具体书籍资料必须在独立工程内。英文框架不照搬简体中文质量规则。

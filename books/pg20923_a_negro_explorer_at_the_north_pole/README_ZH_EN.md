# EPUB 制作流水线模板（中英双语） / EPUB Pipeline Template (ZH-EN)

## 你只需要提供 / Only required inputs
- `TEMPLATE_ROOT`：模板目录绝对路径
- `SOURCE_URL`：英文原书地址

## 执行顺序 / Execution order
1. `prompts/00_orchestrator_zh_en.md`
2. `prompts/01_ingest_clean_zh_en.md`
3. `prompts/02_split_zh_en.md`
4. `prompts/03_glossary_zh_en.md`
5. `prompts/04_translate_all_zh_en.md`
6. `prompts/05_review_fidelity_all_zh_en.md`
7. `prompts/06_review_readability_all_zh_en.md`
8. `prompts/07_review_terminology_all_zh_en.md`
9. `prompts/08_build_validate_zh_en.md`

## 中文干预点 / Human override points
- `glossary/terms.csv`：术语统一
- `glossary/style_guide.md`：文风规范
- `metadata/book.yaml`：书籍元数据
- `state/pipeline_state.json`：当前状态

# Generic EPUB Translation Pipeline Template

You only provide:
- TEMPLATE_ROOT
- SOURCE_URL

Run prompts in order:
00_orchestrator -> 01_ingest_clean -> 02_split -> 03_glossary -> 04_translate_all -> 05_review_fidelity_all -> 06_review_readability_all -> 07_review_terminology_all -> 08_build_validate

All naming/output paths are fixed by PIPELINE_SPEC.md.

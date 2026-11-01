# Simplified Chinese to English / 简体中文到英文 Agent 规则

Read repository AGENTS.md, common PIPELINE_SPEC and policies, this template's SKILL.md, and `template/epub_pipeline/targets/en/quality_framework/` before work. Create projects with `books/scripts/create_book_project.py --source-target Simplified-Chinese-to-English --target en`; private-use projects also require `--mode private-use`, source evidence, declaration, and the private overlay. Book-specific files stay in the numbered project, never this template.

Translate from the Chinese source directly. Do not use an English pivot translation or silently modernize source claims. Preserve simplified/traditional variants and OCR doubts as evidence. Resolve omitted subjects, topic chains, aspect, idioms, classifier functions, meaningful animal names, and scientific terminology using context. Natural English is required without omission or invention.

Follow MASTER_PROMPT.md and all common gates. One translation owner per chapter; independent semantic reviewers and two post-EPUB review agents are mandatory. GPT-family spawned translation/audit workers follow the host-verified gpt-5.6-luna/max default and common capability/ownership rules. No translator may sign independent PASS for their own chapter.

本模板直接从中文译成英文。必须完整保留情节、叙事声音、专名、图表和注释。逐章全量审校与全书问题族追查继续适用；私人自用不降低质量，也不允许公开发布。

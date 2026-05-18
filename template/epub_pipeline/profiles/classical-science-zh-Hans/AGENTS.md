# classical-science-zh-Hans Agent Instructions / 古典科学简体中文控制模板 Agent 指令

This file is for AI agents using the `classical-science-zh-Hans` profile overlay.

本文件供使用 `classical-science-zh-Hans` 控制模板的 AI agent 读取。

## Scope / 适用范围

- Target language: Simplified Chinese.
- 目标语言：简体中文。

- Source language: any public-domain source language, decided by the language-pair template.
- 原文语言：由语言方向模板决定，可为古希腊文、拉丁文、阿拉伯文、英文、德文、法文等。

- Book type: classical scientific, mathematical, astronomical, technical, diagram-heavy, table-heavy, or proof-heavy public-domain works.
- 书籍类型：古典科学、数学、天文学、技术文献，或含大量图表、表格、证明的公版作品。

## Mandatory Rules / 强制规则

- Copy `template/epub_pipeline/common` first, overlay the matching language-pair template second, then overlay `template/epub_pipeline/profiles/classical-science-zh-Hans`.
- 必须通过 `books/scripts/create_book_project.py --profile classical-science-zh-Hans` 创建书籍工程：脚本会先复制 `template/epub_pipeline/common`，再覆盖复制匹配的语言方向模板，最后覆盖复制 `template/epub_pipeline/profiles/classical-science-zh-Hans`。

- Do not write book-specific source text, translations, diagrams, QA files, EPUB output, or metadata into this profile directory.
- 不得把具体书籍的原文、译文、图表、QA、EPUB 输出或 metadata 写入本 profile 目录。

- The original-language public-domain source is the translation base text.
- 公版原书语言文本是翻译底本。

- A second-language translation may be used only as a reference witness for understanding, discrepancy checks, and technical verification. It must not become a hidden base text or direct pivot translation.
- 第二语言译本只能作为理解、差异校对和技术核验的参考证据；不得成为隐藏底本或直接转译底稿。

- If the reference translation is still copyrighted, do not copy its wording, notes, diagrams, tables, layout, or editorial apparatus into project files.
- 如果参考译本仍受版权保护，不得复制其措辞、注释、图表、表格、版式或编辑体例到项目文件中。

- Before bulk translation, create and pass the terminology lock, reference-witness policy, diagram/table inventory, and technical verification plan.
- 批量翻译前，必须创建并通过术语锁定、参考译本使用政策、图表/表格清单和技术校验计划。

- Before final output, complete proof dependency, notation registry, table validation, numeric validation, claim traceability, and domain authority records when applicable.
- 最终输出前，必须按需完成证明依赖、符号注册、表格校验、数值校验、断言追溯和领域权威来源记录。

- Mathematical, astronomical, geometric, numeric, tabular, and diagram labels must stay consistent across the whole book.
- 数学、天文、几何、数值、表格和图表标签必须全书一致。

- AI-generated or AI-redrawn diagrams are draft aids until checked against the source diagram, textual description, labels, and mathematical relations.
- AI 生成或重绘图在完成原图、正文、标签和数学关系核对前，只能视为草稿辅助。

- GPT-Image-2 may be used for diagram drafts, but final publication diagrams must pass source, label, geometry, text-reference, and accessibility checks.
- GPT-Image-2 可用于图表草稿，但最终出版图必须通过源图、标签、几何关系、正文引用和可访问性检查。

- Mathematical and astronomical chapters require terminology lock, proof dependency, model registry, numeric validation, and diagram/table audit before any final chapter gate.
- 数学和天文学章节在进入终稿门禁前，必须完成术语锁定、证明依赖、模型注册、数值校验和图表/表格审计。

- No chapter may enter `chapters/final/` unless its technical audit and diagram/table audit pass when applicable.
- 章节若涉及技术内容、图表或表格，未通过技术审计与图表/表格审计，不得进入 `chapters/final/`。

- After the first full-book EPUB and after each post-EPUB refinement pass, at least two independent agents must run the stratified random spot-check gate with `--profile auto` or `--profile science`. Tables, figures, formula/proof blocks, captions, and notes must be sampled as independent high-risk strata, with special attention to mathematical proof chains, astronomical concepts, numeric notation, diagram labels, image cropping, table structure, and Chinese readability.
- 第一版全书 EPUB 生成后，以及每轮 EPUB 后精校完成后，必须由至少两个独立 Agent 使用 `--profile auto` 或 `--profile science` 执行分层随机抽检门禁。表格、图片、公式/证明块、图注和注释必须作为独立高风险层抽样，重点检查数学证明链、天文学概念、数值表示、图表标签、图片裁剪、表格结构和中文可读性。

## Human Checkpoints / 人类可选检查点

- `metadata/reference_witness_policy.md`
- `glossary/technical_terms.csv`
- `qa/technical/terminology_lock_report.md`
- `qa/technical/diagram_table_inventory.md`
- `qa/technical/verification_plan.md`
- `qa/technical/proof_dependency_map.md`
- `qa/technical/equation_notation_registry.csv`
- `qa/technical/table_validation_log.md`
- `qa/technical/claim_traceability_matrix.csv`
- `qa/technical/textual_variant_log.csv`
- `qa/technical/domain_authority_sources.md`
- `qa/technical/astronomical_model_registry.csv`
- `qa/technical/mathematical_term_lock.md`
- `qa/technical/chord_angle_calculation_policy.md`
- `qa/technical/diagram_redraw_workflow.md`
- `qa/technical/{NNN_slug}.technical_audit.md`
- `qa/technical/{NNN_slug}.diagram_table_audit.md`
- `reviews/random_spotcheck/random_sample_manifest.json`
- `reviews/random_spotcheck/round_XXX/`
- `reviews/agent_a/random_spotcheck_review.md`
- `reviews/agent_b/random_spotcheck_review.md`
- `reviews/scorecards/final_science_score.md`

如果不需要等待人工反馈，也只能在对应报告明确 `PASS` 后继续。

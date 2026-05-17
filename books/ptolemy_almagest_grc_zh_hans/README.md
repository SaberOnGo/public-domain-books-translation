# 古典科学与数学天文学 EPUB 控制模板 / Classical Science EPUB Control Profile

## 定位 / Purpose

本目录不是单一语言方向模板，而是一个第三层控制 overlay。

It is not a source-target language-pair template. It is an optional third-layer production-control profile.

适用对象：

- 古典科学、数学、天文学、地理学、光学、力学、医学等技术性公版书。
- 含大量证明、术语、图表、表格、数值、单位、专名、校勘版本差异的作品。
- 需要使用“原书语言 + 第二参考语言译本”共同校读，但禁止从现代译本直接转译的项目。

Typical examples include classical astronomy, mathematics, optics, mechanics, geography, and other technical public-domain works whose translation depends on stable terminology, diagrams, tables, and mathematical verification.

## 复制顺序 / Overlay Order

制作具体书籍时必须按顺序复制：

1. `template/epub_pipeline/common`
2. 匹配的语言方向模板，例如 `template/epub_pipeline/en-zh-Hans`、未来的 `grc-zh-Hans`、`la-zh-Hans`、`ar-zh-Hans`
3. 本目录：`template/epub_pipeline/profiles/classical-science-zh-Hans`

所有具体书籍输出只能写入 `books/{book_id_slug}/`，不得写回本目录。

## 核心原则 / Core Principles

- 原书语言是底本。第二语言译本只能用于理解、校对、定位疑难，不得作为直接转译底稿。
- 本书的具体来源分工是：Heiberg PDF 扫描为主底本影像；PAL Heiberg 古希腊文转写为辅助转写和 OCR/细节校正来源；英译本只作 reference witness。
- 英译本不能进入 `source/` 作为底稿，不能作为 OCR/转写修正 authority，也不能替代 PDF/PAL 古希腊证据链。
- 版权未确认的现代译本不能纳入工作流。即使可以作为私人校读参考，也不得复制其表达、注释、图表或译文结构。
- 全书术语必须稳定。数学、天文、仪器、几何图形、角度、单位、表格字段、证明用语必须进入术语锁定流程。
- 图表必须可追溯。原图、重绘图、图注、正文引用、术语表、数值表之间必须能互相核对。
- 数值必须单独校验。角度、弦表、比例、日期、星表、页码、卷章节编号不得只靠语言审校。
- AI 初译不能直接发布。必须经过原文对照、参考译本差异审计、数学/天文逻辑审计、图表审计、术语锁定和 EPUB 校验。

## 关键记录 / Key Records

- `metadata/reference_witness_policy.md`：原文底本和第二语言参考译本的版权、用途和禁止事项。
- `qa/technical/reference_witness_diff_log.md`：原文与参考译本差异及最终取舍。
- `glossary/technical_terms.csv`：技术术语、图表标签、单位和证明用语。
- `qa/technical/terminology_change_log.md`：锁定术语变更与影响范围。
- `qa/technical/diagram_table_inventory.md`：图、表、星表、数值表和几何图清单。
- `qa/technical/numeric_validation_log.md`：角度、比例、单位、弦表、星表和日期等数值校验。
- `qa/technical/proof_dependency_map.md`：定义、命题、证明、推论的依赖关系。
- `qa/technical/equation_notation_registry.csv`：变量、符号、单位、图表标签和表格字段。
- `qa/technical/table_validation_log.md`：弦表、星表、历表、地理表、医学表等表格校验。
- `qa/technical/claim_traceability_matrix.csv`：关键技术断言到原文、术语、图表和审计记录的追溯。
- `qa/technical/textual_variant_log.csv`：影响技术内容的异文、拟补、残损或版本差异。
- `qa/technical/domain_authority_sources.md`：实际采用的术语、单位、命名和校勘权威来源。
- `qa/technical/astronomical_model_registry.csv`：天文学模型术语，如本轮、均轮、偏心圆、等分点。
- `qa/technical/mathematical_term_lock.md`：证明动作词和几何对象锁定。
- `qa/technical/chord_angle_calculation_policy.md`：弦表、角度、比例和计算校验策略。
- `qa/technical/diagram_redraw_workflow.md`：GPT-Image-2 草图、结构化重绘和最终图表核验记录。
- `qa/technical/{NNN_slug}.technical_audit.md`：逐章技术审计。
- `qa/technical/{NNN_slug}.diagram_table_audit.md`：逐章图表/表格审计。

## 参考规则 / Reference Rules

- `references/technical_publication_control.md`
- `references/units_symbols_policy.md`
- `references/figure_redraw_spec.md`
- `references/domain_authority_sources.md`
- `references/math_astronomy_proof_control.md`
- `references/gpt_image_diagram_workflow.md`
- `references/domains/astronomy.md`
- `references/domains/mathematics.md`
- `references/domains/geography.md`
- `references/domains/optics_mechanics.md`
- `references/domains/medicine.md`

## 与语言方向模板的关系 / Relationship to Language-Pair Templates

语言方向模板负责“源语言到目标语言”的语言问题，例如英文句法、希腊文转写、拉丁文格变化或阿拉伯文术语传统。

本 profile 负责“古典科学书”的工程问题，例如术语冻结、证明链检查、图表重绘、数值表校验、参考译本使用边界。

如果两者冲突，本 profile 的科学/数学/图表硬门禁优先；语言风格问题仍遵循语言方向模板和 `targets/zh-Hans` 目标语质量框架。

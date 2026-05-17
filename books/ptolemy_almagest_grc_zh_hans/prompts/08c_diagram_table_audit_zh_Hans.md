# 08C 图表/表格审计 / Diagram and Table Audit

## 输入 / Input

- `chapters/src/{NNN_slug}.md`
- `chapters/translated/{NNN_slug}.md`
- `qa/technical/diagram_table_inventory.md`
- `qa/technical/table_validation_log.md`
- `qa/technical/equation_notation_registry.csv`
- `references/figure_redraw_spec.md`
- `references/epub_assets_figures_tables.md`
- `qa/technical/_TEMPLATE.diagram_table_audit.md`
- 图表源文件、重绘文件或 EPUB 输出片段

## 任务 / Tasks

如果章节包含图、表、星表、几何图、模型图或数值表，创建：

- `qa/technical/{NNN_slug}.diagram_table_audit.md`

必须检查：

1. 原图/表与输出图/表是否一一对应。
2. 图中标签、图注、正文引用和术语表是否一致。
3. 表格字段、行列、单位、数值和注释是否完整。
4. AI 重绘图是否按源图和数学关系核对。
5. EPUB 中是否有可访问替代文本或足够说明。
6. 表格行列、字段、单位、注释和数值是否进入表格校验记录。
7. 图表标签是否和 notation registry、术语表、正文一致。
8. Markdown 图片引用是否能转换为 XHTML `<figure>`，并保留 `alt`、`figcaption` 和必要长描述。
9. 技术表格是否优先输出为 XHTML `<table>`，并含 `caption`、`thead`、`th`。
10. 图像、SVG、CSS、字体等资源是否位于 `assets/` 下，并能被 OPF manifest 登记。
11. 是否已运行 `node scripts/asset_manifest_check.js --write-report`，且资源路径无硬错误。

## PASS 条件 / PASS Criteria

- `diagram_table_audit_status=PASS`
- 无未登记、未核对或标签错配的图表。
- 所有涉及数学关系的图表都有核对证据。
- EPUB 资源路径、OPF manifest、可访问文本和 XHTML 表格结构均已核对。

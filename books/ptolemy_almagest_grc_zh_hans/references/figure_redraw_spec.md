# 图表重绘规格 / Figure Redraw Specification

## 目的 / Purpose

AI 可用于重绘草图，但古典科学书的最终图表必须可校验、可维护、可访问。

## 输出优先级 / Output Priority

1. 结构化 HTML 表格。
2. SVG。
3. TikZ 或可复现绘图源。
4. 高分辨率位图，仅在无法结构化表达时使用。

## EPUB 资源位置 / EPUB Asset Locations

- 最终图表放入 `assets/figures/`，优先 `*.svg`。
- 影印页局部、扫描图、复杂位图放入 `assets/images/`。
- 表格源数据放入 `source/tables/*.csv` 或 `source/tables/*.tsv`，读者可见表格输出为 XHTML `<table>`。
- 构建 EPUB 时，所有图像、SVG、CSS、字体和其他资源必须写入 OPF manifest。
- Markdown 中的图片引用只是编辑源；最终 EPUB 内必须是合法 XHTML `<figure>`、`<img>`、`<figcaption>` 或等效结构。

## 必须记录 / Required Records

每个图表必须在 `qa/technical/diagram_table_inventory.md` 中登记，并在需要时进入：

- `qa/technical/{NNN_slug}.diagram_table_audit.md`
- `qa/technical/table_validation_log.md`
- `qa/technical/claim_traceability_matrix.csv`

## 图表核对项 / Check Items

- 源图位置。
- 输出文件位置。
- 图号和图注。
- 标签原文、中文译名、术语表条目。
- 正文引用位置。
- 数学关系或几何关系。
- 可访问替代文本或长描述。
- 是否由 AI 重绘，以及人工/脚本核对结果。
- EPUB 内部路径、OPF manifest 登记和 `asset_manifest_check` 结果。

## 影印裁图规则 / Facsimile Crop Rules

当 EPUB 正文采用 Heiberg PDF 等公版扫描页局部作为 facsimile figure 时，裁图不得只靠人工目测截图。必须使用可复现脚本，并满足以下条件：

- 粗裁框必须包住完整图形、全部原图字母标签、线段端点和必要符号。
- 输出图只保留图形和必要标签；不得夹带旁边正文、脚注、页眉、页码或校勘文字。
- 裁图后必须自动去白边，再补少量固定白边，避免手机 EPUB 显示时字母贴边。
- 脚本必须检查最外边缘是否有墨迹被切穿；若疑似切到标签或线条，必须失败，不得继续构建 EPUB。
- 若原书正文紧贴图形，允许脚本在粗裁后用白色遮盖邻近正文区域，但遮盖规则必须写入脚本或图像 manifest，不能只靠口头说明。
- EPUB CSS 必须让图像可响应式缩放：`max-width: 100%`、`height: auto`，技术图独占一行，不与正文并排。

## 禁止 / Forbidden

- 禁止让美观替代正确。
- 禁止只保留 AI 位图而无源图依据。
- 禁止标签、图注、正文引用和术语表不一致。
- 禁止复杂图表没有替代文本或说明。
- 禁止 XHTML 或 CSS 引用本机绝对路径、`file://`、Windows 盘符或外链热链接。
- 禁止把可结构化的数值表只做成图片。
- 禁止裁掉原图字母标签，或把夹带正文的裁图作为通过样本。

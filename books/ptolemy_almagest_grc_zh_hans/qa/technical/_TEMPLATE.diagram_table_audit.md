# 图表/表格审计模板 / Diagram and Table Audit Template

chapter_id: "{NNN_slug}"
audit_status: "FAIL"

## 图表记录 / Diagram and Table Records

| id | source_location | output_location | check_item | PASS/FAIL | notes |
|---|---|---|---|---|---|
|  |  |  | source matched | FAIL |  |
|  |  |  | labels matched | FAIL |  |
|  |  |  | text references matched | FAIL |  |
|  |  |  | numeric relations checked | FAIL |  |
|  |  |  | accessibility text present | FAIL |  |
|  |  |  | EPUB asset path exists | FAIL |  |
|  |  |  | OPF manifest item present | FAIL |  |

## EPUB 输出控制 / EPUB Output Control

- 最终图像资源应放在 `assets/figures/` 或 `assets/images/`。
- Markdown 图像引用必须能转换为 XHTML `<figure>`，并保留 `alt`、`figcaption` 和必要长描述。
- 技术表格必须优先输出为 XHTML `<table>`，含 `caption`、`thead`、`th`。
- EPUB 构建后必须运行 `node scripts/asset_manifest_check.js --write-report`，并确认 `output/asset_manifest_check.json` 无硬错误。
- OPF manifest 必须登记本章实际使用的图片、SVG、CSS、字体等资源。

## AI 重绘限制 / AI Redraw Restrictions

- AI 生成图只能作为草稿，必须按原图、正文说明、标签和数学关系核对。
- 最终输出应优先使用可维护的 SVG、TikZ、HTML 表格或其他结构化格式；位图只用于无法结构化表达的场景。
- 不得让好看的图替代不正确的图。
- 不得让 EPUB 依赖本机绝对路径、`file://`、仓库外文件或未经许可的远程图片。

## 结论 / Conclusion

本章图表/表格全部 PASS 后，才可进入 `chapters/final/`。

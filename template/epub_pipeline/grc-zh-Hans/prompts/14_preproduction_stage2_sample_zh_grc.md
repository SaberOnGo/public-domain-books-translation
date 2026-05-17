# 14 预制作阶段 2：样章制作 / Preproduction Stage 2: Sample Chapter Build

## 目的 / Purpose

在制作全书前，先按预制作阶段 1 的规格生成一个样章，检查封面、版本说明、字体、标题、排版、metadata、目录、图表/表格资源和阅读器表现。避免整本制作完成后才发现排版或资源系统性错误。

## 输入 / Input

- `preproduction/stage1/production_spec.md`
- `chapters/final/{sample_chapter}.md`
- `metadata/book.yaml`
- `state/human_feedback_control.md`
- 若书中含图表：`assets/figures/`、`assets/images/`、`source/tables/`、相关 `qa/technical/*.diagram_table_audit.md`

## 输出 / Output

生成：

- `preproduction/stage2_sample/sample_chapter.xhtml`
- `preproduction/stage2_sample/sample_book.epub`
- `preproduction/stage2_sample/sample_review.md`

## 人类检查 / Human Check

读取 `state/human_feedback_control.md`：

- 如果 `human_required=true`：AI 必须停止并提示用户检查样章。
- 如果 `human_required=false`：AI 必须自动检查样章，不等待用户。

## 自动检查项目 / Automatic Checks

1. 封面是否存在，是否写入 OPF `cover-image`。
2. 封面体积是否合理。
3. 版本说明是否包含 `LifeBook 书坊 + 个人名`、译制时间、公版来源 URL、公版说明。
4. 是否仍有旧品牌名如 `LifeBook 翻译组`。
5. 是否锁死难看字体或嵌入完整超大中文字体。
6. 章节标题在手机窄屏下是否过大。
7. `第X章` 与章节说明字号是否协调。
8. EPUB `nav.xhtml` 是否使用短目录题名，而不是纸书目录式长标题链。
9. 页面主标题和副标题是否按 `production_spec.md` 呈现，是否存在半截标题或多重破折号堆叠。
10. 正文段落、行距、缩进是否适合中文阅读。
11. 若样章含图：Markdown 图像是否已变成 XHTML `<figure>`，图片文件是否存在，`alt`、`figcaption` 和长描述是否存在。
12. 若样章含表：是否为 XHTML `<table>`，是否有 `caption`、`thead`、`th`，是否不靠图片承载可结构化数值。
13. OPF manifest 是否登记样章实际使用的图片、SVG、CSS、字体等资源。
14. `node scripts/asset_manifest_check.js --write-report` 是否通过。
15. EPUBCheck 是否通过。

## PASS / FAIL

- PASS：进入全书制作。
- FAIL：回到 `13_preproduction_stage1_spec` 或具体构建脚本修正，不得继续全书制作。

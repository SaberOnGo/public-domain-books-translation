# 预制作规格模板 / Production Spec Template

production_spec_status: "DRAFT" # DRAFT | PASS | FAIL
human_required: false

## 书籍身份 / Book Identity

- 中文书名：
- 英文原名：
- 作者：
- 译制：LifeBook 书坊 + 个人名
- 翻译/译制时间：
- 公版来源 URL：
- 公版说明：

## 封面 / Cover

- 封面来源：AI 生成 / 公版图片 / 自制设计 / 其他。
- EPUB 内封面格式：推荐 `cover.jpg`。
- 封面尺寸：建议长边 1600-2560px，比例 2:3 或接近书籍封面比例。
- 封面体积：建议控制在 200KB-800KB；除非有特殊理由，不应数 MB。
- OPF：manifest 必须包含 `properties="cover-image"`。
- 必须有 `cover.xhtml`。

## 版本说明页 / Book Info Page

必须优先展示本项目版本信息：

1. 中文书名。
2. 英文原名。
3. 作者信息。
4. `LifeBook 书坊 + 个人名` 译制。
5. 译制时间。
6. 公版来源 URL。
7. 公版/版权说明。
8. 原书信息。
9. 本书简介。

## 字体 / Font

默认模式：不写死 `font-family`，让阅读器默认字体和用户设置接管。

禁止：

- 禁止因为个人审美直接锁死宋体、黑体等具体中文字体。
- 禁止直接嵌入完整中文字体文件。

可选：

- 若必须使用 `霞鹜文楷/LXGW WenKai` 等字体，必须先做字体子集化，并记录体积和授权。

## 标题与正文 / Headings and Body

- 手机窄屏下标题不得过大。
- `第X章` 与章节说明字号必须一致或视觉协调。
- 长章节标题必须按 `references/chapter_title_policy.md` 拆分为短目录题名、页面主标题和可选副标题。
- EPUB `nav.xhtml` 应使用短目录题名，不应塞入纸书目录式长标题链。
- 正文段首缩进通常为 `2em`。
- 行距建议 `1.55-1.8`。
- 避免用 CSS 阻止阅读器改字体、字号、行距。
- 旧纸书页码目录不得作为正文输出；EPUB 应使用 `nav.xhtml` 表达目录。
- 靠连续空格对齐的内容必须改成真实列表、表格或删除，不得让普通正文出现可见异常空格。

## Publication Lint / 出版文本检查

构建前必须运行：

```powershell
node scripts/publication_lint.js --target={target-language} --write-report
```

输出必须保存为 `output/publication_lint.json`。

## Metadata / 元数据

OPF 必须包含：

- `dc:title`
- `dc:creator`
- `dc:contributor` 译者/译制者
- `dc:publisher`
- `dc:source`
- `dc:description`
- `dc:rights`
- `dcterms:modified`
- `cover-image`

## PASS 条件 / PASS Criteria

- 没有旧品牌名残留。
- 封面存在且体积合理。
- 版本说明完整。
- 字体策略不会导致读者无法调整字体。
- 标题和正文排版适合手机阅读。
- `output/publication_lint.json` 无硬错误。

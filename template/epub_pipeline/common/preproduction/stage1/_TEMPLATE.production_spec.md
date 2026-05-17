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

必须优先展示本项目版本信息，文字要短，不写成长篇宣传：

1. 页首放一句：`更多 LifeBook：https://yourlifebook.app`。
2. 中文书名。
3. 英文原名。
4. 作者信息。
5. `LifeBook 书坊 + 个人名` 译制。
6. 译制时间。
7. 公版来源 URL。
8. `版权说明`：分两小段写清楚原书版权状态和译本授权。原书段说明使用的公版来源；译本段参考仓库 `license/LICENSE.md`，默认说明中文译文、译注、整理文本、封面、排版设计与 EPUB 打包内容按 `CC BY-NC-SA 4.0` 发布，第三方商业使用需另行授权。
9. 原书信息。
10. 本书简介。
11. `译者说明`：简短介绍 LifeBook 书坊，说明本项目链接 `https://github.com/SaberOnGo/public-domain-books-translation` 和 LifeBook 链接 `https://yourlifebook.app`，邀请读者参与试读、校对、查资料、统一术语或后续书籍制作。末尾可再次放一句：`更多 LifeBook：https://yourlifebook.app`。

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

## 图表、图片与表格 / Figures, Images, and Tables

- `chapters/final/*.md` 是编辑源文件；EPUB 正文必须生成 XHTML。
- Markdown 图片引用必须转换为 XHTML `<figure><img><figcaption>` 或等效结构。
- 几何图、天文学图、光学/力学线图优先使用 `assets/figures/*.svg`。
- 封面、影印页局部、复杂扫描图使用 `assets/images/*.jpg|png|webp`。
- 技术性数值表必须优先生成 XHTML `<table>`，源数据保存在 `source/tables/*.csv` 或 `source/tables/*.tsv`。
- 每张图必须有 `alt`、图注和必要长描述；每个表必须有 `caption`、`thead`、`th`。
- OPF manifest 必须登记所有图片、CSS、字体和其他 EPUB 内部资源。
- 不得在 XHTML 或 CSS 中保留本机绝对路径、`file://`、Windows 盘符或在线热链接。
- 若书中没有图表，也必须在本规格中写明 `figures_and_tables: none`。

## Publication Lint / 出版文本检查

构建前必须运行：

```powershell
node scripts/publication_lint.js --target={target-language} --write-report
node scripts/asset_manifest_check.js --write-report
```

输出必须保存为 `output/publication_lint.json`。
资源检查输出必须保存为 `output/asset_manifest_check.json`。

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
- 所有被 XHTML/CSS 引用的图像、样式、字体等资源。

## PASS 条件 / PASS Criteria

- 没有旧品牌名残留。
- 封面存在且体积合理。
- 版本说明完整。
- 字体策略不会导致读者无法调整字体。
- 标题和正文排版适合手机阅读。
- `output/publication_lint.json` 无硬错误。
- `output/asset_manifest_check.json` 无硬错误。
- 图表、表格、图片资源路径和 OPF manifest 一致。

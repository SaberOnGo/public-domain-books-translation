# 预制作规格模板 / Production Spec Template

production_spec_status: "DRAFT" # DRAFT | PASS | FAIL
human_required: false

## 书籍身份 / Book Identity

- 中文书名：
- 英文原名：
- 作者：
- 公版或授权项目译制：LifeBook 书坊 + 个人名
- 私人自用项目制作标识：参考public-domain-books-translation 开源项目 个人自制
- 翻译/译制时间：
- 公版或授权来源 URL：
- 公版说明（仅公版或授权项目）：
- 私人自用说明（仅 `publication_mode=private_use`）：仅供个人自用，不传播，不商业使用；风险由个人承担；public-domain-books-translation 开源项目仅用于公版书翻译发布，不承担其他个人翻译、保存、传播或使用非公版内容导致的版权风险及责任。

## 封面 / Cover

- 封面来源：AI 生成 / 公版图片 / 自制设计 / 其他。
- 全书主题群：概括本书主要问题意识、主题链或解释框架，避免把封面压缩成单个术语或单章概念。
- 主视觉依据：说明主视觉如何来自全书内容、时代、地域、人物、核心意象或问题链。
- 读者吸引力检查：缩略图是否清楚；标题区是否高对比；主视觉是否会让目标读者愿意打开阅读。
- 真实感检查：是否存在比例失真的巨型道具、虚假文字、畸形物体、透视错误、不可信物体组合或明显 AI 生成痕迹。
- 禁用视觉元素：长横线、多重横线、乱码感细线、仿扫描线、阴暗低对比底图、与主题无关的装饰图、巨型书本/钢笔/棋子/硬币等概念道具。
- EPUB 内封面格式：推荐 `cover.jpg`。
- 封面原图/背景图 output 文件：`output/cover_source.png` 或本书记录的等效文件。
- 带文字压缩封面 output 文件：`output/cover.jpg` 或本书记录的等效文件。
- 封面尺寸：建议长边 1600-2560px，比例 2:3 或接近书籍封面比例。
- 封面体积：建议控制在 200KB-800KB；除非有特殊理由，不应数 MB。
- OPF：manifest 必须包含 `properties="cover-image"`。
- 必须有 `cover.xhtml`。

## 书籍信息页 / Book Info Page

必须优先展示本项目版本信息，文字要短，像正式出版物的版权页/版本页，不得写成制作日志、宣传页或 README。

必备内容：

1. 目标语言书名。
2. 原书名。
3. 作者信息。
4. 公版或授权项目使用 `LifeBook 书坊 + 个人名` 译制；`private_use` 项目使用 `参考public-domain-books-translation 开源项目 个人自制`。
5. 译制时间。
6. 公版来源名称与 URL。
7. 公版说明：公版或授权项目用一条简短说明写清源文本公版/授权依据，并提醒跨地区发行需复核目标地区版权状态。`private_use` 项目不得写公版说明，必须写个人自用边界和风险责任。
8. 本书简介：只介绍作品本身，不混入 EPUB 制作、译者署名、来源 URL 或版权提醒。
9. 作者简介。
10. 创作/成书背景。

可选内容：

- 译制说明、底本选择、术语原则、图表策略等确有必要时，放入单独的 `translator-note.xhtml` 或 `edition-note.xhtml`，文字必须短而读者友好。
- 项目链接、参与方式、QA 过程、prompt、工作流日志、图表审计日志不得放入 `book-info.xhtml`；但可以在页首保留一条短 LifeBook 入口：`更多：访问 LifeBook`，链接文字内部嵌入 `https://yourlifebook.app`，不得直接显示长 URL。
- 不要在 `book-info.xhtml` 页首、页尾重复放置 `更多 LifeBook` 或其他项目链接。
- 不要在同一前置页中反复出现多个 `版权说明`；版权和公版状态应集中、简短、一次说明。

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
python scripts/check_no_local_absolute_paths.py --write-report
node scripts/publication_lint.js --target={target-language} --write-report
node scripts/asset_manifest_check.js --write-report
python scripts/check_template_workflow_gate.py --write-report
python scripts/check_cover_output_assets.py --write-report
python scripts/check_reader_facing_policy.py --write-report
```

输出必须保存为 `output/publication_lint.json`。
资源检查输出必须保存为 `output/asset_manifest_check.json`。
本机绝对路径门禁输出必须保存为 `output/local_absolute_path_check.json`。
模板流程门禁输出必须保存为 `output/template_workflow_gate.json`。
封面 output 资产门禁输出必须保存为 `output/cover_output_assets_check.json`。
读者可见内容门禁输出必须保存为 `output/reader_facing_policy_check.json`。

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
- `output/local_absolute_path_check.json` 无硬错误。
- `output/template_workflow_gate.json` 无硬错误。
- `output/cover_output_assets_check.json` 无硬错误。
- `output/reader_facing_policy_check.json` 无硬错误。
- 图表、表格、图片资源路径和 OPF manifest 一致。

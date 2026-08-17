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

## 输出版本 / Output Editions

- `edition_type`：`target_only` 或 `bilingual_parallel`。
- `English-to-Simplified-Chinese` 项目默认使用 `edition_type: bilingual_parallel`，必须同时生成单简体中文 EPUB 和中英双语对照 EPUB；这与 `publication_mode` 解耦，公版、授权和 `private_use` 都适用。
- 其他语言方向只有用户明确写明“请输出 edition_type: bilingual_parallel，同时生成目标语言版 EPUB 和源语言-目标语言双语对照版 EPUB”时，才生成双语对照版。
- `target_only` 成书稿仍以 `chapters/final/` 为准；双语版不得把源文块写入 `chapters/final/`，不得降低单目标语 EPUB 的章节门禁、publication lint、随机抽检和 release 要求。
- 双语版必须遵守 `references/bilingual_parallel_edition_policy.md`，由源文、目标语成书稿和对齐映射生成。
- 双语 visible unit 固定为“完整源语短段 -> 紧随的完整目标语译段”；不得逐句交错、跨两个源自然段、按页面/视口聚合或连续多段源文后集中目标语。
- 翻译前必须记录 `state/translation_contract.json`，完成全书专名 discovery/candidate decision/`entity_id`/occurrence ledger/CSV 锁定。用户未选专名策略时默认策略 `3` 并记录 `selection_source=default`，不得以默认值跳过发现。
- `translation_units/` 是唯一权威 store；并行 worker 只输出 chapter patch，CAS 合并器唯一写入。`chapters/translated` 与 `chapters/final` 从同一 target hash 投影。
- 双语对齐映射默认写入 `qa/bilingual_parallel/alignment_map.json`；双语版启用后必须运行 `npm run build:bilingual` 生成独立双语 EPUB，并通过 `npm run check:bilingual`。这两个脚本只读取输出版本状态，不得按 `publication_mode` 判断。
- 一个读者可见双语 unit 只能来自一个原著自然段；自然段过长时，只能按完整句群拆为数个短段，并让每个完整 source short paragraph 后立即紧跟它的完整 target short paragraph。
- 字数和屏幕尺寸只能用于提示长段风险，不能作为切分或合并依据；严禁为接近一屏而合并多个自然段、截断句子或集中后置译文。
- 双语版默认顺序为源语言短段在前、其完整目标语言译段紧随其后；不得逐句字幕式交错，也不得连续输出多个源段后再集中输出目标语。
- 双语版不得反复加入 `原文` / `译文` 标签，不得在每章开头加“原文在前，译文在后”之类说明。
- 目标语言是主阅读文本，保持正常正文字号和节奏；源语言为辅助对照文本，建议 `0.92em`，不得低于 `0.88em`，不得依赖字体族、斜体或颜色作为唯一区分。

## 自适应并行编排 / Adaptive Parallel Orchestration

- 本书加权工作量（`weighted_source_units`）：
- 客户端能力来源与验证时间：
- 用户是否允许派生 worker：
- 用户上限、速率上限、预算上限、质量上限：
- provider family：`gpt` / `non_gpt` / `unknown`。
- worker profile（客户端本地标识，可空）：
- pilot 章节与结果：
- 最终派生 worker 上限与理由：
- 翻译 producer 数、独立 audit consumer 数、唯一 merger：

并行策略必须遵守 `references/adaptive_parallel_orchestration.md`。不得只按 PDF 页数决定并发；必须先完成全书合同、专名、出现账本、术语和 canonical units 锁定。能力未知、用户未授权或小书默认 0 worker；GPT 家族最多派生 4 个，非 GPT 最多 8 个。首轮最多 2 个 worker，只有当前 pilot 的结构违规/专名违规为 0、语义首过率至少 90%、返工率不超过 10%、patch 冲突率不超过 1% 才能扩容。

每章只能有一个 translation producer；相邻章节优先保持同一 owner。audit consumer 不得审核自己翻译的章节，coordinator 是唯一 canonical merger。单目标语和双语版共用一套 canonical target，不得分别翻译。

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

制作规格必须显式覆盖以下通用规则文件：

- `template/epub_pipeline/common/preproduction/stage1/_TEMPLATE.production_spec.md`
- `template/epub_pipeline/common/references/cover_design_policy.md`
- `template/epub_pipeline/common/references/book_info_frontmatter_policy.md`
- `template/epub_pipeline/common/references/epub_assets_figures_tables.md`
- `template/epub_pipeline/common/references/bilingual_parallel_edition_policy.md`
- `template/epub_pipeline/common/references/adaptive_parallel_orchestration.md`
- `template/epub_pipeline/common/references/quality_gate_framework.md`
- `template/epub_pipeline/common/references/proper_noun_display_policy.md`
- `template/epub_pipeline/common/references/note_marker_policy.md`

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

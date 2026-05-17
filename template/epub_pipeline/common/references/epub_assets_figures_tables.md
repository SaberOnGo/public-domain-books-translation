# EPUB 图表、图片与表格资源规则 / EPUB Assets, Figures, and Tables

## 核心原则 / Core Principle

`chapters/final/*.md` 是编辑源文件，不是 EPUB 内部最终格式。制作 EPUB 时必须把 Markdown 转成 XHTML，并把图片、SVG、CSS、表格和辅助资源登记到 OPF manifest 中。

Markdown source is acceptable as the authoring format, but EPUB content must be valid XHTML plus declared package resources.

## 推荐目录 / Recommended Directories

| path | purpose |
|---|---|
| `assets/figures/` | 最终可发布图表，优先 SVG；也可放受控 PNG/JPG/WebP |
| `assets/images/` | 封面、影印页局部、照片、位图插图 |
| `assets/tables/` | 若需要作为 EPUB 资源附带的结构化表格文件或衍生数据 |
| `assets/styles/` | EPUB CSS 或额外样式资源 |
| `source/tables/` | 从原书整理出的 CSV/TSV 原始表格数据，不直接作为读者可见正文 |
| `qa/technical/` | 图表审计、表格校验、数值校验、重绘记录 |

## Markdown 写法 / Markdown Authoring

简单图像可在 Markdown 中引用：

```md
![图 I.10-1：弦长几何图](../../assets/figures/i-10-fig-01.svg)
```

但构建 EPUB 时必须转换为 XHTML `figure`：

```html
<figure id="fig-i-10-01">
  <img src="../assets/figures/i-10-fig-01.svg" alt="图 I.10-1：弦长几何图">
  <figcaption>图 I.10-1：弦长几何图</figcaption>
</figure>
```

复杂图必须提供长描述，可以放在正文、脚注、图注后段或单独 XHTML 注释块中。不能只用 `alt="diagram"`。

## 图像格式 / Image Formats

| content | preferred format | notes |
|---|---|---|
| 几何图、天文学示意图、光学/力学线图 | SVG | 首选。点名、线段、弧、箭头、比例关系清晰，可缩放 |
| 公式化或可复现绘图 | SVG + 可选 TikZ/脚本源 | 可维护性优先 |
| 影印页局部、扫描图、复杂老版图像 | PNG | 保留清晰度，必要时压缩 |
| 照片、封面位图 | JPG/WebP | 控制体积 |
| 大型表格 | XHTML table | 不要做成图片，除非附影印件 |

## 表格规则 / Table Rules

读者可见表格必须优先生成 XHTML `<table>`，而不是图片。

```html
<table id="tbl-i-11-chords">
  <caption>弦表节选</caption>
  <thead>
    <tr><th>弧</th><th>弦长</th></tr>
  </thead>
  <tbody>
    <tr><td>1°</td><td>1;2,50</td></tr>
  </tbody>
</table>
```

源数据应保存在 `source/tables/*.csv` 或 `source/tables/*.tsv`，并在 `qa/technical/table_validation_log.md` 记录：

- 来源页或 marker。
- 转写值。
- 规范化显示值。
- 校验公式或 checksum。
- 人工/脚本复核结果。

## OPF Manifest Requirements

EPUB 构建脚本必须把所有实际使用的资源写入 `package.opf` manifest：

```xml
<item id="fig-i-10-01" href="assets/figures/i-10-fig-01.svg" media-type="image/svg+xml"/>
<item id="img-page-032" href="assets/images/page-032.png" media-type="image/png"/>
<item id="style-main" href="assets/styles/main.css" media-type="text/css"/>
```

所有 XHTML 中的 `img src`、CSS 中的 `url(...)`、封面图和附加资源都必须能在 manifest 中找到。路径必须是 EPUB 内相对路径，不得出现 Windows 盘符、本机绝对路径或 `file://`。

## Accessibility / 可访问性

每张图必须至少有：

- 简短 `alt`。
- 图注 `figcaption`。
- 对复杂图的正文说明或长描述。

表格必须有：

- `caption`。
- `thead` 与 `th`。
- 必要时使用 `scope="col"` 或 `scope="row"`。

## Gates / 门禁

进入 `PREPRODUCTION_SAMPLE_PASS` 前必须确认：

- Markdown 图像引用均能解析到项目内文件。
- XHTML `img src` 均能解析到 EPUB 内资源。
- OPF manifest 覆盖所有使用资源。
- 不存在本机绝对路径、外链热链接、丢失图片或未登记图片。
- 图表密集书籍已完成 `qa/technical/{NNN_slug}.diagram_table_audit.md`。
- 技术表格已完成 `qa/technical/table_validation_log.md`。

## Forbidden / 禁止

- 禁止把现代受版权保护译本的图表、表格或编辑结构复制进 EPUB。
- 禁止把 GPT-image 或其他 AI 输出的图直接当最终图，除非已经完成源图、标签、正文引用、数学关系和可访问性核对。
- 禁止用图片承载可结构化的数值表。
- 禁止 EPUB 依赖仓库外、本机路径或在线图片。

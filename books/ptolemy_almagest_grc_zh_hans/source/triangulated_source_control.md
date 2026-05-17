# 三源校对控制 / Triangulated Source Control

control_status: `PAL_TRANSCRIPTION_INGESTED_FOR_AUXILIARY_SOURCE_CONTROL`

## 结论

本书后续试译和正式翻译采用“三源校对”：

1. **Heiberg PDF 扫描**：底本影像、版面、页码、图表、表格和最终核对依据。
2. **PAL Heiberg 古希腊文转写 XML**：可复制的古希腊文辅助转写，用于检索、章节切分、PAL/Heiberg 页标、分词链、长周期句分析、OCR/人工转写疑点校正和试译 source text。
3. **英译本**：只作 reference witness，帮助理解疑难数学/天文学段落、术语差异和解释方向，不得成为隐藏底稿。

严格边界：

- PDF 扫描 + PAL 古希腊转写共同构成本书的古希腊证据链。
- 英译本不属于古希腊底稿链，只属于参考理解链。
- 英译本若提示某处可能读法不同，必须回查 PDF/PAL/校勘语境；不得直接改中文译文或古希腊 source text。

## PAL 文本来源

| field | value |
|---|---|
| repository | `https://gitlab.lrz.de/badw-data/pal-texts.git` |
| commit | `368c5f1f6555679f2d7ab84062839e921a6293cb` |
| local_xml | `source/transcriptions/pal_heiberg/pal_heiberg_mathematike_syntaxis_1.xml` |
| local_license | `source/transcriptions/pal_heiberg/LICENSE.md` |
| local_readme | `source/transcriptions/pal_heiberg/README.md` |
| xml_sha256 | `3f4dd5e0bf3a52255ac7cd1c719cffe4b26a706b75ae4100b23e74fc729a300d` |
| license_sha256 | `4f0ab3bddffd5b1c2fe4b12f9213d22ca032d86a391419486290de355a4d1c90` |
| license_summary | PAL `LICENSE.md` states that CC BY 4.0 applies to all transcriptions except the listed Quadripartitum exception. `Mathematike Syntaxis #1/#19` is not that exception. |

## Book I.10 试译定位

PAL XML 中 Book I.10 的标题位置：

- start: `<h3 id="I.10">`
- source line in cloned XML: `738`
- next chapter: `<h3 id="I.11">`
- next chapter source line: `1043`
- Heiberg/PAL page marks: starts at `I_31_7`, runs through before `I_48`
- title: `ιʹ. Περὶ τῆς πηλικότητος τῶν ἐν τῷ κύκλῳ εὐθειῶν.`

## 使用规则

- 试译章节的 `chapters/src/{trial_chapter}.md` 可以从 PAL XML 抽取古希腊文，但必须保留 PAL 页行标记或可回查标记。
- PDF 扫描必须用于核对标题、页码、图表、表格和明显 OCR/转写疑点。
- 若 PAL 与 PDF 影像不一致，以 PDF 影像和 Heiberg 校勘语境为最终核对对象，并记录到 `qa/textual/textual_uncertainty_log.md`。
- 英译本只能用于疑难理解与差异摘要，不复制其措辞、注释、图表、表格。
- 英译本不得作为 OCR/转写修正 authority；任何修正都必须有古希腊文证据。
- 任何复制自 PAL 的正式 source text 必须保留 CC BY attribution。

## 仍需完成

- 将 Book I.10 从 PAL XML 抽取为 `chapters/src` 之前，先建立抽取脚本或手工抽取记录。
- 用 PDF viewer 核对 Book I.10 对应的扫描页和图形。
- 为 Book I.10 建立图表审计文件。

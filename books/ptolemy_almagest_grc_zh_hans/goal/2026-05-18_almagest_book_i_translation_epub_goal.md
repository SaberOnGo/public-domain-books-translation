# /goal Book I 前16章受控翻译、Book I EPUB 预制作与双独立 Agent 评审

goal_status: `ACTIVE`
created_date: `2026-05-18`
scope: `Book I only, chapters I.1-I.16`

## 目标

进入《Almagest》Book I 前16章的受控翻译阶段，严格依据本书目录文档、模板、QA 控制文件、章节源文和技术审计要求，完成：

1. Book I.1-I.16 章节译文。
2. Book I.11 弦表和 Book I.15 数值/表格内容的结构化处理。
3. Book I 图形、表格、证明链、天文学模型、六十进制数值和古今概念边界审校。
4. 第一版 Book I EPUB 预制作。
5. EPUB 后再评审、精校和迭代校正。
6. 至少 2 个独立 Agent 通过随机抽检评审后退出任务。

## 范围

- 只处理 Book I，章节 `I.1` 至 `I.16`。
- 允许继续使用已完成的 Book I.1-I.10 章节质量门禁成果。
- 必须补齐 Book I.11-I.16 的 source/control/translation/review/post-technical/chapter-gate 链路。
- 允许生成 Book I 专用 EPUB 预览产物。
- 不得进入 Book II-XIII。
- 不得启动 13 卷全书级翻译、全书级终稿或全书级 EPUB 生产。

## 三源分工

本目标采用三源互证，但职责必须清楚：

| 来源 | 角色 | 可用于 | 禁止 |
|---|---|---|---|
| Heiberg PDF 扫描 | 主底本影像和最终核对依据 | 页码、版面、希腊正文核对、图形、表格、几何标签、校勘区、facsimile 图 | 裸 OCR 后直接作为正文或表格数据 |
| PAL Heiberg 古希腊转写 XML | 主要正文工作文本 | 普通正文 source extraction、章节切分、页标、可复制希腊文、长句/术语分析 | 跳过 PDF 核对；替代图表/表格影像本体 |
| 英译本 | reference witness only | 疑难理解、术语对照、表头/列义辅助、差异提示、识别 PDF/PAL 疑点 | 作为中文转译底稿；复制措辞、注释、图表、表格或编辑结构 |

## 正文底本规则

- 普通正文以 PAL 古希腊转写为主要工作文本。
- 每章进入翻译前必须用 Heiberg PDF 核对页码、标题、章节边界、图形/表格缺漏和明显转写疑点。
- 英译本提示的差异必须回查 PDF/PAL/校勘语境后才能进入译文或 QA。
- 不得把英译本单独作为修正古希腊正文的 authority。

## 图形与表格规则

- 图形和表格以 Heiberg PDF 为主依据，因为 PAL 往往不含图表本体。
- Book I.11 弦表必须先从 PDF 表格影像结构化转录为 `source/tables/book_i_11_chord_table_raw.csv` 或等效 JSON。
- 英译本如含弦表，只能作为 reference witness，用于表头理解、列结构确认、疑难项抽查和发现 PDF 转录疑点。
- PDF 表格不得裸 OCR 直接用；必须逐行校验。
- 表格读者版 EPUB 采用“表分段 + 横向滚动 + 简单 CSS”。
- 大表不得做成整张缩放图片。
- Book I.11 读者版 EPUB 不放原图旁证；facsimile crop 只保留在 `source/` 和 `qa/` 中作为转录、复核和争议项证据。

## Book I.11 弦表控制

Book I.11 是本目标的高风险门禁点：

1. 保留已生成的 `source/tables/book_i_11_chord_table_regions.csv` 和逐页裁图作为转录证据。
2. 逐行转录 Heiberg printed pages `48`-`63`。
3. 每行记录 PDF viewer page、printed page、列块、弧、弦、差分、原图区域和校验状态。
4. 现代公式 `chord = 120 * sin(arc / 2)` 只能用于 QA 旁证，不得作为表格底稿。
5. 对不确定数字标记 `DISPUTED`，回查 PDF 原图和英译 witness 后记录处理结论。

## Book I.15 控制

Book I.15 是表格/数值高风险章：

- 先完成章节 source extraction PDF 复核。
- 若 PDF 含表格或数值列，按 Book I.11 同类结构化表格策略处理。
- 保留古代表达、六十进制值和近似说明；不得只转成现代小数。

## 翻译质量要求

- 中文正文应现代、清楚、可读，但不得丢失古希腊原书证明链和技术结构。
- 数学证明必须保留推理步骤、图中点名、线段/弧/角/弦关系、Euclid 依赖和近似说明。
- 天文学章节必须保留古代模型边界，不得改写成现代天体物理解释。
- 引入现代术语时，正文保持可读，章末注说明古今概念边界。
- `Eucl. VI.33` 等依据应在正文简化表达，并在注释中说明相应定理/定义内容。

## EPUB 预制作要求

- 只生成 Book I EPUB 预览，不生成 13 卷全书 EPUB。
- EPUB 表格使用 XHTML table，表分段、横向滚动、简单 CSS。
- 图形使用 facsimile 或经过审计的图像/SVG，并设置 `max-width: 100%`、`height: auto`。
- EPUB 后必须进行预制作评审：正文可读性、移动端表格可读性、图表清晰度、目录、注释、数学/天文学内容和源证据一致性。

## 精校与独立 Agent 评审

第一版 Book I EPUB 完成后，进入可重复迭代的精校流程：

1. 数学、天文学、图表、表格、数值和中文可读性详细精校。
2. 精校后启动 2 个或以上独立 Agent 随机抽检。
3. 每个 Agent 每轮至少随机抽检 10 个段落或表格片段。
4. Agent 必须按模板和本书设计要求评审：忠实度、可读性、术语、证明链、图表标签、数值、古今概念边界、手机 EPUB 可读性。
5. 任何 Agent 判断读者理解有明显问题，必须回到精校。
6. 只有 2 个独立 Agent 均给出通过结论，且评分达到 `70-75` 分以上，才能退出目标。

## 禁止项

- 不得进入 Book II-XIII。
- 不得启动 13 卷全书翻译。
- 不得生成全书级正式 `output/book.epub`。
- 不得把 Toomer 等现代英译本当底稿。
- 不得裸 OCR PDF 正文或表格后直接发布。
- 不得把 Book I.11 弦表散文化翻译。
- 不得把可结构化表格只做成图片。

## 完成定义

本目标只有在以下全部满足后才可完成：

- Book I.1-I.16 译文完成。
- Book I.11 和 Book I.15 的表格/数值控制完成。
- Book I.1-I.16 章节质量门禁通过。
- 第一版 Book I EPUB 生成并通过结构检查。
- EPUB 后精校至少一轮完成。
- 至少 2 个独立 Agent 各自随机抽检至少 10 个段落/表格片段并通过。
- 评审记录保存在 `reviews/` 或既有评审路径中。

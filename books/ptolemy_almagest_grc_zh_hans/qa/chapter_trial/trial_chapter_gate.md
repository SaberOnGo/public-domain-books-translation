# 章节试译门禁 / Trial Chapter Gate

gate_status: `BOOK_I10_SINGLE_TRIAL_TRANSLATION_ALLOWED__FULL_BOOK_BLOCKED`

## 目标

先完成一个章节试翻译。通过后进入全书翻译；不通过则退回研究、预翻译、OCR/转写、术语或技术校验阶段。

## 当前候选章节

| priority | candidate | reason | status |
|---|---|---|---|
| 1 | Book I.10 | 几何证明与弦表预备，能检验数学术语、证明链、图表标签和技术审计 | SINGLE_TRIAL_TRANSLATION_ALLOWED |
| 2 | Book I.1 | 风险较低，可测试文体、术语、古希腊文句法和中文表达 | FALLBACK_ONLY |

## 进入试译的硬性前置

| check | required result | current status | next action |
|---|---|---|---|
| rights | exact source text rights allow project use | PASS_FOR_PAL_AUXILIARY_SOURCE | PAL license permits CC BY 4.0 transcriptions except Quadripartitum; Almagest is not the exception |
| source text | trial chapter Greek text exists in `chapters/src/` | PASS_FOR_TRIAL_SOURCE | Book I.10 extracted to `chapters/src/010_book_i_10_chords.md`; PAL markers `I_31_7` through before `I_48` retained |
| page mapping | trial chapter source page range known | PASS_FOR_BOOK_I10_TRIAL | PDF viewer pages `19`-`27` map to Book I.10; page `28` starts Book I.11 |
| figure/table mapping | Book I.10 figures/tables inventoried if selected | PASS_FOR_BOOK_I10_TRIAL | `qa/technical/010_book_i_10_chords.diagram_table_audit.md` records 7 figures, labels, source lines, and table boundary |
| terminology | trial chapter terms at least `PILOT_LOCKED` | PARTIAL_PASS_FOR_BOOK_I10 | `mathematical_term_lock.md` now includes Book I.10 Greek source terms; full lock still pending |
| proof dependency | Book I.10 proof chain mapped before trial translation | PASS_FOR_BOOK_I10_TRIAL | `qa/technical/proof_dependency_map.md` maps local constructions, Euclid citations, lemmas, and numeric dependencies |
| sexagesimal numeric control | Book I.10 numeric scale and values controlled before trial translation | PASS_FOR_BOOK_I10_TRIAL | `qa/technical/numeric_validation_log.md` records `τξ`, `ρκ`, angular values, chord values, approximation policy, and Book I.11 table boundary |
| pretranslation report | explicitly allows one chapter formal trial | PASS_FOR_BOOK_I10_SINGLE_TRIAL | `qa/pretranslation/pretranslation_report.md` updated after technical controls |

## 执行结论

当前允许写入一个且仅一个文件：`chapters/translated/010_book_i_10_chords.md`，作为 Book I.10 单章节受控试译。不得写入 `chapters/final/`，不得翻译 Book I.11 弦表，且不得进入全书翻译。

允许试译时必须使用以下控制文件：

- `chapters/src/010_book_i_10_chords.md`
- `qa/technical/010_book_i_10_chords.diagram_table_audit.md`
- `qa/technical/proof_dependency_map.md`
- `qa/technical/numeric_validation_log.md`
- `qa/technical/mathematical_term_lock.md`
- `qa/technical/010_book_i_10_chords.technical_audit.md`

## 2026-05-16 执行记录

- 已尝试用 Playwright/浏览器打开本地 Heiberg PDF；`file://` 被阻止，改用本地 `python -m http.server` 后浏览器可访问 PDF，但当前 Playwright PDF viewer 没有渲染可操作页面内容。
- 已检查本机 Python：只有 `PIL` 可用，`pypdf` 与 `fitz/PyMuPDF` 不可用。
- 已尝试安装 `pypdf pymupdf`；`pymupdf` wheel 下载在当前网络环境下长时间无进展，已终止，避免遗留进程。
- 结论：本轮未能完成 PDF 页图渲染和 Book I.10 页图定位；试译门禁继续保持 `BLOCKED_PENDING_SOURCE_TEXT_UNLOCK`。
- 下一步建议：优先安装/提供可用 PDF 渲染与 OCR 工具链，例如 Poppler `pdftoppm/pdfinfo`、Tesseract Greek OCR、或可用的 PyMuPDF wheel；或者明确批准使用可合法复制的 Heiberg 数字转写作为 trial chapter source。

## 2026-05-17 三源控制更新

- 用户确认当前浏览器 PDF viewer 已正常显示本地 PDF，截图显示第 `3 / 589` 页可读。因此 PDF 扫描页可作为页图和图表核验依据。
- 已浅克隆 PAL `pal-texts` 仓库到临时目录核查；仓库 `LICENSE.md` 明确除 Quadripartitum 例外外，其他 transcriptions 为 CC BY 4.0。
- 已保存 PAL `Mathematike Syntaxis #1/#19` XML 到 `source/transcriptions/pal_heiberg/pal_heiberg_mathematike_syntaxis_1.xml`。
- Book I.10 在 PAL XML 中为 `<h3 id="I.10">`，从 Heiberg/PAL 标记 `I_31_7` 开始，到 `<h3 id="I.11">` 前结束。
- 试译 source gate 已从“无文本来源”推进为“PAL source 可用，等待抽取与 PDF 页图核验”。

## 2026-05-17 试译原文抽取

- 已新增正式目标文件：`goal/2026-05-17_almagest_trial_chapter_to_review_to_epub_goal.md`。
- 已新增抽取脚本：`scripts/extract_pal_trial_chapter.py`。
- 已生成试译原文：`chapters/src/010_book_i_10_chords.md`。
- 已生成 trial toc：`source/trial_toc.json`。
- 抽取范围：PAL marker `I_31_7` 到 `<h3 id="I.11">` 前，页标记覆盖 `I_32` 至 `I_47`。
- 当前结论：source text gate 对 Book I.10 试译原文为 `PASS_FOR_TRIAL_SOURCE`，但 PDF page/figure mapping 仍为 `PENDING_VISUAL_VERIFICATION`，因此不得进入正式试译和全书翻译。

## 2026-05-17 PDF 页图定位

- 已用浏览器访问本地 PDF 并截取 viewer pages `19`-`28`。
- Book I.10 起点：viewer page `19` 右栏，printed page `31`。
- Book I.10 范围：viewer pages `19`-`27`。
- Book I.11 起点：viewer page `28` 左栏，printed page `48`，可见弦表。
- 几何图可见于 viewer pages `20`, `22`, `23`, `24`, `25`, `26`。
- 截图证据目录：`qa/technical/page_screenshots/`。
- 章节图表审计文件：`qa/technical/010_book_i_10_chords.diagram_table_audit.md`。
- 当前结论：PDF range mapping 对 Book I.10 为 `PASS_FOR_BOOK_I10_TRIAL`，但 figure label/proof-reference audit 仍未完成，因此仍不得进入正式试译和全书翻译。

## 2026-05-17 术语与技术控制更新

- 已更新 `qa/technical/mathematical_term_lock.md`，把 Book I.10 中出现的关键希腊词/短语填入试译级术语锁定。
- 已新增 `qa/technical/010_book_i_10_chords.technical_audit.md`。
- 当前阻断项转为：figure label audit、proof dependency map、sexagesimal numeric controls。
- 当前结论：术语对 Book I.10 达到 `PARTIAL_PASS_FOR_BOOK_I10`，但技术控制未 PASS，因此仍不得进入正式试译和全书翻译。

## 2026-05-17 Book I.10 试译前技术控制通过

- 已完成 `qa/technical/010_book_i_10_chords.diagram_table_audit.md`：7 个图的点名、线段/弧/构造关系、来源行和试译控制规则已登记；Book I.10 无正文数值表，viewer page `28` 的弦表归入 Book I.11。
- 已完成 `qa/technical/proof_dependency_map.md` 的 Book I.10 试译级依赖图：覆盖开篇数值方法、十边形/五边形证明、四边形乘积引理、弧差、弧半、弧和、弦弧比不等式、1 度与半度弦值、Book I.11 表格交界。
- 已完成 `qa/technical/numeric_validation_log.md` 的 Book I.10 六十进制控制：覆盖 `τξ=360`、`ρκ=120`、`36°/72°/60°/90°/120°/144°/12°/6°/3°/1°30'/0°45'/1°/0°30'` 等值和近似规则。
- 当前结论：Book I.10 可进入单章节受控试译；全书翻译、`chapters/final/`、EPUB 生产和 Book I.11 弦表仍然阻断。

## 回退规则

- 若 Book I.10 的 source text 或图表无法核清，先回退到研究/预翻译阶段，必要时改选 Book I.1。
- 若 Book I.1 也无法建立合法希腊文底稿，停止正式试译，只能继续 OCR/转写研究。

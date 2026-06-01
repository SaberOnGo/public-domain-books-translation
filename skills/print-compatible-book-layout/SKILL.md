---
name: print-compatible-book-layout
description: Use when designing, translating, reviewing, or fixing LifeBook book/page layout, including print-compatible EPUB typography, Chinese title hierarchy, body rhythm, paragraph style, traditional note markers such as [1] or (1), vertical-writing considerations, block quotes, tables, figures, frontmatter/backmatter pages, section breaks, CSS layout rules, EPUB nav labels, title maps, and future PDF or physical-book publication compatibility. / 用于设计、翻译、审查或修复 LifeBook 书籍页面排版，包括 EPUB 与纸书兼容的 typography、中文标题层级、正文节奏、段落样式、[1] 或 (1) 等传统注记、竖排实现、引文、图表、前后置页、分隔符、CSS、目录题名和未来 PDF/实体书出版兼容性。
---

# 印刷兼容书籍排版 / Print-Compatible Book Layout

Use this skill to design LifeBook EPUB pages that read well on screen and can later become PDF or physical books without redesigning the text structure.
使用本 skill 设计 LifeBook 电子书页面：当前适合 EPUB 阅读，未来也能平滑进入 PDF 或纸质书出版。

## Boundary / 边界

- Keep this skill limited to book/page layout design; do not merge these rules into unrelated workflow skills.
  本 skill 只负责书籍与页面排版设计；不要把这些规则混入无关的流水线 skill。
- Do not modify source, rights, translation, QA, or release workflow rules unless the user explicitly asks for that.
  除非用户明确要求，不要修改来源、版权、翻译、QA 或发布流程规则。

## Required Reading / 必读文件

- Read `AGENTS.md` before any repository task.
  执行仓库任务前先读 `AGENTS.md`。
- Read `template/epub_pipeline/common/preproduction/stage1/_TEMPLATE.production_spec.md` before changing production layout policy.
  修改制作规格或排版策略前，读取 `template/epub_pipeline/common/preproduction/stage1/_TEMPLATE.production_spec.md`。
- Read `template/epub_pipeline/common/references/chapter_title_policy.md` before designing titles or headings.
  设计标题或标题层级前，读取 `template/epub_pipeline/common/references/chapter_title_policy.md`。
- Read `template/epub_pipeline/common/references/book_info_frontmatter_policy.md` before editing frontmatter or book-info pages.
  编辑前置页或书籍信息页前，读取 `template/epub_pipeline/common/references/book_info_frontmatter_policy.md`。
- Read `template/epub_pipeline/common/references/epub_assets_figures_tables.md` before changing figure, table, image, or CSS resource layout.
  修改图、表、图片或 CSS 资源排版前，读取 `template/epub_pipeline/common/references/epub_assets_figures_tables.md`。
- For Simplified Chinese output, read `template/epub_pipeline/targets/zh-Hans/quality_framework/references/title_punctuation_and_heading_style.md`.
  输出简体中文时，读取 `template/epub_pipeline/targets/zh-Hans/quality_framework/references/title_punctuation_and_heading_style.md`。
- Read `references/research_basis.md` only when revising this skill or when a decision needs external justification.
  只有在修订本 skill 或需要外部依据时，才读取 `references/research_basis.md`。

## Core Principle / 核心原则

- Design a book system, not an EPUB trick.
  设计一本书的系统，不是设计 EPUB 小技巧。
- Make the page structure work as a printed book first: title, contents, body, notes, figures, tables, frontmatter, and backmatter must remain meaningful without links or scripts.
  页面结构必须先像正式纸书一样成立：标题、目录、正文、注释、图表、前置页和后置页在没有链接或脚本时也要可读。
- Treat EPUB links, popups, and navigation as enhancements, not as the only carrier of meaning.
  EPUB 链接、弹窗和导航只能作为增强，不能成为意义的唯一载体。

## Layout Model / 排版模型

Record a book-level layout plan in `preproduction/stage1/production_spec.md` or a book-local layout note.
在 `preproduction/stage1/production_spec.md` 或书籍本地排版说明中记录全书排版计划。

```yaml
layout_plan:
  output_mode: "reflowable_epub_first_print_compatible"
  writing_mode:
    primary: "horizontal-tb"
    vertical_variant: "none | planned_separate_build | required"
  body:
    paragraph_style: "first_line_indent"
    first_line_indent: "2em"
    line_height: "1.55-1.8"
    paragraph_spacing: "0"
  headings:
    title_map: "metadata/title_map.yaml or production_spec.md"
    max_visible_levels: 3
    nav_uses_short_titles: true
  notes:
    marker_style: "[1] | (1) | superscript_number | circled_number | custom"
    numbering_scope: "per_chapter | whole_book"
    placement: "chapter_end | book_end | footnote_style"
    vertical_policy: "tested | not_applicable | separate_build_required"
  figures_tables:
    mobile_first: true
    print_compatible_captions: true
  css_policy:
    no_locked_body_font: true
    relative_units: true
    no_epub_only_meaning: true
```

## Page Design Rules / 页面设计规则

### Reflowable EPUB and print compatibility / Reflowable EPUB 与纸书兼容

- Prefer reflowable EPUB for prose books; use fixed layout only when meaning depends on exact page geometry.
  普通长文书优先使用 reflowable EPUB；只有内容意义依赖精确页面几何时才使用固定版式。
- Use semantic XHTML first and CSS second; do not choose headings, tables, lists, or notes purely for appearance.
  先保证 XHTML 语义正确，再用 CSS 呈现；不要为了外观滥用标题、表格、列表或注释标签。
- Use relative units such as `em`, `%`, and unitless `line-height`; avoid fixed-pixel body layout.
  正文排版优先使用 `em`、`%` 和无单位 `line-height`；避免固定像素正文版式。
- Preserve reader control of font, size, background, margins, and line spacing unless a specific element requires controlled rendering.
  默认保留读者调整字体、字号、背景、页边距和行距的能力；只有特定元素确有必要时才限制。
- Ensure important information remains visible in PDF and paper if EPUB interactivity disappears.
  确保 EPUB 交互消失后，重要信息在 PDF 和纸书中仍然可见。

### Body text / 正文

- For Chinese long-form prose, default to first-line indent rather than web-style blank-line paragraphs.
  中文长文正文默认使用段首缩进，而不是网页式段间空行。
- Do not combine first-line indent and large paragraph spacing for ordinary body paragraphs.
  普通正文段落不要同时使用段首缩进和大段间距。
- Use about `2em` first-line indent unless the book records a reason otherwise.
  默认段首缩进约 `2em`；如有例外必须在书籍排版计划中记录理由。
- Use comfortable line height, normally `1.55-1.8` for Chinese EPUB body text.
  中文 EPUB 正文行距通常使用 `1.55-1.8`，避免过密或过散。
- Do not hard-code body `font-family` by personal taste; let the reading system and user settings control fonts by default.
  不要凭个人审美写死正文字体；默认让阅读器和用户设置接管字体。
- Do not embed full Chinese fonts; subset and document license, size, and reason if a special font is necessary.
  不要嵌入完整中文字体；确需特殊字体时，必须子集化并记录授权、体积和理由。
- Avoid decorative body treatments such as letter spacing, forced justification hacks, continuous bold emphasis, excessive centering, or all-caps source residue.
  避免正文装饰化：字距拉开、强行两端对齐 hack、连续粗体、过度居中或残留原文全大写。

### Paragraph and section rhythm / 段落与章节节奏

- Decide intentionally whether the first paragraph after a heading, scene break, table, figure, or block quote should be indented.
  标题、场景分隔、表格、图片或引文后的首段是否缩进，要有统一策略。
- Use indentation for ordinary prose; use spacing and hierarchy for frontmatter, notes, lists, reference matter, and special forms.
  普通叙事正文用缩进组织段落；前置页、注释、列表、参考资料和特殊体裁可用间距与层级组织。
- Use a real section-break marker for scene breaks; do not preserve random hyphens, asterisks, or old print ornaments.
  场景分隔应使用正式分隔符；不要保留随机横线、星号串或旧书装饰符。
- Do not preserve OCR line breaks as paragraph breaks; paragraphs must follow meaning, not scan line width.
  不要把 OCR 行断当成段落；段落应按语义划分，而不是按扫描版行宽划分。
- Remove running heads, page numbers, printed TOC page lists, and image page lists from body text.
  正文中必须移除页眉、页码、纸书目录页码和插图页码清单。

### Titles and headings / 标题与标题层级

- Design the hierarchy, not the source punctuation.
  设计标题层级，不机械复制原文标点。
- Keep semantic structure consistent: book title > part title > chapter title > section title > subsection title > run-in heading.
  保持语义层级一致：书名 > 部/篇名 > 章名 > 节名 > 小节名 > 段内小标题。
- Do not let a subtitle or lower-level heading visually outrank its parent.
  副标题或下级标题的字号、字重和视觉强度不得超过上一级标题。
- Keep EPUB `nav.xhtml` concise; use short navigation titles rather than printed-TOC title chains.
  EPUB `nav.xhtml` 使用短目录题名，不使用纸书目录式长标题链。
- A Chinese title should normally contain no more than one `——`; convert long dash chains into main title, subtitle, or title note.
  中文标题通常不超过一个 `——`；长破折号链应拆成主标题、副标题或标题说明。
- Do not put source names, romanizations, or first-mention explanations into titles unless they are part of the title's meaning.
  除非原名/罗马字本身是标题意义的一部分，不要把它们或首次出现说明塞进标题。

### Traditional notes and markers / 传统注记与注号

- Prefer traditional visible note markers such as `[1]`, `(1)`, superscript numbers, or circled numbers when future print publication matters.
  未来考虑纸书出版时，优先使用传统可见注号，如 `[1]`、`(1)`、上标数字或带圈数字。
- Choose one marker family per book or per clearly defined section; do not mix `[1]`, `(1)`, `①`, and symbolic footnotes casually.
  每本书或每个明确定义的部分只选一种注号体系；不要随意混用 `[1]`、`(1)`、`①` 和符号脚注。
- Define numbering scope before production: restart per chapter, restart per part, or number through the whole book.
  制作前先定义编号范围：每章重排、每篇重排，或全书连续编号。
- Use EPUB internal links only on the visible note marker; the marker must still be meaningful when printed.
  EPUB 内链只增强可见注号；注号印出来后仍必须成立。
- Keep the marker compact and nonintrusive; notes must not visually dominate the sentence.
  注号应短小、不打断阅读；注释标记不能压过正文句子。
- Every note marker must resolve to one note, and every note must have a marker unless it is explicitly an unreferenced editorial note.
  每个注号必须对应一条注释；每条注释也必须有注号，除非明确标为未引用的编辑说明。
- Prefer chapter-end or book-end notes for dense translation notes; use footnote-style notes only when the reading flow benefits.
  译注密集时优先使用章末注或书末注；只有确实改善阅读时才使用脚注式短注。
- Do not make every proper noun a visible note or link; annotate only when readers need context, translation rationale, or cultural background.
  不要给每个人名地名都加注或链接；只在读者需要背景、译名理由或文化说明时加注。
- Keep glossary and index entries in backmatter; do not turn body text into a wiki-style network.
  术语表和索引应放在后置页；不要把正文做成 wiki 式词条网络。

### Vertical writing / 竖排排版

- Default to horizontal writing unless the book, target market, or user request clearly requires vertical layout.
  默认使用横排；只有书籍体裁、目标市场或用户明确要求时才做竖排。
- Treat vertical writing as a separate layout decision, not as a quick CSS toggle.
  竖排是独立版式决策，不是简单加一条 CSS 就完成。
- If vertical EPUB is required, record a separate `vertical_policy` and test actual reading systems; support varies.
  如需竖排 EPUB，必须记录独立 `vertical_policy` 并实测阅读器；不同阅读器支持差异较大。
- Use CSS such as `writing-mode: vertical-rl` and `text-orientation` only after checking punctuation, Latin text, numbers, note markers, tables, and figures.
  只有检查标点、西文、数字、注号、表格和图像后，才使用 `writing-mode: vertical-rl`、`text-orientation` 等 CSS。
- Avoid bracket-heavy note markers like `[123]` in vertical body text if they rotate or disturb rhythm; prefer a tested compact marker such as an upright number, circled number, or project-approved form.
  竖排正文中，如果 `[123]` 这类方括号注号旋转或破坏节奏，应改用实测可读的紧凑形式，如直立数字、带圈数字或项目批准形式。
- Keep horizontal alphanumerics, formulae, URLs, code, and wide tables out of vertical body flow when possible; move them to notes, tables, figures, or horizontal blocks.
  尽量不要把横排西文数字、公式、URL、代码和宽表硬塞进竖排正文；可移至注释、表格、图像或横排块。
- Build vertical PDF/print separately when necessary; do not force one EPUB CSS file to satisfy both horizontal and vertical editions without testing.
  必要时为竖排 PDF/纸书单独构建；不要未经测试就强迫一个 EPUB CSS 同时承担横排和竖排版本。

### Tables and figures / 图表

- Do not turn structured tables into images unless preserving an original scan is the point.
  除非目的就是保留原始影印，否则不要把结构化表格做成图片。
- Split very wide tables for mobile EPUB and future print; prefer several readable tables over one unreadable table.
  面向手机 EPUB 和未来纸书时，应拆分过宽表格；多个可读小表优于一个不可读大表。
- Provide every figure with a caption and useful alt text; complex figures need a longer explanation in body text, caption, or note.
  每张图必须有图注和有效 alt text；复杂图还需要正文、图注或注释中的较长说明。
- Make captions print-compatible: they must identify the figure/table even if EPUB links or hover behavior disappear.
  图注/表注必须纸书兼容：即使 EPUB 链接或 hover 消失，也能识别图表。
- Keep production audit columns, OCR status, and QA metadata out of reader-facing tables.
  生产审计列、OCR 状态和 QA metadata 不得进入读者可见表格。

### Frontmatter and backmatter / 前置页与后置页

- Make `book-info.xhtml` read like a compact publication information page, not a README, changelog, prompt log, or marketing page.
  `book-info.xhtml` 应像紧凑的出版信息页，不应写成 README、更新日志、prompt 日志或营销页。
- Put translator notes, edition notes, terminology principles, and source strategy into separate reader-facing pages only when readers benefit.
  只有读者确实受益时，才把译者说明、版本说明、术语原则和底本策略放入独立读者页。
- Keep workflow details, QA evidence, prompt history, and release evidence out of the reader-facing book.
  工作流细节、QA 证据、prompt 历史和 release 证据不得进入读者版书籍。
- Use backmatter for glossary, notes, bibliography, index, appendices, and source acknowledgments when they are reader-facing.
  读者需要看到的术语表、注释、书目、索引、附录和来源致谢应放在后置页。

### CSS and page behavior / CSS 与页面行为

- Keep CSS minimal and resilient across Readest, Apple Books, Kindle conversion, Moon+ Reader, WeChat Read import, and other reading systems.
  CSS 应尽量简洁，并能适应 Readest、Apple Books、Kindle 转换、静读天下、微信读书导入等不同阅读环境。
- Avoid styling that assumes one viewport size, such as fixed-height title pages, absolute-positioned body text, fixed-width tables, or large top margins that create blank screens.
  避免依赖单一视口的样式，例如固定高度标题页、绝对定位正文、固定宽表格或造成空白屏的大上边距。
- Use `break-inside: avoid` and similar CSS cautiously; reading-system support varies.
  谨慎使用 `break-inside: avoid` 等分页控制；阅读器支持并不一致。
- Record desired PDF/print page-break behavior separately instead of forcing EPUB to mimic one physical page.
  PDF/纸书分页需求应单独记录，不要强迫 EPUB 模拟实体页。
- Inspect generated XHTML, not only Markdown.
  必须检查生成后的 XHTML，不只看 Markdown 源文件。

## Workflow / 工作流

1. Classify the book type: prose, poetry, drama, academic, technical, illustrated, classical text, reference, or mixed.
   判断书籍类型：叙事、诗歌、戏剧、学术、技术、插图、古典文本、工具书或混合类型。
2. Draft a layout plan covering body paragraphs, headings, note markers, writing mode, figures/tables, frontmatter, backmatter, and print compatibility.
   起草排版计划，覆盖正文段落、标题层级、注号、横排/竖排、图表、前置页、后置页和纸书兼容性。
3. Normalize source artifacts: remove OCR line breaks, running heads, page numbers, printed TOC residue, decorative separators, and stale CSS.
   清理来源残留：OCR 行断、页眉、页码、纸书目录残留、装饰分隔符和旧 CSS。
4. Create or update title mapping for long or nested headings.
   为长标题或多级标题创建/更新标题映射。
5. Decide note marker style and numbering scope before inserting notes.
   插入注释前先确定注号样式和编号范围。
6. Decide whether vertical writing is out of scope, a separate future edition, or a required current output.
   明确竖排是排除、本次不做但未来单独版本，还是当前必须输出。
7. Convert tables and figures into mobile-readable and print-compatible structures.
   将表格和图像处理成手机可读、纸书也可排的结构。
8. Build a sample chapter and inspect the generated XHTML on a narrow viewport or EPUB reader when possible.
   构建样章，并尽可能在窄屏或 EPUB 阅读器中检查生成 XHTML。
9. Record exceptions in `production_spec.md`, chapter controls, or technical QA files.
   将例外写入 `production_spec.md`、章节控制文件或技术 QA 文件。
10. Reject final output if layout problems are visible in reader-facing XHTML or would block future print/PDF conversion.
    如果读者可见 XHTML 存在排版问题，或会阻碍未来 PDF/纸书转换，则不得通过最终输出。

## Gate Checklist / 门禁清单

Reject the layout if any item is true.
只要出现以下任一情况，就拒绝该排版：

- Body paragraphs are separated like a web article without a recorded reason.
  正文段落像网页文章一样用空行分隔，但没有记录理由。
- Body text locks fonts, sizes, line height, or colors in a way that defeats reader settings.
  正文锁死字体、字号、行距或颜色，导致读者设置失效。
- OCR line breaks, running heads, page numbers, or printed TOC residue remain in body text.
  正文残留 OCR 行断、页眉、页码或纸书目录残留。
- Heading tags are used for font size rather than semantic hierarchy.
  为了字号而滥用标题标签，而不是按语义层级使用。
- EPUB navigation uses long printed-title chains.
  EPUB 目录使用纸书式长标题链。
- A title, note, glossary, figure, or table depends on EPUB-only interactivity.
  标题、注释、术语表、图片或表格依赖 EPUB 专属交互才能理解。
- Note markers are inconsistent, missing, duplicated, over-linked, or unreadable in print.
  注号不统一、缺失、重复、过度链接，或印刷后不可读。
- Vertical writing is declared but punctuation, Latin text, numbers, note markers, tables, and reader support were not tested.
  已声明竖排，但没有测试标点、西文、数字、注号、表格和阅读器支持。
- Tables overflow narrow screens or would be unreadable in print.
  表格在窄屏溢出，或在纸书中不可读。
- Captions, figure labels, table labels, and body references disagree.
  图注、图号、表注、表号和正文引用不一致。
- CSS creates blank pages, fixed-width body text, or fragile page positioning.
  CSS 造成空白页、固定宽正文或脆弱的页面定位。

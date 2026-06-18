# Research Basis / 调研依据

This file records the compact evidence basis for `print-compatible-book-layout`. Load it only when revising or justifying the skill.
本文件记录 `print-compatible-book-layout` 的简要依据。只有修订或论证该 skill 时才读取。

## Sources consulted / 参考来源

- W3C Chinese Layout Requirements, <https://www.w3.org/International/clreq/>. Use for Chinese paragraph layout, punctuation positioning, line-start/line-end prohibition rules, book title marks, horizontal/vertical writing, and regional differences.
  W3C《中文排版需求》用于中文段落、标点位置、行首行尾禁则、书名号、横排/竖排和地区差异。
- W3C CSS Writing Modes Level 3, <https://www.w3.org/TR/css-writing-modes-3/>. Use for `writing-mode`, `text-orientation`, vertical flow, and mixed-script behavior.
  W3C CSS Writing Modes Level 3 用于 `writing-mode`、`text-orientation`、竖排流向和中西混排行为。
- W3C EPUB 3 Overview, <https://w3c.github.io/epub-specs/archive/epub32/spec/epub-overview.html>. Use for the principle that EPUB adapts to display, font size, and reading environment.
  W3C EPUB 3 Overview 用于确认 EPUB 应适应显示环境、字号和阅读设置。
- W3C EPUB 3 Reading Systems, <https://w3c.github.io/epub-specs/epub34/rs/>. Use for reflowable/pre-paginated expectations and reading-system variability.
  W3C EPUB Reading Systems 用于 reflowable/pre-paginated 预期和阅读器差异。
- DAISY Accessible Publishing Knowledge Base, <https://kb.daisy.org/publishing/docs/index.html>. Use for accessible EPUB practices based on web standards.
  DAISY Accessible Publishing KB 用于基于 Web 标准的无障碍 EPUB 实践。
- W3C WAI Headings tutorial, <https://www.w3.org/WAI/tutorials/page-structure/headings/>. Use for semantic heading ranks and navigability.
  W3C WAI Headings 用于语义标题层级和可导航性。
- Butterick's Practical Typography, <https://practicaltypography.com/summary-of-key-rules.html> and <https://practicaltypography.com/headings.html>. Use for body-text priorities and restrained heading design.
  Butterick's Practical Typography 用于正文优先级和克制的标题设计。
- Purdue OWL Chicago-style headings summary, <https://owl.purdue.edu/owl/research_and_citation/chicago_manual_18th_edition/cmos_formatting_and_style_guide/general_format.html>. Use for heading consistency and limiting excessive heading levels.
  Purdue OWL 的 Chicago headings 摘要用于标题一致性和避免过深标题层级。
- University of Chicago Turabian tip sheet, <https://www.chicagomanualofstyle.org/dam/jcr%3A134b5b19-bdc9-4d69-b4ad-0aa19fdc3730/Turabian-Tip-Sheet-7.pdf>. Use for same-style subhead levels and spacing around subheads.
  University of Chicago Turabian tip sheet 用于同级标题样式一致和标题前后间距。

## Distilled findings / 提炼结论

- EPUB prose should normally be reflowable; good EPUB layout respects user settings instead of freezing a print page.
  EPUB 长文通常应使用 reflowable 版式；好的 EPUB 排版尊重用户设置，而不是冻结纸书页面。
- Future print compatibility is structural: title hierarchy, notes, tables, figures, captions, and backmatter must make sense without links or scripts.
  未来纸书兼容是结构问题：标题层级、注释、表格、图片、图注和后置页必须在没有链接或脚本时仍然成立。
- Chinese long-form reading usually benefits from stable paragraph texture: first-line indent, comfortable line height, and controlled paragraph spacing.
  中文长文通常需要稳定的段落肌理：段首缩进、舒适行距和受控段间距。
- Project-approved visible note markers such as `[1]`, `(1)`, fullwidth `（1）`, and `注1` are safer for print-compatible books than invisible or popup-only notes.
  对纸书兼容项目来说，`[1]`、`(1)`、全角 `（1）` 和 `注1` 等项目批准的可见注号，比隐藏式或纯弹窗注释更安全。
- Vertical writing needs a separate policy and real testing; CSS support, punctuation orientation, Latin text, numbers, notes, tables, and reader support can all affect usability.
  竖排需要独立策略和真实测试；CSS 支持、标点方向、西文、数字、注释、表格和阅读器支持都会影响可用性。
- Typography systems rely on hierarchy and consistency; do not solve layout by ad hoc font-size changes.
  排版系统依赖层级和一致性；不要用临时改字号来解决结构问题。
- Tables and figures must be mobile-readable and print-readable; a valid EPUB manifest is not enough if the reader-facing layout is unreadable.
  表格和图片必须手机可读、纸书可排；仅通过 EPUB manifest 校验并不等于读者版排版合格。

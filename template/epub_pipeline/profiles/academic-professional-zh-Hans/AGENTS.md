# academic-professional-zh-Hans Agent Instructions / 学术与专业书简体中文控制模板 Agent 指令

This file is for agents using the `academic-professional-zh-Hans` profile overlay.

本文件供使用 `academic-professional-zh-Hans` 控制模板的 AI agent 读取。

## Mandatory Rules / 强制规则

- Overlay order must be `common -> {language-pair-template} -> profiles/academic-professional-zh-Hans`, followed by `modes/private_use` when applicable.
- 覆盖顺序必须是 `common -> {language-pair-template} -> profiles/academic-professional-zh-Hans`；如为私人自用项目，最后再覆盖 `modes/private_use`。

- This profile is for academic monographs, thesis-like books, and professional books in fields such as politics, economics, computer science, engineering, electronics, biology, chemistry, medicine, law, and other specialized domains.
- 本 profile 适用于学术专著、论文型书籍，以及政治学、经济学、计算机、机械、电子、生物、化学、医学、法律等专业领域书籍。

- Professional accuracy is not optional. Do not simplify away terms, variables, definitions, formulas, tables, citations, or domain distinctions.
- 专业准确性不是可选项。不得为了通俗而抹掉术语、变量、定义、公式、表格、引文或领域区分。

- Reader-facing Chinese must be Chinese-led. Do not leave unexplained source-language terms in Chinese sentences. Do not default to inline `Chinese term (source term)` in body text. If the original term is useful but not immediately necessary, place it in a footnote, endnote, chapter-end terminology note, or glossary, and leave only a short marker in the body. Variables, code names, standard acronyms, URLs, and bibliography entries may retain source forms, but still need Chinese context when they affect comprehension.
- 面向读者的中文正文必须以中文领头。不得在中文句子中留下未解释的源语言词，也不得默认在正文写成 `中文译名（原文术语）`。原词有保留价值但正文不必立刻显示时，应放入脚注、尾注、章末术语说明或术语表，正文只留简短标记。变量、代码名、标准缩写、URL 和书目条目可以保留原文形态，但只要影响理解，就必须提供中文语境。

- Readability is also not optional. A technically accurate translation that is needlessly awkward, sentence-for-sentence foreign, or hard to follow must be revised.
- 可读性同样不是可选项。技术上准确但不必要地拗口、逐句贴外文、难以跟上的译文必须润色。

- The intended tone is clear, rigorous, and reader-friendly: explain the chain of reasoning in natural Chinese while preserving the book's professional level.
- 目标语气是清楚、严谨、对读者友好：用自然中文讲清论证链条，同时保持专业书的水准。

- Each chapter must receive an academic readability audit under `qa/readability/{NNN_slug}.academic_readability_audit.md` or an equivalent consolidated chapter-by-chapter report.
- 每章必须有学术可读性审校记录，写入 `qa/readability/{NNN_slug}.academic_readability_audit.md`，或写入等效的逐章汇总报告。

- After each chapter translation or refinement pass, run the chapter completion gate. It must check the whole chapter package, not only the issue just edited: metadata, nav/TOC impact, body, notes, figures, formulas, tables, images, styles, reader-facing text, readability, terminology, comments/notes, generated XHTML/EPUB behavior, and private/public mode constraints when applicable.
- 每章翻译或精修完成后，必须执行章节完成门禁。检查范围必须覆盖完整章节包，不得只看刚修改的问题：metadata、nav/目录影响、正文、注释、图表、公式、表格、图片、样式、读者可见内容、通俗化、可读性、术语、注释/说明、生成 XHTML/EPUB 表现，以及适用时的私人/公开模式约束。

- Blocking issues include: unexplained foreign terms in reader-facing Chinese, unnecessary inline source-term parentheses that interrupt reading, half-translated institutional or technical names, unreadable proof/statistical explanations, mistranslated terms, over-simplified professional content, missing qualification or condition, formula/table explanation that no longer matches the source, and style that prevents a normal educated reader from following the argument.
- 阻塞问题包括：中文正文中出现未解释外文词、不必要的正文原词括注打断阅读、制度名或技术名半翻译、证明或统计解释读不懂、术语误译、过度通俗化导致专业内容丢失、限定条件缺失、公式/表格解释与原文不再一致，以及普通受教育读者无法跟上论证的表达。

- Do not write book-specific source text, translations, QA files, EPUB output, or metadata into this profile directory.
- 不得把具体书籍原文、译文、QA、EPUB 输出或 metadata 写入本 profile 目录。

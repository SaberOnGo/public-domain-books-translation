# Literary Refinement Policy / 文学精修策略

This file is language-neutral. It defines how a book moves from a technically valid EPUB to a publishable translation edition.

本文件是语言中立规则，用于定义一本书如何从“工程上可用的 EPUB”推进到“可出版质量的译本”。

## Scope / 适用范围

Use this policy for any source-target direction, for example French to English, Japanese to Spanish, Chinese to English, English to Spanish, German to Traditional Chinese, Arabic to Indonesian, or English to Simplified Chinese.

本策略适用于任何源语言到目标语言方向，例如法语到英语、日语到西班牙语、中文到英语、英语到西班牙语、德语到繁体中文、阿拉伯语到印尼语、英文到简体中文等。

## Core Principle / 核心原则

A valid EPUB is not automatically a finished book. Passing EPUBCheck, metadata validation, and publication lint only proves the file is structurally acceptable. A publishable translation also needs editorial refinement, target-language readability, title design, terminology control, and retrospective template updates.

一个 EPUB 能通过 EPUBCheck、metadata 校验和出版文本 lint，只能说明文件结构合格；这不等于书已经完成。可出版译本还必须完成编辑级精修、目标语言可读性打磨、标题设计、术语控制和模板经验回填。

## Mandatory Refinement Targets / 强制精修目标

Every book project must review:

每一本书都必须复核：

- Chapter title strategy: navigation labels, displayed headings, subtitles, and heading hierarchy.
- 章节标题策略：目录题名、页面标题、副标题和标题层级。

- Paragraph rhythm: overlong paragraphs, paragraph breaks, scene transitions, and list-like compression.
- 段落节奏：过长段落、分段、场景转换，以及清单式压缩。

- Sentence quality: fidelity, target-language fluency, cadence, and whether key sentences carry the force of the source.
- 句子质量：忠实度、目标语言流畅度、节奏，以及关键句是否保留原文力量。

- Typography and punctuation: target-language punctuation, abnormal spacing, legacy print artifacts, notes, appendices, lists, tables, and emphasis.
- 排版和标点：目标语言标点、异常空格、旧纸书遗留物、注释、附录、列表、表格和强调形式。

- Source paratext leakage: repeated chapter headings, running titles, next-section titles, page numbers, or table-of-contents fragments that remain in body text after segmentation.
- 原书副文本泄漏：分章后仍残留在正文里的重复章节标题、页眉题名、下一节标题、页码或目录碎片。

- Digital-source artifacts: Project Gutenberg transcriber notes, OCR correction notes, scanner comments, source-file boilerplate, or conversion logs that remain in the literary body.
- 数字来源工件：Project Gutenberg 转录者说明、OCR 修正说明、扫描者备注、源文件样板文字或转换日志误入文学正文。

- Terminology and names: people, places, ships, organizations, technical terms, historical terms, and first-mention notes.
- 术语和专名：人名、地名、船名、组织名、专业术语、历史称谓和首次出现说明。

- Reader experience: EPUB navigation, metadata, book info page, cover, file size, and mobile readability.
- 读者体验：EPUB 目录、metadata、书籍信息页、封面、文件体积和手机阅读表现。

## Refinement Phases / 精修阶段

### Phase 1: Book-Specific Goal / 阶段 1：本书目标

Create a book-specific goal document under `books/{book_id_slug}/goal/`.

必须在 `books/{book_id_slug}/goal/` 下建立本书专属目标文档。

The document must record concrete issues found in that book, not only generic quality slogans. It should list high-risk chapters, title problems, terminology risks, paragraphs that need review, and build-script work required before final output.

该文档必须记录这本书的具体问题，不能只写泛泛的质量口号。它应列出高风险章节、标题问题、术语风险、需要复核的段落，以及最终输出前必须完成的构建脚本工作。

### Phase 2: Editorial Pass / 阶段 2：编辑精修

For each high-risk chapter, create or update:

对每个高风险章节，必须创建或更新：

- `qa/refinement/{chapter}.refinement.md`
- `chapters/final/{chapter}.md`
- relevant terminology, title map, notes, or production-spec files
- 相关术语表、标题映射、译注或制作规格文件

The refinement record must explain what changed and why. It should distinguish source-faithfulness corrections from target-language polish and EPUB-format fixes.

精修记录必须说明修改了什么、为什么修改。应区分忠实度修正、目标语言润色和 EPUB 格式修复。

Before marking a chapter refined, compare the first and last body blocks against the source segmentation. Remove duplicated headings, running-title residue, or the next chapter/book title if those fragments entered the translated body by mistake.

标记某章精修完成前，必须对照源文分章检查正文开头和结尾。若重复标题、页眉残留或下一章/下一书名误入译文正文，必须删除。

Also inspect the final book blocks for digital-source artifacts such as transcriber notes, OCR errata, source-file boilerplate, and conversion logs. Decide whether to omit them from the reader-facing EPUB or move them to a clearly labeled source-production note.

还必须检查全书末尾是否残留数字来源工件，例如转录者说明、OCR 勘误、源文件样板文字和转换日志。应明确决定是从面向读者的 EPUB 中删除，还是移入清楚标注的来源制作说明。

Appendices that are primarily name lists, catalogues, indexes, or tabular source material may keep a list-like or preformatted presentation when that best preserves spelling, alignment, and lookup value. Paragraph-length gates should not blindly fail such appendices; instead, record the presentation decision in the book QA file and verify mobile readability in the generated EPUB.

主要由姓名表、目录表、索引或表格型源材料构成的附录，可以在最能保留拼写、对齐和检索价值时继续使用列表式或预格式化呈现。段落长度门禁不应机械判定这类附录失败；应在本书 QA 文件中记录呈现选择，并在生成的 EPUB 中复核移动端可读性。

### Phase 3: Template Backfill / 阶段 3：模板回填

Reusable lessons must be copied back into the appropriate layer:

可复用经验必须回填到合适层级：

- `template/epub_pipeline/common/`: language-neutral EPUB workflow, title design, QA gates, path rules, metadata, build and validation rules.
- `template/epub_pipeline/common/`：语言中立的 EPUB 流程、标题设计、QA 门禁、路径规则、metadata、构建和校验规则。

- `template/epub_pipeline/targets/{target}/`: target-language typography, punctuation, readability, review rubrics, and local-language style standards.
- `template/epub_pipeline/targets/{target}/`：目标语言排版、标点、可读性、审校规则和本地语言文体标准。

- `template/epub_pipeline/{source-target}/`: source-language interference, source-to-target title handling, culture-specific terms, prompts, and workflow warnings.
- `template/epub_pipeline/{source-target}/`：源语言干扰、源到目标语言标题处理、文化专名、prompt 和流程警告。

Book-specific findings may overlap with template rules. This is acceptable and often necessary because the book project guides work on one book, while templates guide future books.

本书专属发现可以与模板规则有一定重复。这是允许且必要的，因为书籍工程指导某一本书，模板指导未来所有同类书。

## Hard Gate / 硬门禁

A book must not be marked `DONE` if:

出现以下情况时，不得把书籍标记为 `DONE`：

- the book-specific refinement goal has not been created when major editorial issues were found;
- 发现重大编辑问题后，尚未建立本书专属精修目标；

- known reusable lessons were not added back to the relevant template layer;
- 已知可复用经验没有回填到对应模板层；

- title design, paragraph refinement, terminology, or EPUB presentation issues remain open without a revision route;
- 标题设计、段落精修、术语或 EPUB 呈现问题仍未关闭，也没有回退路线；

- validation only proves EPUB structure, while translation quality has not passed editorial review.
- 只证明了 EPUB 结构合格，但译文质量尚未通过编辑级审查。

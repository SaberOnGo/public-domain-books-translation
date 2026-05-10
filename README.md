# LifeBook 书坊：公版书翻译与 EPUB 制作协作项目

LifeBook 书坊是一个面向公版书的翻译与电子书制作项目。我们希望把一些已经进入公版、但中文世界还不容易读到的书，重新整理、翻译、审校，并制作成可阅读的 EPUB。

这里的“翻译”不是把原文丢给 AI 后直接发布。AI 可以帮我们做很多重复工作，例如清洗文本、初译、分章、生成术语表、检查漏译、构建 EPUB；但一本书要真正好读，仍然需要人来判断：句子顺不顺，人物名是否统一，历史称谓是否妥当，译文有没有机械味，书在手机阅读器里看起来是否舒服。

如果你爱读书、愿意翻几段文字、愿意帮忙校对、能发现错别字、喜欢查资料，或者只是愿意试读一章并指出哪里读不下去，都可以参与。

This repository is also documented in English below. The current working materials are mostly Chinese-first because the first finished book is an English-to-Chinese public-domain translation, but the project is not limited to that direction. Future books may include other foreign-language public-domain works translated into Chinese, or Chinese public-domain works translated into English.

## 项目想做什么

我们想做几件具体的小事：

- 从可靠来源选择公版书，例如 Project Gutenberg、Wikisource、Standard Ebooks 等。
- 在翻译前先保存版权与来源证据，避免使用现代出版社版本、现代注释版或不明来源文本。
- 让 AI 做可追踪的初译和检查，而不是一次性生成不可复核的整本译文。
- 把每章拆成原文、初译、终稿、审校报告、术语报告等可检查文件。
- 让更多人可以只参与一小段工作：查资料、统一术语、审一章、试读 EPUB、检查目录和封面。
- 最终生成格式有效、读起来舒服、来源清楚的 EPUB。

我们不想把这个项目说得很宏大。它更像一个小型书坊：有人找书，有人翻译，有人校对，有人排版，有人试读。每个人做一点，书就会比一个人单独做得更稳。

## 最简单怎么开始

普通参与者不需要手动填写一堆工程文件。最简单的方式是：把模板目录和一本书的公版来源交给 AI，让 AI 按流水线自动创建书籍工程、填写元数据、抓取原文、分章、翻译、审校、排版和生成 EPUB。

你通常只需要告诉 AI 三件事：

- 想做哪本书。
- 公版来源 URL，如果有的话。
- 翻译方向，例如英文到中文、中文到英文、法文到中文。

例如，可以这样发给 AI：

```text
/goal 按 D:\project\49_public-domain-books-translation\books\pg20923_a_negro_explorer_at_the_north_pole 工程制作《黑人北极探险家》中文 EPUB，
从 https://www.gutenberg.org/ebooks/20923 抓取原文，
按 00-08 流水线完成翻译、校对、排版、生成 output/book.epub，并通过 epubcheck。
```

如果你只知道书名，不知道 URL，也可以先让 AI 帮你找可靠公版来源：

```text
请帮我查找《某本书》的可靠公版原文来源，优先 Project Gutenberg、Wikisource、Standard Ebooks。
确认来源和版权风险后，再用 epub_pipeline_template_zh_en 创建 books/ 下的新书工程。
```

AI 会自动处理大部分工程文件。人类更适合在关键节点介入：看研究是否靠谱、试译是否好读、术语是否统一、某章是否需要返工、样章 EPUB 在阅读器里是否舒服。

## 当前仓库里有什么

### `epub_pipeline_template_zh_en/`

这是制作一本书时要复制使用的模板目录。不要直接在这个目录里做某本书。这个目录主要是给 AI 读取和执行的，人类一般不需要逐个文件去看；普通参与者只需要知道“做新书时让 AI 复制它，不要改模板原件”。

里面包含：

- `README_ZH_EN.md`：模板说明。
- `MASTER_PROMPT_ZH_EN.md`：启动 AI 制作一本书时可以使用的主控提示词。
- `PIPELINE_SPEC_ZH_EN.md`：流水线规范，说明每一步的输入、输出、状态和目录约定。
- `prompts/`：从抓取原文、分章、研究、试译、翻译、审校到构建 EPUB 的分步提示词。
- `metadata/`：书籍信息、版权核查、来源证据、文体画像等模板文件。
- `chapters/`：章节原文、初译、终稿的放置位置。
- `qa/`：忠实度、可读性、术语、意象词、章节门禁等审校文件。
- `preproduction/`：封面、版式、metadata、样章 EPUB 等出版前规格。
- `reviews/`：独立评审与评分表。
- `output/`：最终 EPUB 与校验结果。
- `retrospective/`：一本书完成后的复盘和模板改进建议。

### `books/`

这里放每一本具体书的工程目录。每本书都应该是从模板复制出来的独立目录。

当前已有一本样例书：

`books/pg20923_a_negro_explorer_at_the_north_pole/`

这本书基于 Project Gutenberg #20923，作者 Matthew A. Henson，中文题名暂作《黑人北极探险家》。它已经完成：

- 原文来源与版权初筛记录。
- 26 个章节的原文、译文和终稿。
- 术语、文体、预翻译、章节审校等质量文件。
- EPUB 构建。
- EPUBCheck 校验，结果为 fatal=0、error=0、warning=0。

注意：样例书证明这套流程可以跑通，但不代表所有章节已经经过人工出版编辑终审。公开发布前，仍建议继续做逐章人工精修、专名统一和试读反馈。

### `translation_quality_framework/`

这是翻译质量框架。它不绑定某一本书，用来说明“好译文”应该怎样被研究、试译、审校和返工。

重点包括：

- 翻译前要做作者、时代、文体、术语、敏感点研究。
- 正式翻译前要做预翻译试译，试译不通过就不能批量翻译。
- 每章要检查准确性、中文性、文学/叙事效果和出版性。
- 不把“通顺”误认为“好译文”。
- 不保存或使用受版权保护的现代译本作为翻译来源。

### `doc/public/`

这里放公开的选题、版权初筛、候选书报告等资料。它们可以帮助我们选择下一本适合制作的公版书。

## 谁可以参与

你不需要会写代码，也不需要懂 EPUB。下面这些工作都很有价值。

### 1. 试读者

适合喜欢读书的人。

你可以：

- 打开 `books/.../output/book.epub` 试读。
- 记录哪一章读起来不顺。
- 标出明显别扭的句子。
- 反馈人物、地点、术语哪里让你困惑。
- 检查手机、平板、电脑阅读器里的排版是否舒服。

最简单的反馈格式：

```text
书名：
章节：
原句或位置：
问题：这里读起来不顺 / 疑似错译 / 术语前后不一致 / 排版有问题
建议：如果有建议可以写，没有也没关系
```

### 2. 校对者

适合细心的人。

你可以检查：

- 错别字。
- 标点问题。
- 重复段落。
- 漏译段落。
- 人名、地名、船名、部落名是否统一。
- 章节标题是否前后一致。

### 3. 译文审校者

适合懂原文或愿意对照原文的人。

你可以做：

- 对照 `chapters/src/` 原文和 `chapters/final/` 终稿。
- 检查是否漏译、误译、数字错误、方向错误。
- 判断语气是否偏离原文。
- 指出机械直译、过度发挥、省字式翻译。
- 帮忙改写一小段，让它更像自然中文或自然英文。

### 4. 术语和资料协作者

适合喜欢查资料的人。

你可以帮助：

- 查作者、出版年份、历史背景。
- 统一专有名词。
- 补充地名、人名、民族称谓、历史称谓说明。
- 检查某本书是否真的公版。
- 确认来源文本是否来自可靠公版来源。

### 5. EPUB 试制和技术协作者

适合愿意折腾工具的人。

你可以帮助：

- 构建 EPUB。
- 检查封面、目录、metadata。
- 运行 EPUBCheck。
- 修复 CSS、标题层级、图片体积、阅读器兼容性。
- 改进自动化脚本和模板。

## 一本书怎么从 0 开始制作

下面是给新手看的流程。它不是要求你手动做完每一步，而是告诉你 AI 会做什么、你可以在哪里检查和参与。

### 第一步：选书

先从 `doc/public/` 里的候选书报告看起，或者自己提出一本书。

选书时要先问：

- 原书是不是公版？
- 作者去世年份是否足够早？
- 使用的文本来源是否可靠？
- 有没有现代编辑、现代注释、现代插图等可能受版权保护的内容？
- 是否已经有很多成熟中文译本或英文译本？
- 这本书是否适合现在投入时间？

重要提醒：Project Gutenberg 常说 “Public domain in the USA”。这只说明美国维度，不能自动等同于全球都无风险。正式公开发布前，仍应按目标地区复核。

### 第二步：把书名或公版 URL 交给 AI

你不需要自己复制目录、填写 YAML、写工程文件。把书名、公版 URL 和翻译方向告诉 AI 即可。

如果已经有可靠来源，可以这样说：

```text
请用 epub_pipeline_template_zh_en 创建一本新的书籍工程。
原文来源：https://www.gutenberg.org/ebooks/20923
翻译方向：英文到中文
目标：生成可阅读的中文 EPUB，并通过 EPUBCheck。
```

如果想参考已经跑通的样例工程，可以补一句：

```text
请参考 books/pg20923_a_negro_explorer_at_the_north_pole 的工程结构和质量控制方式。
```

AI 应该自动完成：

- 复制模板。
- 创建 `books/{book_id_or_author_title_slug}/`。
- 填写项目说明、metadata、来源证据和版权核查文件。
- 抓取或读取原文。
- 清洗、分章、建立术语表和文体画像。
- 进入试译、分章翻译、审校和 EPUB 制作。

新书工程会放在：

```text
books/{book_id_or_author_title_slug}/
```

例如：

```text
books/pg20923_a_negro_explorer_at_the_north_pole/
```

### 第三步：让 AI 自动生成来源和项目说明

这些文件主要由 AI 自动填写，人类只需要复核，不需要手动从零填写。

AI 会把关键信息写入：

- `PROJECT_BRIEF_ZH_EN.md`
- `metadata/book.yaml`
- `metadata/rights_checklist.md`
- `metadata/source_evidence.md`

你可以检查这些问题：

- 书名、作者、生卒年是否正确。
- 原文来源 URL 是否可靠。
- 版权判断是否写得谨慎，没有把“美国公版”直接说成“全球公版”。
- 翻译方向是否正确。
- 有没有误用了现代出版社版本、现代注释版或盗版来源。

### 第四步：在人类可干预点检查

AI 可以全流程自动跑，但最好在几个节点请人看一眼。你不需要懂全部工程，只要打开对应文件，提出“通过 / 不通过 / 哪里不对”即可。

#### 译前研究阶段

看这些文件：

- `metadata/book_specific_translation_research.md`
- `metadata/style_profile.md`
- `glossary/terms.csv`
- `glossary/style_guide.md`

适合检查：

- 作者、时代、题材理解是否靠谱。
- 文体判断是否符合原书。
- 人名、地名、术语是否统一。
- 历史称谓、民族称谓、宗教或文化内容是否需要译注。

#### 预翻译阶段

看这个文件：

- `qa/pretranslation/pretranslation_report.md`

适合检查：

- 试译是否像自然中文或自然英文。
- 有没有明显机器味。
- 难句、关键句、开篇语气是否处理得好。
- 如果试译不好，要求 AI 回到研究或试译阶段返工，不要直接翻整本。

#### 章节翻译控制阶段

看这些目录：

- `chapters/src/`：原文。
- `chapters/translated/`：初译。
- `chapters/final/`：通过审校后的终稿。
- `qa/chapter_controls/`
- `qa/fidelity/`
- `qa/readability/`
- `qa/terminology/`
- `qa/imagery/`
- `qa/gates/`

适合检查：

- 有没有漏译、误译。
- 人名、地名、数字、方向是否错误。
- 读起来是否顺。
- 是否有机械直译、过度发挥、省字式翻译。
- 术语是否前后一致。

#### 预制作阶段 1

看这个文件：

- `preproduction/stage1/production_spec.md`

适合检查：

- 书名、作者、译制信息是否正确。
- 封面方向是否合适。
- metadata 是否包含来源、公版说明、LifeBook 书坊信息。
- 标题、目录、版式、字体策略是否适合阅读器。

#### 预制作阶段 2

看这些文件：

- `preproduction/stage2_sample/sample_book.epub`
- `preproduction/stage2_sample/sample_review.md`

适合检查：

- 样章 EPUB 能否打开。
- 手机窄屏下标题是否太大。
- 正文行距、缩进、封面、目录是否舒服。
- 如果样章不好看，让 AI 先修样章，不要急着生成整本。

#### 全书 EPUB 和最终评审

看这些文件：

- `output/book.epub`
- `output/epubcheck.json` 或 `output/epubcheck.log`
- `reviews/agent_a/review.md`
- `reviews/agent_b/review.md`
- `reviews/scorecards/final_quality_score.md`
- `reviews/revision_route.md`

适合检查：

- EPUB 是否能在常用阅读器打开。
- EPUBCheck 是否 fatal=0、error=0。
- 独立评审是否还有必须修的问题。
- 如果还有 P0/P1/P2 问题，应让 AI 回到对应阶段返工。

### 第五步：让 AI 继续，直到生成 EPUB

如果你不想参与中间阶段，也可以让 AI 全自动跑完。只要记住最终至少检查这几个结果：

- `output/book.epub` 存在。
- EPUB 可以打开。
- `output/epubcheck.json` 或 `output/epubcheck.log` 没有 fatal/error。
- `metadata/rights_checklist.md` 没有明显版权风险。
- 至少有人试读过一部分正文。

## 如果你只想帮一点点

完全可以。

你可以只做下面任意一件事：

- 试读 3 页。
- 检查一个章节标题。
- 帮忙确认一个人名怎么译。
- 找出一处错别字。
- 对照一段原文看有没有漏译。
- 在手机阅读器里打开 EPUB，看看排版是否舒服。
- 查一本候选书的作者死亡年份。
- 帮忙确认某个来源是不是公版。

这些小工作累积起来，就是一本书质量提升的来源。

## 提交反馈的建议方式

如果你熟悉 GitHub：

- 可以开 Issue。
- 可以提交 Pull Request。
- 可以直接评论某个文件。

如果你不熟悉 GitHub：

- 复制有问题的句子。
- 写明书名和章节。
- 用普通文字说明哪里不顺。
- 发给项目维护者即可。

反馈不需要完美。能指出“这里我读不懂”“这里像机器翻译”“这里名字前后不一样”，就已经很有帮助。

## 翻译方向

当前模板名里有 `zh_en`，主要表示模板文档是中英双语，并且第一本样例是英文公版书译成中文。

未来可以支持更多方向：

- 英文公版书译成中文。
- 法文、德文、日文等其他外文公版书译成中文。
- 中文公版书译成英文。
- 中文公版书译成其他语言。

无论方向如何，原则不变：

- 先确认版权和来源。
- 先做译前研究。
- 先试译，再批量翻译。
- 初译不能直接发布。
- 译文必须经过人和 AI 的多轮检查。
- EPUB 必须经过格式校验和实际试读。

如果是中文译英文，需要相应调整：

- `metadata/style_profile.md` 中的目标文体。
- `glossary/terms.csv` 中的术语方向。
- `qa/readability/` 的审校标准。
- `prompts/` 中关于目标语言的表述。
- EPUB metadata 的语言字段，例如 `en` 或 `en-US`。

## 重要原则

### 1. 不使用已有现代译本作为翻译来源

即使网上能找到中文译本，也不要把它复制进项目，不要让 AI 参考、改写或对照它。我们只从公版原文重新翻译。

### 2. 不使用盗版来源

不要从盗版站、网盘、非授权 EPUB 站下载文本作为底本。

### 3. 不把 AI 初稿当成成品

AI 初稿只是起点。真正重要的是审校、返工、统一、试读和出版前检查。

### 4. 保留失败记录

如果某次试译失败，应该记录失败原因。失败记录会帮助后面的人少走弯路。

### 5. 模板目录只读

`epub_pipeline_template_zh_en/` 是模板。做新书时让 AI 复制它，不要直接在里面写某本书的数据。普通参与者不需要阅读模板里的每个提示词文件。

## 给 AI 助手的最小启动提示词

如果你想让 AI 帮你从一本公版书开始，可以使用下面这段，然后替换书名和来源。

```text
请在本仓库中制作一本新的公版书翻译工程。

模板目录：epub_pipeline_template_zh_en
新书目录：books/{请用书号或书名生成清晰目录名}
原文来源：{填写 Project Gutenberg / Wikisource / Standard Ebooks 等可靠来源 URL}
翻译方向：{例如 英文到中文 / 中文到英文 / 法文到中文}

要求：
1. 不要直接修改模板目录。
2. 先复制模板到新书目录。
3. 先做来源与版权核查，不能确认公版就停止。
4. 不要使用已有现代译本作为翻译来源。
5. 先做译前研究、术语表、文体画像和预翻译试译。
6. 预翻译没有 PASS，不要批量翻译。
7. 每章必须经过忠实度、可读性、术语、意象词和章节门禁检查。
8. 最终生成 EPUB，并运行 EPUBCheck 或等价校验。
9. 记录所有关键产物路径，方便其他人继续审校。
```

## English Guide

LifeBook Shufang is a collaborative project for translating public-domain books and producing readable EPUB editions.

The goal is not to publish raw AI output. AI can help with repetitive work: cleaning source text, splitting chapters, drafting translations, creating glossaries, checking omissions, and building EPUB files. But good books still need human judgment. People are needed to read, question, correct, polish, verify names and terms, and test the final book in real reading apps.

You do not need to be a programmer to help. Reading a chapter and saying “this part is confusing” is already useful.

### What Is In This Repository

- `epub_pipeline_template_zh_en/`: the reusable book-production template. It is mainly for AI agents to read and execute; human contributors usually do not need to inspect every file in it.
- `books/`: one folder per actual book project.
- `translation_quality_framework/`: translation quality rules, review workflow, prompt templates, and quality gates.
- `doc/public/`: public notes for book selection, copyright screening, and candidate lists.

The current example book is:

```text
books/pg20923_a_negro_explorer_at_the_north_pole/
```

It is based on Project Gutenberg #20923, Matthew A. Henson's *A Negro Explorer at the North Pole*. The project includes source evidence, rights notes, chapter files, review files, a generated EPUB, and an EPUBCheck report with zero fatal errors, zero errors, and zero warnings.

### How You Can Help

You can help even if you only have a little time.

Useful contributions include:

- Read a few pages and report awkward passages.
- Compare one source paragraph with its translation.
- Check names, places, and recurring terms.
- Find typos or punctuation issues.
- Test an EPUB on a phone, tablet, or e-reader.
- Research whether a candidate book is truly public domain.
- Improve cover, metadata, layout, or EPUB compatibility.
- Review whether a chapter sounds like natural Chinese or natural English.

Simple feedback format:

```text
Book:
Chapter:
Location or sentence:
Problem:
Suggestion, if any:
```

### Easiest Way To Start A New Book

Most people do not need to manually copy folders or fill in metadata files. Give an AI assistant the template folder, a public-domain source URL if you have one, and the translation direction. The AI should create the book project, fill in project metadata, document source evidence, run the translation pipeline, and build the EPUB.

Minimal prompt:

```text
Please create a new public-domain book translation project.

Template folder: epub_pipeline_template_zh_en
Source URL: {Project Gutenberg / Wikisource / Standard Ebooks URL, if known}
Translation direction: {for example English to Chinese, Chinese to English, French to Chinese}
Goal: produce output/book.epub and pass EPUBCheck.

Use books/pg20923_a_negro_explorer_at_the_north_pole as the reference project structure.
```

Human contributors can step in at clear checkpoints:

- Book research: `metadata/book_specific_translation_research.md`, `metadata/style_profile.md`, `glossary/terms.csv`.
- Pre-translation trial: `qa/pretranslation/pretranslation_report.md`.
- Chapter review: `chapters/src/`, `chapters/translated/`, `chapters/final/`, and `qa/`.
- Preproduction stage 1: `preproduction/stage1/production_spec.md`.
- Preproduction stage 2: `preproduction/stage2_sample/sample_book.epub` and `sample_review.md`.
- Final output: `output/book.epub`, `output/epubcheck.json`, and review files under `reviews/`.

### Translation Directions

The first example is English to Chinese, but the project can grow beyond that:

- English public-domain books into Chinese.
- Other foreign-language public-domain books into Chinese.
- Chinese public-domain books into English.
- Chinese public-domain books into other languages.

For each direction, the same principles apply: verify rights, document sources, research before translating, test samples first, review chapters carefully, and validate the final EPUB.

### Rules We Care About

- Do not use modern copyrighted translations as source material.
- Do not use pirate websites or unclear EPUB downloads.
- Do not treat raw AI output as publishable text.
- Do not write real book data into the template folder.
- Keep review records and failure records.
- Prefer small, reviewable improvements over untraceable whole-book rewrites.

### Minimal Prompt For An AI Assistant

```text
Please create a new public-domain book translation project in this repository.

Template folder: epub_pipeline_template_zh_en
New book folder: books/{clear_book_id_or_title_slug}
Source URL: {reliable public-domain source URL}
Translation direction: {for example English to Chinese, Chinese to English, French to Chinese}

Rules:
1. Do not modify the template folder directly.
2. Copy the template into the new book folder first.
3. Verify source and rights before translating.
4. Do not use modern copyrighted translations as source material.
5. Create book research, glossary, style profile, and pre-translation trials first.
6. Do not batch-translate chapters until the sample trial passes.
7. Review every chapter for fidelity, readability, terminology, imagery, and gate status.
8. Build the final EPUB and run EPUBCheck or an equivalent validator.
9. Record all important output paths so other contributors can continue reviewing.
```

## License And Rights Notes

Each source book must be checked separately. A text may be public domain in one country but not automatically public domain everywhere.

Project Gutenberg texts are often public domain in the United States. Before wider distribution, contributors should review the copyright status for the target region.

Translations, notes, covers, formatting, and EPUB packaging created in this project may have their own rights status. Project maintainers should define the release license clearly before public distribution.

## A Practical Invitation

If you like books and want to help bring overlooked public-domain works to more readers, you can start small. Read a chapter. Mark one awkward sentence. Check one name. Test one EPUB. A book improves through many small acts of attention.

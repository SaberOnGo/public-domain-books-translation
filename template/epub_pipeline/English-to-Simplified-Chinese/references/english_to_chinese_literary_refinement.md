# 英文到简体中文文学精修策略 / English-to-Simplified-Chinese Literary Refinement

本文件面向 `English-to-Simplified-Chinese` 模板。它把通用精修策略落实到英文公版书译入简体中文的场景，供 AI 在翻译、审校、返工和最终 EPUB 输出前读取。

This file applies the common refinement policy to English public-domain books translated into Simplified Chinese.

## 基本判断 / Basic Judgment

英文到简体中文的 EPUB 不能只满足“意思大概对”和“文件能打开”。中文读者最终读到的应是一本有中文节奏、历史质地和出版完成度的书。

An English-to-Chinese EPUB is not finished just because the meaning is mostly preserved and the file opens. It must read like a finished Chinese book while preserving the historical texture of the source.

## 精修重点 / Refinement Focus

### 1. 标题 / Titles

- 旧英文纸书目录常用 `--` 串联小题，不能机械译成多个中文 `——`。
- 必须读取完整英文原标题，不得使用被分章脚本截断的标题。
- 必要时建立 `metadata/chapter_title_map.yaml`，包含 `source_full`、`nav_title`、`display_title`、`subtitle`、`title_note`。
- `nav.xhtml` 使用短目录题名，页面内再用主标题和副标题承载完整信息。
- 如果英文原书章节只有罗马数字、阿拉伯数字或简单编号，不得为中文 EPUB 自创读者可见小标题；章节内容概括只能放入 `title_note`、制作说明或 QA 记录。

English printed-title chains with `--` must not be mechanically converted into Chinese em-dash chains. Use a title map when needed. If the source chapter only has a number or Roman numeral, do not invent a visible Chinese subtitle; keep summaries in notes or QA.

### 2. 句子 / Sentences

- 先保事实，再调中文；不得为了“雅”改写事实、情绪、动作强度或叙述立场。
- 英文长句不应直接搬成中文长串；要按中文阅读顺序重排，但保留因果、转折、递进。
- 英文短促句也不能被压成中文动作清单。中文可以紧，但必须像人在叙述。
- 关键句要复核“信、达、雅”：事实不误，中文自足，声调与原文功能相当。

Refinement must preserve facts first, then improve Chinese rhythm. Short source sentences should not become dry Chinese bullet-like prose.

### 3. 段落 / Paragraphs

- 超过 300 字的普通叙述段应进入人工或 AI 专门复核；超过 500 字通常要判断是否拆段。
- 拆段不能破坏原文逻辑。按场景转换、动作阶段、时间推进、人物判断或情绪转折拆分。
- 不能为了“看起来整齐”随意拆段；也不能保留旧纸书中不适合 EPUB 的巨段。

Long paragraphs should be reviewed for mobile readability, but paragraph breaks must respect scene, logic, and narrative rhythm.

### 4. 专名、历史称谓与译注 / Names, Historical Terms, and Notes

- 人名、地名、船名、机构名必须统一。正文中的陌生人名或陌生地名不强制汉译，可以按 `glossary/proper_nouns.csv.display_policy` 保留英文原名，例如 `Professor Marvin`、`Grant Land`。章节标题和副标题中的人名优先使用中文译名，标题、目录、页眉、图注索引等标题性位置不计入“正文首次出现”；如果人名第一次被读者看到是在标题里，标题仍只用中文译名，原文名词应按专名译表延后到正文第一次自然出现处、译注或术语表。
- 普通名词、器物名、衣物名、材料名和动作名应译成中文，不得写成 `source term（中文释义）`，也不得写成 `中文词（source term）`。专名首次出现保留原文的规则只适用于 `glossary/proper_nouns.csv` 中记录的重点专名；普通名词能准确翻译时，不应附加原文词。
- 历史称谓、制度名、身份称谓、专业术语和文化负载词也不应默认写成 `中文译名（source term）`。正文优先使用中文译名或准确意译；原词、定义、译名选择理由和必要背景优先放入本章译注、章末注或术语表。正文首次出现处可使用短注号，如 `王室领主[术语]`、`贤人会议[术语]`，而不是把 `thegns`、`witenagemot` 等源语词直接塞进正文。
- 对 `thegn` / `thane` 这类盎格鲁-撒克逊制度身份词，正文不推荐音译为“塞恩”。在政治史、土地和军事义务语境中，应按上下文译为“王室领主”“领主近臣”“盎格鲁-撒克逊领主”等能体现土地、等级和服役义务的中文；术语说明再写明原文为 `thegns`，又作 `thanes`。只有专门讨论词源、不同译名或英文文献术语时，才可在正文短括注原词。
- 只有三类例外可以在正文使用短括注原词：一是不保留原词会造成明显误解；二是该原词本身是作者论证对象；三是学界译名分歧或本书术语体系需要读者当场知道原词。每个例外都必须在 `glossary/terms.csv`、`glossary/proper_nouns.csv`、本章译注或 `qa/chapter_controls/{chapter}.control.md` 中记录理由。不得为了“显得严谨”而让正文大面积夹杂英文、古英语、拉丁文或其他源语词。
- 注号只能使用 `[1]`、`(1)` / `（1）`、`注1` 三类体系；`尼禄（Nero）` 这样的专名原文括注不是注号，策略 `5` 才另加合规注号。
- 历史称谓应忠实呈现原书时代语境，同时用克制译注帮助现代读者理解。
- 不得在同一本书里随意切换称谓，例如一处用旧称、一处用现代称，除非译注策略明确。

Names and historically loaded terms need a stable first-mention and note policy. Less familiar personal names and place names may stay in English; if translated, the first occurrence must preserve the original English name.

### 4a. EPUB 后分层随机抽检 / Post-EPUB Stratified Random Spot Checks

- 第一版全书 EPUB 生成后，以及每轮 EPUB 后精校完成后，必须运行 `npm run review:random-samples` 或等效脚本，从 `chapters/final` 和读者可见资源生成分层随机审计单元样本。
- 至少 2 个独立 Agent 检查样本，不能由主执行 AI 人工挑选内容。
- 抽样层至少包括正文段落、表格、图片、公式/证明块、图注和注释；实际存在的表格、图片、公式不得被普通段落抽样替代。
- 抽检 Agent 必须假设自己是认真阅读本书的中文读者，逐项判断：中文是否读得懂、是否忠实于英文公版原文、是否有英文句法硬搬、是否无依据润饰、专名/称谓/译注/标题策略是否一致，表格/图片/公式是否正确。
- 每个样本 0-100 分；`80` 只是硬失败线，低于 80 必须 FAIL。最终 release/private artifact 默认要求每个 Agent `average_score >= 92`、`lowest_score >= 88`，且每个抽中样本都有逐项评分行。80-87 代表可读但仍需精修；88-91 代表较好但未达最终优秀门槛。
- 评语中若出现“可读但略硬”“较硬”“偏密”“略抽象”“稍显解释化”“英式分析腔”等，不得只当作温和瑕疵后给优秀分；应计入 `style_debt` 或相应问题族，反复出现时回到中文独立润色和英语句法重组。
- 任一样本存在读不懂、事实误解、叙述关系误判、英文腔明显、术语/专名/译注/表格/图片/公式错误，即使平均分达标，也必须回到精校或更早阶段修复；修复后在旧轮次关闭问题，并使用新 seed 重新生成样本。

Stratified random spot checks are a hard post-EPUB gate. They test whether the book reads as Chinese and whether reader-facing tables, figures, formulas, captions, and notes survive publication production.

### 5. 标点和排版 / Punctuation and Typography

- 普通中文正文不得出现 ASCII 分号 `;`。
- 中文分号 `；` 只能用于真实并列分层，不得机械对应英文分号或连接词。
- 中文字符之间不得保留用于纸书对齐的连续空格。
- 英文原书分章后，常会在译文正文开头或结尾残留重复标题、running title、下一节书名或目录碎片。精修时必须检查每章首尾，正文中不得保留这类副文本残片。
- 也要检查 AI 或译者是否把章节内容概括成新的可见小标题；若英文源文没有对应标题，必须从 EPUB 可见正文和目录中移除。
- Project Gutenberg 等英文数字源常带有 `Transcriber's Notes`、OCR correction notes 或源文件尾注。除非本书版本有意保留来源制作说明，否则不要把这些内容混入中文正文；若保留，必须译为清楚标注的“原文转录说明/来源制作说明”，不能让读者误以为是作者正文。
- 下载的英文 raw source 是公版来源证据，不能因为其中有 BOM、Project Gutenberg 样板文字或排版残留就随意改写；清理对象应是中文终稿、metadata、frontmatter 和生成 EPUB。
- 附录、名单、表格、页码目录等旧纸书结构，必须转成适合 EPUB 的列表、表格、注释或导航结构。
- 旧纸书正文中的 `* * * * *`、`*****`、`----` 等分隔符不得进入成书正文，也不要替换成另一种可见符号。若只是排版分隔，直接删除；若确实表示内容转换，应由段落自然承接或另写小标题。

Chinese punctuation and EPUB typography are publication issues, not cosmetic details.

## 本书目标文档位置 / Book Goal Location

如果某本书已经发现标题、段落、术语、译注、排版或文学精修方面的系统问题，目标文档必须放在：

```text
books/zh-Hans/{number}_{目标语言书名}_{目标语言作者名}/goal/
```

不能放在仓库根目录的通用 `goal/` 下。根目录目标会让 AI 误以为这是项目级任务，而不是某本书的执行目标。

If systematic issues are found in a specific book, the goal document belongs under that book project, not in a repository-level goal directory.

## 模板回填 / Template Backfill

英文到简体中文项目中的可复用经验必须回填到三层：

1. `books/zh-Hans/{number}_{目标语言书名}_{目标语言作者名}/goal/`：记录这本书的具体问题和执行计划。
2. `template/epub_pipeline/common/`：记录所有语言方向都适用的 EPUB、标题、QA、路径和流程规则。
3. `template/epub_pipeline/English-to-Simplified-Chinese/`：记录英文源文到简体中文的专用问题，例如英文标题链、英文长句干扰、英文称谓和中文译注策略。

这三层可以有必要重复。重复不是浪费，而是为了让不同阶段、不同 agent、不同上下文都能读到关键规则，避免生成过程中跑偏。

These three layers may intentionally overlap. The overlap helps different agents read the right rule at the right execution layer.

## 随机抽检同类问题全书审计 / Book-Wide Similar-Issue Audit

随机抽检一旦发现任何需要修复或可能系统性复现的问题，包括但不限于 P0/P1/P2、单项 <80、读者不可理解、事实/术语/图表/公式/注释错误，或本模板硬门禁失败，主执行 AI 不得只修被抽中的样本，也不得等到第二轮才全书检查。必须先把发现归纳为问题族，再对整本读者可见书稿执行全书同类问题审计，覆盖 `chapters/final/`、frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML；修复所有确认命中，记录合理例外，并在该轮 `fix_log.md` 与 `closure_check.md` 中关闭该问题族后，才能使用新 seed 复抽。

若该轮发现译文质量问题族，还必须在 `fix_log.md` 填写 `translation_quality_skill_backfill: "UPDATED"` 或 `"MERGED"`、`translation_quality_skill_backfill_path: "skills/translation-quality-defect-families/SKILL.md"` 和回填摘要，并在 `closure_check.md` 填写 `translation_quality_skill_backfill_verified: true`；若仅有非译文质量问题，必须填写 `NOT_APPLICABLE` 和具体理由。

If a random sample exposes any issue that needs correction or may recur systemically, treat it as a possible systemic defect family immediately in the current round. Audit the whole reader-facing book for similar cases, fix all confirmed matches, document justified exceptions, and close the family in the same round before a new-seed resample.

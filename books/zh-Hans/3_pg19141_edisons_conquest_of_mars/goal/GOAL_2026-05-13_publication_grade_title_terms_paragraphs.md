# /goal：出版级标题工程、章节精修、术语译注与长段落处理

status: "PASS"

## 目标

在现有《爱迪生征服火星》EPUB 基础上，按 `template/epub_pipeline`、`en-zh-Hans` 模板、本书 `AGENTS.md` / `SKILL.md` / `references/` 规则，以及 `a_negro_explorer_at_the_north_pole` 的成书经验，补足文学出版级闭环。

本轮不是重新翻译全书，而是对已经成书的文本执行可追溯的出版级补强：标题工程、章节精修、术语/译注统一、长段落处理、生成后校验和 QA 记录。

## 固定输入与边界

- 书籍目录：`books/zh-Hans/3_pg19141_edisons_conquest_of_mars/`
- 翻译方向：`en-zh-Hans`
- 来源：Project Gutenberg #19141，美国公版英文原文。
- 译者署名：`LifeBook 书坊 SaberOnGo`
- 禁止写入：`template/` 下不得写入本书专属正文、译文、QA、metadata 或 EPUB 输出。
- 不使用现代中文译本、盗版站、来源不明 EPUB 或无权提交材料。

## 参考经验

从 `books/zh-Hans/1_pg20923_a_negro_explorer_at_the_north_pole/` 复用以下经验：

- 必须建立书内 `/goal`，不能只做零散修正。
- 标题工程要区分 `nav_title`、`display_title`、`subtitle`、`title_note`。
- 章节标题中的专名优先用中文译名，英文原名进入正文首次自然出现处或术语表。
- 普通名词、器物名、材料名不得保留原文括注。
- 长段落要按逻辑节点拆分，不能机械切断。
- 术语表不能保留空模板，必须记录本书高频专名和专业词。
- 生成 EPUB 后要检查结构、出版 lint、refinement scan、metadata 和读者可见 XHTML。

## 当前发现

1. 标题工程：本书章节主标题已经使用编号策略，符合源文 `Chapter I.` 至 `Chapter XVIII.`；但还需要记录内文小标题均来自原文分节标题，不是 AI 自创概括。
2. 术语表：`glossary/terms.csv` 仍是空模板，未落地本书专业名词和专名策略。
3. 术语不统一：`electrical ships` 在正文中混用“电力飞船”“电气飞船”“电气飞艇”“电气战舰”；本轮统一为“电力飞船”。火星人的 `airships` 继续译为“飞艇/火星飞艇”。
4. 术语不统一：`air-tight suit/dress` 在研究记录里写“密封服”，正文主要使用“气密服”；本轮统一为“气密服”。
5. 长段落：普通叙述段中仍有 7 段超过 300 字，其中 `002_chapter_i.md` 有 1 段超过 500 字，需要拆分或记录保留理由。
6. 章节精修：重点章节应保留逐章 refinement 记录，至少覆盖第一章、第二章、第三章、第四章、第五章、第十四至十八章这些术语、世界大会、技术说明、战斗和结尾密集章节。

## 执行清单

1. 更新 `glossary/terms.csv` 和 `glossary/style_guide.md`，补全专业名词、专名、历史词、译注策略。
2. 更新 `metadata/book_specific_translation_research.md` 和 `metadata/style_profile.md`，把术语选择和标题策略写实。
3. 统一正文中 Edison 舰队术语：`electrical ships` = “电力飞船”；Martian `airships` = “火星飞艇/飞艇”。
4. 统一 `air-tight suit/dress` 为“气密服”。
5. 对超过 300 字普通叙述段做处理：能自然拆分则拆分，若保留必须在 QA 中说明。
6. 建立本轮出版级 QA 记录，列出标题工程、章节精修、术语/译注、长段落、生成后检查结论。
7. 必须重新运行：
   - `npm run lint:publication`
   - `npm run build:epub`
   - `npm run check:epub`
   - `node scripts/refinement_check.js`
8. 复制最新 `output/book.epub` 到 `preproduction/stage2_sample/sample_book.epub`。
9. 核验 `output/epubcheck.json`：fatal/error/warning 为 0，主标题为 `爱迪生征服火星`，contributors 包含 `LifeBook 书坊 SaberOnGo`。

## 完成定义

- `glossary/terms.csv` 不再是空模板，包含本书高频专名、技术词、历史/文化词。
- `glossary/style_guide.md` 有本书可执行的句法、术语、译注策略。
- 正文不再混用“电气飞船/电气飞艇/电气战舰”指代 Edison 的 `electrical ships`。
- 出版范围普通叙述段无超过 500 字段落；超过 300 字段落要么已拆分，要么有 QA 保留理由。
- 标题策略有记录：章节主标题遵守源文编号，不自创概括标题；内文小标题来自源文分节标题。
- 本轮 QA 记录明确 PASS。
- EPUB 重新构建并通过所有校验。

## 完成记录

- `glossary/terms.csv` 已补全。
- `glossary/style_guide.md` 已补全。
- 正文术语已统一：Edison 舰队为“电力飞船”，`air-tight suit/dress` 为“气密服”。
- 普通叙述段长段检查：`gt300=0`，`gt500=0`，最长 300 字。
- `npm run lint:publication`：PASS，硬错误 0。
- `npm run build:epub`：PASS。
- `npm run check:epub`：PASS，fatal 0，error 0，warning 0。
- `node scripts/refinement_check.js`：PASS，出版范围 BOM 0，mojibake 0，中文异常空格 0。
- EPUB 解包抽查：目录和重点章节标题正常，重点章节 XHTML 中未发现旧术语“电气飞船/电气飞艇/电气战舰/密封服”。

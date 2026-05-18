# 《幽灵海盗》出版级二次总审与查漏补缺报告

review_date: 2026-05-13
status: PASS after fixes
goal: `goal/2026-05-13_pg10966_exhaustive_publication_literary_audit_goal.md`

## 复核依据

- 本项目公共规则：`AGENTS.md`
- EPUB pipeline skill：`skills/public-domain-epub-pipeline/SKILL.md`
- 模板规则：`template/epub_pipeline/README.md`
- 标题规则：`template/epub_pipeline/common/references/chapter_title_policy.md`
- en-zh-Hans 精修规则：`template/epub_pipeline/en-zh-Hans/references/english_to_chinese_literary_refinement.md`
- 简体中文质量框架：`template/epub_pipeline/targets/zh-Hans/quality_framework/references/quality_standard.md`
- 前书经验：`books/zh-Hans/1_pg20923_a_negro_explorer_at_the_north_pole` 的标题工程、出版复核、EPUB 质量整改和精修 QA 记录。

## 本轮发现并修复的缺口

### 1. 标题工程

本轮直接对照 `chapters/src/*.md` 后发现：`source/toc.json` 只记录 I-XVI 章号，但拆章正文中实际保留了源文小题，例如 `The Figure Out of the Sea`、`The End of Williams`、`Hands That Plucked`、`The Ghost Pirates`。此前把所有小题视为不受来源支持，判断过窄。

修复方式：

- `metadata/chapter_title_map.yaml` 的 `source_full` 改为“章号 / 源文小题”。
- EPUB `nav.xhtml` 继续使用短目录题名“第一章”至“第十六章”，避免手机目录过长。
- 章节页由 `display_title` 显示章号，由 `subtitle` 显示真实小题中文译名。
- 更新旧 QA 记录，明确“源文真实小题应作为页面副标题保留，不塞入导航长标题”。

### 2. 章节精修与长段落

本轮重新扫描 `chapters/final/` 普通散文段落。修复前有多处 380 字以上普通叙述段，虽未超过 500 字硬拆阈值，但手机阅读会偏压迫。

已按语义阶段拆分：

- 第四章：二副开始理解真相的回顾段。杰索普观察威廉斯并意识到帆不该吹散的心理段。
- 第五章：威廉斯结局前的全船恐惧判断段。
- 第七章：杰索普在船尾看见神秘全帆装船的段落。
- 第十四章：暮色中雾船成形的段落。
- 第十五章：塔米被影子拖拽的段落。

保留例外：

- 第三章《地狱嗬嗬号子》为船歌/号子格式，虽整块较长，但由短行组成，不按普通散文长段拆分。

### 3. 术语与译注

本轮复扫未发现新的航海术语误译残留。保留并确认：

- `buntline`：帆腹索。
- `gasket`：束帆索。
- `jackstay`：帆缘索。
- `log-reel`：测程绳盘。
- `Quoin`：奎因。
- `Jaskett`：贾斯克特。

拉丁字符残留均有合理来源：

- `Mortzestus`：船名首次自然出现括注。
- `J. E. G.`、`T.`：附录签名缩写。
- metadata、source evidence、title map 中的英文源题和 Project Gutenberg 信息为制作记录，不是中文正文污染。

### 4. 重要段落与“信达雅”

复核结论延续并补强 `full_book_literary_xindaya_review.md`：

- 首章黑影从海上来、又入海：保留观察顺序和“不确定性”。
- 测程绳盘段：保留塔米恐惧、二副看不见、杰索普知道自己所见不可共享的心理压力。
- 汤姆事故、威廉斯坠落、雅各布斯高空崩溃：航海动作链、索具名和人物位置清楚。
- 雾、绿光、雾船、海下船影：没有提前解释为确定怪物或现代惊悚设定。
- 最终登船与《寂静之船》：保留尖叫骤停、幸存者证言和附录文献调性。

“信”方面：未发现事实、方位、人物关系或动作链的新增误差。

“达”方面：长段落拆分后，移动端阅读压力下降。对话和动作推进没有被改成提纲式中文。

“雅”方面：保留霍奇森式克制、迟疑和海上现场感。没有凭空新增比喻物、声音或现代恐怖词。

### 5. 过程产物清洁

- `frontmatter/preface.md`、`frontmatter/translator_note.md` 从英文空标题改为中英并列标题。
- 旧章节 QA 中与当前标题工程冲突的表述已修正。

## 自动扫描结果

- 标题映射检查：PASS，终稿一级标题与 `chapter_title_map.yaml` 一致，目录题名/页面主标题/页面副标题均无英文原名括注。
- 长段落检查：普通散文无 380 字以上段落。仅第三章船歌格式块为例外。
- 残留扫描：旧译名、旧术语、现代恐怖词、AI 痕迹未进入 `chapters/final/`。
- 源文小题检查：I-XVI 章正文真实小题均已进入 `chapter_title_map.yaml`。

## 构建验证

- `npm run lint:publication`：PASS，`asciiSemicolon=0`、`zhSemicolon=0`、`cjkMultiSpace=0`、`mojibake=0`、`legacyPrintToc=0`、`targetTitleLatinResidue=0`。
- `node scripts/refinement_check.js`：PASS，出版范围 `bomFiles=0`、`mojibakeFiles=0`、`cjkMultiSpaceFiles=0`、`zhSemicolon=0`。
- `npm run build:epub`：PASS，重新生成 `output/book.epub` 与 `output/幽灵海盗.epub`。
- `npm run check:epub`：PASS，EPUBCheck 5.2.1 结果 `fatal=0`、`error=0`、`warning=0`。
- EPUB 解包扫描：第 I-XVI 章均出现 `chapter-subtitle`，例如“海中上来的身影”“威廉斯的结局”“从暗处攫来的手”“幽灵海盗”。旧译名和旧术语残留为 0。
- 新 EPUB 文件大小：122382 bytes。
- 新 EPUB SHA256：`2A7BDC0369383EE628DB6C0B9A388468C41ABF6EC182ECEB063B4869330AD6B3`。

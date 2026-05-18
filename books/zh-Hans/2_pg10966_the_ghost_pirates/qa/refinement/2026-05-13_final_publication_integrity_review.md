# 《幽灵海盗》最终出版完整性复查记录

review_status: "PASS"
date: "2026-05-13"
goal: `goal/2026-05-13_pg10966_final_publication_integrity_goal.md`

## 复查目标

本轮按用户指定的 `/goal` 执行，参考《黑人北极探险家》制作过程中关于封面、书籍信息页、标题工程、术语统一、长段落拆分、EPUB 内部结构和终审记录可追溯性的经验，对《幽灵海盗》做最终出版完整性复查。

本轮重点不是重新粗翻，而是确认本书已经满足出版前准入条件：封面真实可用、书籍首页信息完整、译者名统一、标题工程与源文小题一致、航海术语不漂移、重要段落不失真、全书“信达雅”结论有证据。

## 封面、书籍首页和译者名

- `assets/cover.jpg` 存在，尺寸为 1600 x 2400，体积为 363786 bytes。
- EPUB 内部包含 `EPUB/images/cover.jpg`，不再打包临时 `cover.svg`。
- `EPUB/package.opf` 的 manifest 已把 JPG 标记为 `properties="cover-image"`。
- EPUB 内部包含 `EPUB/book-info.xhtml`。
- `EPUB/nav.xhtml` 有“书籍信息”目录入口。
- `book-info.xhtml` 含中文书名、英文原名、作者、译者、译制时间、Project Gutenberg 来源、公版说明、原书信息和本书简介。
- 译者名在 metadata、OPF 和书籍信息页中统一为 `LifeBook 书坊 SaberOnGo`。
- 保留 `publisher: LifeBook 书坊`，因为出版方字段不应混入个人译者名。

## 标题工程复核

已复查 `metadata/chapter_title_map.yaml` 与 I-XVI 章源文小题：

- EPUB 导航使用短题名：第一章至第十六章。
- 章节页面显示中文章号和源文小题译名。
- 源文小题没有被替换成 AI 概括。
- 重要副标题已覆盖：海中上来的身影、威廉斯的结局、换人掌舵、雾来之后、从暗处攫来的手、幽灵船、巨大的幽灵船、幽灵海盗。

结论：标题工程满足“导航短、页面完整、来源可追溯”的模板要求。

## 长段落和版面节奏

复扫 `chapters/final/` 后，普通正文没有需要继续拆分的异常超长段落。第三章《地狱嗬嗬号子》存在一个较长格式块，但该段是船歌/号子排版，由短行组成，属于版式例外，不按普通散文拆分。

已确认终稿未出现移动端阅读明显压迫的普通叙事长段；此前已拆分的心理推进、雾船成形、塔米遇险和最终沉没段落保持语义阶段清楚。

## 术语和译注统一

本轮抽查 `glossary/terms.csv`、`qa/terminology/` 和终稿正文，重点确认航海术语、人员称谓和动作动词：

- `Second Mate`：二副。
- `fo'cas'le`：艏楼。
- `buntline`：帆腹索。
- `gasket`：束帆索。
- `jackstay`：帆缘索。
- `halyards`：升降索。
- `clewline`：帆脚索。
- `braces`：转桁索。
- `log-reel`：测程绳盘。
- `Quoin`：奎因。
- `Jaskett`：贾斯克特。

正文保留 `Mortzestus` 首次括注和附录签名缩写，属于必要原名/签名残留，不是中文出版污染。

## 重要段落源译复核

### 第一章：海中上来的身影

源文的关键不是“怪物登场”，而是杰索普先以常识否认，再被同一身影再次出现击穿理性。终稿保留了观察顺序：右舷栏杆外跨入、消失在下风侧阴影、搜索无果、回头再见、最终翻过栏杆入海。译文没有提前解释身影本质，也保留了“影儿太多”的口语触发点。

### 第十四章：幽灵船成形

源文以雾、绿光、桅桁轮廓和四艘影船叠加制造压迫感。终稿保留从“看不清”到“看见船形”的渐进过程，没有把氛围段改写成剧情说明。影船与雾的关系、船体方位和杰索普的迟疑感保持准确。

### 第十五章：巨大的幽灵船与塔米

源文中塔米先因海下巨船陷入惊恐，随后被看不见的力量拖走。终稿保留“海下船影”和“塔米被拖拽”的连续恐怖，不把塔米改写成主动坠海，也没有把未知力量实体化为不受源文支持的怪物。

### 第十六章：幽灵海盗和最终证词

终稿保留灰色人影登船、尖叫骤停、幽灵船员重新操帆、莫尔腾号船首下沉、杰索普逃生和《寂静之船》附录证词。航海动作链清楚：解帆、升桁、转正帆桁、帆面鼓满、船首下沉。结尾关于官方日志会把真实恐怖压成“无法解释的灾难”的反讽也保留到位。

## 全书“信达雅”结论

信：人物、方位、船上空间、索具动作和灾难顺序未发现新增事实错误。重要场景没有把未知现象解释成源文没有写明的现代恐怖设定。

达：中文正文总体按中文叙述节奏推进，口语人物、航海叙事和心理迟疑区分清楚。长句拆分后，移动端阅读压力已控制。

雅：译文保留霍奇森式海事纪实恐怖的克制、迟疑、现场感和压迫感。重要段落没有靠华丽比喻替换源文的冷静观察，也没有压缩成剧情梗概。

## 例外说明

- 第三章船歌/号子长块为格式例外，保留原有节奏。
- `Mortzestus` 首次括注和附录英文签名缩写为必要原文信息。
- metadata、source evidence、title map 中的英文源题和 Project Gutenberg 信息属于制作记录，不视为正文残留。

## 最终准入结论

本轮未发现需要继续改正文的出版阻断问题。封面、书籍首页、译者名、标题工程、术语、长段落、重要段落和全书“信达雅”均达到当前模板准入要求。

## 最终验证结果

- `npm audit`：PASS，0 vulnerabilities。
- `npm run lint:publication`：PASS，`asciiSemicolon=0`、`zhSemicolon=0`、`cjkMultiSpace=0`、`mojibake=0`、`targetTitleLatinResidue=0`。
- `node scripts/refinement_check.js`：PASS，出版范围 `bomFiles=0`、`mojibakeFiles=0`、`cjkMultiSpaceFiles=0`、`zhSemicolon=0`。
- `npm run build:epub`：PASS。
- `npm run check:epub`：PASS，EPUBCheck `fatal=0`、`error=0`、`warning=0`。
- EPUB 内部拆包：`EPUB/images/cover.jpg` 存在，`cover.svg` 未打包，OPF `cover-image` 指向 JPG，`book-info.xhtml` 存在，目录含“书籍信息”，OPF 与书籍信息页均含 `LifeBook 书坊 SaberOnGo`。
- EPUB 章节副标题抽查：海中上来的身影、威廉斯的结局、从暗处攫来的手、幽灵船、巨大的幽灵船、幽灵海盗均在章节 XHTML 中。
- 最终 EPUB：466977 bytes。
- SHA256：`1331200CB47D4557D2CE38BE7AED6C909AE52214BF5822E1FB784387610B2D8A`。

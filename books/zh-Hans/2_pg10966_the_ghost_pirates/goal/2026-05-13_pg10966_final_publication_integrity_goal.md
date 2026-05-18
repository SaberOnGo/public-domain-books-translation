# 《幽灵海盗》最终出版完整性精修目标

goal_status: "PASS"
date: "2026-05-13"

## 目标

参考《黑人北极探险家》制作过程中的经验教训，对《幽灵海盗》做一次最终出版完整性复查与精修。目标不是简单确认 EPUB 能打开，而是确认本书在封面、书籍首页信息、metadata、标题工程、术语统一、长段落处理、重要/高潮段落文学性和全书“信达雅”层面均达到模板要求。

## 必做范围

1. 封面工程：
   - 必须有正式 `assets/cover.jpg`。
   - EPUB 内必须打包 `EPUB/images/cover.jpg`。
   - OPF manifest 必须标记 `properties="cover-image"`。
   - 封面体积应在模板建议范围内，避免临时 SVG 或超大未压缩图进入最终 EPUB。

2. 书籍首页信息：
   - EPUB 必须有 `EPUB/book-info.xhtml`。
   - 读者可见目录中必须有“书籍信息”入口。
   - 书籍信息页必须含中文书名、英文原名、作者、译者、译制时间、Project Gutenberg 来源、公版说明、原书信息和本书简介。
   - 译者名必须统一为 `LifeBook 书坊 SaberOnGo`。后续模板规则为 `LifeBook 书坊 + 个人名`。

3. 标题工程：
   - 复核 Project Gutenberg 原文章节副标题。
   - 复核 `metadata/chapter_title_map.yaml` 的 `source_full`、`nav_title`、`display_title`、`subtitle`、`title_note`。
   - EPUB 目录使用短题名，页面标题与副标题不混入 AI 概括。

4. 全书文学精修：
   - 复查 `chapters/final/` 和 `chapters/translated/` 同步关系。
   - 检查普通正文超长段落，歌曲、名单、格式化文本可记录例外。
   - 复核航海术语、船上部位、人员称谓、动作动词和恐怖叙事语气。
   - 针对重要/高潮段落做源文对照：雾、影子、海中身影、幽灵船、威廉斯、塔米、最终“幽灵海盗”等段落必须抽查。

5. “信达雅”全书分析：
   - 信：事实、动作、人物、海事空间关系不误。
   - 达：中文叙述自然，不是英文结构影子。
   - 雅：保持霍奇森式海事纪实恐怖的冷静、迟疑和压迫感，不乱加意象，不压成剧情梗概。

6. 模板回填：
   - 如发现可复用规则，回填到 `template/epub_pipeline/common/` 或 `template/epub_pipeline/en-zh-Hans/`。
   - 本书专属记录只写入 `books/zh-Hans/2_pg10966_the_ghost_pirates/`。

## 完成条件

- 新增 QA 记录说明检查范围、发现、修复和例外。
- `npm audit` 为 0 vulnerabilities。
- `npm run lint:publication` 通过。
- `node scripts/refinement_check.js` 出版范围通过。
- `npm run build:epub` 通过。
- `npm run check:epub` 通过，EPUBCheck fatal/error/warning 均为 0。
- EPUB 内部拆包检查确认封面、书籍信息、译者名、章节副标题和 metadata 均正确。
- `output/final_manifest.md` 与实际 EPUB 体积、SHA256、字符统计同步。

## 执行结论

- QA 记录：`qa/refinement/2026-05-13_final_publication_integrity_review.md`。
- 封面、书籍信息页、译者名、标题工程、长段落、术语统一、重要/高潮段落和全书“信达雅”复查结论均为 PASS。
- 本轮未发现需要继续改正文的出版阻断问题。
- 最终 EPUB 以重建和 EPUBCheck 结果为准。

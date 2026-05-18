# 出版级复查：标题工程、章节精修、术语译注与长段落

status: "PASS"
review_date: "2026-05-13"
goal: "goal/GOAL_2026-05-13_publication_grade_title_terms_paragraphs.md"

## 模板与参考依据

- 已复读 `template/epub_pipeline/common/references/literary_refinement_policy.md`。
- 已复读 `template/epub_pipeline/targets/zh-Hans/quality_framework/references/title_punctuation_and_heading_style.md`。
- 已复读本书 `AGENTS.md`、`SKILL.md`、`references/english_chapter_title_strategy.md`、`references/english_to_chinese_literary_refinement.md`。
- 已参考 `1_pg20923_a_negro_explorer_at_the_north_pole` 的标题工程、术语表、长段落和 refinement 记录做法。

## 标题工程

- 章节级标题：PASS。原书章节只有 `Chapter I.` 至 `Chapter XVIII.`，本书 `metadata/chapter_title_map.yaml` 使用“第一章”至“第十八章”，不添加 AI 概括式可见章节题名。
- EPUB nav：PASS。`build_epub.js` 使用 `nav_title`，页面标题使用 `display_title`，副标题字段保留但本书章节不需要可见副标题。
- 内文小标题：PASS。正文中的 `##` 小标题对应 Project Gutenberg 源文中原有分节标题，例如 `The Martians Returning.`、`The Power of the Disintegrator.`，不是译者自创概括。
- 标题标点：PASS。未发现多重中文破折号标题链，也未发现英文原名塞入章节标题。

## 术语/译注统一

- `glossary/terms.csv` 已由空模板补全为本书术语表，覆盖 Edison 舰队、火星飞艇、分解器、气密服、火星地名、历史称谓和现实人物。
- `electrical ships/electric ships` 统一为“电力飞船”。
- Martian `airships` 统一按语境译为“飞艇/火星飞艇”，不与 Edison 舰队混同。
- `air-tight suit/dress` 统一为“气密服”。
- `disintegrator` 保持“分解器/分解射线器”分工：泛称装置用“分解器”，完整武器称谓用“分解射线器”。
- `Aryan race` 记录为历史语境术语“雅利安民族”，不在正文中现代化替换。

## 长段落处理

处理前普通叙述段：

- 超过 300 字：7 段。
- 超过 500 字：1 段。
- 最长：`002_chapter_i.md:67`，541 字。

处理后普通叙述段：

- 超过 300 字：0 段。
- 超过 500 字：0 段。
- 最长：300 字，低于人工复核阈值。

拆分原则：只按原文逻辑节点拆分，不改写事实，不新增比喻，不把原文段落重写成提纲。

## 章节精修记录

| 文件 | 处理内容 | 结论 |
| --- | --- | --- |
| `002_chapter_i.md` | 拆分 Edison 飞行器机械原理与彗星电斥力长段。 | PASS |
| `003_chapter_ii.md` | 拆分战争基金、君主赴会、飞船电性控制三个长段；统一“电力飞船”。 | PASS |
| `004_chapter_iii.md` | 拆分华盛顿大会开场长段和中国寓言长引文；统一“电力飞船”。 | PASS |
| `005_chapter_iv.md` | 术语统一为“电力飞船”。当前最长段 300 字，保留。 | PASS |
| `006_chapter_v.md` | 拆分流星技术说明长段；统一“电力飞船”。 | PASS |
| `013_chapter_xii.md` | “密封服”统一为“气密服”。 | PASS |
| `015_chapter_xiv.md` | Edison 舰队术语统一为“电力飞船”，保留火星 `airships` 为“飞艇”。 | PASS |
| `016_chapter_xv.md` | 同上，并保留战斗段“火星飞艇”以区分敌方飞行器。 | PASS |
| `017_chapter_xvi.md` | 宫殿战斗中 Edison 舰队统一为“电力飞船”。 | PASS |
| `018_chapter_xvii.md` | 谈判和返航准备段统一 Edison 舰队术语。 | PASS |

## 未改动但已复核

- 不为章节新增内容概括标题。原因：源文只有章节编号，本书标题工程应保持编号策略。
- 不把 `飞行器` 全部替换为“电力飞船”。原因：源文中 `flying machine` 有时泛指火星或 Edison 的飞行机器，需按上下文区分。
- 不把所有 `分解器` 改为“分解射线器”。原因：源文 `disintegrator` 在武器泛称中短称更自然，完整称谓已在术语表说明。

## Decision

PASS。已重新生成 EPUB 并完成最终校验。

## Validation

- `npm run lint:publication`：PASS，硬错误 0。
- `npm run build:epub`：PASS。
- `npm run check:epub`：PASS，fatal 0，error 0，warning 0。
- `node scripts/refinement_check.js`：PASS，出版范围 BOM 0，mojibake 0，中文异常空格 0。
- 长段落复扫：`gt300=0`，`gt500=0`，最长普通叙述段 300 字。
- EPUB 解包抽查：`nav.xhtml` 与重点章节 XHTML 标题正常；重点章节 XHTML 未发现旧术语残留。

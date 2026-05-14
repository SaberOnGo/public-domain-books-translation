# GPT-IMAGE 封面、书籍信息页与全书二次复核

status: "PASS"
date: "2026-05-13"

2026-05-14 更新：本文件记录的是前一版 GPT-IMAGE 封面复核。最新封面已按 `cover_design_policy.md` 补充规则重做，详见 `qa/refinement/2026-05-14_cover_policy_rebuild_review.md`。

## 复核目标

本轮针对用户指出的封面质量差距，按 `pg20923_a_negro_explorer_at_the_north_pole`、`pg10966_the_ghost_pirates` 的制作经验补齐栅格封面，并重新检查书籍信息页、译者署名、EPUB 封面引用和全书精修闭环。

## 封面

- 源图：`assets/cover_source_gpt_image.png`。
- EPUB 图：`assets/cover.jpg`。
- 生成方式：GPT-IMAGE 生成本书情节图，后续只做确定性文字排版和 JPG 压缩。
- 画面内容：火星压迫画面、电力飞船舰队、蓝白电弧、金色分解射线、地球远景，符合本书“爱迪生带领地球舰队反攻火星”的核心情节。
- 文字核验：中文书名、英文原名、作者、译者、Project Gutenberg 来源可读；无 `LifeBook 翻译组` 残留。
- 体积核验：`assets/cover.jpg` 约 286KB，符合模板建议范围；大源图不直接打入 EPUB。

## 书籍信息页

- 页面标题统一为“书籍信息”，不再只称“版本说明”。
- 包含中文书名、英文原名、作者、译者、翻译时间、Project Gutenberg 来源、公版说明、本书简介和原书信息。
- 译者字段为 `LifeBook 书坊 SaberOnGo`，与封面、metadata、OPF contributor 保持一致。

## 全书信达雅二次复核

- “信”：本轮没有新增或改写正文情节；前次术语统一仍有效，Edison 舰队为“电力飞船”，`air-tight suit/dress` 为“气密服”。
- “达”：重点长段落已在前轮拆分或复核，本轮复扫普通叙述段未发现超过 300 字段落。
- “雅”：高潮段落的节奏仍以清楚、紧凑、画面感为准；火星舰队、分解射线、月球遗迹、艾娜与宫殿战斗、最终返航等重点内容未发现新的文学性问题。

## EPUB 工程复核

- 构建脚本优先读取 `assets/cover.jpg`。
- EPUB 应包含 `EPUB/cover.xhtml`、`EPUB/book-info.xhtml`、`EPUB/images/cover.jpg`。
- OPF manifest 中 `cover-image` 应指向 `images/cover.jpg` 且带 `properties="cover-image"`。
- 历史记录：本轮解包抽查的旧封面尺寸记录已作废；2026-05-14 重制后以最新封面规则和 `qa/refinement/2026-05-14_cover_policy_rebuild_review.md` 为准。
- 解包抽查：`nav.xhtml` 和 `book-info.xhtml` 均显示“书籍信息”；`book-info.xhtml` 含 `LifeBook 书坊 SaberOnGo`。
- `npm run lint:publication`：PASS，硬错误 0。
- `npm run check:epub`：PASS，fatal 0，error 0，warning 0。
- `node scripts/refinement_check.js`：PASS，出版范围 BOM 0，mojibake 0，中文异常空格 0。

## Decision

PASS。封面已从脚本 SVG 占位升级为本书情节驱动的 GPT-IMAGE 封面，书籍信息页、译者署名、OPF cover-image 和 EPUBCheck 闭环一致。

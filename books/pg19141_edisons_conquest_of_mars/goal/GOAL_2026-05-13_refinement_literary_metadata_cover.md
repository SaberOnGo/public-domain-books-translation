# /goal：精修《爱迪生征服火星》译本、封面和发布信息

status: "PASS"

## 目标

在已完成 EPUB 的基础上，对《爱迪生征服火星》执行一次发布前精修闭环：复核全书文学性、信达雅、重要段落、高潮段落、封面、书籍首页信息、译者署名和 EPUB 元数据，修复可确认的问题后重新构建并校验。

## 固定要求

- 译者名统一为 `LifeBook 书坊 SaberOnGo`。
- 历史记录：本轮当时要求封面署名写入“LifeBook 书坊 + 个人名”的译制署名；此规则已被 2026-05-14 最新封面规则取代，最终封面只写 `LifeBook 书坊 译制`。
- 书籍首页信息页必须包含中文书名、英文原名、作者、译者、翻译时间、Project Gutenberg 来源 URL、公版说明、本书简介和原书信息。
- EPUB OPF 主标题必须是中文书名《爱迪生征服火星》，英文原名只能作为原书信息、来源信息或辅助 metadata，不得覆盖主标题。
- 重要段落和高潮段落必须逐项检查，包括第一章灾后与反击动员、第七章俘获火星人、第十三章艾娜身世与克什米尔诗句、第十五至十七章洪水、首都、宫殿战斗和谈判、第十八章返航与结尾。
- 全书信达雅检查必须覆盖忠实性、中文自然度、早期科幻报刊叙事感、术语一致性、分号和长句、诗句与象征段落、殖民时代/战争动员语气的忠实呈现。

## 执行路线

1. 复查模板和本书已有制作经验，确认不可写入 `template/`，所有产物只写入本书目录。
2. 扫描发布范围和 QA 范围，找出旧署名、主标题 metadata、乱码、异常英文残留、AI 痕迹、中文异常空格和可疑标点。
3. 对重要章节执行人工抽读式复核；发现确定可改善的句子，只做忠实、克制、可回溯的润色。
4. 更新封面、首页信息、metadata、预制作记录、最终清单和本轮精修记录。
5. 重新运行出版 lint、EPUB 构建、EPUBCheck 和 refinement check。
6. 核验 `output/epubcheck.json` 中主标题、译者、fatal/error/warning。
7. 提交并推送修复结果。

## 完成定义

- `scripts/build_epub.js`、`metadata/book.yaml`、相关制作记录中的译者署名均为 `LifeBook 书坊 SaberOnGo`。
- 历史记录：本轮曾生成 `output/cover.svg`；此产物已被 2026-05-14 最新封面规则取代，最终 EPUB 使用 `output/cover.jpg`，且不再保留 `output/cover.svg`。
- `output/epubcheck.json` 显示 title 为 `爱迪生征服火星`，contributors 包含 `LifeBook 书坊 SaberOnGo`。
- `node scripts/publication_lint.js --target=zh-Hans --write-report` 无 hard errors。
- `npm run check:epub` fatal/error/warning 均为 0。
- `node scripts/refinement_check.js` 的出版范围 BOM、mojibake、中文异常空格均为 0。
- 本轮 QA 记录明确列出重点段落复核结论和未改动原因。

## 完成记录

- `npm run build:epub`：PASS。
- `npm run check:epub`：PASS，fatal 0，error 0，warning 0。
- `node scripts/refinement_check.js`：PASS，出版范围 BOM 0，mojibake 0，中文异常空格 0。
- `output/epubcheck.json`：主标题为 `爱迪生征服火星`，译者 contributor 为 `LifeBook 书坊 SaberOnGo`。

# 本书复盘 / Book Retrospective

status: "PASS"

## 有效做法

- 先记录 Project Gutenberg #19141 作为主来源，并记录 #21670 为重复参照，避免同书多条目混淆。
- 对只有编号的章节，使用 `chapter_title_map.yaml` 固定短导航题名，避免 AI 自创小标题。
- 批量翻译后立即运行 `publication_lint.js`，发现并修正 ASCII 分号和中文分号阈值问题。

## 后续人工建议

- 第八章、第十四章、第十七章等高密度章节已在 2026-05-13 精修复查中抽读并记录；公开发布前仍建议真人编辑做最终通读。
- 若准备公开发布，按目标发行地区复核 Project Gutenberg 美国公版文本在当地的版权状态。

# 古希腊文标题与章节题名策略 / Ancient Greek Title Strategy

## 基本原则

古希腊文作品常见卷、书、章、节、命题、问题、论题等多层结构。不得把现代编辑者目录直接当成原作标题。

必须区分：

- 古代作者原题。
- 抄本或古代目录题名。
- 现代校勘者题名。
- 现代译本题名。
- 扫描/OCR 文件自动标题。
- AI 概括题名。

## 处理流程

1. 读取完整来源标题，不得只使用被自动分章脚本截断的第一行。
2. 判断标题来源：original / manuscript / editor / translator / scan_artifact / ai_summary。
3. 判断标题功能：
   - 卷册或章节编号。
   - 命题、定义、问题或论题。
   - 内容摘要。
   - 现代编辑辅助导航。
4. 生成三种中文标题：
   - `nav_title`：短目录题名。
   - `display_title`：页面主标题。
   - `subtitle`：副标题或标题说明。
5. 必要时生成 `title_note`，说明标题是否来自现代编辑者。

## `metadata/chapter_title_map.yaml`

如果书中存在复杂标题，必须建立：

```yaml
chapters:
  - id: "001"
    source_full: ""
    source_type: "original|manuscript|editor|translator|scan_artifact|ai_summary"
    nav_title: ""
    display_title: ""
    subtitle: ""
    title_note: ""
```

## 专名规则

- 章节标题、副标题和 EPUB 目录题名中的人名、地名、神名、星座名和天体名只使用中文译名。
- 标题中的出现不计入“正文首次出现”。
- 古希腊文原名、拉丁化转写或参考译本中的外文名应放在正文第一次自然出现处、译注或术语表中。

## 校勘版标题

如果章节标题来自现代校勘者或整理者：

1. 在 `metadata/book_specific_translation_research.md` 记录标题来源。
2. 在 `metadata/chapter_title_map.yaml` 的 `source_type` 标为 `editor`。
3. EPUB 中可使用其导航功能，但不得暗示它必然是古代作者原题。
4. 必要时在译者说明中说明标题体系。

## 禁止

- 禁止用被截断的 `#` 标题作为唯一标题依据。
- 禁止让现代目录摘要全部挤进中文主标题。
- 禁止把参考译本目录直接当成中文标题底稿。
- 禁止让 EPUB nav 使用冗长标题链。
- 禁止在章节标题、副标题或目录题名中写 `中文名（Greek/Latin transliteration）`。
- 禁止把 AI 内容概括变成读者可见标题。


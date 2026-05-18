# 《幽灵海盗》书籍信息页修正记录

review_status: "PASS"
date: "2026-05-14"

## 问题

`book-info.xhtml` 的“本书简介”复用了 OPF `description` 字段，导致简介里混入了项目制作信息和版权地域复核提醒，例如“本中文 EPUB 由 LifeBook 书坊……”一类内容。该内容不属于作品简介，应放在译者、原文来源、公版说明或 metadata 中。

## 修正

- 更新 `template/epub_pipeline/common/references/book_info_frontmatter_policy.md`，明确“本书简介”只能介绍作品本身，不得混入 EPUB 制作、译者署名、来源 URL 或版权复核提醒。
- 更新 `scripts/build_epub.js`：
  - `description` 改为纯作品简介。
  - 新增 `authorBio`。
  - 新增 `compositionBackground`。
  - `book-info.xhtml` 增加“作者简介”和“创作背景”。
- 更新 `metadata/book.yaml`，补充纯作品简介、作者简介和创作背景字段。
- 更新 `preproduction/stage1/production_spec.md`，把书籍信息页要求同步到新规则。

## 书籍信息页当前结构

- 中文书名
- 英文原名
- 作者
- 译者
- 翻译时间
- 原文来源
- 公版说明
- 本书简介
- 作者简介
- 创作背景
- 原书信息

## 验证

- `npm run build:epub`：PASS。
- `npm run lint:publication`：PASS，`zhSemicolon=0`。
- `npm run check:epub`：PASS，EPUBCheck `fatal=0`、`error=0`、`warning=0`。
- EPUB 拆包检查：
  - `book-info.xhtml` 含“本书简介”“作者简介”“创作背景”。
  - “本书简介”段落不含 `LifeBook`。
  - “本书简介”段落不含 EPUB 制作说明。
  - “本书简介”段落不含版权地域复核提醒。
  - OPF description 不含“本中文 EPUB 由……”。

# Book I EPUB Release Note / 第一卷 EPUB 发布说明

## Release v0.0.1 / 版本 v0.0.1

status: DRAFT
created: 2026-05-20T15:12:05Z

### 发布原因 / Release Reason

- 将《天文学大成》Book I.1-I.16 作为独立第一卷 EPUB 候选出版物输出。
- 修复手机分页阅读器中的表格空白页风险，并把项目 URL 改为短文字可点击链接。

### 修改内容 / Changes

- 新增确定性封面：GPT-IMAGE-2 生成无文字背景图，Pillow 脚本叠加书名、卷名、原名、作者、固定封面署名 `LifeBook 书坊 译制` 与来源说明。
- EPUB spine 固定为 `cover.xhtml`、`title-page.xhtml`、`book-info.xhtml`、前言、译制说明、Book I 正文 16 章。
- `book-info.xhtml` 使用短文字链接 `LifeBook 书坊 GitHub 项目` 指向 `SaberOnGo/public-domain-books-translation`，不在正文显示长 URL。
- Book I.11/I.15 表格改为手机分页优先的自适应 XHTML table：分段保留，去掉 `width: max-content`、固定大 `min-width` 和整表 `nowrap`。
- I.15 读者版表格移除 QA 校验状态列；校验状态保留在技术记录和源表中。
- 标准当前构建产物同步输出 `output/book.epub`。

### 问题点 / Issues

- 旧表格 CSS 在部分手机 EPUB 阅读器中会形成超宽不可分页区域，导致翻页空白或必须缩小到极小。
- 直接显示长项目 URL 会干扰窄屏排版。
- 旧 release/manifest 记录没有列出标准 `output/book.epub`。

### 修复方式 / Fixes

- 将表格 CSS 改为 `width: 100%`、`table-layout: fixed`、允许单元格换行，并用门禁禁止旧的超宽表格默认样式。
- 普通 XHTML `<a href="https://...">` 外部链接在资产门禁中被视为可点击链接；图片、CSS、manifest 等远程资产仍会被拦截。
- 发布 manifest 改用 `output/book.epub` 作为标准当前构建产物，并生成目标书名版本文件。

### QA 与证据 / QA and Evidence

- `npm run book-i:publish`: PASS；内部先运行 `preflight:template` 与 `cover:check`。
- `npm run reader:check`: PASS。
- `npm run book-i:publish-check`: PASS，checks=34。
- `npm run lint:publication`: PASS。
- `npm run lint:assets`: PASS。
- 包内检查：`EPUB/styles/book.css` 不含 `table-scroll`、`width: max-content`、`white-space: nowrap` 或 `min-width: 34em`；I.15 读者版不含 `PDF_AUDIT_DEFERRED` / `PDF_LAYOUT_AND_VALUE`。
- `npm run book-i:publish-epubcheck`: BLOCKED_JAVA，未生成 EPUBCheck JSON；当前工作站缺少可运行的 Java/JRE，`npm run book-i:publish-epubcheck` 返回 `spawnSync java ENOENT`。

### 风险 / Risks

- 标准 EPUBCheck 因当前工作站缺少 Java/JRE 未能执行；因此本版本按模板记录为 DRAFT 候选，不标记最终 PASS。
- Book I 之外的 Book II-XIII 不在本版本范围内。

### 下一轮迭代 / Next Iteration

- 在安装 Java/JRE 后重新运行 `npm run book-i:publish-epubcheck`。
- EPUBCheck fatal/error 为 0 后，再按模板将 release 状态提升为 PASS。

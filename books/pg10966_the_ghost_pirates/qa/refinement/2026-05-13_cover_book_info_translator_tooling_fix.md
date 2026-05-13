# 《幽灵海盗》封面、书籍信息与工具依赖修复记录

fix_status: "PASS"
date: "2026-05-13"

## 修复范围

- 共享 Node.js 依赖移除未使用的 `epub-gen`，仅保留实际使用的 `epubchecker`。
- 新增正式封面工程文件 `assets/cover.jpg`，尺寸 1600 x 2400，体积 363786 bytes。
- EPUB 重新打包为 `EPUB/images/cover.jpg`，OPF `cover-image` 指向 JPG，不再把临时 SVG 作为 EPUB 内封面图片。
- 书籍信息页标题从“版本说明”改为“书籍信息”，并在目录与 landmarks 中同步。
- 译者字段统一为 `LifeBook 书坊 SaberOnGo`，覆盖 OPF `dc:contributor`、`schema:translator`、书籍信息页、封面文字和本书 metadata。
- 模板提示已补充“LifeBook 书坊 + 个人名”的译者命名规则。

## 自动验证

- `npm audit`：0 vulnerabilities。
- `npm run build:epub`：PASS。
- `npm run check:epub`：PASS，EPUBCheck `fatal=0`、`error=0`、`warning=0`。
- EPUB 内部检查：
  - `EPUB/images/cover.jpg` 存在。
  - `EPUB/images/cover.svg` 不存在。
  - OPF `cover-image` 指向 `images/cover.jpg`。
  - `EPUB/book-info.xhtml` 存在，并包含 `LifeBook 书坊 SaberOnGo`。
  - `EPUB/nav.xhtml` 目录项包含“书籍信息”。

## 输出

- `output/book.epub`：466977 bytes。
- SHA256：`88294DF8BA7906D5719D9D45E4D1CEF9DBBD4FED6919C0610A5B9C4E6AD70254`。

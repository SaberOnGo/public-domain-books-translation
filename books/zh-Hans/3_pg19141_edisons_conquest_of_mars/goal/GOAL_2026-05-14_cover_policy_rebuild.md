# /goal：按最新封面与书籍信息规则重做《爱迪生征服火星》封面并重建 EPUB

status: "PASS"

## 目标

按 `template/epub_pipeline/common/references/cover_design_policy.md` 与 `book_info_frontmatter_policy.md`，以及本轮补充的封面文字规则，重新制作 `3_pg19141_edisons_conquest_of_mars` 的封面和书籍信息页，并重新生成 EPUB。

## 封面规则

- 主视觉必须使用 GPT-IMAGE-2 生成，并基于本书内容情境。
- 图像模型只生成无字主视觉；封面文字后期确定性排版。
- 中文大标题居中，尽量一行：`爱迪生征服火星`。
- 英文标题居中，字体较小，尽量一行：`Edison's Conquest of Mars`。
- 作者：`加勒特·P. 瑟维斯 著`。
- 译制署名：`LifeBook 书坊 译制`，封面不写个人名。
- 底部最多一行来源：`依据 Project Gutenberg #19141 公版原文制作`。
- 除以上内容外，封面不写其他文字。
- EPUB 内封面使用压缩 JPG，不把源 PNG 大图直接打入 EPUB。

## 书籍信息页规则

- 页面标题为“书籍信息”。
- 包含中文书名、原书名、作者译名 + 原名、译者、翻译时间、原文来源、公版说明、本书简介。
- 补充作者简介：国籍、生卒年、基本人生经历、代表作。
- 补充本书创作基本背景和简短阅读背景。
- 译者写详细格式：`LifeBook 书坊 SaberOnGo`。
- 不写制作日志、prompt、QA 过程或 AI 自述。

## 完成记录

- GPT-IMAGE-2 源图：`assets/cover_source_gpt_image.png`。
- 生成 prompt 记录：`assets/cover_source_gpt_image_prompt.txt`。
- EPUB 封面：`assets/cover.jpg`，1600 x 2400，456011 bytes。
- EPUB 内部封面：`EPUB/images/cover.jpg`，456011 bytes。
- EPUB 内部无 `EPUB/images/cover.svg`。
- OPF `cover-image` 指向 `images/cover.jpg`，media-type 为 `image/jpeg`。
- `book-info.xhtml` 含译者、作者简介、创作背景和关于本书的简短阅读背景。
- `npm run lint:publication`：PASS，硬错误 0。
- `npm run check:epub`：PASS，fatal 0，error 0，warning 0。
- `node scripts/refinement_check.js`：PASS，出版范围 BOM 0，mojibake 0，中文异常空格 0。

## Decision

PASS。封面、书籍信息页和 EPUB 输出均已按最新规则重建。

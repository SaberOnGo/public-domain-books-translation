# 2026-05-14 封面规则重做与书籍信息页复核

status: "PASS"

## 复核依据

- `template/epub_pipeline/common/references/cover_design_policy.md`
- `template/epub_pipeline/common/references/book_info_frontmatter_policy.md`
- 本轮补充规则：中文题名一行、英文题名一行、作者、`LifeBook 书坊 译制`、底部公版来源；封面不写其他内容；个人名只在书籍信息页写详细。

## 封面复核

- 源图：`assets/cover_source_gpt_image.png`，GPT-IMAGE-2 生成。
- 主视觉：纽约港废墟上方，Edison 式电力飞船舰队升空，火星压在天幕中，分解射线和电弧形成核心意象。
- EPUB 封面：`assets/cover.jpg` / `output/cover.jpg`。
- 尺寸与体积：1600 x 2400，456011 bytes，符合 2:3 和 200KB-800KB 建议区间。
- 封面文字：只含 `爱迪生征服火星`、`Edison's Conquest of Mars`、`加勒特·P. 瑟维斯 著`、`LifeBook 书坊 译制`、`依据 Project Gutenberg #19141 公版原文制作`。
- 违规文字检查：无 `LifeBook 公版新译`，无 `SaberOnGo`，无额外宣传语。

## 书籍信息页复核

- `book-info.xhtml` 标题为“书籍信息”。
- 包含中文书名、英文原名、作者、译者、翻译时间、原文来源、公版说明、本书简介和原书信息。
- 新增作者简介：记录 Garrett Putman Serviss 的国籍背景、生卒年、科普与科幻写作经历、代表作。
- 新增创作背景：记录 1898 年、威尔斯《世界大战》火星入侵想象、美国发明家崇拜和电学奇观语境。
- 新增“关于本书”：提示以十九世纪末大众科学语境理解以太、电力排斥、分解射线和电力飞船。
- 译者写详细：`LifeBook 书坊 SaberOnGo`。

## EPUB 工程复核

- EPUB 解包：`EPUB/images/cover.jpg` 存在，456011 bytes。
- EPUB 解包：无 `EPUB/images/cover.svg`。
- OPF：`cover-image` 指向 `images/cover.jpg`，media-type 为 `image/jpeg`。
- 目录：`nav.xhtml` 包含“书籍信息”。
- 书籍信息页：含 `LifeBook 书坊 SaberOnGo`、作者简介和创作背景。

## 校验

- `npm run lint:publication`：PASS，硬错误 0。
- `npm run build:epub`：PASS。
- `npm run check:epub`：PASS，fatal 0，error 0，warning 0。
- `node scripts/refinement_check.js`：PASS，出版范围 BOM 0，mojibake 0，中文异常空格 0。

## Decision

PASS。封面、书籍信息页、metadata、OPF 与 EPUB 产物已按最新规则闭环。

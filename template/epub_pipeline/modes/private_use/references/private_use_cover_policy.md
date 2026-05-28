# Private-Use Cover Policy / 私人自用封面规则

policy_status: "ACTIVE"
scope: "publication_mode=private_use only / 仅私人自用模式"

## Purpose / 目的

Private-use covers must make the EPUB usable for the individual user while avoiding any signal that the book is a public-domain, licensed, or LifeBook-published edition.

私人自用封面要方便用户个人阅读管理，但必须避免让读者误以为这是公版、授权发布或 LifeBook 公开出版版本。

## Required Text / 必备文字

- Target-language title.
- Author.

Do not add a public-project source line such as `依据 Project Gutenberg #xxxxx 公版原文制作`.

封面必须有目标语书名和作者。不要添加 `依据 Project Gutenberg #xxxxx 公版原文制作` 等公版项目来源行。

## Forbidden Text / 禁止文字

- Do not put `仅供个人自用，不传播，不商业使用` on the cover.
- Do not put public-domain source claims on the cover.
- Do not put public license wording on the cover.
- Do not use `LifeBook 书坊 译制`, `LifeBook 书坊 SaberOnGo`, or `LifeBook 书坊 + 个人名`.
- Do not imply LifeBook Shufang published or authorized this private translation.

- 封面不写 `仅供个人自用，不传播，不商业使用`。
- 封面不写公版来源声明。
- 封面不写公开授权措辞。
- 封面不使用 `LifeBook 书坊 译制`、`LifeBook 书坊 SaberOnGo` 或 `LifeBook 书坊 + 个人名`。
- 封面不得暗示 LifeBook 书坊发布或授权了该私人译本。

## Design Requirements / 设计要求

The shared cover quality requirements still apply: readable title, usable thumbnail, clear author, reasonable file size, EPUB `cover.xhtml`, and OPF `cover-image`.

通用封面质量要求仍然适用：书名清晰、缩略图可识别、作者清楚、体积合理、EPUB 内有 `cover.xhtml`，OPF 标记 `cover-image`。

Private-use boundaries belong in book-info/frontmatter and metadata. Do not force `个人学习版` onto the cover if it weakens the cover design, looks like a UI button, competes with the title, or makes the book look less like a normal reader-facing book. If a project keeps a short private-use label on the cover, it must be visually quiet and must not be the only place where the private-use boundary is stated.

私人自用边界应写在书籍信息页/前置页和 metadata 中。若 `个人学习版` 会削弱封面设计、看起来像 UI 按钮、干扰书名，或让封面不像正常读者书封，不要强行放到封面上。若某项目保留短标识，也必须低调清楚，且不能把它作为唯一的私人自用边界说明。

# 私人自用制作规格补充 / Private-Use Production Spec Addendum

private_use_spec_status: "DRAFT" # DRAFT | PASS | FAIL
publication_mode: "private_use"

This addendum is required only for `books/private/{target}/{number}_{目标语言书名}_{目标语言作者名}/` projects. It supplements the shared production spec and overrides public-domain/public-release wording where necessary.

本补充规格只用于 `books/private/{target}/{number}_{目标语言书名}_{目标语言作者名}/` 工程。它补充通用制作规格，并在必要处覆盖公版/公开发布措辞。

## Private Source / 私人书源

- Local source file name:
- Local source SHA256:
- User declaration file: `metadata/private_use_declaration.md`
- Rights decision: `PRIVATE_USE_PASS` / `FAIL`

Do not record the user's local absolute path in reader-facing files or publishable templates.

不得在读者可见文件或可发布模板中记录用户本机绝对路径。

## Cover / 封面

Private-use covers must be visually complete but must not present the book as a public-domain or public-domain-books-translation-published edition.

私人自用封面必须完整可读，但不得把书包装成公版或 public-domain-books-translation 项目出版版本。

Required cover text:

1. Target-language title.
2. Author.

Private-use boundaries must be stated in book-info/frontmatter and metadata. Do not force `个人学习版` onto the cover if it weakens the cover design, looks like a UI button, or competes with the title.

私人自用边界必须写在书籍信息页/前置页和 metadata 中。若 `个人学习版` 会削弱封面设计、看起来像 UI 按钮或干扰书名，不要强行放到封面上。

Forbidden cover text:

- Public-domain source line such as `依据 Project Gutenberg ... 制作`.
- Long rights disclaimer such as `仅供个人自用，不传播，不商业使用`.
- `LifeBook 书坊 译制`.
- `LifeBook 书坊 SaberOnGo`.
- `LifeBook 书坊 + 个人名`.

## Book Info / Frontmatter / 首页与前置页

The private-use book-info/frontmatter page must not contain public-domain notices or public release license wording.

私人自用首页/前置页不得包含公版说明或公开发布授权措辞。

Required reader-facing wording:

- Edition label: `私人学习版本` or target-language equivalent.
- Producer line: `参考public-domain-books-translation 开源项目 个人自制`.
- Local source evidence: local file name and SHA256 summary only.
- Rights/use boundary: `仅供个人自用，不传播，不商业使用`.
- Risk boundary: 风险由个人承担；public-domain-books-translation 开源项目仅用于公版书翻译发布，不承担其他个人翻译、保存、传播或使用非公版内容导致的版权风险及责任。

Forbidden book-info/frontmatter wording:

- `公版说明`
- `公版来源`
- `Project Gutenberg` as a public-domain source claim unless the source really is public-domain and the project mode has been changed accordingly.
- `CC BY-NC-SA 4.0`
- `公开授权`
- `可发布`
- `公开 release`
- `LifeBook 书坊 SaberOnGo`
- `LifeBook 书坊 + 个人名`
- `LifeBook 书坊 译制`

## Private Artifacts / 私人产物

- Current build: `output/book.epub`
- Versioned private artifacts: `output/private_artifacts/{title}_private_vX.X.X.epub`
- Private artifact state: `output/private_artifacts/private_artifact_state.json`
- Private artifact notes: `output/private_artifacts/private_artifact_notes.md`

`output/private_artifacts/` is a local-only private artifact directory. It is not a public release directory and must not be published to GitHub.

`output/private_artifacts/` 是本地私人产物目录，不是公开 release 目录，不得发布到 GitHub。

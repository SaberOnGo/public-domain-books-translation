# Private-Use Mode Overlay / 私人自用模式覆盖层

This directory is copied only for `publication_mode=private_use` projects created with:

```powershell
books/scripts/create_book_project.py --mode private-use --local-source-file ... --private-use-declaration ...
```

本目录只会复制到 `publication_mode=private_use` 的私人自用工程中。

## Boundary / 边界

- This mode is for a user-provided local source file only.
- The produced EPUB is a private personal-study artifact, not a public release.
- Concrete source text, translations, QA, EPUB output, and book metadata must stay under ignored `books/private/{target}/{number}_{slug}/`.
- Public projects under `books/{target}/` must not contain this overlay.

- 本模式只用于用户提供的本地书源。
- 生成的 EPUB 是个人学习自用产物，不是公开 release。
- 具体原文、译文、QA、EPUB 输出和书籍 metadata 必须留在被 Git 忽略的 `books/private/{target}/{number}_{slug}/` 下。
- 公开项目 `books/{target}/` 不得包含本覆盖层文件。

## Reader-Facing Rules / 读者可见规则

- Private-use cover bottom line: `个人学习版`.
- Private-use frontmatter producer line: `参考LifeBook书坊 个人自制`.
- Private-use frontmatter must not contain public-domain notices, public licenses, public release wording, or public source claims unless the source is actually public-domain.
- Rights/risk wording must state: `仅供个人自用，不传播，不商业使用`，风险由个人承担；LifeBook书坊仅发布 LifeBook 翻译发布系统，不承担任何因其他个人翻译、保存、传播或使用非公版内容导致的版权风险及责任。

## Scripts / 脚本

- `scripts/check_private_use_gate.py`: verifies project mode, path, declaration, overlay files, and private package scripts.
- `scripts/check_private_reader_facing_policy.py`: blocks public-domain/public-release wording in private frontmatter and enforces private cover/frontmatter wording.
- `scripts/create_private_artifact.py`: creates versioned private artifacts under `output/private_artifacts/`.
- `scripts/build_private_epub.js`: distinct private-use build entry point that delegates to the shared EPUB builder.

# Private-Use Mode Overlay / 私人自用模式覆盖层

This directory is copied only for `publication_mode=private_use` projects created with:

```powershell
books/scripts/create_book_project.py --mode private-use --local-source-file ... --private-use-declaration ...
```

本目录只会复制到 `publication_mode=private_use` 的私人自用工程中。

## Boundary / 边界

- This mode is for a user-provided local source file only.
- The produced EPUB is a private personal-study artifact, not a public release.
- Concrete source text, translations, QA, EPUB output, and book metadata must stay under ignored `books/private/{target}/{number}_{目标语言书名}_{目标语言作者名}/`.
- Public projects under `books/{target}/` must not contain this overlay.

- 本模式只用于用户提供的本地书源。
- 生成的 EPUB 是个人学习自用产物，不是公开 release。
- 具体原文、译文、QA、EPUB 输出和书籍 metadata 必须留在被 Git 忽略的 `books/private/{target}/{number}_{目标语言书名}_{目标语言作者名}/` 下。
- 公开项目 `books/{target}/` 不得包含本覆盖层文件。

## Reader-Facing Rules / 读者可见规则

- Private-use cover: no public-domain source claims and no long rights disclaimers.
- Private-use frontmatter producer line: `参考public-domain-books-translation 开源项目 个人自制`.
- Private-use frontmatter must not contain public-domain notices, public licenses, public release wording, or public source claims unless the source is actually public-domain.
- Rights/risk wording must state: `仅供个人自用，不传播，不商业使用`，风险由个人承担；public-domain-books-translation 开源项目仅用于公版书翻译发布，不承担其他个人翻译、保存、传播或使用非公版内容导致的版权风险及责任。

## Translation Quality / 译文质量

- Private-use mode changes rights and distribution boundaries; it does not lower the translation-quality bar.
- Translation, chapter controls, random review, private artifact review, and reader-feedback fixes must use `skills/expert-translation-quality/SKILL.md` when expert-level prose, context-dependent word choice, or polysemy back-checking matters.
- Chapter controls and random review evidence must stay under the ignored private book project, not in publishable `books/{target}/` directories.

- 私人自用模式只改变权利和传播边界，不降低译文质量门槛。
- 翻译、章节 control、随机抽检、私人产物审阅和读者反馈修复中，只要涉及专家级译文、上下文依赖选义或多义词回看，必须使用 `skills/expert-translation-quality/SKILL.md`。
- 章节 control 和随机抽检证据必须留在被忽略的私人书籍工程中，不得放入可发布的 `books/{target}/` 目录。

## Scripts / 脚本

- `package.json`: private-use script overlay only. It must add private gates and private artifact aliases without replacing language-pair scripts such as target-language `lint:publication` commands.
- `scripts/check_private_use_gate.py`: verifies project mode, path, declaration, overlay files, and private package scripts.
- `scripts/check_private_reader_facing_policy.py`: blocks public-domain/public-release wording in private frontmatter and enforces private cover/frontmatter wording.
- `scripts/create_private_artifact.py`: creates versioned private artifacts under `output/private_artifacts/`.
- `scripts/build_private_epub.js`: distinct private-use build entry point that delegates to the shared EPUB builder.

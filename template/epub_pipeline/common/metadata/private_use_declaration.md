# Private Use Declaration / 私人自用声明

private_use_status: `DRAFT` # DRAFT | PRIVATE_USE_PASS | FAIL

This file is required only for `publication_mode=private_use` projects under `books/private/{target}/{number}_{target_language_title}_{target_language_author}/`.

本文件只用于 `books/private/{target}/{number}_{目标语言书名}_{目标语言作者名}/` 下的 `publication_mode=private_use` 工程。

## User Declaration / 用户声明

- Personal study only:
- No redistribution:
- No commercial use:
- User-provided local source file:
- Declaration timestamp:

## Source Evidence / 书源证据

- Local source file name:
- Local source SHA256:
- Source acquired by user:
- Source URL or store/library record if available:

Do not record a local absolute path in publishable files. A private project may record the local file name and checksum so the user can verify the source without exposing a workstation path.

不得在可发布文件中记录本机绝对路径。私人项目可以记录本地文件名和校验和，便于用户核对书源，同时避免暴露工作站路径。

## Boundaries / 边界

- The project may translate, review, build EPUB, run stratified random spot-checks, and create private-use versioned artifacts for the user's personal study.
- Personal risk is borne by the individual user.
- LifeBook Shufang publishes only the LifeBook translation publishing system.
- LifeBook Shufang does not assume copyright risk or liability caused by other individuals' translation, storage, redistribution, or use of non-public-domain content.
- The project must not publish source text, translations, QA files, EPUB output, or book-specific metadata to GitHub.
- The project must not treat private-use artifacts as public release artifacts.
- If the user did not provide a local source file, the agent must search only public-domain, authorized, or otherwise clearly lawful sources.

- 本工程可以为了用户个人学习进行翻译、审校、EPUB 构建、分层随机抽检，并生成私人自用版本化产物。
- 风险由个人承担。
- LifeBook书坊仅发布 LifeBook 翻译发布系统。
- LifeBook书坊不承担任何因其他个人翻译、保存、传播或使用非公版内容导致的版权风险及责任。
- 本工程不得把原文、译文、QA、EPUB 输出或具体书籍 metadata 发布到 GitHub。
- 本工程不得把私人自用产物当作公开 release。
- 如果用户没有提供本地书源文件，agent 只能查找公版、授权或其他权利清楚的合法来源。

## Decision / 结论

- `PRIVATE_USE_PASS` or `FAIL`:
- Reason:

# LifeBook Shufang Public-Domain Translation Project

<table align="center">
  <tr>
    <td align="center"><strong><a href="./readme/README.md">简体中文</a></strong></td>
    <td align="center"><strong><a href="./readme/README.zh-TW.md">繁體中文</a></strong></td>
    <td align="center"><strong><a href="./readme/README.en.md">English</a></strong></td>
    <td align="center"><strong><a href="./readme/README.ja.md">日本語</a></strong></td>
  </tr>
</table>

LifeBook Shufang is a global, multilingual project for translating public-domain books and producing high-quality EPUB editions with AI-assisted workflows and human review.

LifeBook 书坊是一个全球多语言公版书翻译与 EPUB 制作协作项目。它使用 AI 提高整理、翻译、审校和制书效率，但最终质量仍依赖人的判断、校对和阅读体验检查。

## What This Project Does

Many public-domain books are legally available but still difficult to read across languages, regions, and devices. This project helps contributors turn reliable public-domain sources into readable, reviewable, and reusable EPUB editions.

许多公版书虽然已经可以合法获取，但在不同语言、地区和设备上仍然不容易阅读。本项目希望把可靠来源的公版作品整理成可翻译、可审校、可追踪、可制作 EPUB 的协作工程。

The project is not limited to one language direction. Templates can support many pairs, for example French to English, Japanese to Spanish, Chinese to English, English to Indonesian, German to Traditional Chinese, or English to Simplified Chinese.

本项目不只面向某一个翻译方向。模板可以支持多种语言组合，例如法语到英语、日语到西班牙语、中文到英语、英语到印尼语、德语到繁体中文、英语到简体中文等。

## Why It Matters

- Public-domain works should be easier to discover, translate, read, and preserve.
- AI can accelerate repetitive work, but raw AI output should not be treated as a finished book.
- A book project should keep source evidence, rights checks, terminology, translation notes, QA reports, EPUB output, and retrospective records together.
- Small contributions should be useful: one chapter review, one terminology correction, one source note, one EPUB test, or one proofread paragraph can all improve a book.

- 公版作品应该更容易被发现、翻译、阅读和保存。
- AI 可以加速重复劳动，但 AI 初稿不能直接当作成书发布。
- 每本书都应该保留来源证据、版权核查、术语表、翻译说明、质量报告、EPUB 输出和复盘记录。
- 小贡献也应该有价值：审一章、改一个术语、补一条来源、试读一次 EPUB、校对一段文字，都能让一本书变好。

## How The Pipeline Works

1. Verify the source and public-domain status.
2. Create a book workspace under `books/{book_id_slug}/`.
3. Copy the shared EPUB pipeline from `template/epub_pipeline/common`.
4. Overlay the matching language-pair template, such as `template/epub_pipeline/en-zh-Hans`.
5. Run research, terminology preparation, trial translation, chapter translation, review, quality gates, EPUB production, validation, and retrospective.

1. 先确认来源可靠，并核查公版状态。
2. 在 `books/{book_id_slug}/` 下创建具体书籍工程。
3. 先复制共享 EPUB 流水线：`template/epub_pipeline/common`。
4. 再覆盖对应语言方向模板，例如 `template/epub_pipeline/en-zh-Hans`。
5. 依次执行译前研究、术语准备、试译、章节翻译、审校、质量门禁、EPUB 制作、格式校验和复盘。

## Ways To Contribute

You do not need to translate a whole book. Useful contributions include:

- finding reliable public-domain source texts;
- checking copyright and source evidence;
- building or improving language-pair templates;
- reviewing chapter translations for readability and accuracy;
- improving terminology, names, dates, places, and historical notes;
- testing EPUB files on phones, tablets, e-readers, and desktop readers;
- improving prompts, quality gates, scripts, and documentation.

你不需要一次翻译整本书。可以参与的事情包括：

- 寻找可靠的公版原文来源；
- 核查版权状态与来源证据；
- 新增或改进语言方向模板；
- 审校章节译文的准确性和可读性；
- 改进术语、人名、日期、地点和历史说明；
- 在手机、平板、电纸书和桌面阅读器上试读 EPUB；
- 改进 prompt、质量门禁、脚本和文档。

## Repository Map

- [readme/](./readme/) contains detailed localized README files.
- [license/](./license/) contains public license, contributor rules, and commercial-use notes.
- [template/epub_pipeline/](./template/epub_pipeline/) contains shared and language-pair EPUB pipeline templates.
- [books/](./books/) is reserved for concrete book projects.
- [skills/](./skills/) contains public AI-agent workflow instructions for this repository.
- [AGENTS.md](./AGENTS.md) contains mandatory public instructions for AI agents.

- [readme/](./readme/) 存放详细的多语言 README。
- [license/](./license/) 存放公开许可证、贡献者规则和商业使用说明。
- [template/epub_pipeline/](./template/epub_pipeline/) 存放共享模板与语言方向模板。
- [books/](./books/) 用于放置具体书籍工程。
- [skills/](./skills/) 存放本仓库公开的 AI agent 工作说明。
- [AGENTS.md](./AGENTS.md) 存放 AI agent 必须遵守的公开指令。

## Start Here

For readers and contributors:

- Read the detailed guide in your preferred language: [简体中文](./readme/README.md), [繁體中文](./readme/README.zh-TW.md), [English](./readme/README.en.md), [日本語](./readme/README.ja.md).
- Check the license and contribution rules in [license/](./license/).
- Open an issue or pull request for source suggestions, template improvements, translation review, EPUB fixes, or documentation improvements.

对读者和贡献者：

- 先阅读你熟悉语言的详细说明：[简体中文](./readme/README.md)、[繁體中文](./readme/README.zh-TW.md)、[English](./readme/README.en.md)、[日本語](./readme/README.ja.md)。
- 再查看 [license/](./license/) 中的许可证与贡献者规则。
- 可以通过 issue 或 pull request 提交书源建议、模板改进、译文审校、EPUB 修复或文档改进。

For AI agents:

- Read [AGENTS.md](./AGENTS.md) first.
- Then read [skills/public-domain-epub-pipeline/SKILL.md](./skills/public-domain-epub-pipeline/SKILL.md).
- For book work, never write book-specific output back into `template/`; use `books/{book_id_slug}/`.

对 AI agent：

- 必须先读取 [AGENTS.md](./AGENTS.md)。
- 然后读取 [skills/public-domain-epub-pipeline/SKILL.md](./skills/public-domain-epub-pipeline/SKILL.md)。
- 处理具体书籍时，不得把书籍产物写回 `template/`，只能写入 `books/{book_id_slug}/`。

## License

Non-code book content is generally released under `CC BY-NC-SA 4.0` unless a file states otherwise. Code is generally released under the MIT License unless a file or directory states otherwise. Third-party commercial use requires separate permission from LifeBook Shufang and relevant rights holders.

除非文件另有说明，非代码书籍内容通常按 `CC BY-NC-SA 4.0` 公开发布；代码通常按 MIT License 发布。第三方商业使用必须另行取得 LifeBook 书坊及相关权利人的授权。

See [license/](./license/) for the full terms.

完整说明见 [license/](./license/)。

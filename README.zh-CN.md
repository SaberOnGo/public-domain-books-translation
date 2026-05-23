# LifeBook 书坊公版书翻译项目

<table align="center">
  <tr>
    <td align="center"><h3><a href="./README.zh-CN.md">简体中文</a></h3></td>
    <td align="center"><h3><a href="./readme/README.zh-TW.md">繁體中文</a></h3></td>
    <td align="center"><h3><a href="./README.md">English</a></h3></td>
    <td align="center"><h3><a href="./readme/README.ja.md">日本語</a></h3></td>
  </tr>
</table>

LifeBook 书坊是一个多语言公版书翻译与 EPUB 制作流程。它不是把 AI 初稿直接发布的项目，而是把来源证据、版权核查、初译、审校、EPUB 校验、分层随机抽检和版本化发布都保留下来，方便人和 AI 一起复核。

你不需要会写代码也能参与：可以推荐书、查公版来源、试读章节、对照原文、反馈别扭句子、测试 EPUB，或改进模板和脚本。

## 快速开始

更短的使用说明见：

- [简体中文说明](./doc/public/how-to-use-prompts.zh-CN.md)
- [繁體中文說明](./doc/public/how-to-use-prompts.zh-TW.md)
- [English guide](./doc/public/how-to-use-prompts.en.md)
- [日本語ガイド](./doc/public/how-to-use-prompts.ja.md)

给 AI 客户端的最小提示：

```text
我要翻译的书：{书名、作者；如果已有可靠来源 URL，也可以贴上}
目标语言：{例如 简体中文、英文、日文、西班牙文}

请先读取 AGENTS.md，再读取 template/epub_pipeline 下的相关规则。
使用 books/scripts/create_book_project.py 创建书籍工程。
不要把具体书籍的原文、译文、QA、EPUB 输出或 metadata 写进 template/。
如果来源证据或公版状态不清楚，请停止。
```

## AI 客户端

本仓库不绑定模型。Codex App、Claude Code、OpenCode、aider、Antigravity 或其他能读取本地文件的 AI 客户端都可以用，只要它能读仓库、改文件、运行命令，并遵守 `AGENTS.md`。

如果想让普通用户开箱即用，使用 **LifeBook Launcher**：

- Windows 用户当前可双击：`tools\lifebook-launcher\LifeBook Launcher Setup.exe`。
- 发布版用户只需要下载并双击 **LifeBook Launcher** 应用或安装包；Launcher 会自动准备和更新 LifeBook 项目目录，Windows 默认项目目录是 `D:\LifeBook`。
- 仓库中的源码目录是 `tools/lifebook-launcher/source/`，供开发者打包和维护。
- 它会自动维护 LifeBook 项目更新、检查/更新 OpenCode Desktop、支持 LifeBook Launcher 自更新，并允许用户设置开机自动启动。

Launcher 不会保存 API Key，也不会把 OpenCode 本体放进本仓库。详见 [LifeBook Launcher 设计说明](./docs/lifebook-launcher/design.zh-CN.md) 和 [OpenCode 客户端说明](./docs/ai-clients/opencode.zh-CN.md)。

## 用户需要知道的重要目录

- `.\template\epub_pipeline`：查看当前有哪些源语言/语言方向模板。`en-zh-Hans`、`ja-zh-Hans`、`grc-zh-Hans` 等目录都在这里。
- `.\tools\lifebook-launcher`：LifeBook Launcher 启动器目录。Windows 用户双击里面的 `LifeBook Launcher Setup.exe`。
- `.\doc\public\user_prompt`：公共启动提示词目录。用户想了解提示词细节，或想手动调整给 AI 的 prompt，可以看这里。
- `.\books\zh-Hans`：简体中文书籍工程和成书输出目录。翻译成功后，到对应书籍目录里找 `output\book.epub` 和 `output\release\`。

## 仓库结构

- `AGENTS.md`：所有 AI agent 必须先读的规则。
- `template/epub_pipeline/`：权威流程模板和规则。
- `template/epub_pipeline/common/`：通用 EPUB 流程、脚本、来源证据、版权核查、质量门禁、随机抽检和发布规则。
- `template/epub_pipeline/{source-target}/`：具体语言方向的提示词、术语、文风和审校规则。
- `template/epub_pipeline/targets/{target}/`：目标语言质量规则。
- `template/epub_pipeline/profiles/{profile-target}/`：特殊书籍类型的附加规则。
- `books/{target}/{number}_{book_slug}/`：具体书籍工程。书籍内容只能写在这里。
- `books/`：共享 Node.js 工具依赖，统一安装一次。
- `doc/public/`：公开说明、prompt 使用文档和候选书资料。
- `research/{source-target}/`：特定语言方向调研产物。
- `.opencode/` 与 `opencode.jsonc`：OpenCode 薄适配层，不是流程规则源。
- `tools/lifebook-launcher/`：LifeBook Launcher 桌面启动器入口；`source/` 内是开发源码。

## 创建新书

不要手动复制模板，使用脚本：

```powershell
cd books
npm run new:book -- {book_id_slug} --source-target {source-target}
```

新书目录格式：

```text
books/{target}/{number}_{book_id_slug}/
```

脚本会先复制 `template/epub_pipeline/common`，再覆盖对应语言方向模板。若书籍需要特殊 profile，再叠加 `profiles/{profile-target}/`。

## 核心规则

- 翻译前必须保留来源证据和版权核查记录。
- 不使用现代受版权保护译本、盗版站或来源不明 EPUB。
- AI 初稿不能直接发布。
- 具体书籍内容不能写回 `template/`。
- 面向人的重要模板文件必须包含目标贡献者能读懂的本地语言。
- 最终交付前必须经过 EPUB 校验、读者可见内容检查、分层随机抽检和版本化 release。

## 书籍工具

共享依赖只安装一次：

```powershell
cd books
npm install
```

然后进入具体书籍工程运行：

```powershell
npm run build:epub
npm run check:epub
npm run review:random-samples
npm run review:random-validate:pass
npm run release:create
```

## 参与方式

有价值的贡献包括：找公版来源、查版权、审译文、统一术语、测试 EPUB、反馈排版可读性、改进自动化脚本。优先做小而可复核的修改，不做无法追踪的大段重写。

## 版权和授权

每本源书都要单独核查版权。某文本在一个国家进入公版，不代表自动在所有地区都进入公版。

本项目产生的译文、注释、封面、排版和 EPUB 打包等非代码内容，默认按 `CC BY-NC-SA 4.0` 发布；第三方商业使用必须另行取得 LifeBook 书坊及相关权利人的授权。

参见：

- [LICENSE.md](./license/LICENSE.md)
- [CONTRIBUTING.md](./license/CONTRIBUTING.md)
- [COMMERCIAL_LICENSE.md](./license/COMMERCIAL_LICENSE.md)

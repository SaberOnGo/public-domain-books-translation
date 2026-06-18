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

您不需要会写代码也能参与：可以推荐书、查公版来源、试读章节、对照原文、反馈别扭句子、测试 EPUB，或改进模板和脚本。

## 快速开始

更短的使用说明见：

- [简体中文说明](./doc/public/how-to-use-prompts.zh-CN.md)
- [繁體中文說明](./doc/public/how-to-use-prompts.zh-TW.md)
- [English guide](./doc/public/how-to-use-prompts.en.md)
- [日本語ガイド](./doc/public/how-to-use-prompts.ja.md)

给 AI 客户端的最小提示：

```text
我要翻译的书：{书名、作者（可选）；如果已有可靠来源 URL，也可以贴上}
目标语言：{例如 简体中文、英文、日文、西班牙文}
[重点专有名词(人名、地名、术语、罕见名词、音译后体验很差的名字等) 的翻译格式] 设置 = 3

请自动选择正确的翻译 prompt：
- 如已有对应语言方向模板，执行 doc/public/user_prompt/book_translation_existing_template.md。
- 如无对应语言方向模板，执行 doc/public/user_prompt/book_translation_new_template.md。

除非版权或来源无法确认，不要让我填写技术字段。请自动查找可靠公版来源，自动创建项目，完成翻译、审校、EPUB 构建、分层随机抽检和 release。
翻译执行时必须逐章执行“每章译后全量检查并修复”：发现任何问题时，先修复该章，但该轮不能 PASS，必须追加新一轮整章复查，直到最新一轮零问题 PASS。
第一版 EPUB 后必须执行“分层随机抽检与问题族追杀”：抽检发现任何问题，不得只修被抽中的样本；必须在当轮归纳问题族、全书同类审计、修复确认命中、记录例外，并用新 seed 追加一轮。译文质量问题族必须使用 `skills/translation-quality-defect-families/SKILL.md`。
未声明是否启用 LifeBook Digest 时，请自动判断；长篇小说、专业书籍、哲学书在 EPUB 输出后生成 Digest，短篇小说、自然科学类和其他类型不生成。
如需生成 Digest，请在书籍工程根目录写入 `digest.config.json`（`enabled=true`、`merge_into_epub=true`），并在仓库根目录运行：`python -m digest.lifebook_digest --book-root books/{target}/{number}_{目标语言书名}_{目标语言作者名}`。输出仍然是标准 EPUB。
```

专有名词翻译格式设置可省略，默认值为 `3`。取值含义：`1` 直接翻译成目标语言；`2` 保留原文不翻译；`3` 第一次正文出现写 `译名（原文）`，后续用译名；`4` 第一次正文出现写 `译名（原文）`，后续用原文；`5` 第一次正文出现写 `译名（原文）` 并使用合规注号，后续用译名。

如果已经生成第一版 EPUB，但想继续提高质量，请不要只写“帮我精修”。使用 how-to-use 文档里的两个后期 prompt：先按需要执行 **Prompt B：章节全量复检与修复**，再执行 **Prompt C：分层随机抽检与问题族追杀**。

如果是非公版书，只能使用本地私人模式。用户必须提供自己的本地电子书文件，并明确声明仅供个人学习自用、不传播、不商业使用；AI 应创建 `books/private/{target}/{number}_{目标语言书名}_{目标语言作者名}/` 下的私人工程。脚本还会叠加 `template/epub_pipeline/modes/private_use/`，把私人封面、首页/前置页和产物规则与公版发布规则隔离。`books/private/` 被 Git 忽略，里面的原文、译文、QA、EPUB 和私人产物不能发布到 GitHub。

## AI 客户端

本仓库不绑定模型。Codex App、Claude Code、OpenCode、aider、Antigravity 或其他能读取本地文件的 AI 客户端都可以用，只要它能读仓库、改文件、运行命令，并遵守 `AGENTS.md`。

如果想让普通用户开箱即用，使用 **LifeBook Launcher**：

- Windows 用户当前可双击：`tools\lifebook-launcher\LifeBook Launcher Setup.exe`。
- 发布版用户只需要下载并双击 **LifeBook Launcher** 应用或安装包；Launcher 会自动准备和更新 LifeBook 项目目录，Windows 默认项目目录是 `D:\LifeBook`。
- 仓库中的源码目录是 `tools/lifebook-launcher/source/`，供开发者打包和维护。
- 它会自动维护 LifeBook 项目更新、检查/更新 OpenCode Desktop、支持 LifeBook Launcher 自更新，并允许用户设置开机自动启动。

Launcher 不会保存 API Key，也不会把 OpenCode 本体放进本仓库。OpenCode客户端使用见 [OpenCode 客户端说明](./doc/project/ai-clients/opencode.zh-CN.md)。

## 用户需要知道的重要目录

- `.\template\epub_pipeline`：查看当前有哪些源语言/语言方向模板。`English-to-Simplified-Chinese`、`Japanese-to-Simplified-Chinese`、`Ancient-Greek-to-Simplified-Chinese` 等目录都在这里。
- `.\tools\lifebook-launcher`：LifeBook Launcher 客户端安装启动目录。用户需要知道这个位置，以使用 LifeBook 项目和安装 OpenCode。
- `.\doc\public\user_prompt`：公共启动提示词目录。用户想了解提示词细节，或想手动调整给 AI 的 prompt，可以看这里。
- `.\books\zh-Hans`：最重要的成书目录。翻译成简体中文成功后，到对应书籍目录里找 `output\release\`；只有 release 目录里的成品才算可发布结果。
- `.\books\private`：本地私人自用书籍工程目录。这里用于用户提供本地书源的非公版个人学习翻译，已被 Git 忽略，不能发布到 GitHub。

## LifeBook Digest

<table align="center">
  <tr>
    <td align="center"><h3><a href="./readme/digest/README.zh-CN.md">LifeBook Digest 说明</a></h3></td>
    <td align="center"><h3><a href="./license/DIGEST_LICENSE.md">Digest 许可证</a></h3></td>
  </tr>
</table>

LifeBook 翻译发布系统增加了 LifeBook Digest 模块。它把书读薄：在 EPUB 输出后，LifeBook Digest 可以把长篇书籍交给 AI agent 自动提炼核心内容。处理结果不只是文字摘要，也会生成章节拓扑与知识脉络图，让整本书结构更容易一眼看清，为读者提供新的阅读视角。

LifeBook Digest 当前实现为独立的 LifeBook 后处理模块。致谢与第三方启发说明见 [LifeBook Digest 说明](./readme/digest/README.zh-CN.md) 和 [Digest 许可证](./license/DIGEST_LICENSE.md)；许可证与后续复用约束以 [Digest 许可证](./license/DIGEST_LICENSE.md) 为准。

## 仓库结构

- `AGENTS.md`：所有 AI agent 必须先读的规则。
- `digest/`：LifeBook Digest 通用后处理模块；由具体书籍的 `digest.config.json` 控制是否启用、是否合并进 EPUB。
- `template/epub_pipeline/`：权威流程模板和规则。
- `template/epub_pipeline/common/`：通用 EPUB 流程、脚本、来源证据、版权核查、质量门禁、随机抽检和发布规则。
- `template/epub_pipeline/{language-pair-template}/`：具体语言方向的提示词、术语、文风和审校规则。
- `template/epub_pipeline/targets/{target}/`：目标语言质量规则。
- `template/epub_pipeline/profiles/{profile-target}/`：特殊书籍类型的附加规则。
- `template/epub_pipeline/modes/private_use/`：只复制到非公版个人自用项目的模式覆盖层，包含私人封面、首页/前置页、私人产物和门禁脚本。
- `books/{target}/{number}_{目标语言书名}_{目标语言作者名}/`：具体书籍工程。数字后使用目标语言可读书名和作者名；书籍内容只能写在这里。
- `books/`：共享 Node.js 工具依赖，统一安装一次。
- `doc/public/`：公开说明、prompt 使用文档和候选书资料。
- `doc/project/`：项目工程文档、AI 客户端说明、Launcher 设计和实施计划。
- `research/{language-pair-template}/`：特定语言方向调研产物。
- `.opencode/` 与 `opencode.jsonc`：OpenCode 薄适配层，不是流程规则源。
- `tools/lifebook-launcher/`：LifeBook Launcher 桌面启动器入口；`source/` 内是开发源码。

## 创建新书

不要手动复制模板，使用脚本：

```powershell
cd books
npm run new:book -- "{目标语言书名}_{目标语言作者名}" --source-target {language-pair-template}
```

新书目录格式：

```text
books/{target}/{number}_{目标语言书名}_{目标语言作者名}/
```

脚本会先复制 `template/epub_pipeline/common`，再覆盖对应语言方向模板。若书籍需要特殊 profile，再叠加 `profiles/{profile-target}/`。私人自用项目还会最后叠加 `template/epub_pipeline/modes/private_use/`。

私人自用项目必须显式使用 `private-use` 模式：

```powershell
cd books
npm run new:book -- "{目标语言书名}_{目标语言作者名}" --source-target {language-pair-template} --mode private-use --local-source-file "{path_to_local_ebook}" --private-use-declaration "仅供个人学习自用；不传播；不用于商业。"
```

私人模式不降低翻译、审校、EPUB 校验、分层随机抽检要求，但会改变权利、读者可见措辞和产物语义。私人封面底部使用 `个人学习版`；私人首页/前置页使用 `参考public-domain-books-translation 开源项目 个人自制`，去掉所有公版说明，并写明仅供个人自用、不传播、不商业使用、风险由个人承担。私人产物写入 `output/private_artifacts/`，不是公开 release。

## 核心规则

- 翻译前必须保留来源证据和版权核查记录；公开项目必须是公版或授权来源。
- 非公版个人自用项目必须进入 `private_use` 模式，并保存在被 Git 忽略的 `books/private/` 下。
- 私人自用项目必须带有 `modes/private_use` 覆盖层，不得复用公版封面、首页/前置页和公开 release 措辞。
- 不使用现代受版权保护译本、盗版站或来源不明 EPUB。
- AI 初稿不能直接发布。
- 每章译后必须完成当前章全量检查并修复；发现问题后追加整章复查，直到最新轮零问题 PASS。
- 具体书籍内容不能写回 `template/`。
- 面向人的重要模板文件必须包含目标贡献者能读懂的本地语言。
- 第一版 EPUB 后必须执行分层随机抽检；发现问题必须当轮归纳为问题族，做全书同类审计、修复、关闭，并用新 seed 复抽。
- 译文质量问题族必须沉淀到 `skills/translation-quality-defect-families/SKILL.md`，但只合并可复用经验，不盲目重复追加。
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

私人自用项目在同样完成 build、EPUBCheck 和分层随机抽检后，使用私人产物命令：

```powershell
npm run build:private-epub
npm run check:epub
npm run review:random-samples
npm run review:random-validate:pass
npm run private:artifact:create
```

## 参与方式

有价值的贡献包括：找公版来源、查版权、审译文、统一术语、测试 EPUB、反馈排版可读性、改进自动化脚本。优先做小而可复核的修改，不做无法追踪的大段重写。

## 版权和授权

每本源书都要单独核查版权。某文本在一个国家进入公版，不代表自动在所有地区都进入公版。

本项目产生的译文、注释、封面、排版和 EPUB 打包等非代码内容，默认按 `CC BY-NC-SA 4.0` 发布；第三方商业使用必须另行取得 LifeBook 书坊及相关权利人的授权。

`books/private/` 下的私人自用项目不属于公开发布内容，不适用默认公开授权，不得提交或发布到 GitHub。任何私人译本仅供个人自用，不传播，不商业使用；相关风险由个人承担。public-domain-books-translation 开源项目仅用于公版书翻译发布，不承担其他个人翻译、保存、传播或使用非公版内容导致的版权风险及责任。

参见：

- [LICENSE.md](./license/LICENSE.md)
- [CONTRIBUTING.md](./license/CONTRIBUTING.md)
- [COMMERCIAL_LICENSE.md](./license/COMMERCIAL_LICENSE.md)

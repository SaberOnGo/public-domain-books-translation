# 小白用户使用说明：只填三项内容

这套 prompt 的目标是：用户不需要懂 EPUB、source-target、slug、模板、抽检、release。用户只要给 AI 三项内容：

1. 我要翻译的书是什么。
2. 我要翻译成什么语言。
3. 请 AI 自动选择正确的翻译 prompt。完整写法见下面的[最省事的推荐入口](#最省事的推荐入口)。

其他事情都交给 AI Agent 自动完成：找可靠公版/授权来源或记录私人本地书源、判断源语言、选择或创建模板、建立书籍项目、翻译、审校、构建 EPUB、随机抽检、生成 release 或私人版本化产物。

## 用户需要知道的 5 个目录

- `.\template\epub_pipeline`：查看当前有哪些源语言/语言方向模板。用户不需要判断模板，但如果想确认“已有模板/没有模板”，看这里。
- `.\tools\lifebook-launcher`：LifeBook Launcher 客户端安装启动目录。用户需要知道这个位置，以使用 LifeBook 项目和安装 OpenCode。
- `.\doc\public\user_prompt`：公共 prompt 目录。用户想了解提示词细节，或想手动修改 prompt，可以看这里。
- `.\books\zh-Hans`：最重要的成书目录。翻译成简体中文成功后，到对应书籍目录里找 `output\release\`；只有 release 目录里的成品才算可发布结果。
- `.\books\private`：非公版私人自用工程目录。这里被 Git 忽略，里面的原文、译文、QA 和 EPUB 不能发布到 GitHub。

## 你只需要这样写

如果仓库里已经有这个源语言到目标语言的模板，例如日语到简体中文、英语到简体中文、古希腊语到简体中文：

```text
我要翻译的书：谷崎润一郎《刺青》
目标语言：简体中文

请自动选择正确的翻译 prompt：
- 如已有对应源语言模板，执行 doc/public/user_prompt/book_translation_existing_template.md。
- 如无对应源语言模板，执行 doc/public/user_prompt/book_translation_new_template.md。
```

如果仓库里还没有这个源语言到目标语言的模板，例如法语到简体中文：

```text
我要翻译的书：{书名、作者（可选）}
目标语言：简体中文

请自动选择正确的翻译 prompt：
- 如已有对应源语言模板，执行 doc/public/user_prompt/book_translation_existing_template.md。
- 如无对应源语言模板，执行 doc/public/user_prompt/book_translation_new_template.md。
```

如果你不确定有没有模板，就这样写：

```text
我要翻译的书：{书名、作者（可选）}
目标语言：{目标语言}

请自动选择正确的翻译 prompt：
- 如已有对应源语言模板，执行 doc/public/user_prompt/book_translation_existing_template.md。
- 如无对应源语言模板，执行 doc/public/user_prompt/book_translation_new_template.md。
```

## 你不需要填写这些

不要让普通用户填写这些技术字段：

- 源语言标签。
- source-target，例如 `ja-zh-Hans`。
- Project slug。
- SOURCE_URL。
- profile。
- 书籍目录编号。
- npm 命令。
- 随机抽检参数。
- release 版本号。

这些字段应该由 AI Agent 自动判断、自动生成、自动记录。用户只在 AI 找不到可靠来源、版权不清楚、本地文件来源不明时再补充信息。

## 用户给本地文件时怎么写

如果本地文件是公版或你有明确授权，可以继续使用上面的公版/授权 prompt，并让 AI 核查来源和权利。

```text
我要翻译的书：我本地的文件 ./source/example.txt
目标语言：简体中文

请自动选择正确的翻译 prompt：
- 如已有对应源语言模板，执行 doc/public/user_prompt/book_translation_existing_template.md。
- 如无对应源语言模板，执行 doc/public/user_prompt/book_translation_new_template.md。

请先核查这个文件的来源、版权状态和我是否有权提交。
如果版权或来源不清楚，请停止，不要开始翻译。
```

本地文件存在，不代表可以发布。AI 必须先做来源和版权核查。

如果这是非公版书，只做个人学习自用，不传播、不商业使用，应使用私人自用 prompt：

```text
我要翻译的书：我本地的文件 ./source/example.epub
目标语言：简体中文
私人自用声明：仅供个人学习自用；不传播；不用于商业。

请自动选择正确的私人自用翻译 prompt：
- 如已有对应源语言模板，执行 doc/public/user_prompt/book_translation_private_existing_template.md。
- 如无对应源语言模板，执行 doc/public/user_prompt/book_translation_private_new_template.md。
```

私人自用项目必须创建在 `books/private/{target}/{number}_{slug}/`，不是公开 `books/{target}/`。`books/private/` 被 Git 忽略，不得发布到 GitHub。

## 最省事的推荐入口

给小白用户时，只给这一段即可：

### 公版书翻译prompt

```text
我要翻译的书：{书名、作者（可选）；如果有可靠来源链接也可以贴上}
目标语言：{例如 简体中文}

请自动选择正确的翻译 prompt：
- 如已有对应源语言模板，执行 doc/public/user_prompt/book_translation_existing_template.md。
- 如无对应源语言模板，执行 doc/public/user_prompt/book_translation_new_template.md。

除非版权或来源无法确认，不要让我填写技术字段。请自动查找可靠公版来源，自动创建项目，完成翻译、审校、EPUB 构建、分层随机抽检和 release。
```

### 个人自用书翻译prompt

```text
我要翻译的书：{书名、本地目录: XXX }
目标语言： {例如 简体中文}

请自动选择正确的翻译 prompt：
- 如已有对应源语言模板，执行 doc/public/user_prompt/book_translation_private_existing_template.md。
- 如无对应源语言模板，执行 doc/public/user_prompt/book_translation_private_new_template.md。

这是我个人自用的,不传播,不用于商业,使用我给出的本地的书源。
请自动创建项目，严格完成整个模板规定的系统翻译流程,不允许有任何遗漏。
```

私人自用项目必须输出到 `books/private/{target}/{number}_{slug}/`，最终版本化产物位于 `output/private_artifacts/`，不是公开 release，不得发布到 GitHub。

## EPUB 后精修审校 prompt（可选）

第一版 EPUB 已经生成后，如果用户想提高译本质量，可以再给 AI 这一段。`N` 是“连续无问题轮数”：`1` 最省 token，`3` 更严格，质量要求更高；不确定时填 `2`。

```text
本书项目：{书籍项目路径，例如 books/{target}/{number}_{slug}}
连续无问题退出轮数 N：{1/2/3；默认 2}

请先读取 AGENTS.md、该书 SKILL.md（如有）、template/epub_pipeline/README.md、template/epub_pipeline/common/README.md，以及封面、book-info/frontmatter、图表资产、质量门禁、分层随机抽检、release 相关规则。

请设置 /goal：对已生成 EPUB 做精修审校，严格按模板要求检查封面、首页/前置页、metadata、nav、目录、正文、注释、图表、公式、表格、图片、样式、读者可见内容、EPUB 构建与 release。不得只检查我点名的项目。

启动 2 个独立评审 agent 做分层随机抽检。至少执行 4 轮；每轮使用新 seed，并按模板保存样本、证据、评审、修复和闭环记录。若任何轮发现 P0/P1/P2、单项 <70、读者不可理解、事实/术语/图表/公式错误或模板硬门禁失败，修复后必须追加新一轮。

退出条件：最近连续 N 轮均无新增阻塞问题，且 npm run review:random-validate:pass 通过。N=1 为最低强度，较省 token；N=3 更严格，审校后译本质量更高，用户可自行调整。

通过后清理或重建 staging，重新生成 EPUB，运行 publication lint、asset manifest、cover output、reader-facing policy、EPUBCheck，以及 release 或 private artifact 脚本。公版或授权项目的最终可发布 EPUB 必须输出到该书 output/release/，release_state.json.latest_status 必须为 PASS。私人自用项目的最终私人产物必须输出到 output/private_artifacts/，private_artifact_state.json.latest_status 必须为 PASS。报告 release EPUB 或 private artifact 路径、抽检轮次、修复摘要、验证命令结果和剩余风险。
```

## AI Agent 必须交付什么

任务完成时，AI 至少要报告：

- 书籍项目路径。
- 可靠公版来源或本地来源证据。
- release EPUB 路径，或私人自用项目的 private artifact 路径。
- 执行过的验证命令和结果。
- 分层随机抽检轮次。
- 修复摘要。
- 如果有模板回填，说明回填了什么。
- 剩余风险。

公版或授权项目没有 `output/release/` 下的 PASS release，就不算完成。私人自用项目没有 `output/private_artifacts/` 下的 PASS private artifact，就不算完成。

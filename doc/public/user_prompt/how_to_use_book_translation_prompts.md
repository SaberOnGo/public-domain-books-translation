# 小白用户使用说明：只填三项内容

这套 prompt 的目标是：用户不需要懂 EPUB、source-target、slug、模板、抽检、release。用户只要给 AI 三项内容：

1. 我要翻译的书是什么。
2. 我要翻译成什么语言。
3. 请 AI 自动选择正确的翻译 prompt。

其他事情都交给 AI Agent 自动完成：找可靠公版来源、判断源语言、选择或创建模板、建立书籍项目、翻译、审校、构建 EPUB、随机抽检、生成 release。

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

```text
我要翻译的书：我本地的文件 D:\books\example.txt
目标语言：简体中文

请自动选择正确的翻译 prompt：
- 如已有对应源语言模板，执行 doc/public/user_prompt/book_translation_existing_template.md。
- 如无对应源语言模板，执行 doc/public/user_prompt/book_translation_new_template.md。

请先核查这个文件的来源、版权状态和我是否有权提交。
如果版权或来源不清楚，请停止，不要开始翻译。
```

本地文件存在，不代表可以发布。AI 必须先做来源和版权核查。

## 最省事的推荐入口

给小白用户时，只给这一段即可：

```text
我要翻译的书：{书名、作者（可选）；如果有可靠来源链接也可以贴上}
目标语言：{例如 简体中文}

请自动选择正确的翻译 prompt：
- 如已有对应源语言模板，执行 doc/public/user_prompt/book_translation_existing_template.md。
- 如无对应源语言模板，执行 doc/public/user_prompt/book_translation_new_template.md。

除非版权或来源无法确认，不要让我填写技术字段。请自动查找可靠公版来源，自动创建项目，完成翻译、审校、EPUB 构建、分层随机抽检和 release。
```

## AI Agent 必须交付什么

任务完成时，AI 至少要报告：

- 书籍项目路径。
- 可靠公版来源或本地来源证据。
- release EPUB 路径。
- 执行过的验证命令和结果。
- 分层随机抽检轮次。
- 修复摘要。
- 如果有模板回填，说明回填了什么。
- 剩余风险。

如果没有 `output/release/` 下的 PASS release，就不算完成。

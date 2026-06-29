# 小白用户使用说明：只填三项内容

这套 prompt 的目标是：用户不需要懂 EPUB、语言方向模板名、目录名、模板、抽检、release。用户只要给 AI 三项内容：

1. 我要翻译的书是什么。
2. 我要翻译成什么语言。
3. 请 AI 自动选择正确的翻译 prompt。完整写法见下面的[最省事的推荐入口](#最省事的推荐入口)。

其他事情都交给 AI Agent 自动完成：找可靠公版/授权来源或记录私人本地书源、判断源语言、选择或创建模板、建立书籍项目、翻译、审校、构建 EPUB、随机抽检、生成 release 或私人版本化产物。

英译简中项目默认会同时输出单简体中文 EPUB 和中英双语对照 EPUB；这个决定与公版或私人自用模式无关。其他语言方向如需双语对照版，在启动 prompt 里加一句：`请输出 edition_type: bilingual_parallel，同时生成目标语言版 EPUB 和源语言-目标语言双语对照版 EPUB。`

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
[重点专有名词(人名、地名、术语、罕见名词、音译后体验很差的名字等) 的翻译格式] 设置 = 3

请自动选择正确的翻译 prompt：
- 如已有对应语言方向模板，执行 doc/public/user_prompt/book_translation_existing_template.md。
- 如无对应语言方向模板，执行 doc/public/user_prompt/book_translation_new_template.md。
```

如果仓库里还没有这个源语言到目标语言的模板，例如法语到简体中文：

```text
我要翻译的书：{书名、作者（可选）}
目标语言：简体中文
[重点专有名词(人名、地名、术语、罕见名词、音译后体验很差的名字等) 的翻译格式] 设置 = 3

请自动选择正确的翻译 prompt：
- 如已有对应语言方向模板，执行 doc/public/user_prompt/book_translation_existing_template.md。
- 如无对应语言方向模板，执行 doc/public/user_prompt/book_translation_new_template.md。
```

如果你不确定有没有模板，就这样写：

```text
我要翻译的书：{书名、作者（可选）}
目标语言：{目标语言}
[重点专有名词(人名、地名、术语、罕见名词、音译后体验很差的名字等) 的翻译格式] 设置 = 3

请自动选择正确的翻译 prompt：
- 如已有对应语言方向模板，执行 doc/public/user_prompt/book_translation_existing_template.md。
- 如无对应语言方向模板，执行 doc/public/user_prompt/book_translation_new_template.md。
```

## 你不需要填写这些

不要让普通用户填写这些技术字段：

- 源语言标签。
- 语言方向模板名，例如 `Japanese-to-Simplified-Chinese`。
- 目录名。AI 必须按目标语言生成 `目标语言书名_目标语言作者名`，例如简体中文目标书用 `天文学大成_托勒密`，日语目标书用日语书名和作者名。
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
[重点专有名词(人名、地名、术语、罕见名词、音译后体验很差的名字等) 的翻译格式] 设置 = 3

请自动选择正确的翻译 prompt：
- 如已有对应语言方向模板，执行 doc/public/user_prompt/book_translation_existing_template.md。
- 如无对应语言方向模板，执行 doc/public/user_prompt/book_translation_new_template.md。

请先核查这个文件的来源、版权状态和我是否有权提交。
如果版权或来源不清楚，请停止，不要开始翻译。
```

本地文件存在，不代表可以发布。AI 必须先做来源和版权核查。

如果这是非公版书，只做个人学习自用，不传播、不商业使用，应使用私人自用 prompt：

```text
我要翻译的书：我本地的文件 ./source/example.epub
目标语言：简体中文
[重点专有名词(人名、地名、术语、罕见名词、音译后体验很差的名字等) 的翻译格式] 设置 = 3
私人自用声明：仅供个人学习自用；不传播；不用于商业。

请自动选择正确的私人自用翻译 prompt：
- 如已有对应语言方向模板，执行 doc/public/user_prompt/book_translation_private_existing_template.md。
- 如无对应语言方向模板，执行 doc/public/user_prompt/book_translation_private_new_template.md。
```

私人自用项目必须创建在 `books/private/{target}/{number}_{目标语言书名}_{目标语言作者名}/`，不是公开 `books/{target}/`。`books/private/` 被 Git 忽略，不得发布到 GitHub。

## 最省事的推荐入口

给小白用户时，只给这一段即可：

### 公版书翻译prompt

```text
我要翻译的书：{书名、作者（可选）；如果有可靠来源链接也可以贴上}
目标语言：{例如 简体中文}
[重点专有名词(人名、地名、术语、罕见名词、音译后体验很差的名字等) 的翻译格式] 设置 = 3

请自动选择正确的翻译 prompt：
- 如已有对应语言方向模板，执行 doc/public/user_prompt/book_translation_existing_template.md。
- 如无对应语言方向模板，执行 doc/public/user_prompt/book_translation_new_template.md。

除非版权或来源无法确认，不要让我填写技术字段。请自动查找可靠公版来源，自动创建项目，完成翻译、审校、EPUB 构建、分层随机抽检和 release。
翻译执行时必须逐章执行“每章译后全量检查并修复”：发现问题后先修复，但该轮不能 PASS，必须追加新一轮整章复查，直到最新一轮零问题 PASS。第一版 EPUB 后必须执行“分层随机抽检与问题族追杀”：抽检发现问题时，不得只修被抽样本，必须归纳问题族、全书同类审计、修复确认命中、新 seed 复抽。译文质量问题族必须使用 `skills/translation-quality-defect-families/SKILL.md`。
```

专有名词翻译格式设置可省略，默认值为 `3`。取值含义：`1` 直接翻译成目标语言；`2` 保留原文不翻译；`3` 第一次正文出现写 `译名（原文）`，后续用译名；`4` 第一次正文出现写 `译名（原文）`，后续用原文；`5` 第一次正文出现写 `译名（原文）` 并使用合规注号，后续用译名。

### 个人自用书翻译prompt

```text
我要翻译的书：{书名、本地目录: XXX }
目标语言： {例如 简体中文}
[重点专有名词(人名、地名、术语、罕见名词、音译后体验很差的名字等) 的翻译格式] 设置 = 3

请自动选择正确的翻译 prompt：
- 如已有对应语言方向模板，执行 doc/public/user_prompt/book_translation_private_existing_template.md。
- 如无对应语言方向模板，执行 doc/public/user_prompt/book_translation_private_new_template.md。

这是我个人自用的,不传播,不用于商业,使用我给出的本地的书源。
请自动创建项目，严格完成整个模板规定的系统翻译流程,不允许有任何遗漏。
翻译执行时必须逐章执行“每章译后全量检查并修复”；第一版 EPUB 后必须执行“分层随机抽检与问题族追杀”。发现译文质量问题族时，先在本书闭环，再把可复用经验合并进 `skills/translation-quality-defect-families/SKILL.md`。
```

私人自用项目必须输出到 `books/private/{target}/{number}_{目标语言书名}_{目标语言作者名}/`，最终版本化产物位于 `output/private_artifacts/`，不是公开 release，不得发布到 GitHub。

## EPUB 后精修审校 prompt（可选）

第一版 EPUB 已经生成后，不要只说“帮我精修”。给小白用户时，按目的给下面两个 prompt：

- **Prompt B：章节全量复检与修复。** 旧流程项目、缺少每章零问题 control 记录、或担心译文质量没做到位时先用。
- **Prompt C：分层随机抽检与问题族追杀。** 第一版 EPUB 后发布前必用；负责抽样发现系统性盲点、全书同类审计、新 seed 复抽和 release/private artifact。

如果不确定，先跑 B，再跑 C。

### Prompt B：章节全量复检与修复

```text
本书项目：{书籍项目路径，例如 books/{target}/{number}_{目标语言书名}_{目标语言作者名}}

请先读取 AGENTS.md、该书 SKILL.md（如有）、template/epub_pipeline/README.md、template/epub_pipeline/common/README.md、template/epub_pipeline/common/prompts/08a_chapter_post_translation_control.md、template/epub_pipeline/common/references/quality_gate_framework.md、目标语言质量框架，以及 `skills/translation-quality-defect-families/SKILL.md`。

请设置 /goal：对本书所有已翻译章节执行“每章译后全量复检并修复”。每章必须对照整章原文、整章译文和读者可见上下文，覆盖但不限于忠实度、漏译误译、中文顺读、文学性、可读性和吸引力、教学/解释节奏、术语稳定、案例/专名/地名/书名/船名/机构名、标题与小标题、注释、图表/公式/表格/图片文字接口、源语句法残留、过硬过直过板句、过度解释、无依据加戏、读者可见 AI/制作痕迹、异常空格/乱码、旧纸书目录残留。

可并行处理不同章节，但每个章节必须独立闭环：每一轮都检查整章；只要发现任何问题，先修复该章，但该轮只能记为 `FIXED_RECHECK_REQUIRED`，不能 PASS；随后追加新一轮整章复查。只有最新一轮记录 `scope: FULL_CHAPTER`、`issues_found: 0`、`fixes_applied: 0`、`unresolved_blocking_issues: 0`、`latest_round_status: PASS`、`allow_next_chapter: true` 时，该章才算通过。

若任一章发现可复现译文质量问题族，例如短句切断、比喻自撞、排比标点拖拽、代词指代不清、源语句法残留、术语漂移、标题超载、过度解释或加戏，必须按 `skills/translation-quality-defect-families/SKILL.md` 处理：记录如何发现、如何归纳、如何用低 token 方法查全书同类、如何修复、如何复查。

完成后重新生成或更新章节控制和章节 gate 记录，把通过章节写入或更新到 `chapters/final/`。然后重建 EPUB，运行可用的 chapter-control/preflight/publication lint/asset/EPUBCheck 命令。报告修复章节、问题族、验证命令结果和仍需进入 Prompt C 的事项。
```

### Prompt C：分层随机抽检与问题族追杀

`N` 是“连续无问题抽检轮数”：`1` 最省 token，`2` 更稳，`3` 更严格；不确定时填 `2`。

```text
本书项目：{书籍项目路径，例如 books/{target}/{number}_{目标语言书名}_{目标语言作者名}}
连续无问题抽检轮数 N：{1/2/3；默认 2}

请先读取 AGENTS.md、该书 SKILL.md（如有）、template/epub_pipeline/README.md、template/epub_pipeline/common/README.md、template/epub_pipeline/common/prompts/16a_stratified_random_spotcheck.md、template/epub_pipeline/common/references/stratified_random_spotcheck.md、template/epub_pipeline/common/references/quality_gate_framework.md、封面、book-info/frontmatter、图表资产、release 相关规则，以及 `skills/translation-quality-defect-families/SKILL.md`。

请设置 /goal：对已生成 EPUB 执行“分层随机抽检与问题族追杀”，并在通过后重新生成 release 或 private artifact。不要把本 prompt 当作普通润色；它的核心是发布前发现系统性盲点、全书同类审计、修复闭环和新 seed 复抽。

运行分层随机抽样，抽样总体是 reader-facing audit units，不是页数，也不只是段落。必须覆盖实际存在的 paragraph、table、figure、formula/proof、caption/note。至少派生 2 个独立评审 agent，并按模板保存 `reviews/random_spotcheck/round_XXX/` 下的 seed、manifest、samples、evidence、reviews、fixes/fix_log.md、verification/closure_check.md。

若任一样本发现 P0/P1/P2、单项 <80、读者不可理解、忠实度偏移、事实/术语/专名/标题/注释/图表/公式错误、源语句法残留、过硬过直句、短句切断、比喻自撞、排比标点拖拽、代词指代不清、过度解释或加戏，必须在本轮把它归纳为问题族，执行全书同类问题审计并修复所有确认命中。不得只修被抽中的样本，不得等第二轮才查全书。

译文质量问题族必须优先低 token 审计：先用 `rg`、`glossary/terms.csv`、`forbidden_body_renderings`、标题映射、章节控制记录、抽样 manifest 和小上下文原文对照收集候选，再把候选片段交给 agent 复核。可复用经验必须合并进 `skills/translation-quality-defect-families/SKILL.md`。

每次修复后必须重建 EPUB，并用新 seed 追加下一轮抽检。退出条件：最近连续 N 个新 seed 抽检轮均 PASS，所有已发现问题族均关闭，`npm run review:random-validate:pass` 通过，且 release_confidence 达到模板要求。

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

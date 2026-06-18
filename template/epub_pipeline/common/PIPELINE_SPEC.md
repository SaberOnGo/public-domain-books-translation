# 流水线规范 / Pipeline Spec

## 1. 输入 / Inputs

- `TEMPLATE_ROOT`
- `PROFILE_ROOT`：可选。特殊书型控制模板目录，例如 `template/epub_pipeline/profiles/classical-science-zh-Hans`。
- `MODE_ROOT`：可选。模式覆盖层目录；非公版私人自用项目必须使用 `template/epub_pipeline/modes/private_use`。
- `PROJECT_ROOT`
- `SOURCE_URL`：公开模式或授权模式的来源 URL。
- `LOCAL_SOURCE_FILE`：可选，仅用于 `publication_mode=private_use` 的用户本地书源文件。
- `publication_mode`：`public_domain` / `licensed` / `private_use`。

## 2. 模板保护与写入范围 / Template Protection & Write Scope

- `TEMPLATE_ROOT` 是只读模板目录。
- AI 不得把具体书籍的原文、译文、QA、EPUB 输出写入模板原目录。
- 实际做书时，AI 必须通过 `books/scripts/create_book_project.py` 复制模板为独立书籍工程目录，例如 `books/{target}/{number}_{目标语言书名}_{目标语言作者名}/`。`{target}` 是输出电子书的目标语言标签，`{number}` 由脚本在该目标语言目录内自动递增分配。数字前缀后的目录名必须使用目标语言可读书名和作者名。
- 非公版私人自用书籍必须通过 `books/scripts/create_book_project.py --mode private-use --local-source-file ... --private-use-declaration ...` 创建到 `books/private/{target}/{number}_{目标语言书名}_{目标语言作者名}/`。`books/private/` 被 Git 忽略；其中的原文、译文、QA、EPUB 输出和具体书籍 metadata 不得发布到 GitHub。
- 若启用 `PROFILE_ROOT`，必须先复制 `common` 和语言方向模板，再把 `PROFILE_ROOT` 覆盖复制到同一个书籍工程目录。
- 若 `publication_mode=private_use`，必须最后叠加 `MODE_ROOT=template/epub_pipeline/modes/private_use`。私人自用封面、首页/前置页、私人产物和门禁脚本不得混入公版或授权发布项目。
- 复制完成后，后续 `PROJECT_ROOT` 指向独立书籍工程目录。
- AI 只能写入 `PROJECT_ROOT` 内文件。
- 例外：`books/package.json`、`books/package-lock.json` 和被 Git 忽略的 `books/node_modules/` 是所有书籍共享的构建工具目录，不属于任何单本书的原文、译文、QA 或 EPUB 输出。
- 如果检测到当前目录仍在 `template/epub_pipeline/common`、某个 `template/epub_pipeline/{language-pair-template}` 语言模板或 `template/epub_pipeline/profiles/{profile-target}` 控制模板内，必须停止并先复制模板到书籍工程。

## 3. 状态机 / State Machine

`state/pipeline_state.json.status` 只能使用以下状态之一：

- `INIT`
- `SOURCE_INGESTED`
- `SOURCE_SPLIT`
- `GLOBAL_RESEARCH_DONE`
- `BOOK_RESEARCH_DONE`
- `PRETRANSLATION_FAILED`
- `PRETRANSLATION_PASS`
- `GLOSSARY_STYLE_DONE`
- `TRANSLATING`
- `TRANSLATED`
- `CHAPTER_POST_CONTROL_PASS`
- `REVIEWING`
- `CHAPTER_GATES_PASS`
- `PREPRODUCTION_SPEC_DONE`
- `PREPRODUCTION_SAMPLE_FAILED`
- `PREPRODUCTION_SAMPLE_PASS`
- `EPUB_BUILT`
- `RANDOM_SPOTCHECK_FAILED`
- `RANDOM_SPOTCHECK_PASS`
- `INDEPENDENT_REVIEW_FAILED`
- `INDEPENDENT_REVIEW_PASS`
- `REVISION_ROUTING_REQUIRED`
- `FINAL_OUTPUT_PASS`
- `RELEASE_DRAFT`
- `RELEASE_PASS`
- `RETROSPECTIVE_DONE`
- `DONE`
- `FAILED`

每一步结束必须更新：

- `status`
- `current_step`
- `last_error`
- 对应产物路径

## 4. 目录合约 / Directory Contract

### Source

- `source/source_text_raw.txt`：原始文本。
- `source/source_text.txt`：清洗后的正文。
- `source/source_manifest.json`：来源、哈希、抓取时间、章节统计。

### Metadata

- `metadata/book.yaml`：EPUB 元数据。
- `metadata/rights_checklist.md`：版权/公版/授权/私人使用边界核查。
- `metadata/source_evidence.md`：原文来源证据。
- `metadata/private_use_declaration.md`：私人自用声明。仅 `publication_mode=private_use` 必需；公开项目不得用它替代公版或授权证据。
- `metadata/source_witness_manifest.md`：可选语言/profile 文件。记录底本、版本、witness、扫描/OCR/转写状态和编号体系。
- `metadata/book_specific_translation_research.md`：本书专项翻译研究。
- `metadata/style_profile.md`：文体画像。
- `metadata/reference_witness_policy.md`：可选 profile 文件。记录第二语言参考译本的版权状态、允许用途、禁止用途和差异校读边界。

### Glossary

- `glossary/terms.csv`：术语、概念、制度词、技术词和高风险表达的机器可读术语表。
- `glossary/proper_nouns.csv`：用户可编辑的重点专有名词译表。必备列为 `source_name,target_name,category,display_policy,first_rendering,subsequent_rendering,note_required,repeat_original_allowed_when,notes`。用户未显式设置时，重点专有名词默认使用策略 `3`：第一次正文自然出现写作 `译名（原文）`，后续用译名。

### Research

- `references/translation_research_universal.md`：由目标语言模板或语言方向模板提供的翻译研究规则。
- `references/quality_standard.md`：由目标语言模板或语言方向模板提供的质量标准。
- `references/chapter_title_policy.md`：通用章节标题、目录短题名和副标题策略。
- `references/literary_refinement_policy.md`：通用文学精修、书籍目标和模板经验回填策略。
- `references/proper_noun_display_policy.md`：重点专有名词显示策略，定义用户 prompt 设置值 `1` 到 `5`、默认策略 `3`、正文首次出现规则和 `glossary/proper_nouns.csv`。
- `references/note_marker_policy.md`：脚注、尾注、译注和编辑注的注号硬规则；只允许 `[1]`、`(1)`、`（1）` 或 `注1` 体系。
- `skills/translation-quality-defect-families/SKILL.md`：仓库级译文质量问题族 skill。发现忠实度、中文顺读、术语、标题/小标题、注释、图表文字接口、源语句法残留、过硬过直句、短句切断、比喻自撞、排比标点拖拽、代词指代不清、过度解释或加戏等可复现质量问题时，必须用于归纳、全书同类审计、修复和经验回填。
- `references/epub_assets_figures_tables.md`：通用 EPUB 图片、图表、表格、资源目录、XHTML 转换和 OPF manifest 规则。
- `references/stratified_random_spotcheck.md`：第一版 EPUB 后强制执行的分层随机抽检、修复闭环和退出置信度规则。
- `references/release_versioning.md`：EPUB 按软件版本发布的版本号、release note、`output/release/` 目录和退出门禁规则。
- `references/private_use_cover_policy.md`：仅由 `modes/private_use` 覆盖层提供。私人自用封面不得放长版权免责声明或公版来源行；私人自用边界必须写在书籍信息页/前置页和 metadata 中。
- `references/private_use_frontmatter_policy.md`：仅由 `modes/private_use` 覆盖层提供。私人自用首页/前置页不得包含公版说明，制作标识必须使用 `参考public-domain-books-translation 开源项目 个人自制`。
- `references/private_use_artifact_policy.md`：仅由 `modes/private_use` 覆盖层提供。私人自用版本化产物写入 `output/private_artifacts/`，不是公开 release。
- `automation_contract.md`：自动化执行合约。

### Chapters

- `chapters/src/{NNN_slug}.md`：分章原文。
- `chapters/translated/{NNN_slug}.md`：分章译文草稿。
- `chapters/final/{NNN_slug}.md`：通过门禁后的终稿。
- `chapters/final/*.md` 是编辑源文件。生成 EPUB 时必须转换为 XHTML；不得把 Markdown 文件直接当作 EPUB spine 正文。

### Assets

- `assets/figures/`：最终可发布图表。几何图、天文学示意图、光学/力学线图优先使用 SVG。
- `assets/images/`：封面、影印页局部、照片、扫描图、复杂位图插图。
- `assets/tables/`：需要随 EPUB 附带的结构化表格资源或衍生数据。
- `assets/styles/`：EPUB CSS 和样式资源。
- `source/tables/`：从原书整理出的 CSV/TSV 原始表格数据，供生成 XHTML table 和 QA 校验使用。
- 所有 EPUB 内实际使用的 assets 必须写入 OPF manifest。XHTML 中不得出现本机绝对路径、`file://`、Windows 盘符或外链热链接。

### QA

- `qa/pretranslation/source_*.md`：预翻译样本原文。
- `qa/pretranslation/trial_*.md`：预翻译试译记录。
- `qa/pretranslation/pretranslation_report.md`：预翻译总报告。
- `qa/chapter_controls/{NNN_slug}.control.md`：每章节译后控制文件。
- `qa/fidelity/{NNN_slug}.md`：忠实度审校。
- `qa/readability/{NNN_slug}.md`：中文可读性审校。
- `qa/imagery/{NNN_slug}.imagery.md`：意象词/过度发挥/省字式翻译审计。
- `qa/terminology/{NNN_slug}.md`：术语一致性审校。
- `qa/gates/{NNN_slug}.gate.md`：章节终稿门禁。
- `qa/refinement/refinement_check.json`：整书精修扫描报告，重点检查出版文本中的 BOM、乱码、异常空格、标点和残留问题。
- `qa/refinement/*.md`：整书或章节级精修复查记录。
- `qa/textual/`：可选语言/profile 目录。用于异文、残损、拟补、OCR 不确定、语法歧义和参考译本冲突记录。
- `qa/technical/`：可选 profile 目录。用于术语锁定、图表/表格清单、技术校验计划、章节技术审计和图表/表格审计。

### Preproduction

- `preproduction/stage1/production_spec.md`：全书制作规格。
- `preproduction/stage2_sample/sample_chapter.xhtml`：样章 XHTML。
- `preproduction/stage2_sample/sample_book.epub`：样章 EPUB。
- `preproduction/stage2_sample/sample_review.md`：样章检查结果。
- 若书中含图表，样章必须至少覆盖一个带图或带表章节，或在 `sample_review.md` 中明确说明为什么样章不覆盖图表。

### Reviews

- `reviews/agent_a/review.md`：翻译与内容独立评审。
- `reviews/agent_b/review.md`：EPUB 工程与排版独立评审。
- `reviews/random_spotcheck/round_XXX/random_sample_manifest.json`：第一版 EPUB 后分层随机审计单元抽检清单，必须记录 seed、样本来源、Agent 数、每层候选数、抽样数和每个 Agent 的样本编号。
- `reviews/random_spotcheck/round_XXX/strata_summary.json`：按 `paragraph`、`table`、`figure`、`formula`、`caption_note` 分层记录抽样规模和置信度。
- `reviews/random_spotcheck/round_XXX/validation_report.json`：记录 `release_confidence`、每层置信度和脚本校验结论；最终退出要求 `release_confidence >= 0.80` 且 `status=PASS`。
- `reviews/random_spotcheck/round_XXX/samples/agent_a/`、`reviews/random_spotcheck/round_XXX/samples/agent_b/`：两个独立 Agent 的分层样本；表格、图片、公式不得被普通段落样本替代。
- `reviews/random_spotcheck/round_XXX/evidence/`：抽检样本对应的图片、表格、公式等人工可核查证据。
- `reviews/random_spotcheck/round_XXX/reviews/agent_a_review.md`、`reviews/random_spotcheck/round_XXX/reviews/agent_b_review.md`：两个独立 Agent 对分层样本的逐项评分和结论。
- `reviews/random_spotcheck/round_XXX/fixes/fix_log.md`：抽检发现问题的返工记录；必须记录每个问题族的全书同类问题审计范围、检索式或复查方法、命中、修复和例外。
- `reviews/random_spotcheck/round_XXX/verification/closure_check.md`：已发现 P0/P1/P2 的定点闭环复查；必须确认单点旧问题和全书同类问题审计均已关闭。
- `reviews/random_spotcheck/random_sample_manifest.json`、`reviews/random_spotcheck/agent_a_samples.md`、`reviews/random_spotcheck/agent_b_samples.md`：最近一轮兼容入口；人工核查应优先查看对应 `round_XXX/` 子目录。
- `reviews/agent_a/random_spotcheck_review.md`、`reviews/agent_b/random_spotcheck_review.md`：两个独立 Agent 对最近通过轮次的兼容评审结论。
- `reviews/scorecards/random_spotcheck_score.md`：随机抽检汇总评分表。
- `reviews/scorecards/final_quality_score.md`：最终质量评分表。
- `reviews/revision_route.md`：评审回退路由。

### Retrospective

- `retrospective/book_retrospective.md`：本书复盘。
- `retrospective/template_update_suggestions.md`：模板更新建议。

### Output

- `output/book.epub`：最终 EPUB。
- `output/release/{目标语言书名}_vX.X.X.epub`：公版或授权项目的带版本号 EPUB 发布产物，例如 `金属巨兽_v0.0.4.epub`；不得平铺在 `output/` 根目录，也不得使用英文 slug 或通用 `book_` 前缀。
- `output/release/release_notes.md`：公版或授权项目的累计中英文发布说明；每次发布把最新版本条目插入文件顶部，必须记录发布原因、问题点、修复、QA 证据、风险和下一轮迭代。
- `output/release/release_state.json`：公版或授权项目的当前 release 状态；`latest_status = PASS` 是公开发布 `DONE` 的必要条件。
- `output/release/release_index.md`：公版或授权项目的所有版本发布索引。
- `output/private_artifacts/{目标语言书名}_private_vX.X.X.epub`：私人自用项目的本地版本化 EPUB 产物，不是公开 release，不得提交到 GitHub。
- `output/private_artifacts/private_artifact_notes.md`：私人自用产物累计说明。
- `output/private_artifacts/private_artifact_state.json`：私人自用产物状态；`latest_status = PASS` 是私人自用 `DONE` 的必要条件。
- `output/private_artifacts/private_artifact_index.md`：私人自用产物索引。
- `output/epubcheck.log` 或 `output/epubcheck.json`：EPUB 校验结果。
- `output/publication_lint.json`：出版文本 lint 结果，检查编码污染、异常空格、旧纸书页码目录等问题。
- `output/asset_manifest_check.json`：EPUB 资源引用检查结果，检查图片/样式资源是否存在、路径是否相对、OPF manifest 是否覆盖。
- `output/final_manifest.md`：最终产物清单。

### Shared Tooling

- `books/{target}/{number}_{目标语言书名}_{目标语言作者名}/`：具体书籍工程目录，目录名必须使用目标语言书名和作者名，便于人工识别。
- `books/package.json`：所有书籍共享的 Node.js 工具依赖声明。
- `books/package-lock.json`：共享工具依赖锁文件。
- `books/node_modules/`：共享工具安装目录，必须被 Git 忽略。
- 每本书的 `package.json` 只保留本书脚本，不得声明与共享工具重复的通用依赖。
- EPUBCheck 等脚本必须向上查找共享 `node_modules/`，不得硬编码 `PROJECT_ROOT/node_modules/`。

## 5. 出版文本硬检查 / Publication Text Lint

构建 EPUB 前必须运行出版文本 lint：

```powershell
node scripts/publication_lint.js --target={target-language} --write-report
node scripts/asset_manifest_check.js --write-report
```

通用硬检查：

- 不得出现编码污染、替换字符或明显 mojibake。
- 不得把旧纸书的页码目录、插图页码目录当正文放入 EPUB。
- 不得在普通正文中保留用于纸书对齐的连续空格。
- 不得让脚本依赖本机绝对路径；所有路径必须相对 `PROJECT_ROOT`。
- 不得把本机绝对路径、Windows 盘符路径、`file://` 或包含个人工作区名称的仓库绝对路径写入可提交的 metadata、QA、reviews、release、private artifact、JSON 报告或 Markdown 证据。随机抽检、发布状态和校验报告中的路径必须序列化为书籍工程相对路径或仓库相对路径。
- 不得把旧纸书目录式长标题链直接塞入 EPUB 导航；长标题必须按 `references/chapter_title_policy.md` 拆分为短目录题名、页面主标题和可选副标题。
- 不得把 AI 或译者概括出的章节说明当成读者可见标题。若源文某章只有编号、罗马数字或简单题名，EPUB 页面标题通常也只应使用对应编号或题名；解释性说明应放入 `title_note`、制作说明或 QA 记录。
- 不得把专有名词的“首次出现”原文括注放进标题、副标题或 EPUB 导航题名；标题中的出现不计入正文首次出现。重点专有名词必须按 `glossary/proper_nouns.csv` 和 `references/proper_noun_display_policy.md` 执行。
- 注号只能使用 `[1]`、`(1)`、`（1）` 或 `注1` 体系；不得出现带圈数字、孤立小字“注”、裸 `译注：` 标签或尾随裸数字注号。
- 不得让 Markdown 图片引用、XHTML `img src`、CSS `url(...)` 指向不存在的文件、本机绝对路径、`file://` 或未经许可的远程热链接。
- 若存在 OPF 文件，所有 EPUB 内使用的图片、CSS、字体等资源必须登记在 OPF manifest 中。
- 技术性表格应优先生成 XHTML `<table>`；不得把可结构化的数值表只做成图片。
- `source/source_text_raw.txt` 是来源证据，不应为了通过出版文本检查而改写。出版文本硬检查重点覆盖 `frontmatter/`、`chapters/final/`、`metadata/` 和生成 EPUB 内的 XHTML。

目标语言相关检查由 `template/epub_pipeline/targets/{target}/` 追加规则。例如简体中文会限制分号滥用、中文字符之间的异常空格、中文排版标点等。

## 6. 文件命名 / Naming

- 章节统一三位序号：`001_xxx.md`、`002_xxx.md`。
- `src`、`translated`、`final`、`qa` 必须同名对应。
- 不得让 AI 自创多套命名方案。

## 7. 新增硬门禁 / New Hard Gates

- 每章翻译后必须立即经过 `qa/chapter_controls/{NNN_slug}.control.md` 所记录的“每章译后，全量检查并修复节点”。该节点只检查当前章，不检查全书其他章节。
- 该节点必须全章检查该章是否符合模板要求，包括但不限于该章对 metadata/nav/目录的影响、正文、注释、图表/公式/表格/图片的文字接口、样式、读者可见内容、通俗化、可读性、润色、名词术语和注释。不得只检查用户点名项目。
- 该节点必须按 `glossary/terms.csv.forbidden_body_renderings` 逐项扫描正文。若出现正文禁用写法、无授权原词括注、裸露源语词或误导性泛译，必须修复并追加同节点复查。
- 该节点必须检查 `glossary/proper_nouns.csv`：重点人名、地名、术语、罕见名词和音译体验很差的名字必须按用户设置值 `1` 到 `5` 呈现；用户未设置时默认 `3`。若选择 `5`，第一次正文出现必须同时有 `译名（原文）` 和合规注号。
- 该节点必须检查注号格式；全角 `（1）` 是 `(1)` 的中文排版等价形式，但带圈数字、裸 `注` 标签、裸 `译注：` 和尾随裸数字不得进入终稿。
- 未完成每章译后全量检查，或最近一轮不是 `scope: FULL_CHAPTER`、`issues_found: 0`、`fixes_applied: 0`、`unresolved_blocking_issues: 0`、`latest_round_status: PASS`、`allow_next_chapter: true` 的零问题 PASS，或未满足更严格项目/profile 规则时，不得进入下一章翻译、后续审校或 `chapters/final/`。任何评分、主观印象或“已经修过”都不能抵消 P0/P1/P2、读者难以理解、事实/术语/当前章文字接口错误、中文润色不足、为了通俗而损害专业质量，或模板硬门禁失败。
- 图表、表格、公式和图片在本节点只做当前章文字接口检查与资产分流。复杂重绘、OCR、裁剪、数值校验、公式排版、资源路径或 manifest 问题应写入资产/技术门禁记录；这类问题阻止终稿、构建和 release，但不让当前章译后文字门禁无限循环。
- 每次未通过都必须记录问题点、修复摘要和追加复查轮次；不得覆盖旧失败记录。
- 若每章译后全量检查发现可复现的译文质量问题族，必须使用 `skills/translation-quality-defect-families/SKILL.md`，在书籍工程记录即时证据，先用低 token 方法审计同类，再把可复用经验合并回填到该 skill。
- `preflight:template` 在发现 `chapters/translated/*.md` 时，必须校验每个已译章节都有对应 `qa/chapter_controls/{NNN_slug}.control.md`，且最近一轮是以上零问题 PASS；在发现 `chapters/final/*.md` 时，还必须校验每个终稿章节都有 PASS 的 `qa/gates/{NNN_slug}.gate.md`。
- 全部翻译完成后不得直接构建 EPUB，必须先完成预制作阶段 1。
- 未通过样章制作检查，不得制作整本 EPUB。
- 未通过出版文本 lint，不得构建最终 EPUB。
- 未通过资源引用检查，不得构建或发布最终 EPUB。
- 未完成长章节标题的导航题名、页面标题和副标题设计，不得进入最终 EPUB 输出。
- 含图表或表格的章节，未确认 Markdown 源、XHTML 输出、assets 文件、OPF manifest、alt 文本、figcaption/table caption 一致，不得进入最终 EPUB 输出。
- 若启用特殊书型 profile，未完成该 profile 要求的参考译本政策、术语锁定、技术审计、图表/表格审计，不得进入最终 EPUB 输出。
- 整本 EPUB 构建后必须执行精修复查或等效扫描，并在 `qa/refinement/` 下记录结果。
- 若发现来源不支持的读者可见标题、BOM、乱码、AI 输出残留、异常英文残留或 EPUB metadata 问题，不得进入最终交付。
- 第一版全书 EPUB 生成后，必须执行分层随机抽检模块。抽样总体 `N` 是读者可见审计单元总数，不是页数，也不是正文段落数；审计单元至少包括 `paragraph`、`table`、`figure`、`formula`、`caption_note`。
- 每一轮精校完成后，必须运行 `npm run review:random-samples`，或等效运行 `python scripts/select_random_review_passages.py --source-dir chapters/final --agents 2 --samples-per-agent 120 --rounds-planned 4 --min-current-run-pass-rounds 2 --target-confidence 0.80 --defect-rate 0.10 --profile auto`。脚本必须生成 `reviews/random_spotcheck/round_XXX/` 子目录、seed、manifest、分层样本和人工可核查证据。
- 每次新的 AI 执行随机抽检时，旧轮次只能作为历史证据，不能计入本次退出条件。抽样脚本必须在 manifest 写入 `review_run_id` 与 `generated_at`；用户可以通过 `--min-current-run-pass-rounds N` 指定任意 `N>=1` 的当前运行连续 PASS 轮次要求；用户未指定时默认 `N=2`。`npm run review:random-validate:pass` 只统计同一 `review_run_id` 下、晚于最近 release/private artifact 的最新连续 PASS 轮次。缺少 `review_run_id`、缺少 `generated_at`、属于旧 release/private artifact 之前、或来自不同运行批次的 PASS 轮次，一律不得计入本次连续 PASS。
- AI 不得用已有 `round_XXX` 的历史 PASS 记录、旧 `validation_report.json`、旧 release note 或旧 private artifact state 代替本次新抽样。若用户要求继续精校、重新抽检、再出产物或确认最终质量，必须新生成本次运行的随机抽检轮次，并让 `validation_report.json.current_run_pass_rounds_count >= validation_report.json.current_run_pass_rounds_required`。
- 默认发布前抽样预算为：正文层每个 Agent 每轮 120；表格和图片 `N<=80` 全检，否则每轮总抽 20；公式/证明块 `N<=100` 全检，否则每轮总抽 20；图注/表注/注释 `N<=120` 全检，否则每轮总抽 20。该预算用于控制 token 成本；若任一层、任一样本发现任何需要修复或可能系统性复现的问题，本轮立即把发现归纳为问题族，并执行全书同类问题审计和闭环；不得只修被抽中的样本，也不得等到第二轮才全书检查。同层可被标记为高风险，用于后续抽样和人工复核，但不能替代本轮全书同类问题审计。
- 抽样脚本必须读取最近轮次 `round_XXX/reviews/*_review.md` 中带样本单元编号的 P0/P1/P2 行，并在下一轮 manifest 中记录 `blocking_issue_strata_in_recent_rounds`、`blocking_issue_seen_in_previous_round` 和 `dedicated_audit_required_after_consecutive_blockers`。
- 随机抽检中，两个 Agent 必须互不参考，均按模板、本书 profile 和目标语言规则检查正文、表格、图片、公式、图注/表注/注释、EPUB 阅读风险。每个样本必须逐项给出 0-100 分、问题类型、优先级、是否返工和理由。
- 任一单项 < 80，或任一 P0/P1/P2，或任一读不懂、证明链断裂、概念误导、术语/数值/图表/公式错误，即使平均分达标也必须判为失败。`80` 只是硬失败线；80-87 表示仍需精修，88-91 表示较好但未达最终优秀门槛。
- 任一随机抽检 Agent 未通过时，必须写入 `reviews/revision_route.md`，回到精校或更早阶段修复。每个发现必须先归纳为问题族，并对整本读者可见书稿执行同类问题审计，范围至少包括 `chapters/final/`、frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML；不得只修改被抽中的样本。修复后必须在旧轮次 `fixes/fix_log.md` 和 `verification/closure_check.md` 中记录问题族、检索式或审计方法、命中数、修复位置、合理例外和关闭结论，并使用新 seed 重新生成新轮次样本，不得复用上一轮样本自证通过。
- 对译文质量问题族，审计顺序必须优先低 token：`rg`、术语表、禁用正文写法、标题映射、抽样 manifest、章节控制记录和小上下文原文对照；只有候选片段进入 agent 复核。书内闭环后，可复用经验必须合并回填到 `skills/translation-quality-defect-families/SKILL.md`。问题轮次的 `fix_log.md` 必须用机器可读字段记录 `translation_quality_defect_family_count`、`translation_quality_skill_backfill`、`translation_quality_skill_backfill_path` 和 `translation_quality_skill_backfill_summary`；`closure_check.md` 必须记录 `translation_quality_skill_backfill_verified: true`。没有译文质量问题族时也必须写 `NOT_APPLICABLE` 和原因。
- 最终退出前必须运行 `npm run review:random-validate:pass`。该命令失败时，不得进入 `FINAL_OUTPUT_PASS`、`RETROSPECTIVE_DONE` 或 `DONE`。
- `npm run review:random-validate:pass` 必须写入 `current_review_run_id`、`current_run_pass_rounds_required`、`current_run_pass_rounds_count` 和 `current_run_pass_rounds`。正式退出、公开 release 或 private artifact 要求 `current_run_pass_rounds_required >= 1` 且 `current_run_pass_rounds_count >= current_run_pass_rounds_required`；用户未指定时默认 `current_run_pass_rounds_required = 2`。旧 PASS 轮次不得补数。
- `npm run review:random-validate:pass` 必须计算并写入 `release_confidence = min_h confidence_h`。若 `release_confidence < 0.80`，即使 Agent 文字评审写了 PASS，也不得退出任务。
- `npm run review:random-validate:pass` 还必须校验每个 Agent 的硬失败线 `average_score >= 80`、`lowest_score >= 80`、`blocking_issue_count = 0`，并默认执行优秀出版线 `average_score >= 92`、`lowest_score >= 88`、每个样本均有逐项评分行；同时校验闭环文件中的 `open_p0_p1_p2_count = 0`，以及当前 `review_run_id` 中所有问题轮次的译文质量问题族 skill backfill 字段。显式 `--skip-excellence-gate` 只能用于硬下限诊断，不能作为正式退出、公开 release 或 private artifact 依据。
- 分层随机抽检通过后，公版或授权项目必须执行 `prompts/18a_release_versioning.md` 或等效命令 `npm run release:create`。正式发布必须生成 `output/release/{目标语言书名}_vX.X.X.epub`、`release_notes.md`、`release_state.json` 和 `release_index.md`。
- 分层随机抽检通过后，`publication_mode=private_use` 项目必须执行 `npm run private:artifact:create`。私人自用产物必须生成 `output/private_artifacts/{目标语言书名}_private_vX.X.X.epub`、`private_artifact_notes.md`、`private_artifact_state.json` 和 `private_artifact_index.md`。
- `npm run release:create` 和 `npm run private:artifact:create` 必须拒绝未使用 `--require-pass` 生成的随机抽检校验报告；结构性抽样校验或 `DRAFT` 产物不得作为 `DONE` 的依据。
- 每次 EPUB 内容、排版、metadata、图表、注释或抽检修复发生变化后，都必须创建新的 patch release 或 private artifact。不得覆盖旧版本 EPUB；release note 或 private artifact note 必须追加到累计文件顶部，不得每次散落新建 note 文件。
- 如果已经发现系统性文学精修问题，必须在 `books/{target}/{number}_{目标语言书名}_{目标语言作者名}/goal/` 建立本书目标，并把可复用经验回填到 common、目标语言或语言方向模板。
- 整本 EPUB 制作后，必须派生 2 个独立 Agent 评审。
- 评审失败时必须通过 `reviews/revision_route.md` 回到对应前置阶段。
- 未完成复盘和经验沉淀，不得标记 `DONE`。

## 8. 完成定义 / Done Definition

必须同时满足：

- `metadata/rights_checklist.md` 明确可继续：公开项目必须是 `PUBLICATION_PASS` 或 `LICENSED_PASS`；私人自用项目必须是 `PRIVATE_USE_PASS`。
- 若 `publication_mode=private_use`，`metadata/private_use_declaration.md` 必须存在并记录用户本地书源文件名、SHA256、个人自用、不传播、不商业使用声明、风险由个人承担、public-domain-books-translation 开源项目仅用于公版书翻译发布，且不承担他人翻译/保存/传播/使用非公版内容导致的版权风险及责任；工程路径必须位于 `books/private/{target}/{number}_{目标语言书名}_{目标语言作者名}/`。
- 若启用特殊书型 profile，`metadata/reference_witness_policy.md` 必须明确原文底本和第二语言参考译本的使用边界。
- `qa/pretranslation/pretranslation_report.md` 结论为 `PASS`。
- 所有章节存在 `qa/chapter_controls/*.control.md` 且结论为 `PASS`。
- 所有章节的 `qa/chapter_controls/*.control.md` 均记录了每章译后全量检查范围、发现问题、修复摘要、复查轮次和最终允许继续结论；若曾失败，必须保留失败记录。
- 若启用特殊书型 profile，相关章节必须存在 `qa/technical/*.technical_audit.md`，且涉及图表/表格的章节必须存在 `qa/technical/*.diagram_table_audit.md`，结论均为 `PASS`。
- 所有章节存在 `qa/gates/*.gate.md` 且结论为 `PASS`。
- `preproduction/stage1/production_spec.md` 存在。
- `preproduction/stage2_sample/sample_review.md` 结论为 `PASS`。
- `output/publication_lint.json` 存在，且无硬错误。
- `output/asset_manifest_check.json` 存在，且无硬错误；若全书无图像、表格、样式外部资源，报告中也必须明确记录 0 asset refs。
- `qa/refinement/` 存在；若使用 `scripts/refinement_check.js`，出版范围内 BOM、乱码、中文连续空格和不当标点应为 0，或在 QA 中记录明确例外。
- `reviews/random_spotcheck/round_XXX/random_sample_manifest.json`、`strata_summary.json`、`validation_report.json`、`samples/`、`evidence/`、`reviews/`、`fixes/fix_log.md`、`verification/closure_check.md` 均存在；`validation_report.json.release_confidence >= 0.80`；`validation_report.json.excellence_gate_required = true`；`validation_report.json.current_run_pass_rounds_required >= 1` 且 `validation_report.json.current_run_pass_rounds_count >= validation_report.json.current_run_pass_rounds_required`；至少两个独立 Agent 分层随机抽检通过，且每个 Agent `average_score >= 92`、`lowest_score >= 88`、每个样本均有逐项评分行、无单项 < 80、无未关闭 P0/P1/P2 必修项；若任何轮发现过问题，`fix_log.md` 与 `closure_check.md` 必须证明每个问题族已完成全书同类问题审计并关闭。
- `reviews/random_spotcheck/random_sample_manifest.json`、`reviews/agent_a/random_spotcheck_review.md`、`reviews/agent_b/random_spotcheck_review.md` 和 `reviews/scorecards/random_spotcheck_score.md` 均指向或记录最近通过轮次。
- `npm run review:random-validate:pass` 通过。
- `output/book.epub` 存在。
- 公版或授权项目：`output/release/{目标语言书名}_vX.X.X.epub`、`output/release/release_notes.md`、`output/release/release_state.json` 和 `output/release/release_index.md` 存在。
- 公版或授权项目：`output/release/release_state.json.latest_status == PASS`，且 `release_notes.md` 顶部最新条目已记录随机抽检轮次、`release_confidence >= 0.80`、EPUBCheck、publication lint、修复闭环、风险和下一轮迭代。
- 私人自用项目：`output/private_artifacts/{目标语言书名}_private_vX.X.X.epub`、`output/private_artifacts/private_artifact_notes.md`、`output/private_artifacts/private_artifact_state.json` 和 `output/private_artifacts/private_artifact_index.md` 存在。
- 私人自用项目：`output/private_artifacts/private_artifact_state.json.latest_status == PASS`，且 `private_artifact_notes.md` 顶部最新条目已记录随机抽检轮次、`release_confidence >= 0.80`、EPUBCheck、publication lint、私人读者可见门禁、修复闭环和风险。
- EPUBCheck 无 fatal/error。
- `reviews/agent_a/review.md` 和 `reviews/agent_b/review.md` 均存在，且评分通过。
- `reviews/revision_route.md` 中无未关闭 P0/P1/P2 必修项。
- `retrospective/book_retrospective.md` 和 `retrospective/template_update_suggestions.md` 存在。
- 重大精修问题已有书籍专属目标或修复记录，可复用经验已回填到对应模板层。
- 可复现译文质量问题族已合并回填到 `skills/translation-quality-defect-families/SKILL.md`，并已被随机抽检 `review:random-validate:pass` 的 skill backfill 字段校验覆盖；若没有新的可复用问题族，问题轮次必须记录 `NOT_APPLICABLE` 与原因。
- `state/pipeline_state.json.status == DONE`。

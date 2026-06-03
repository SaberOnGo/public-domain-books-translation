# 自动化执行合约 / Automation Contract

## AI 的职责

AI 必须自动决定：

- 如何先把模板复制成独立书籍工程目录。
- 如何在需要时叠加特殊书型 profile，例如古典科学、数学、天文学或图表密集型作品。
- 下载哪个文本版本。
- 如何清洗和分章。
- 如何命名章节文件。
- 如何生成元数据、术语表、文体画像。
- 如何选择预翻译样本。
- 如何在每章译后立即执行全量检查与修复节点，并在未通过时阻止进入下一章翻译或进入终稿。
- 如何在失败时回溯到正确阶段。
- 如何构建并校验 EPUB。
- 如何把 Markdown 章节转换为 XHTML，并把图像、SVG、CSS、表格等 EPUB 资源复制、登记到 OPF manifest。
- 如何在第一版 EPUB 后执行分层随机抽检模块，生成正文、表格、图片、公式、图注/注释等读者可见审计单元样本，派生至少 2 个独立 Agent 评审，并根据抽检、问题族全书同类审计、修复闭环和新 seed 复抽结果自动返工或继续。
- 如何在随机抽检闭环通过后创建带版本号的 EPUB 产物：公版或授权项目把 `output/book.epub` 固化为 `output/release/{目标语言书名}_vX.X.X.epub`，并把最新中英文说明追加到累计 `release_notes.md` 顶部；私人自用项目使用 `modes/private_use` 的脚本把本地私人产物写入 `output/private_artifacts/`。

## AI 不应询问用户

除非来源无法访问、版权状态无法判断，或用户请求非公版私人自用但没有提供本地书源文件，AI 不应询问：

- 文件名怎么起。
- 目录怎么组织。
- 章节怎么编号。
- QA 文件写哪里。
- EPUB 输出到哪里。
- 图表资源目录怎么命名；默认使用 `assets/figures/`、`assets/images/`、`assets/styles/`、`source/tables/`。

## 模板保护硬规则 / Template Protection

- `template/epub_pipeline/common` 和 `template/epub_pipeline/{source-target}` 语言方向模板永远视为只读模板。
- `template/epub_pipeline/profiles/{profile-target}` 控制模板也永远视为只读模板。
- 任何具体书籍的数据不得写入模板目录。
- 若当前工作目录就是模板目录，AI 必须先创建并切换到独立工程目录。
- 推荐目录：`books/{target}/{number}_{pg_id_or_author_title_slug}/`，并且必须由 `books/scripts/create_book_project.py` 自动创建和分配编号。
- 非公版私人自用工程必须使用 `--mode private-use` 创建到被 Git 忽略的 `books/private/{target}/{number}_{目标语言书名}_{目标语言作者名}/`；不得把私人原文、译文、QA、EPUB 输出或具体书籍 metadata 写入可发布的 `books/{target}/`。
- 只有复制后的 `PROJECT_ROOT` 可以写入原文、章节、QA、译文和 EPUB。

## 人类可选审阅

AI 可以在以下文件生成后提示用户审阅，但不能把流程设计成必须人工操作：

- `metadata/book_specific_translation_research.md`
- 启用语言模板要求时的 `metadata/source_witness_manifest.md`
- 启用语言模板要求时的 `qa/textual/textual_uncertainty_log.md`
- `qa/pretranslation/pretranslation_report.md`
- `glossary/terms.csv`
- `metadata/style_profile.md`
- 启用 profile 时的 `metadata/reference_witness_policy.md`
- 启用 profile 时的 `qa/technical/terminology_lock_report.md`
- 启用 profile 时的 `qa/technical/diagram_table_inventory.md`
- 含图表书籍的 `qa/technical/{NNN_slug}.diagram_table_audit.md`
- 预制作阶段的 `output/asset_manifest_check.json`

如果用户没有介入，AI 必须按 PASS/FAIL 规则自行继续或返工。

## 每章译后全量检查硬门禁

- 每章写入 `chapters/translated/{NNN_slug}.md` 后，AI 必须立即只针对该章执行“每章译后，全量检查并修复节点”，并写入 `qa/chapter_controls/{NNN_slug}.control.md`。
- 该节点必须检查该章是否符合模板要求，包括但不限于该章对 metadata/nav/目录/章节标题的影响、正文、注释、图表/公式/表格/图片的文字接口、样式、读者可见内容、通俗化、可读性、润色、名词术语、注释密度、事实和数值。不得只检查用户点名项目，也不得扩大成全书门禁。
- 该节点必须全章检查，而不是只抽样检查。抽样朗读或抽样段落只能作为辅助证据，不能替代全章核查。
- 若发现 P0/P1/P2、读者不可理解、事实/术语/文字接口错误、模板硬门禁失败、目标语言翻译腔、读起来费劲、中文润色不足、为了通俗而损害专业度、专业术语解释不足，或任何其他翻译/润色问题，必须修复；但发现并修复问题的这一轮只能记录为 `FIXED_RECHECK_REQUIRED`，不得直接 `PASS`。
- 必须追加一次新的整章复查。只有最近一轮同时记录 `scope: FULL_CHAPTER`、`issues_found: 0`、`fixes_applied: 0`、`unresolved_blocking_issues: 0`、`latest_round_status: PASS`、`allow_next_chapter: true` 时，才允许继续；若 profile/项目规则更严格，按更严格规则。分数不能抵消 P0/P1/P2、读者难以理解、事实/术语/文字接口错误、模板硬门禁失败或明显目标语言翻译腔。
- 通俗化与专业质量不是二选一。当前章文字应尽量读得顺、有趣、不费劲，同时保持原书应有的专业术语、概念层级、论证水准和知识风格；不得为了“好懂”把专业内容改扁、改错或泛化。
- 只有满足上述条件后，才允许进入下一章翻译、后续 fidelity/readability/terminology 审校或 `chapters/final/`。
- 图表、表格、公式和图片在本节点只做当前章文字接口检查与资产分流。重绘、OCR、裁剪、数值校验、公式排版、资源路径或 manifest 问题应路由到资产/技术门禁；已路由问题阻止进入终稿、构建和 release，但不让译后文字门禁无限循环。
- 所有失败点、修复摘要、复查轮次和是否允许继续，必须记录在该章 control 文件中；不得覆盖失败教训。
- `preflight:template` 必须检查 `chapters/translated/*.md` 的对应章节 control 是否存在，且最近整章轮次是否满足上述零问题 PASS 字段。发现 `chapters/final/*.md` 时，还必须检查对应章节 gate 是否存在且 PASS。失败时不得继续下一章、构建 EPUB、创建 release 或 private artifact。

## EPUB 资源自动化规则

- AI 必须把读者可见 Markdown 转成 XHTML 后再打包 EPUB。
- AI 必须把所有 EPUB 内使用的图片、SVG、CSS、字体等资源登记到 OPF manifest。
- AI 必须运行 `node scripts/asset_manifest_check.js --write-report` 或等效检查。
- 技术表格应优先生成 XHTML `<table>`；不得把可结构化数值表只做成图片。
- 资源检查失败时，必须回到预制作或构建脚本阶段修复，不得继续最终输出。

## 第一版 EPUB 后分层随机抽检自动化规则

- 第一版 `output/book.epub` 完成后，AI 必须立即执行 `prompts/16a_stratified_random_spotcheck.md` 和 `references/stratified_random_spotcheck.md`，不得直接宣布完成。
- 每一轮精校完成后，AI 必须运行 `npm run review:random-samples`，或等效运行 `python scripts/select_random_review_passages.py --source-dir chapters/final --agents 2 --samples-per-agent 60 --rounds-planned 4 --min-current-run-pass-rounds 2 --target-confidence 0.80 --defect-rate 0.10 --profile auto`。
- 每个新的 AI 执行批次必须产生自己的新随机抽检轮次；旧 Agent、旧 release 或旧 private artifact 之前已经 PASS 的 `round_XXX` 只能作为历史记录，不得计入当前执行者的退出条件。manifest 必须带 `review_run_id` 和 `generated_at`。用户可以指定任意 `>=1` 的当前运行连续 PASS 轮次要求；未指定时默认 2。强校验只统计同一当前 `review_run_id` 下、晚于最近 release/private artifact 的最新连续 PASS 轮次。
- 默认发布前抽样预算为正文层每个 Agent 每轮 60；表格和图片 `N<=80` 全检，否则每轮总抽 20；公式/证明块 `N<=100` 全检，否则每轮总抽 20；图注/表注/注释 `N<=120` 全检，否则每轮总抽 20。
- 若任一层、任一样本发现任何需要修复或可能系统性复现的问题，本轮立即把发现归纳为问题族，并执行全书同类问题审计和闭环；不得只修被抽中的样本，也不得等到第二轮才全书检查。同层可被标记为高风险，用于后续抽样和人工复核，但不能替代本轮全书同类问题审计。
- 脚本必须通过最近轮次 `round_XXX/reviews/*_review.md` 中的 P0/P1/P2 样本行自动记录高风险层，不能只依赖主执行 AI 自觉标记。风险标记只用于后续抽样和复核；本轮一旦发现问题，仍必须立即执行问题族全书同类审计。
- 抽样总体 `N` 是读者可见审计单元总数；抽样层至少包括 `paragraph`、`table`、`figure`、`formula`、`caption_note`。表格、图片、公式不得被普通段落抽样替代。
- 每次抽检必须生成 `reviews/random_spotcheck/round_XXX/` 子目录，包含 seed、manifest、分层样本、图片/表格/公式证据、Agent 评审、修复记录和闭环验证文件，供人工核查。
- 随机抽检必须至少使用 2 个独立 Agent；每个 Agent 必须逐样本给出 0-100 分、问题类型、优先级、是否返工和理由。
- 两个 Agent 均必须按模板、本书 profile、目标语言规则和读者视角认真分析：读不读得懂、是否忠实、数学/天文学链条是否成立、表格/图片/公式/术语/数值/注释是否符合书籍设计。
- 退出精校的最低条件是：两个 Agent 均 PASS，无单项 < 70，无未关闭 P0/P1/P2，无读不懂样本，无数学或天文学阻断，无术语/数值/图表/公式错误，并且 `npm run review:random-validate:pass` 通过；该报告必须记录 `current_run_pass_rounds_required >= 1` 且 `current_run_pass_rounds_count >= current_run_pass_rounds_required`。用户未指定时默认要求 2。
- 任一 Agent 抽检不通过时，AI 必须写入 `reviews/revision_route.md`，回到精校或更早阶段修复；每个发现必须先归纳为“问题族”，再对整本读者可见书稿执行全书同类问题审计，覆盖 `chapters/final/`、frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML，不得只修改被抽中的样本；修复所有确认命中、记录合理例外后，必须在旧轮次 `fixes/fix_log.md` 与 `verification/closure_check.md` 中定点关闭单个问题和该问题族，并使用新 seed 重新生成下一轮样本，不得复用旧样本。

## EPUB 版本化发布自动化规则

- 随机抽检模块执行后，公版或授权项目必须执行 `prompts/18a_release_versioning.md` 或等效 release 脚本；私人自用项目必须执行 `npm run private:artifact:create` 或等效 private artifact 脚本；不得只留下 `output/book.epub` 就宣布完成。
- 版本号格式必须是 `v{main_version}.{sub_version}.{patch_version}`，默认首版 `v0.0.1`；没有人工明确变更 main/sub 时，每次迭代发布只递增 patch。
- 公版或授权项目的所有版本化 EPUB 必须写入 `output/release/`，文件名为 `{目标语言书名}_vX.X.X.epub`，例如 `金属巨兽_v0.0.4.epub`；不得把多个版本平铺在 `output/` 根目录，不得使用英文 slug 或通用 `book_` 前缀。
- 私人自用项目的所有版本化 EPUB 必须写入 `output/private_artifacts/`，文件名为 `{目标语言书名}_private_vX.X.X.epub`；它不是公开 release，不得发布到 GitHub。
- 每个版本必须把说明追加到累计 `release_notes.md` 或 `private_artifact_notes.md` 顶部，记录发布原因、问题点、修复方式、QA 证据、风险和下一轮迭代。
- `DRAFT` release 可用于人工核查，但不得作为 `DONE` 依据。
- `PASS` release 或 private artifact 必须来自 `npm run review:random-validate:pass` 或等效 `--require-pass --min-current-run-pass-rounds N` 校验，其中 `N>=1`，用户未指定时默认 `N=2`；校验报告必须满足 `current_run_pass_rounds_count >= current_run_pass_rounds_required`、`release_confidence >= 0.80`、EPUBCheck fatal/error 为 0、publication lint 无未解决问题。私人自用项目还必须通过 `preflight:private-use` 和 `reader:private-check`。
- 后续读者评论、人工审校、阅读行为分析、自动化 QA 或随机抽检发现的问题，必须进入下一轮修复和新的 patch release 或 private artifact，不得覆盖旧产物证据。

## 失败处理

失败时：

1. 写明失败阶段。
2. 写明失败文件。
3. 写明回溯目标。
4. 修改对应规则或试译。
5. 保留失败版本，不要覆盖失败教训。

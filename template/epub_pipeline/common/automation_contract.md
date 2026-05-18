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
- 如何在失败时回溯到正确阶段。
- 如何构建并校验 EPUB。
- 如何把 Markdown 章节转换为 XHTML，并把图像、SVG、CSS、表格等 EPUB 资源复制、登记到 OPF manifest。
- 如何在第一版 EPUB 后执行分层随机抽检模块，生成正文、表格、图片、公式、图注/注释等读者可见审计单元样本，派生至少 2 个独立 Agent 评审，并根据抽检、修复闭环和新 seed 复抽结果自动返工或继续。
- 如何在随机抽检闭环通过后创建带版本号的 EPUB release，把 `output/book.epub` 固化为 `output/release/book_vX.X.X.epub`，并写入中英文 `release_note_vX.X.X.md`。

## AI 不应询问用户

除非来源无法访问或版权状态无法判断，AI 不应询问：

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

## EPUB 资源自动化规则

- AI 必须把读者可见 Markdown 转成 XHTML 后再打包 EPUB。
- AI 必须把所有 EPUB 内使用的图片、SVG、CSS、字体等资源登记到 OPF manifest。
- AI 必须运行 `node scripts/asset_manifest_check.js --write-report` 或等效检查。
- 技术表格应优先生成 XHTML `<table>`；不得把可结构化数值表只做成图片。
- 资源检查失败时，必须回到预制作或构建脚本阶段修复，不得继续最终输出。

## 第一版 EPUB 后分层随机抽检自动化规则

- 第一版 `output/book.epub` 完成后，AI 必须立即执行 `prompts/16a_stratified_random_spotcheck.md` 和 `references/stratified_random_spotcheck.md`，不得直接宣布完成。
- 每一轮精校完成后，AI 必须运行 `npm run review:random-samples`，或等效运行 `python scripts/select_random_review_passages.py --source-dir chapters/final --agents 2 --samples-per-agent 60 --rounds-planned 4 --target-confidence 0.80 --defect-rate 0.10 --profile auto`。
- 默认发布前抽样预算为正文层每个 Agent 每轮 60；表格和图片 `N<=80` 全检，否则每轮总抽 20；公式/证明块 `N<=100` 全检，否则每轮总抽 20；图注/表注/注释 `N<=120` 全检，否则每轮总抽 20。
- 若任一层发现 P0/P1/P2，下一轮随机抽样量保持不变；若同层连续两轮发现 P0/P1/P2，必须进入定向专项审计和闭环复查，默认不强制全检。
- 脚本必须通过最近轮次 `round_XXX/reviews/*_review.md` 中的 P0/P1/P2 样本行自动记录高风险层和专项审计要求，不能只依赖主执行 AI 自觉标记。
- 抽样总体 `N` 是读者可见审计单元总数；抽样层至少包括 `paragraph`、`table`、`figure`、`formula`、`caption_note`。表格、图片、公式不得被普通段落抽样替代。
- 每次抽检必须生成 `reviews/random_spotcheck/round_XXX/` 子目录，包含 seed、manifest、分层样本、图片/表格/公式证据、Agent 评审、修复记录和闭环验证文件，供人工核查。
- 随机抽检必须至少使用 2 个独立 Agent；每个 Agent 必须逐样本给出 0-100 分、问题类型、优先级、是否返工和理由。
- 两个 Agent 均必须按模板、本书 profile、目标语言规则和读者视角认真分析：读不读得懂、是否忠实、数学/天文学链条是否成立、表格/图片/公式/术语/数值/注释是否符合书籍设计。
- 退出精校的最低条件是：两个 Agent 均 PASS，无单项 < 70，无未关闭 P0/P1/P2，无读不懂样本，无数学或天文学阻断，无术语/数值/图表/公式错误，并且 `npm run review:random-validate:pass` 通过。
- 任一 Agent 抽检不通过时，AI 必须写入 `reviews/revision_route.md`，回到精校或更早阶段修复；修复后必须在旧轮次中定点关闭旧问题，并使用新 seed 重新生成下一轮样本，不得复用旧样本。

## EPUB 版本化发布自动化规则

- 随机抽检模块执行后，AI 必须执行 `prompts/18a_release_versioning.md` 或等效 release 脚本；不得只留下 `output/book.epub` 就宣布完成。
- 版本号格式必须是 `v{main_version}.{sub_version}.{patch_version}`，默认首版 `v0.0.1`；没有人工明确变更 main/sub 时，每次迭代发布只递增 patch。
- 所有版本化 EPUB 必须写入 `output/release/`，文件名为 `book_vX.X.X.epub`；不得把多个版本平铺在 `output/` 根目录。
- 每个版本必须生成中英文 `release_note_vX.X.X.md`，记录发布原因、问题点、修复方式、QA 证据、风险和下一轮迭代。
- `DRAFT` release 可用于人工核查，但不得作为 `DONE` 依据。
- `PASS` release 必须来自 `npm run review:random-validate:pass` 或等效 `--require-pass` 校验，且 `release_confidence >= 0.80`、EPUBCheck fatal/error 为 0、publication lint 无未解决问题。
- 后续读者评论、人工审校、阅读行为分析、自动化 QA 或随机抽检发现的问题，必须进入下一轮修复和新的 patch release，不得覆盖旧 release 证据。

## 失败处理

失败时：

1. 写明失败阶段。
2. 写明失败文件。
3. 写明回溯目标。
4. 修改对应规则或试译。
5. 保留失败版本，不要覆盖失败教训。

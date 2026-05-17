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
- 如何在每轮精校后生成随机段落抽检样本，派生至少 2 个独立 Agent 各抽检不少于 10 段，并根据抽检结果自动返工或继续。

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
- 推荐目录：`books/{pg_id_or_author_title_slug}/`。
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

## 精校后随机抽检自动化规则

- 第一版 EPUB 完成后，AI 必须先完成全书再评审和精校，不得直接宣布完成。
- 每一轮精校完成后，AI 必须运行 `npm run review:random-samples`，或等效运行 `python scripts/select_random_review_passages.py --source-dir chapters/final --agents 2 --samples-per-agent 10`。
- 随机抽检必须至少使用 2 个独立 Agent；每个 Agent 至少检查 10 个随机正文段落，并逐段给出 0-100 分、问题类型、是否返工和理由。
- 两个 Agent 均必须按中文读者视角认真分析：读不读得懂、是否忠实、数学/天文学链条是否成立、术语/数值/图表/注释是否符合书籍设计。
- 退出精校的最低条件是：两个 Agent 平均分均 >= 75，且无单段 < 70、无读不懂段落、无数学或天文学阻断、无术语/数值/图表错误。
- 任一 Agent 抽检不通过时，AI 必须写入 `reviews/revision_route.md`，回到精校或更早阶段修复；修复后必须重新生成随机样本并重新抽检，不得复用旧样本。

## 失败处理

失败时：

1. 写明失败阶段。
2. 写明失败文件。
3. 写明回溯目标。
4. 修改对应规则或试译。
5. 保留失败版本，不要覆盖失败教训。

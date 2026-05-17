# /goal: 《Almagest》章节试译、全书翻译与第一版 EPUB 闭环

日期：2026-05-16

本 `/goal` 是 `books/ptolemy_almagest_grc_zh_hans/` 的执行目标。必须遵守仓库根目录 `AGENTS.md`、本书 `AGENTS.md`、`PIPELINE_SPEC.md`、`template/epub_pipeline/grc-zh-Hans`、`template/epub_pipeline/targets/zh-Hans`、`template/epub_pipeline/profiles/classical-science-zh-Hans`，以及本书已有 metadata、source、qa、research、references、prompts、state 文件。

## 总目标

从当前研究/预翻译阶段开始，先完成一个章节的正式试翻译与评审。若试译通过，才进入全书翻译、章节 QA、第一版 EPUB 构建、全书再评审、数学/天文学精校和多轮修订。若试译不通过，必须退回研究、预翻译、术语、图表、OCR/转写或技术校验阶段，不得继续批量翻译。

最终退出条件：第一版 EPUB 完成，并经过至少 2 个独立 Agent 评审通过；所有 P0/P1/P2 必修项关闭；数学、天文学、图表、数值、术语和来源证据检查通过；`state/pipeline_state.json.status` 才能进入最终完成状态。

## 当前事实

- Heiberg 希腊文扫描 PDF 已下载并记录 SHA256。
- 当前 `formal_translation_allowed=false`。
- 当前尚未完成正式 OCR/转写底稿。
- 当前 `chapters/src/`、`chapters/translated/`、`chapters/final/` 不应有正式章节产物。
- 英译本只能作为 reference witness；Toomer 不得下载进仓库，Taliaferro 未找到合法 full-view 下载源。
- PAL Heiberg 转写可作为结构和定位参考；是否可批量复制文本必须先完成权利与来源政策核查。

## 试译章节选择

首选试译章节：Book I.10。

理由：

- 它能压力测试本书最危险的部分：几何证明、弦表预备、图表标签、数学关系和术语一致性。
- 如果 Book I.10 不能稳定处理，不能进入全书翻译。

允许回退候选：Book I.1。

回退条件：

- Book I.10 的本地 PDF 页图、图表、希腊文本或转写在合理时间内无法核清。
- 权利核查不允许使用现有数字转写，而 OCR/人工转写暂不可行。
- 试译门禁判断 Book I.10 不适合作为第一章正式试译。

回退到 Book I.1 时，必须记录为什么放弃 Book I.10，并明确 Book I.10 仍需后续数学专门试译。

## 阶段 0：试译前解锁门禁

在写入任何 `chapters/translated/*.md` 前，必须完成：

1. `source/source_text_raw.txt` 和 `source/source_text.txt` 的策略确定。
2. 试译章节的古希腊文本来源确定：本地 PDF OCR、人工转写、可合法使用的数字转写，三者择一或组合。
3. 试译章节页码/卷章定位记录。
4. 若试译章节含图或表，完成对应图表清单和重绘/核对策略。
5. `qa/pretranslation/pretranslation_report.md` 对“一个章节正式试译”给出 PASS，而不是只给 micro-sample PASS。
6. `state/pipeline_state.json.formal_translation_allowed` 只能在试译门禁 PASS 后，为“单章节试译”设置有限允许；不得直接放开全书翻译。

若任何一项失败，进入“退回研究/预翻译阶段”。

## 阶段 1：章节正式试译

输出：

- `chapters/src/{trial_chapter}.md`
- `chapters/translated/{trial_chapter}.md`
- `qa/chapter_controls/{trial_chapter}.control.md`
- `qa/technical/{trial_chapter}.technical_audit.md`
- `qa/technical/{trial_chapter}.diagram_table_audit.md`，如适用
- `reviews/trial_chapter/{trial_chapter}.review.md`

硬规则：

- 必须从古希腊文底本翻译。
- 英译本只能帮助理解，不得作为隐藏底稿。
- 不得省略证明步骤。
- 不得把古代天文学改写成现代天体物理说明。
- 数学术语、点名、图名、表名、单位和数值必须可追踪。
- 不得写入 `chapters/final/`。

## 阶段 2：试译评审与路由

试译 PASS 条件：

- 忠实度评审 PASS。
- 中文可读性评审 PASS。
- 术语一致性评审 PASS。
- 数学/天文学技术审计 PASS。
- 图表/表格审计 PASS，若适用。
- 没有 P0/P1 问题。
- P2 问题有明确修复并复核。

试译 FAIL 路由：

- 来源/OCR/转写问题：回到 `01_ingest_clean`。
- 分章/页码/标题问题：回到 `02_split`。
- 术语问题：回到 `06_glossary_style` 和 `06a_technical_terminology_lock`。
- 图表/表格问题：回到 `06b_diagram_table_inventory`。
- 翻译策略问题：回到 `04_book_specific_research` 和 `05_pretranslation_trials`。
- 数学/天文学理解问题：回到 `qa/technical/verification_plan.md`、`mathematical_term_lock.md`、`proof_dependency_map.md`、`astronomical_model_registry.csv`。

试译不 PASS，不得进入全书翻译。

## 阶段 3：全书翻译

只有试译 PASS 后，才能执行：

1. 完成全书 `chapters/src/*.md` 稳定切分。
2. 更新 `source/toc.json`。
3. 全书术语锁定从 `PILOT_LOCKED` 提升为可执行的 `LOCKED` 或分域 `LOCKED_WITH_SCOPE`。
4. 逐章写入 `chapters/translated/*.md`。
5. 每章立即执行 `08a`、`08b`、`08c`、`10`、`11` 相关门禁。
6. 每章只有章节门禁 PASS 后，才可进入 `chapters/final/*.md`。

## 阶段 4：第一版 EPUB

所有章节终稿 PASS 后，按现有 prompt 严格执行：

1. `13_preproduction_stage1_spec_zh_grc.md`
2. `14_preproduction_stage2_sample_zh_grc.md`
3. `15_full_book_production_zh_grc.md`

输出至少包括：

- `preproduction/stage1/production_spec.md`
- `preproduction/stage2_sample/sample_book.epub`
- `preproduction/stage2_sample/sample_review.md`
- `output/book.epub`
- `output/publication_lint.json`
- `output/epubcheck.json` 或 `output/epubcheck.log`

EPUBCheck 必须 fatal=0、error=0。

## 阶段 5：全书再评审、精校与迭代

第一版 EPUB 完成后，必须进行多轮检查，特别是：

- 数学证明依赖。
- 弦表、角度、六十进制数值。
- 天文学模型术语。
- 图表标签与正文引用。
- 古代科学概念与现代解释边界。
- 中文可读性、术语一致性、标题策略、metadata、封面、目录、排版。

任何 P0/P1/P2 问题必须回退到对应阶段修复，不得只在 EPUB 上表面修补。

## 阶段 6：至少两个独立 Agent 评审

按 `prompts/16_independent_review_agents_zh_grc.md` 派生至少 2 个独立 Agent：

- Agent A：翻译、古希腊文忠实度、中文可读性、术语一致性、数学/天文学内容。
- Agent B：EPUB 工程、metadata、封面、排版、目录、可读性、lint、EPUBCheck。

对于本书，还需确保至少一个评审覆盖数学/天文学技术细节；若 Agent A/B 都没有覆盖，必须增加 Agent C：数学/天文学专项评审。

通过条件：

- 至少 2 个独立 Agent 明确 PASS。
- 每个 PASS Agent 的总分必须 >= 85。
- 无 P0/P1。
- P2 必修项全部关闭。
- `reviews/revision_route.md` 明确无未解决阻断项。

## 禁止捷径

- 禁止未完成正式希腊文底稿就批量翻译。
- 禁止试译不 PASS 就进入全书翻译。
- 禁止把英译本当底稿。
- 禁止把 AI 微样本当正式章节。
- 禁止未核图表、表格、数值就通过数学章节。
- 禁止未通过双 Agent 评审就宣布完成。
- 禁止把模板目录作为书籍产物写入位置。

## 完成定义

只有同时满足以下条件，才能宣布本 `/goal` 完成：

- `state/pipeline_state.json.status = DONE` 或项目约定的最终完成状态。
- `output/book.epub` 存在并通过 EPUBCheck。
- `output/final_manifest.md` 存在。
- 所有章节有 src、translated、final 和 QA 记录。
- 所有数学/天文学/图表/表格检查 PASS。
- 至少 2 个独立 Agent 评审 PASS。
- 复盘和模板经验回填完成或明确记录为不需要。

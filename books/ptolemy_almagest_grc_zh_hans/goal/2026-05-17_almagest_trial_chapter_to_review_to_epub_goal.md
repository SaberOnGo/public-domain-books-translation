# /goal: 《Almagest》章节试译评审到第一版 EPUB 闭环

日期：2026-05-17

本 `/goal` 是 `books/ptolemy_almagest_grc_zh_hans/` 的当前正式执行合约。它必须同时遵守仓库根目录 `AGENTS.md`、本书 `AGENTS.md`、`PIPELINE_SPEC.md`、`MASTER_PROMPT.md`、`template/epub_pipeline/grc-zh-Hans`、`template/epub_pipeline/targets/zh-Hans`、`template/epub_pipeline/profiles/classical-science-zh-Hans`，以及本书已有 `metadata/`、`source/`、`qa/`、`references/`、`prompts/`、`state/` 文件。

会话 `/goal` 工具目标与本文件一致：先做一个章节试翻译并评审；评审通过才进入全书翻译；评审不通过或被阻断则回到研究、预翻译、术语、图表、OCR/转写或技术校验阶段。

## 当前事实

- 本书仍处于研究与预翻译阶段，不是全书翻译阶段。
- Heiberg 希腊文扫描 PDF 已保存到 `source/facsimile/Almagest_Complete_Heiberg_1898.pdf`，并记录 SHA256。
- PAL Heiberg 古希腊转写 XML 已保存到 `source/transcriptions/pal_heiberg/pal_heiberg_mathematike_syntaxis_1.xml`，许可记录为 CC BY 4.0 辅助原文控制来源。
- PDF 扫描仍是页图、图表、表格、旧版页码与最终源图核验依据。
- 英译本只能作为 reference witness，用于理解、差异校读与技术核验；不得作为隐藏底稿，不得复制仍受版权保护译本的措辞、注释、表格、图版或编辑结构。
- `formal_translation_allowed=false` 表示不得批量翻译，也不得写入 `chapters/final/`。

## 总目标

完成以下闭环：

1. 抽取并核定一个试译章节的古希腊原文底稿。
2. 进行一个章节试翻译。
3. 对该试译章节做忠实度、中文、术语、数学、天文学、图表、表格和数值评审。
4. 若试译评审 PASS，才进入全书正式切分、翻译、章节门禁、第一版 EPUB 构建。
5. EPUB v1 完成后，进行全书再评审、精校和必要迭代，尤其检查数学、天文学、图表、表格、数值、单位、术语和古代科学概念边界。
6. 每轮精校后，必须由至少 2 个独立 Agent 做随机段落抽检，每个 Agent 至少 10 个随机正文段落；两个 Agent 都达到抽检通过条件后，才可进入最终独立评审结论。
7. 至少 2 个独立 Agent 明确评审 PASS 后，才允许退出本目标。

## 试译章节

首选试译章节：Book I.10。

理由：

- 它包含几何证明、弦表预备、比例关系和图表依赖，能暴露本书最危险的问题。
- 如果 Book I.10 无法稳定处理，不能证明本项目具备整本书翻译能力。

允许回退章节：Book I.1。

回退条件：

- Book I.10 的 PDF 页图、图表或表格无法核清。
- Book I.10 的古希腊转写与扫描无法建立可追踪对应。
- 术语或证明链审计显示当前系统无法控制数学内容。

回退到 Book I.1 时，必须在 `qa/chapter_trial/trial_chapter_gate.md` 记录原因；Book I.10 仍必须作为后续数学专项试译。

## 阶段 0：试译前门禁

写入 `chapters/translated/` 前，必须满足：

- `chapters/src/{trial_chapter}.md` 存在，且说明来源、许可、PAL marker、PDF 页图核验状态。
- `source/trial_toc.json` 或等效 trial toc 记录试译章节范围。
- `qa/chapter_trial/trial_chapter_gate.md` 明确允许单章节试译；不得默认允许全书翻译。
- 术语至少达到 Book I 试译范围的 `PILOT_LOCKED`，且术语未锁定项必须进入 `qa/technical/mathematical_term_lock.md` 或 `qa/technical/terminology_change_log.md`。
- Book I.10 若涉及图表，必须在 `qa/technical/diagram_table_inventory.md` 或章节图表审计中记录“待 PDF 页图核验”或“已核验”。
- `state/pipeline_state.json` 只能记录“有限试译允许”或“仍被阻断”；不得将 `formal_translation_allowed` 改成全书 `true`。

阶段 0 不通过时，必须停止在研究/预翻译阶段。

## 阶段 1：章节试翻译

允许输出：

- `chapters/src/{trial_chapter}.md`
- `chapters/translated/{trial_chapter}.md`
- `qa/chapter_controls/{trial_chapter}.control.md`
- `qa/technical/{trial_chapter}.technical_audit.md`
- `qa/technical/{trial_chapter}.diagram_table_audit.md`
- `reviews/trial_chapter/{trial_chapter}.review.md`

禁止输出：

- `chapters/final/{trial_chapter}.md`
- 全书批量章节译文
- `output/book.epub`

试译硬规则：

- 必须从古希腊文底稿翻译。
- 英译本只能作为 reference witness。
- 不得省略证明步骤、数值、比例关系、图表标签或点线关系。
- 不得用现代天文学结论改写古代文本；现代解释只能进入译注、校注或 QA。
- 弦、弧、直径、半径、比例、角度、六十进制数值、天球、黄道、赤道等术语必须保持一致。
- 不确定的词、句、图、数值必须标记，不得用流畅中文掩盖疑点。

## 阶段 2：试译评审和路由

试译 PASS 条件：

- 古希腊文本忠实度 PASS。
- 中文可读性 PASS。
- 术语一致性 PASS。
- 数学证明链 PASS。
- 天文学概念边界 PASS。
- 图表/表格/数值审计 PASS 或明确无图表/表格/数值。
- 无 P0/P1 问题。
- P2 必修项已修复并复核。

试译 FAIL 或 BLOCKED 路由：

- 来源、OCR、转写问题：回到 `01_ingest_clean`、`source/`、`qa/textual/`。
- 分章、页码、标题问题：回到 `02_split`、`source/book_i_segmentation.md`。
- 术语问题：回到 `06_glossary_style`、`06a_technical_terminology_lock`、`qa/technical/mathematical_term_lock.md`。
- 图表、表格、数值问题：回到 `06b_diagram_table_inventory`、`08c_diagram_table_audit`、`qa/technical/`。
- 数学或天文学理解问题：回到 `qa/technical/verification_plan.md`、`proof_dependency_map.md`、`astronomical_model_registry.csv`、领域 authority 资料。
- 中文策略问题：回到 `04_book_specific_research`、`05_pretranslation_trials`、`style_profile`。

试译不 PASS，不得进入全书翻译。

## 阶段 3：全书翻译

只有阶段 2 PASS 后，才能执行：

1. 全书或至少 Book I 先完成稳定 `chapters/src/*.md` 切分。
2. 更新 `source/toc.json`。
3. 术语从 `PILOT_LOCKED` 提升到 `LOCKED` 或 `LOCKED_WITH_SCOPE`。
4. 逐章生成 `chapters/translated/*.md`。
5. 每章完成 `08a` 译后控制、`08b` 技术审计、`08c` 图表/表格审计、`10` 术语审校、`11` 章节门禁。
6. 每章门禁 PASS 后，才可写入 `chapters/final/*.md`。

## 阶段 4：第一版 EPUB

所有章节终稿 PASS 后，按现有 prompt 执行：

- `13_preproduction_stage1_spec_zh_grc.md`
- `14_preproduction_stage2_sample_zh_grc.md`
- `15_full_book_production_zh_grc.md`
- `12_build_validate_zh_grc.md`

必须输出：

- `preproduction/stage1/production_spec.md`
- `preproduction/stage2_sample/sample_book.epub`
- `preproduction/stage2_sample/sample_review.md`
- `output/book.epub`
- `output/publication_lint.json`
- `output/epubcheck.json` 或 `output/epubcheck.log`

EPUBCheck 必须 fatal=0、error=0。出版文本 lint 不得有硬错误。

## 阶段 5：EPUB 后精校和迭代

第一版 EPUB 完成后，必须多轮检查：

- 数学证明依赖是否断裂。
- 弦表、角度、六十进制数值是否漂移。
- 天文学模型术语是否全书一致。
- 图表标签、正文引用、点线关系是否一致。
- 古代科学概念是否被现代化误改。
- 中文是否通顺但不过度润饰。
- 标题、目录、metadata、封面、注释、排版是否符合模板。

发现 P0/P1/P2 必修项时，必须通过 `reviews/revision_route.md` 回到对应阶段修复；不得只在 EPUB 成品上表面修补。

每轮精校结束后必须执行随机段落抽检：

- 运行 `npm run review:random-samples`，生成 `reviews/random_spotcheck/random_sample_manifest.json`、`agent_a_samples.md`、`agent_b_samples.md`；若 npm 脚本不可用，则运行 `python scripts/select_random_review_passages.py --source-dir chapters/final --agents 2 --samples-per-agent 10`。
- 两个独立 Agent 各检查不少于 10 个随机段落，不得互相参考，不得使用主执行 AI 挑选的段落。
- 每个 Agent 必须假设自己是普通但认真的中文读者，逐段检查是否读得懂、是否忠实、数学/天文学链条是否成立、术语/数值/图表/注释是否清楚。
- 每段给出 0-100 分。每个 Agent 平均分必须 >= 75，且无单段 < 70。
- 任一段存在读不懂、数学证明链断裂、天文学概念误导、术语/数值/图表关系错误，即使平均分达标也必须判为抽检失败。
- 任一 Agent 抽检失败时，必须更新 `reviews/revision_route.md` 并回到精校或更早阶段；修复后重新生成随机样本，重新进行双 Agent 抽检。

## 阶段 6：独立 Agent 评审

必须至少派生 2 个独立 Agent：

- Agent A：古希腊文忠实度、中文可读性、术语一致性、数学/天文学内容。
- Agent B：EPUB 工程、metadata、目录、排版、lint、EPUBCheck。

若 Agent A/B 未充分覆盖数学/天文学技术细节，必须增加 Agent C：数学/天文学专项评审。

退出条件：

- `reviews/random_spotcheck/random_sample_manifest.json` 存在，且 seed、候选段落数、Agent 样本编号可审计。
- `reviews/agent_a/random_spotcheck_review.md` 和 `reviews/agent_b/random_spotcheck_review.md` 均存在。
- 两个随机抽检 Agent 平均分均 >= 75，且无单段 < 70。
- 至少 2 个独立 Agent 明确 PASS。
- 每个 PASS Agent 总分 >= 85。
- 无 P0/P1。
- P2 必修项全部关闭。
- `reviews/revision_route.md` 无未关闭阻断项。

## 禁止捷径

- 禁止试译评审未通过就进入全书翻译。
- 禁止从英译本转译。
- 禁止未核 PDF 页图就把 AI 重绘图当最终图。
- 禁止未核表格、数值、单位就通过数学或天文学章节。
- 禁止把 pretranslation micro-sample 当正式章节。
- 禁止把模板目录当作书籍产物写入位置。
- 禁止在 2 个独立 Agent 评审 PASS 前宣布整书完成。

## 当前执行边界

本轮只允许推进阶段 0：

- 可抽取 Book I.10 PAL 古希腊试译底稿到 `chapters/src/`。
- 可建立 `source/trial_toc.json`。
- 可更新试译门禁和 pipeline state。
- 不得写入 `chapters/final/`。
- 若 PDF 页图核验仍未完成，试译评审必须保持 `BLOCKED` 或 `NOT_PASS`，不得进入阶段 3。

## 完成定义

本 `/goal` 只有在以下条件全部满足时才能完成：

- 试译章节 PASS，且全书翻译已完成。
- `output/book.epub` 存在并通过 EPUBCheck。
- `output/final_manifest.md` 存在。
- 所有章节存在 src、translated、final 和 QA 记录。
- 所有数学、天文学、图表、表格、数值检查 PASS。
- 精校后随机段落抽检已通过：至少 2 个独立 Agent，各不少于 10 段，平均分均 >= 75，且无单段 < 70、无读不懂或技术阻断段落。
- 至少 2 个独立 Agent 评审 PASS。
- 复盘和模板经验回填完成或明确记录为不需要。
- `state/pipeline_state.json.status` 达到项目最终完成状态。

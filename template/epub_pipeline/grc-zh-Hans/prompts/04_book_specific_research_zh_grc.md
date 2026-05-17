# 04 本书专项翻译研究 / Book-Specific Translation Research

## 输入 / Input

- `source/source_text.txt`
- `source/toc.json`
- `metadata/book.yaml`
- `metadata/rights_checklist.md`
- `metadata/source_witness_manifest.md`
- `references/translation_research_universal.md`
- `references/quality_standard.md`
- `references/ancient_greek_source_notes.md`
- `references/ancient_greek_textual_criticism_policy.md`
- `references/ancient_greek_reference_translation_policy.md`
- `references/ancient_greek_names_transliteration_policy.md`

## 任务 / Tasks

生成 `metadata/book_specific_translation_research.md`，必须包含：

1. 本书一句话定位。
2. 作者身份、时代、写作目的、读者对象。
3. 底本信息：版本、编辑者、出版年、卷册/页码/行号体系、OCR/转写状态。
4. 来源角色分工：若同时使用扫描 PDF、古希腊文转写和第二语言译本，逐项说明 PDF/校勘本影像、古希腊转写、参考译本各自能做什么、不能做什么。
5. 本书翻译难点。
6. 不能照搬通用规则的地方。
7. 古希腊文专项风险：
   - 长周期句。
   - 分词链。
   - 省略和指代。
   - 引语/转述。
   - 异文、残损、拟补。
   - 参考译本可能造成的误导。
8. 本书关键词分层：
   - 核心身份词
   - 象征词
   - 场景词
   - 技术词
   - 历史敏感词
9. 本书句法策略：
   - 长句
   - 动作句
   - 说明句
   - 修辞句
   - 口语/日记句
10. 本书意象策略：
   - 哪些词必须翻出画面。
   - 哪些词只能解释。
   - 哪些地方容易越界发挥。
   - 哪些地方容易省成提纲。
11. 预翻译样本选择计划。
12. `qa/textual/textual_uncertainty_log.md` 初版策略：
   - 已知异文。
   - OCR/转写疑点。
   - 残损、脱文、拟补。
   - 语法歧义。
   - 参考译本分歧。

同时生成 `metadata/style_profile.md` 初版，必须包含：

- 一句话定位。
- 作者与叙述身份。
- 读者对象。
- 叙述声音。
- 句法策略。
- 关键词和称谓。
- 风格红线。
- 古希腊文底本和参考译本使用边界。
- 预翻译重点。

## 人类可选干预 / Optional Human Review

生成后可提示用户审阅。但如果用户没有介入，AI 只有在 `metadata/book_specific_translation_research.md` 和 `metadata/style_profile.md` 自评 `PASS` 时才可进入预翻译。

## 输出 / Output

- `metadata/book_specific_translation_research.md`
- `metadata/style_profile.md`
- `qa/textual/textual_uncertainty_log.md`

## 状态 / State

成功后：

- `status = BOOK_RESEARCH_DONE`
- `current_step = book_specific_translation_research_done`

# 04 本书专项翻译研究 / Book-Specific Translation Research

## 输入 / Input

- `source/source_text.txt`
- `source/toc.json`
- `metadata/book.yaml`
- `metadata/rights_checklist.md`
- `references/translation_research_universal.md`
- `references/quality_standard.md`
- `references/english_source_notes.md`

## 任务 / Tasks

生成 `metadata/book_specific_translation_research.md`，必须包含：

1. 本书一句话定位。
2. 作者身份、时代、写作目的、读者对象。
3. 本书翻译难点。
4. 不能照搬通用规则的地方。
5. 本书关键词分层：
   - 核心身份词
   - 象征词
   - 场景词
   - 技术词
   - 历史敏感词
6. 本书句法策略：
   - 长句
   - 动作句
   - 说明句
   - 修辞句
   - 口语/日记句
7. 本书意象策略：
   - 哪些词必须翻出画面。
   - 哪些词只能解释。
   - 哪些地方容易越界发挥。
   - 哪些地方容易省成提纲。
8. 预翻译样本选择计划。

同时生成 `metadata/style_profile.md` 初版，必须包含：

- 一句话定位。
- 作者与叙述身份。
- 读者对象。
- 叙述声音。
- 句法策略。
- 关键词和称谓。
- 风格红线。
- 预翻译重点。

## 人类可选干预 / Optional Human Review

生成后可提示用户审阅。但如果用户没有介入，AI 只有在 `metadata/book_specific_translation_research.md` 和 `metadata/style_profile.md` 自评 `PASS` 时才可进入预翻译。

## 输出 / Output

- `metadata/book_specific_translation_research.md`
- `metadata/style_profile.md`

## 状态 / State

成功后：

- `status = BOOK_RESEARCH_DONE`
- `current_step = book_specific_translation_research_done`

# Spanish-to-Simplified-Chinese MASTER PROMPT

你是在 public-domain-books-translation 仓库中执行西班牙语到简体中文 EPUB 制作的 Agent。

必须先读取：

1. 仓库根目录 `AGENTS.md`
2. `template/epub_pipeline/README.md`
3. `template/epub_pipeline/common/README.md`
4. `template/epub_pipeline/targets/zh-Hans/quality_framework/README.md`
5. `template/epub_pipeline/Spanish-to-Simplified-Chinese/AGENTS.md`
6. `template/epub_pipeline/Spanish-to-Simplified-Chinese/SKILL.md`
7. `template/epub_pipeline/Spanish-to-Simplified-Chinese/references/`
8. common 的 cover、book-info、assets、quality gate、random spotcheck、release policies

核心要求：

- 先核查西班牙语原文来源、版权/公版/授权状态、底本文字形态和现代参考材料使用边界；公开发布权利不明确且没有私人本地书源时停止。
- 所有具体书籍产物只能写入 `books/zh-Hans/{number}_{目标语言书名}_{目标语言作者名}/`。
- 批量翻译前必须完成 `metadata/spanish_source_profile.md`、`metadata/book_specific_translation_research.md`、`metadata/style_profile.md`、`glossary/terms.csv`。
- 分章翻译时，每章必须立即执行 08a 全章译后检查；发现问题的轮次只能 `FIXED_RECHECK_REQUIRED`，追加新一轮零问题 PASS 后才可继续。
- 第一版 EPUB 后必须执行分层随机抽检；发现任何问题必须归纳问题族并全书同类审计，不得只修样本。
- 发现可复用译文质量问题族时，按 `skills/translation-quality-defect-families/SKILL.md` 回填。
- 最终必须生成 `output/release/` 下 `release_state.json.latest_status = PASS` 的版本化 EPUB。

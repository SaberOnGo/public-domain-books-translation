# 流水线规范 / Pipeline Spec

## 1. 输入 / Inputs

- `TEMPLATE_ROOT`
- `PROJECT_ROOT`
- `SOURCE_URL`

## 2. 模板保护与写入范围 / Template Protection & Write Scope

- `TEMPLATE_ROOT` 是只读模板目录。
- AI 不得把具体书籍的原文、译文、QA、EPUB 输出写入模板原目录。
- 实际做书时，AI 必须先复制模板为独立书籍工程目录，例如 `books/{book_id_slug}/`。
- 复制完成后，后续 `PROJECT_ROOT` 指向独立书籍工程目录。
- AI 只能写入 `PROJECT_ROOT` 内文件。
- 例外：`books/package.json`、`books/package-lock.json` 和被 Git 忽略的 `books/node_modules/` 是所有书籍共享的构建工具目录，不属于任何单本书的原文、译文、QA 或 EPUB 输出。
- 如果检测到当前目录仍在 `template/epub_pipeline/common` 或某个 `template/epub_pipeline/{source-target}` 语言模板内，必须停止并先复制模板到书籍工程。

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
- `INDEPENDENT_REVIEW_FAILED`
- `INDEPENDENT_REVIEW_PASS`
- `REVISION_ROUTING_REQUIRED`
- `FINAL_OUTPUT_PASS`
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
- `metadata/rights_checklist.md`：版权/公版核查。
- `metadata/source_evidence.md`：原文来源证据。
- `metadata/book_specific_translation_research.md`：本书专项翻译研究。
- `metadata/style_profile.md`：文体画像。

### Research

- `references/translation_research_universal.md`：由目标语言模板或语言方向模板提供的翻译研究规则。
- `references/quality_standard.md`：由目标语言模板或语言方向模板提供的质量标准。
- `references/chapter_title_policy.md`：通用章节标题、目录短题名和副标题策略。
- `references/literary_refinement_policy.md`：通用文学精修、书籍目标和模板经验回填策略。
- `automation_contract.md`：自动化执行合约。

### Chapters

- `chapters/src/{NNN_slug}.md`：分章原文。
- `chapters/translated/{NNN_slug}.md`：分章译文草稿。
- `chapters/final/{NNN_slug}.md`：通过门禁后的终稿。

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

### Preproduction

- `preproduction/stage1/production_spec.md`：全书制作规格。
- `preproduction/stage2_sample/sample_chapter.xhtml`：样章 XHTML。
- `preproduction/stage2_sample/sample_book.epub`：样章 EPUB。
- `preproduction/stage2_sample/sample_review.md`：样章检查结果。

### Reviews

- `reviews/agent_a/review.md`：翻译与内容独立评审。
- `reviews/agent_b/review.md`：EPUB 工程与排版独立评审。
- `reviews/scorecards/final_quality_score.md`：最终质量评分表。
- `reviews/revision_route.md`：评审回退路由。

### Retrospective

- `retrospective/book_retrospective.md`：本书复盘。
- `retrospective/template_update_suggestions.md`：模板更新建议。

### Output

- `output/book.epub`：最终 EPUB。
- `output/epubcheck.log` 或 `output/epubcheck.json`：EPUB 校验结果。
- `output/publication_lint.json`：出版文本 lint 结果，检查编码污染、异常空格、旧纸书页码目录等问题。
- `output/final_manifest.md`：最终产物清单。

### Shared Tooling

- `books/package.json`：所有书籍共享的 Node.js 工具依赖声明。
- `books/package-lock.json`：共享工具依赖锁文件。
- `books/node_modules/`：共享工具安装目录，必须被 Git 忽略。
- 每本书的 `package.json` 只保留本书脚本，不得声明与共享工具重复的通用依赖。
- EPUBCheck 等脚本必须向上查找共享 `node_modules/`，不得硬编码 `PROJECT_ROOT/node_modules/`。

## 5. 出版文本硬检查 / Publication Text Lint

构建 EPUB 前必须运行出版文本 lint：

```powershell
node scripts/publication_lint.js --target={target-language} --write-report
```

通用硬检查：

- 不得出现编码污染、替换字符或明显 mojibake。
- 不得把旧纸书的页码目录、插图页码目录当正文放入 EPUB。
- 不得在普通正文中保留用于纸书对齐的连续空格。
- 不得让脚本依赖本机绝对路径；所有路径必须相对 `PROJECT_ROOT`。
- 不得把旧纸书目录式长标题链直接塞入 EPUB 导航；长标题必须按 `references/chapter_title_policy.md` 拆分为短目录题名、页面主标题和可选副标题。
- 不得把 AI 或译者概括出的章节说明当成读者可见标题。若源文某章只有编号、罗马数字或简单题名，EPUB 页面标题通常也只应使用对应编号或题名；解释性说明应放入 `title_note`、制作说明或 QA 记录。
- `source/source_text_raw.txt` 是来源证据，不应为了通过出版文本检查而改写。出版文本硬检查重点覆盖 `frontmatter/`、`chapters/final/`、`metadata/` 和生成 EPUB 内的 XHTML。

目标语言相关检查由 `template/epub_pipeline/targets/{target}/` 追加规则。例如简体中文会限制分号滥用、中文字符之间的异常空格、中文排版标点等。

## 6. 文件命名 / Naming

- 章节统一三位序号：`001_xxx.md`、`002_xxx.md`。
- `src`、`translated`、`final`、`qa` 必须同名对应。
- 不得让 AI 自创多套命名方案。

## 7. 新增硬门禁 / New Hard Gates

- 每章翻译后必须经过 `qa/chapter_controls/{NNN_slug}.control.md`。
- 未完成每章译后控制，不得进入后续审校。
- 全部翻译完成后不得直接构建 EPUB，必须先完成预制作阶段 1。
- 未通过样章制作检查，不得制作整本 EPUB。
- 未通过出版文本 lint，不得构建最终 EPUB。
- 未完成长章节标题的导航题名、页面标题和副标题设计，不得进入最终 EPUB 输出。
- 整本 EPUB 构建后必须执行精修复查或等效扫描，并在 `qa/refinement/` 下记录结果。
- 若发现来源不支持的读者可见标题、BOM、乱码、AI 输出残留、异常英文残留或 EPUB metadata 问题，不得进入最终交付。
- 如果已经发现系统性文学精修问题，必须在 `books/{book_id_slug}/goal/` 建立本书目标，并把可复用经验回填到 common、目标语言或语言方向模板。
- 整本 EPUB 制作后，必须派生 2 个独立 Agent 评审。
- 评审失败时必须通过 `reviews/revision_route.md` 回到对应前置阶段。
- 未完成复盘和经验沉淀，不得标记 `DONE`。

## 8. 完成定义 / Done Definition

必须同时满足：

- `metadata/rights_checklist.md` 明确可翻译。
- `qa/pretranslation/pretranslation_report.md` 结论为 `PASS`。
- 所有章节存在 `qa/chapter_controls/*.control.md` 且结论为 `PASS`。
- 所有章节存在 `qa/gates/*.gate.md` 且结论为 `PASS`。
- `preproduction/stage1/production_spec.md` 存在。
- `preproduction/stage2_sample/sample_review.md` 结论为 `PASS`。
- `output/publication_lint.json` 存在，且无硬错误。
- `qa/refinement/` 存在；若使用 `scripts/refinement_check.js`，出版范围内 BOM、乱码、中文连续空格和不当标点应为 0，或在 QA 中记录明确例外。
- `output/book.epub` 存在。
- EPUBCheck 无 fatal/error。
- `reviews/agent_a/review.md` 和 `reviews/agent_b/review.md` 均存在，且评分通过。
- `reviews/revision_route.md` 中无未关闭 P0/P1/P2 必修项。
- `retrospective/book_retrospective.md` 和 `retrospective/template_update_suggestions.md` 存在。
- 重大精修问题已有书籍专属目标或修复记录，可复用经验已回填到对应模板层。
- `state/pipeline_state.json.status == DONE`。

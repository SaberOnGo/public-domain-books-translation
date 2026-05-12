# 自动化执行合约 / Automation Contract

## AI 的职责

AI 必须自动决定：

- 如何先把模板复制成独立书籍工程目录。
- 下载哪个文本版本。
- 如何清洗和分章。
- 如何命名章节文件。
- 如何生成元数据、术语表、文体画像。
- 如何选择预翻译样本。
- 如何在失败时回溯到正确阶段。
- 如何构建并校验 EPUB。

## AI 不应询问用户

除非来源无法访问或版权状态无法判断，AI 不应询问：

- 文件名怎么起。
- 目录怎么组织。
- 章节怎么编号。
- QA 文件写哪里。
- EPUB 输出到哪里。

## 模板保护硬规则 / Template Protection

- `template/epub_pipeline/common` 和 `template/epub_pipeline/{source-target}` 语言方向模板永远视为只读模板。
- 任何具体书籍的数据不得写入模板目录。
- 若当前工作目录就是模板目录，AI 必须先创建并切换到独立工程目录。
- 推荐目录：`books/{pg_id_or_author_title_slug}/`。
- 只有复制后的 `PROJECT_ROOT` 可以写入原文、章节、QA、译文和 EPUB。

## 人类可选审阅

AI 可以在以下文件生成后提示用户审阅，但不能把流程设计成必须人工操作：

- `metadata/book_specific_translation_research.md`
- `qa/pretranslation/pretranslation_report.md`
- `glossary/terms.csv`
- `metadata/style_profile.md`

如果用户没有介入，AI 必须按 PASS/FAIL 规则自行继续或返工。

## 失败处理

失败时：

1. 写明失败阶段。
2. 写明失败文件。
3. 写明回溯目标。
4. 修改对应规则或试译。
5. 保留失败版本，不要覆盖失败教训。

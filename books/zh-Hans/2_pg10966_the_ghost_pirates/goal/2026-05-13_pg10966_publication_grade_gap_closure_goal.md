# /goal：出版级查漏补缺与精修闭环

## 目标

在既有 EPUB 完成版基础上，按 `template/epub_pipeline` 和本书 `books/zh-Hans/2_pg10966_the_ghost_pirates` 的要求补做出版级查漏补缺，确认标题工程、章节精修、术语/译注统一、长段落处理、航海专业名词语境准确性均有证据闭环。

## 必读依据

- `template/epub_pipeline/common/PIPELINE_SPEC.md`
- `template/epub_pipeline/common/references/literary_refinement_policy.md`
- `template/epub_pipeline/common/references/chapter_title_policy.md`
- `template/epub_pipeline/en-zh-Hans/references/english_to_chinese_literary_refinement.md`
- `books/zh-Hans/2_pg10966_the_ghost_pirates/AGENTS.md`
- `books/zh-Hans/2_pg10966_the_ghost_pirates/SKILL.md`
- `books/zh-Hans/2_pg10966_the_ghost_pirates/metadata/book_specific_translation_research.md`
- `books/zh-Hans/2_pg10966_the_ghost_pirates/metadata/chapter_title_map.yaml`
- `books/zh-Hans/2_pg10966_the_ghost_pirates/glossary/terms.csv`

## 执行范围

1. 标题工程：复核终稿 Markdown、EPUB nav/OPF/XHTML 与 `chapter_title_map.yaml` 是否一致；原书仅罗马数字章节不得出现自拟可见副标题。
2. 章节精修：抽查高风险章节首尾、高潮段落、附录呈现和生成后 XHTML，确认无副文本泄漏、AI 输出残留、乱码、异常空格。
3. 术语/译注统一：复核人名、船名、职务、航海器具、帆位、索具、值班术语；修复终稿与 QA 中发现的不一致。
4. 长段落处理：普通叙述段超过 500 字应拆段或记录明确例外；诗歌、号子、签名表等特殊格式可保留，但必须说明理由。
5. 重新构建与校验：修复后运行出版 lint、精修扫描、EPUBCheck，并更新 QA 记录和最终 manifest。

## 初始缺口

- `Jaskett` 在终稿和 QA 中存在“贾斯克特/贾斯克特”两种译法，需要统一。
- `glossary/terms.csv` 缺少后续出现的 `Quoin`、`Jaskett`、`Jacobs`、`Toppin` 等人物或职务条目。
- `log-reel` 已定为“测程绳盘”，终稿中仍有一处“测程绳盘”。
- 第十六章高潮段落超过 500 字，应按动作阶段拆分；第三章船歌长段落属于号子排版例外，需在 QA 中记录。
- 旧章节 QA 中有早期自拟副题记录，需用新的标题工程复查结果覆盖，避免误导后续 agent。

## 完成标准

- 终稿章节标题与 `chapter_title_map.yaml` 一致；EPUB 中无来源不支持的可见章节副题。
- 终稿中 `Jaskett` 译名统一为“贾斯克特”；术语表补齐后续关键人物和高风险航海术语。
- 普通叙述段不再出现超过 500 字的未处理长段；格式性长文本有 QA 例外说明。
- `qa/refinement/` 下新增本次查漏补缺报告，列明修复项、保留例外和验证结果。
- 出版 lint、精修扫描、EPUBCheck 重新通过，最终 EPUB 与 manifest 更新。

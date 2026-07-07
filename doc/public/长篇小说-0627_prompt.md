我要翻译的书：鲍斯威尔《约翰生传》
目标语言：中文
[重点专有名词(人名、地名、术语、罕见名词、音译后体验很差的名字等) 的翻译格式] 设置 = 3

请自动选择正确的翻译 prompt：
- 如已有对应语言方向模板，执行 doc/public/user_prompt/book_translation_existing_template.md。
- 如无对应语言方向模板，执行 doc/public/user_prompt/book_translation_new_template.md。

除非版权或来源无法确认，不要让我填写技术字段。请自动查找可靠公版来源，自动创建项目，完成翻译、审校、EPUB 构建、分层随机抽检和 release。
翻译执行时必须逐章执行“每章译后全量检查并修复”：每章都要对照整章原文和整章译文检查忠实度、
中文顺读、术语、标题/小标题、注释、图表文字接口、源语句法残留、过硬过直句、过度解释或加戏等问题；
发现问题后先修复，但该轮不能 PASS，必须追加新一轮整章复查，直到最新一轮零问题 PASS。
第一版 EPUB 生成后必须执行“分层随机抽检与问题族追杀”：抽检发现任何问题，不得只修被抽样本，
必须在当轮归纳为问题族，用 `rg`、术语表、标题表、抽样 manifest 和小上下文原文对照做全书同类审计，
修复确认命中，记录例外，再用新 seed 追加一轮。译文质量问题族必须使用 `skills/translation-quality-defect-families/SKILL.md` 做经验沉淀。
未声明是否启用 LifeBook Digest 时，请自动判断；长篇小说、专业书籍、哲学书在 EPUB 输出后生成 Digest，短篇小说、自然科学类和其他类型不生成。
如需生成 Digest，请在书籍工程根目录写入 `digest.config.json`（`enabled=true`、`merge_into_epub=true`），
并在仓库根目录运行：`python -m digest.lifebook_digest --book-root books/{target}/{number}_{目标语言书名}_{目标语言作者名}`。输出仍然是标准 EPUB。
特别注意: 翻译过程中积累的任何经验、教训、有用的积累、“18 世纪英语、传记、引语、典故、人物索引、注释”能力，等等都要必须要复盘沉淀进skill，模板、必要时增加新文档，
不要在已有文档里添加，按照职责、风格、模块可新建目录/文件。
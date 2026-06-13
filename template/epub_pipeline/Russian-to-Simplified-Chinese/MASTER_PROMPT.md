# 俄语到简体中文 EPUB 总控 Prompt / Russian to Simplified Chinese Master Prompt

你是在 `public-domain-books-translation` 仓库内工作的 EPUB 翻译出版 Agent。执行俄语到简体中文项目时，必须先读取仓库 `AGENTS.md`、`template/epub_pipeline/common/`、`template/epub_pipeline/targets/zh-Hans/` 和本 `Russian-to-Simplified-Chinese` 模板；不得把具体书籍原文、译文、QA 或 metadata 写入模板目录。

## 工作顺序

1. 自动确认公开项目的俄语公版或授权来源；权利不清楚时停止。
2. 使用 `books/scripts/create_book_project.py` 创建 `books/zh-Hans/{number}_{目标语言书名}_{目标语言作者名}/`。
3. 在书籍工程内记录 `metadata/source_evidence.md`、`metadata/rights_checklist.md`、`metadata/source_text_profile.md` 和 `qa/textual/source_textual_notes.md`。
4. 完成本书研究、文体画像、术语表、预翻译试译和小样本测试；未 PASS 不得批量翻译。
5. 逐章翻译。每章写入 `chapters/translated/` 后立即执行整章译后检查与修复；修复轮不能 PASS，必须追加新一轮零问题整章复查。
6. 生成 EPUB 后执行 EPUBCheck、publication lint、asset lint、cover check、reader-facing check、分层随机抽检、问题族全书追杀和版本化 release。
7. 若发现可复用俄语翻译问题族，先在书籍工程闭环，再回填到本模板或 `skills/translation-quality-defect-families/SKILL.md`。

## 俄语专项注意

- 以俄语底本为唯一翻译源；现代译本只能作为背景或疑难核验，不能转译。
- 先处理格关系、体貌、运动动词、反身/无人称结构、分词/副动词结构和称谓语气，再输出中文。
- 中文正文默认不夹俄文原词；只有术语争议、原词本身被讨论或省略会造成误解时，才允许按术语表策略呈现。
- 小说文本要保留叙述者距离、讽刺、心理暗流和对白口吻；不得把俄语抽象名词链直译成中文硬壳，也不得为顺滑添加原文没有的动机。

# 韩语/朝鲜语到简体中文译文质量标准 / Korean to Simplified Chinese Quality Standard

本文件是 `template/epub_pipeline/targets/zh-Hans/quality_framework/` 的简体中文目标语言规则在韩语/朝鲜语源文本场景下的应用摘要。更完整的中文目标语言质量规则见目标语言质量框架；韩语/朝鲜语源语言干扰问题见 `references/korean_source_notes.md`；题名策略见 `references/korean_title_strategy.md`。

## 核心标准

译文要像优秀中文译者写出来的书，而不是韩文/朝鲜文文本的中文影子。

必须同时满足：

- 忠实：事实、人物关系、视角、语气、叙述距离和暧昧程度不偏离原文。
- 可读：中文读者不被韩语/朝鲜语修饰链、省略和语序绊住。
- 有声调：叙述有节奏，关键句有力度，沉默和停顿也有功能。
- 有判断：汉字词、敬语、称谓、时代词、官能或心理描写都经过译者判断。
- 可验收：每章有控制、审校、门禁和抽检证据。

## 不合格模式

- 韩语/朝鲜语汉字词机械照搬，造成现代中文误读。
- 把韩语/朝鲜语省略关系译成中文断裂句，读者不知道谁在做什么。
- 把暧昧心理解释得过度明确。
- 把官能描写加重成色情化表达，或删弱成空泛心理说明。
- 为了“文雅”抹掉身体动作、羞耻、压迫、不适或病态心理。
- 为了“通顺”删掉原文重复、停顿、犹疑和视角限制。
- 译注太多，正文像研究笔记。
- 章节标题、目录或正文混入韩文/朝鲜文原题、读音、罗马字或长括注。
- 底本说明、韩国 Wikisource工作说明、OCR 注记或现代编者注混入作者正文。

## PASS 条件

- `metadata/source_evidence.md` 和 `metadata/rights_checklist.md` 已记录来源与版权。
- `metadata/korean_source_profile.md` 已记录底本文字形态。
- `qa/textual/korean_textual_notes.md` 已记录文本疑难或明确无疑难。
- `metadata/book_specific_translation_research.md` 已说明作者、时代、文体、题材边界和参考材料使用边界。
- `metadata/style_profile.md` 已建立中文文体画像。
- 预翻译试译为 `PASS`。
- 每章译后控制、忠实度审校、可读性/意象审校、术语审校和章节门禁均为 `PASS`。
- EPUB 构建、publication lint、asset manifest check、reader-facing policy check、随机抽检和 release gate 均通过。

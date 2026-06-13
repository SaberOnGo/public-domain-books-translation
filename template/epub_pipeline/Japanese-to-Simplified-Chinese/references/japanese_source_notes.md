# 日语源文本进入简体中文的专项说明 / Japanese Source To Simplified Chinese Notes

本文件只记录日语原文进入简体中文时容易出现的源语言干扰问题。更通用的简体中文译文质量规则见 `template/epub_pipeline/targets/zh-Hans/quality_framework/`。

This file records source-language issues specific to Japanese source text translated into Simplified Chinese. General Simplified Chinese target-language quality rules live under `template/epub_pipeline/targets/zh-Hans/quality_framework/`.

## 底本文字形态 / Source Text Form

- 必须记录来源文本是旧字体、现代字体、历史假名遣、现代假名遣、扫描 OCR、人工校订文本，还是混合形态。
- 不得把现代校订者说明、输入者注、青空文库工作说明、版权说明、底本说明或 OCR 修订说明误当作者正文。
- 振假名、旁点、旁注、割注、编者注、底本注应先分类记录，再决定是否进入译文、译注或 QA 证据。
- 若同一词存在旧字/新字、假名/汉字、异体字或多种读法，必须写入 `qa/textual/japanese_textual_notes.md`。

## 日语干扰 / Japanese Interference

- 日语省略主语、宾语和因果连接时，中文需要补出可读关系，但不得补成原文没有的新事实。
- 日语修饰链较长时，中文可拆分和重排；必须保留焦点、转折、递进、对照和心理迟疑。
- 敬语、谦让语、亲疏称谓、性别化口吻、时代语气不能只按字面翻译，应转成中文读者能感到的关系强度。
- 句末语气、未明说的心理动机和暧昧态度，不能被译成过度明确的中文判断。
- 日语汉字词不能因为字形相同就照搬；要检查现代中文语义是否变窄、变强、变弱或转义。
- 拟声拟态词应按场景转成中文动感、触感、节奏或心理色彩；不得一律删掉，也不得硬塞日语音译。
- 和歌、俳句、俗谚、佛教语、艺道语、江户/明治/大正时代词，应按本书策略处理：正文自然可读，必要时短注，不做百科式长注。

## 官能与心理描写边界 / Sensual And Psychological Boundary

- 官能、欲望、羞耻、支配、服从、病态心理、暴力或强制关系，必须作为原作文学结构的一部分处理。
- 不得把隐晦描写译得比原文更露骨；不得为了“文雅”删掉原文的身体性或压迫感。
- 不得添加现代道德评语、心理诊断或色情化词汇，除非原文确实有同等叙述力度。
- 若作品涉及年龄差、性别压迫、身体伤害或强制关系，必须在 `metadata/book_specific_translation_research.md` 中写明处理边界。

## 人名、题名与译注 / Names, Titles, And Notes

- 人名优先使用已有中文通行译名；没有通行译名时建立统一音译策略。
- 题名、章题、目录题名中只放中文题名；日文原题、读音、异名可放在书籍信息页、译注或术语表。
- 正文首次出现重要人名、地名、作品名或术语时，可按项目策略保留日文原文或读音，但不得让每个普通名词都带括注。
- 译注必须短，服务阅读，不得成为研究论文或制作日志。

## Boundary / 边界

中文节奏、标点、段落气息、中文排版和中文读者体验属于简体中文目标语言质量框架；本文件只补充日语源语言带来的问题。

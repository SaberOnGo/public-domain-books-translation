# 07 分章翻译

每次只翻译当前章节或当前段落组。翻译 prompt 保持瘦身：当前原文、必要上下文、文体画像 5-8 条、当前术语。正文只输出译文，不混入 QA、prompt、制作说明或分析。章节译文先写入 `chapters/translated/`，不得直接进 `chapters/final/`。

## 专家级译文与多义词回看 / Expert Quality and Polysemy Back-Check

翻译调用仍然只输出译文，不输出 QA 或流程记录；但译者必须按 `skills/expert-translation-quality/SKILL.md` 在内部建立观察清单。遇到多义词、习语、称谓、术语或需要后文判义的语法结构，先避免错误收窄；后文译出后，必须在 `08a` 回到前文位置复查并必要时修订。观察清单不得进入读者正文。

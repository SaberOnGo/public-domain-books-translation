# 学术与专业书简体中文 EPUB 控制模板 / Academic and Professional Chinese Readability Profile

## 定位 / Purpose

本目录不是单一语言方向模板，而是一个第三层控制 overlay。它服务于学术专著、论文型书籍和现代专业书，目标是在保持专业准确性的同时，让译文读得顺、有趣、不费劲。

It is not a language-pair template. It is an optional third-layer profile for academic and professional books translated into Simplified Chinese.

## 适用对象

- 政治学、经济学、社会科学、法律、管理学等学术专著。
- 计算机、机械、电子、生物、化学、医学等专业书。
- 含模型、证明、公式、统计结果、图表、表格、术语体系、引文和长论证链条的作品。
- 读者需要专业内容，但不应被不必要的翻译腔、长句和术语堆叠挡住。

## 核心原则 / Core Principles

- 通俗不等于降级。专业术语、变量、定义、公式、图表和限定条件必须保留。
- 专业不等于拗口。能用自然中文讲清的地方，不保留外文句法。
- 解释链条优先。定义、假设、推理、证据和结论之间要有清楚衔接。
- 表格和统计结果要“先告诉读者看什么”，再保留精确数字或原图证据。
- 公式和证明可以严谨，但应补足中文路标，例如“这里要证明的是……”“这个条件的作用是……”。
- 引文边界必须清楚，不能让读者分不清作者转述和被引文本。

## 复制顺序 / Overlay Order

```text
template/epub_pipeline/common
template/epub_pipeline/{language-pair-template}
template/epub_pipeline/profiles/academic-professional-zh-Hans
books/zh-Hans/{number}_{目标语言书名}_{目标语言作者名}/
```

私人自用项目在此之后再覆盖：

```text
template/epub_pipeline/modes/private_use
```

## 关键记录 / Key Records

- `metadata/academic_professional_style_profile.md`
- `references/academic_professional_readability_policy.md`
- `references/formula_rendering_policy.md`（来自 common；含公式、模型、统计表达式或方程组时必须读取）
- `qa/readability/{chapter}.academic_readability_audit.md`
- `qa/readability/academic_professional_polish_round_001.md`
- `reviews/scorecards/final_academic_professional_score.md`
- `reviews/random_spotcheck/round_XXX/`

## 与语言方向模板的关系

语言方向模板处理“从哪种源语言到中文”的问题，例如英语长句、日语敬体、古希腊术语或文言断句。

本 profile 处理“专业书如何读得懂”的问题，例如术语保真、论证路标、统计解释、表格导读、公式说明和学术长句拆分。

含公式、模型、统计表达式或方程组的项目，还必须按 `references/formula_rendering_policy.md` 建立全书公式清单，并优先使用 MathML 处理稳定可识别的显示公式。

如果二者冲突，先保证事实、术语、公式和图表正确，再用中文表达修复可读性。不得为了通顺而删掉专业内容，也不得为了专业感而保留不必要的拗口表达。

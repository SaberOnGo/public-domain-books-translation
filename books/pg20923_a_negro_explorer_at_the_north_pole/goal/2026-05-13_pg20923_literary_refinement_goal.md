# 《黑人北极探险家》精修目标 / Literary Refinement Goal

日期：2026-05-13

文件位置说明：本文件是《黑人北极探险家》这一具体书籍工程的精修目标，因此放在本书目录 `books/pg20923_a_negro_explorer_at_the_north_pole/goal/` 下。项目级、语言中立、语言方向专用的可复用规则，分别回填到 `template/epub_pipeline/common/`、`template/epub_pipeline/targets/zh-Hans/` 和 `template/epub_pipeline/en-zh-Hans/`。

## 目标

在现有可读 EPUB 的基础上，把《黑人北极探险家》推进到更接近正式出版的版本。重点不是重新生成一遍，而是按可复用标准做编辑级精修：

- 章节标题重构。
- 段落节奏与长句拆分。
- 错别字、术语、标点、异常排版复查。
- 专名、历史称谓、译注策略统一。
- 信、达、雅三层质量复核。
- EPUB 标题层级、目录、正文排版复核。

## 参考原则

- 严复“信达雅”可作为中文译文目标的传统框架，但本项目不能把“雅”理解为文言化或堆砌辞藻；本书的“雅”应是准确、清楚、节制、有现场感。
- Tytler 的翻译原则传统强调完整传达思想、保持风格方式、译文自然流畅；本项目转化为“事实不误、声调相当、中文自足”。
- ATA 关于翻译质量的现代描述强调准确、流畅、面向受众和目的；本项目转化为“目标读者能像读一本中文书一样阅读，同时不丢失源文本的历史质地”。
- EPUB 3.3 强调 package metadata、spine、navigation document 等结构；本项目转化为“目录、标题、页面标题、metadata 不只是工程字段，而是读者体验的一部分”。

参考来源：

- W3C EPUB 3.3: https://www.w3.org/TR/epub-33/
- American Translators Association, Summary of “Defining Translation Quality”: https://www.atanet.org/translation/summary-of-defining-translation-quality/
- Alexander Fraser Tytler, `Essay on the Principles of Translation`, Chapter I: https://en.wikisource.org/wiki/Essay_on_the_Principles_of_Translation_(Tytler)/Chapter_1

## 当前主要发现

### 1. 标题问题

原书不少章节标题确实包含多个 `--`，这是旧英文纸书目录式小题串联，不应逐个译成中文破折号。当前书稿中仍有高风险标题：

| 文件 | 当前标题 | 问题 |
| --- | --- | --- |
| `004_*` | 第一章 早年岁月：学生、船舱侍童、水手，以及皮里中尉的贴身仆役——初赴北极 | 主标题过长，副题应拆出 |
| `005_*` | 第二章 向北极点出发——其他探险者的模样——羔羊般的 | 标题被截断，且破折号过多 |
| `006_*` | 第三章 发现 Rudolph Franke——Whitney 登陆——交易和装煤——与 | 明显截断，必须重拟 |
| `008_*` | 第五章 制作皮里式雪橇——在北极之夜狩猎——容易激动的狗 | 纸书目录串，应拆成主标题+副标题 |
| `009_*` | 第六章 皮里计划——石雨——我的朋友爱斯基摩人 | 可改成冒号或副标题 |
| `011_*` | 第八章 哥伦比亚营地——文学冰屋——北极壮美的荒凉 | 可保留意象，但不宜塞入同一主标题 |
| `012_*` | 第九章 准备向北极点冲刺——指挥官抵达 | 可接受，但仍建议主副标题拆分 |

### 标题目标方案

为本书建立 `metadata/chapter_title_map.yaml`，至少包含：

- `source_full`
- `nav_title`
- `display_title`
- `subtitle`
- `title_note`

示例：

```yaml
chapter_titles:
  "005_chapter_ii_off_for_the_pole_how_the_other_explorers_looked_the_lamb_like.md":
    source_full: "CHAPTER II OFF FOR THE POLE--HOW THE OTHER EXPLORERS LOOKED--THE LAMB-LIKE ESQUIMOS--ARRIVAL AT ETAH"
    nav_title: "第二章 向北极点出发"
    display_title: "第二章 向北极点出发"
    subtitle: "探险者群像、爱斯基摩人，以及抵达伊塔"
```

构建脚本后续应支持：

- `nav.xhtml` 使用 `nav_title`。
- 章节页 `<h1>` 使用 `display_title`。
- 副标题用 `<p class="chapter-subtitle">` 或 `<h2 class="chapter-subtitle">`，字号小于主标题。

## 2. 段落和句子精修

当前 EPUB 已消除硬格式错误，但仍有编辑级问题：

- 多个段落超过 300 字，最长普通叙述段超过 500 字，应逐章判断是否拆段。
- 有些句子忠实但偏“说明”，现场动作和叙述呼吸还可以加强。
- 陌生人名、陌生地名不强制汉译，如 `Rudolph Franke`、`Whitney`、`Professor Marvin`、`Grant Land` 等可保留英文；若选择汉译，首次出现处必须保留英文原名，后文再统一使用既定形式。
- 纪实段落中“工作、事情、开始、进行、很”等泛词需要逐章抽查，能具体化时应具体化。
- 历史称谓 `Esquimo` 当前译作“爱斯基摩人”，需要统一译注说明，不应在正文中忽然改成“因纽特人”。

## 3. 标点与排版

已完成：

- 分号清零。
- 中文连续空格清零。
- mojibake 清零。
- 旧纸书页码目录清理。
- EPUBCheck 0 fatal / 0 error / 0 warning。

仍需改进：

- 章节标题和副标题层级。
- 目录短题名。
- 长段落拆分后重新构建 EPUB。
- 附录名单是否保留为 `<pre>`，还是改成列表或表格。
- 书中外文船名、人名、拉丁学名的斜体/括注规则。

## 4. 信达雅复核标准

逐章复核时按以下顺序，不可只看中文顺不顺：

1. 信：事实、人名、地名、时间、路线、动作、因果是否与原文一致。
2. 达：中文句子是否自然，长句是否拆分得当，段落推进是否顺。
3. 雅：是否有本书应有的朴素、坚韧、现场感，而不是泛泛说明文或过度文学化。
4. 史：历史称谓和时代偏见是否如实保留，并用译注帮助现代读者理解。
5. 版：标题、目录、段落、注释、附录是否适合 EPUB 阅读。

## 执行阶段

### Phase 1：标题工程

- 新建 `metadata/chapter_title_map.yaml`。
- 修订 26 个章节标题。
- 修改 `scripts/build_epub.js` 支持 `nav_title/display_title/subtitle`。
- 重新生成 EPUB 并检查手机窄屏标题。

### Phase 2：逐章文学精修

优先顺序：

1. 第 2-6 章：标题截断、早期译稿痕迹、长段落密集。
2. 第 8、11、18、21、23、25 章：最长段落超过 380 字，需要精修和拆段判断。
3. 附录：名单、术语、历史称谓和译注策略。

每章输出：

- `qa/refinement/{chapter}.refinement.md`
- 修改后的 `chapters/final/{chapter}.md`
- 术语或模板更新建议。

### Phase 3：术语和译注

- 新建或更新专名表。
- 固定船名、地名、人名、爱斯基摩语词、极地术语。
- 明确首次出现译注策略：陌生人名、陌生地名可保留英文；若汉译，首次出现必须括注英文原名。

### Phase 4：出版复核

- 运行 `npm run lint:publication -- --strict-spaces`。
- 运行 `npm run build:epub`。
- 运行 `npm run check:epub`。
- 抽取 EPUB XHTML 检查标题、目录、长段落、附录。

## 模板回填要求

本次分析已回填以下模板规则：

- `template/epub_pipeline/common/references/literary_refinement_policy.md`
- `template/epub_pipeline/common/references/chapter_title_policy.md`
- `template/epub_pipeline/en-zh-Hans/references/english_to_chinese_literary_refinement.md`
- `template/epub_pipeline/targets/zh-Hans/quality_framework/references/title_punctuation_and_heading_style.md`
- `template/epub_pipeline/en-zh-Hans/references/english_chapter_title_strategy.md`

后续每完成一章精修，如果发现可复用问题，必须继续回填模板或目标语言质量框架。一次性修书但不沉淀规则，视为未完成。

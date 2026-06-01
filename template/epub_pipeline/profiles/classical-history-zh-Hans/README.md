# 古代历史简体中文 EPUB 控制模板 / Classical History EPUB Control Profile

## 定位 / Purpose

本目录不是单一语言方向模板，而是一个第三层控制 overlay。它服务于古代历史叙事、编年、列传、外交、战争、礼制、人物关系密集文本。

It is not a source-target language-pair template. It is an optional third-layer production-control profile for ancient historical works translated into Simplified Chinese.

## 适用对象

- 《战国策》《左传》《国语》《史记》列传等。
- 春秋战国、秦汉或其他古代政治历史文本。
- 人物、国名、地名、官名、爵位、宗族、年代、战争、外交、礼制密集文本。
- 需要高密度但受控注释的文本。

## 与 `lzh-zh-Hans` 的关系

`lzh-zh-Hans` 负责文言文到现代中文的语言问题：底本、断句、古今词义、原文-今译对照、注释总策略。

本 profile 负责历史叙事控制：人物是谁、属于哪国、处于什么时代、事件前后关系、官爵制度、地理变迁、战争外交和读者必要背景。

## 复制顺序 / Overlay Order

```text
template/epub_pipeline/common
template/epub_pipeline/lzh-zh-Hans
template/epub_pipeline/profiles/classical-history-zh-Hans
books/zh-Hans/{number}_{目标语言书名}_{目标语言作者名}/
```

## 核心原则 / Core Principles

- 历史关系是硬门禁。人物、国家、年代、官制、地理和事件因果翻错，不是风格问题。
- 注释可以多，但必须有读者功能。不注会误解才进入读者版；长背景、人物表和年表应放到附录或前置说明。
- 人物、地名、国名、官名、爵位、族属和事件必须进入锁定表。
- 每章翻译前必须有章节历史上下文；每章进入终稿前必须有历史审计。
- 随机抽检必须把注释、人物关系、国家关系、时间线和制度背景作为高风险点。

## 关键记录 / Key Records

- `metadata/historical_context.md`
- `glossary/historical_terms.csv`
- `glossary/people_places.csv`
- `qa/historical/event_timeline.md`
- `qa/historical/state_relations_matrix.csv`
- `qa/historical/{chapter}.historical_audit.md`
- `reviews/scorecards/final_history_score.md`

## 战国策试译策略 / Zhan Guo Ce Trial Strategy

《战国策》正式翻译前，必须先做小范围试译，用来验证：

1. 原文-今译对照正文是否适合读者阅读。
2. 注释密度是否足够又不压迫。
3. 人物、国家、外交关系和游说策略是否能被模板管住。
4. 试译复盘是否产生需要回填的模板规则。

试译复盘完成并回填模板前，不得开始《战国策》批量翻译。

## 随机抽检同类问题全书审计 / Book-Wide Similar-Issue Audit

随机抽检一旦发现任何需要修复或可能系统性复现的问题，包括但不限于 P0/P1/P2、单项 <70、读者不可理解、事实/术语/图表/公式/注释错误，或本模板硬门禁失败，主执行 AI 不得只修被抽中的样本，也不得等到第二轮才全书检查。必须先把发现归纳为问题族，再对整本读者可见书稿执行全书同类问题审计，覆盖 `chapters/final/`、frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML；修复所有确认命中，记录合理例外，并在该轮 `fix_log.md` 与 `closure_check.md` 中关闭该问题族后，才能使用新 seed 复抽。

If a random sample exposes any issue that needs correction or may recur systemically, treat it as a possible systemic defect family immediately in the current round. Audit the whole reader-facing book for similar cases, fix all confirmed matches, document justified exceptions, and close the family in the same round before a new-seed resample.

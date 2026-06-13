# 梵语诗歌翻译 Profile / Sanskrit Poetry Translation Profile

本文件适用于梵语诗歌、抒情诗、长短篇叙事诗、戏剧中的诗节，以及以诗体承载宗教或哲学内容的作品。它是 `Sanskrit-to-Simplified-Chinese` 的体裁补充，不替代 `targets/zh-Hans` 的中文质量框架，也不替代具体书籍的 `metadata/source_text_profile.md`。

## 必须记录 / Required Records

具体书籍进入批量翻译前，必须在 `metadata/sanskrit_poetry_profile.md` 或 `metadata/source_text_profile.md` 中记录：

- 体裁：抒情诗、叙事诗、戏剧诗节、宗教诗、哲理诗或混合体。
- 格律与分段：如 `mandakranta`、`sloka`、`anustubh`、`vasantatilaka` 等；若不可靠，写明未知。
- 源文单位：按诗节、半诗节、句群还是段落翻译；不得把 OCR 行当作自然章段。
- 复合词策略：长复合词先解析语义关系，再转成自然中文；不得堆成硬名词链。
- 意象链：云、季风、山川、城市、花木、神话人物、身体感官、颜色和声音等重复意象必须建表。
- 译注策略：只解释会造成误读的神话、地理、节令、格律、双关或文本疑难；不写百科式长注。
- 中文体裁策略：散文化诗行、节奏化散文、短行诗或其他方式；说明为何适合本书。

## 翻译原则 / Translation Principles

- 忠实度优先于押韵。不得为了韵脚、对仗或古雅语气改写事实、方向、关系或情感强度。
- 中文必须有诗性，但诗性来自源文意象和节奏转换，不来自凭空添加的花饰。
- 梵语长复合词常同时包含形容、动作、空间、修辞和文化信息。翻译时可拆成两个或多个中文分句，但必须保留核心限定关系。
- 地名和路径在诗歌中经常是叙事结构。地名可以加短注或章末路线说明，但正文不要每次括注原名。
- 神名、仙人、夜叉、乾闼婆、阿湿罗摩等文化负载词应先用稳定中文译名；梵语原词和转写放入译注或术语表。
- 源文故意含混或双关时，译文应保留含混，或用正文加短注说明双关；不得默默选一个义项后让另一层消失。

## 每章译后加严项 / Chapter Control Additions

诗歌章节的 `qa/chapter_controls/{chapter}.control.md` 除通用字段外，还必须记录：

```text
sanskrit_poetry_profile_used: true
meter_or_poetic_unit_checked: "PASS"
compound_resolution_review: "PASS"
imagery_chain_review: "PASS"
myth_geography_note_review: "PASS"
unsupported_poetic_addition_count: 0
```

如任一项发现问题，当前轮只能记为 `FIXED_RECHECK_REQUIRED`；修复后必须追加新一轮整章复查。

## 常见问题族 / Defect Families

- 复合词硬壳：把梵语长复合词译成中文名词堆叠，读者无法看见动作、空间和修饰关系。
- 诗性加戏：为了好看添加原文没有的花、风声、心理判断、悲喜评价或因果。
- 地理断链：路线诗、信使诗或巡游诗中漏掉方位、地名、先后顺序或景物转换。
- 神话误降格：把神名、族类、修行地、圣河、山岳等文化节点译成普通景物，削弱诗歌结构。
- 译注泛滥：每个陌生词都写长注，破坏诗歌阅读。

发现这些问题族时，按 `skills/translation-quality-defect-families/SKILL.md` 做低 token 同类审计、全书修复、复查和可复用经验回填。

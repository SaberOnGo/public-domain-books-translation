# 鲍斯威尔第88单元：饮酒年表、古典引文、剧场术语与期刊出版接口

## 可复用问题族

传记脚注中的长年表和出版史说明，常把日期、酒类、缩写文献、古典引文和舞台行话连在一起。译文若只逐句准确，容易留下机械年表、错误制度词或无功能英文；若过度解释，又会让脚注失去鲍斯威尔式紧凑。

## 发现方式

- 章节控制中扫描 `_post_`、`_ib_`、`_id_`、`_Pr.`、`_Gent` 等源文排版残留。
- 对照长注中的酒类、日期和引文，检查 `Bishop`、`water-drinker`、`inebriating sustenance`、`toast`、`bumpers` 是否功能化译出。
- 对照原文特意标注“that is the term”的行话，如 `Bear-garden bruisers`，确认中文可读且保留术语接口。
- 检查霍金斯、凯夫、假发误属等校勘句，避免把 `accent` 误作“口音”或把修正对象弄错。

## 风险

- 饮酒史时间线若中文句法太散，会让读者丢失戒酒、复饮、再戒之间的阶段关系。
- `free use of wine` 直译为“自由使用葡萄酒”或“放开使用葡萄酒”会形成现代管理语腔。
- `Bear-garden bruisers` 若只译义，失去“这就是当时术语”的证据；若只留英文，则普通读者无法理解。
- `asterisk` / `dagger`、期刊扉页署名、卷页号若处理不清，会影响后续真伪标记系统。

## 修复模式

- 长年表按时间顺序保留短句链，但把阶段判断句译清楚，例如“大体戒酒”“不久又重新喝了”。
- 酒类和饮酒行为用中文功能词：`free use of wine` 译为“大量饮用葡萄酒”，`two bumpers` 译为“两大杯”，`inebriating sustenance` 译为“使人醉的滋养品”。
- 当原文说明术语形态重要时，采用“中文释义（原文作 source term）”接口，例如“‘熊园打手’（原文作 Bear-garden bruisers，这就是当时的说法）”。
- 校勘性纠误句要先判定指代对象，再译；`bushy-wigged Cave` 的错误在于假发归属，译文应明确“被描写的假发是约翰生的，不是凯夫的”。

## 低 token 审计

```powershell
rg -n "_post_|_ib_|_id_|_Pr\\.|_Gent|free use|water-drinker|inebriating sustenance|Bear-garden|bruisers|bushy-wigged|quickset hedge|asterisk|dagger" chapters/final chapters/translated
```

分类时区分合理保留的专名/书名/术语接口，与无功能源文残留。凡修复后又改动正文，当前复查轮不得 PASS，必须追加新一轮整章复查。

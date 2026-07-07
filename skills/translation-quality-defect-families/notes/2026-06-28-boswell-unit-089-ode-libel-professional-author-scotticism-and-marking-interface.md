# 鲍斯威尔第89单元：颂歌、诽谤、职业作者、苏格兰式英语与标记接口

## 可复用问题族

十八世纪传记脚注中，诗歌翻译、法语/拉丁短语、诽谤法语境、职业作者自我陈情、苏格兰式英语讥讽和真伪标记常在同一单元出现。译文需要同时保留文学声音、证据接口和出版史功能。

## 发现方式

- 扫描 `_post_`、`_ante_`、`_ib_`、`_Gent` 等源文排版残留。
- 检查外语接口：`l'ilustre Lockman`、`For anything I see, foreigners are fools`、`Ad Urbanum`。
- 对照卷篇行号和标记系统：`ii. l. 71`、`asterisk`、`dagger`。
- 检查历史计数/付酬词，如 `long hundred` 是否读者可理解。

## 风险

- 诗歌若只逐字转写，会失去颂歌语气；若过度润饰，又会越过原文的平庸译诗属性。
- 诽谤与出版自由语境若误译，会改变十八世纪新闻/法律背景。
- `ii. l. 71` 这类行号接口误读，会造成引用定位错误。
- `long hundred` 若直译为“长百行”，读者不知其为超出普通一百的计数/付酬暗账。

## 修复模式

- 对引用诗保留诗行分行和基本修辞，但不把平庸原诗翻成过度华丽的中文诗。
- 外语短句先给中文功能义，再保留原文接口；书名/颂歌题名按“译名（原文）”处理。
- 卷篇行号译为“第几卷第几篇，第几行”，避免把 `l.` 误读成“第1行”。
- `long hundred` 译为“按‘长百’来交足行数”，必要时用引号提示这是历史计数习惯。

## 低 token 审计

```powershell
rg -n "_post_|_ante_|_ib_|_Gent|l'ilustre|For anything I see|Ad Urbanum|ii\\. l\\.|long hundred|asterisk|dagger|Scotch|English" chapters/final chapters/translated
```

若确认修复任何引用定位、外语接口或历史术语，该轮不能 PASS，必须追加整章复查。

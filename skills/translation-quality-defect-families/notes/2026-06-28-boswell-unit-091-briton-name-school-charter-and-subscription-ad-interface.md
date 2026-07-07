# 鲍斯威尔第91单元：不列颠称谓、学校章程与订阅广告接口

## 可复用问题族

十八世纪传记脚注常把诗歌地名、国家称谓、学校慈善基金章程、拉丁章程句和出版订阅广告放在同一单元。若只求中文顺读，容易漏掉诗句中的地名接口；若只保留原形，广告条款又会像未翻译的史料。

## 发现方式

- 扫描诗句地名和国家称谓：`Briton`、`Hibernia`、`Strand`、`Little Britain`。
- 检查学校章程关键词：`sixty pounds`、`Master of Arts`、`Greek and Latin tongues`、`ne ullius praeceptorum...`。
- 检查订阅广告金额和书籍形式：`18_s_`、`half-a-guinea`、`Two-pence`、`quarto`、`large paper`。
- 对照 `far/air/vain/man/despair/bar` 这类韵脚示例，确认保留源形是为了说明押韵问题。

## 风险

- `Hibernia`、`Strand` 等诗句地名若只译中文，不符合重点专名策略，且削弱诗句地理文化接口。
- 慈善学校章程若压缩过度，会丢失薪金、学位、大学背景和董事提名机制。
- 订阅广告中的印张、散页、半基尼、每少一印张减二便士等条款若误译，会影响出版史事实。
- 拉丁章程句若无中文释义，读者无法理解它是阿普尔比学校归属考证的关键证据。

## 修复模式

- 诗句地名首次出现用“译名（原文）”，如“希伯尼亚（Hibernia）”“斯特兰德街（Strand）”。
- 韵脚示例保留原文词形，因为讨论的是英语押韵缺陷；不要硬译成中文词。
- 章程条文先译制度功能，再保留必要拉丁原句并给中文释义。
- 订阅广告按条款逐项译出，保留印张、四开本、散页、大纸本和金额关系。

## 低 token 审计

```powershell
rg -n "Hibernia|Strand|Briton|Little Britain|ne ullius|praeceptorum|18_s_|half-a-guinea|Two-pence|quarto|large paper|far|air|vain|despair" chapters/final chapters/translated
```

若修复专名接口、章程释义或广告金额，该轮不能 PASS，必须追加整章复查。

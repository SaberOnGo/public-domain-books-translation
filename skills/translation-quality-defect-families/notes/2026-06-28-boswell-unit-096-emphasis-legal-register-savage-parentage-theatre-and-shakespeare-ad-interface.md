# 鲍斯威尔第96单元：重音、法律登记、萨维奇身世、戏剧角色与莎士比亚广告接口

## 可复用问题族

传记脚注若同时处理英文重音、十诫措辞、法律登记、私生子争议、戏剧角色和书目广告，译文不能只求中文顺句。源文形式本身常是证据，必须在不破坏中文阅读的前提下保留接口。

## 发现方式

- 扫描英文重音与源词：`daggers`、`use none`、`shalt`、`not`、`false witness`。
- 扫描法律登记和证人姓名：`Brook Street`、`Fox Court`、`Mr. Burbridge`、`Mary Pegler`、`Mrs. Pheasant`、`Mrs. Lee`、`St. Andrew's, Holborn`。
- 扫描戏剧和广告接口：`Careless Husband`、`Sir Charles`、`Lady Easy`、`Edging`、`Miscellaneous Observations`、`Proposals`、`Shakespear`。
- 回看称谓：`the Queen` 在乔治二世宫廷语境中常应译为“王后”，不宜机械译为“女王”。

## 风险

- 英文重音讨论若只译意，会丢失论点；必须保留原句和强调位置。
- 法律登记人名、地名若缺少源名，读者无法追索证据链；但普通解释词仍应中文化。
- 戏剧角色名和广告题名若过短，会让后文关于版本、提案和出版时间的辨析失去文本锚点。
- 王室称谓误判会改变史实关系。

## 修复模式

- 对证据性英文行保留源文，再用中文说明其功能；不要强行把重音差异转成纯中文。
- 法律登记首次出现的人名、地名用“中文译名（source）”，后文用中文。
- 广告题名按术语表给完整接口；后文可用短称，如《麦克白杂评》。
- 对 `the Queen`、`Viscount`、`Chaplain` 等身份词做历史语境判断，必要时译为“王后”“子爵”“随行牧师”。

## 低 token 审计

```powershell
rg -n "daggers|false witness|Brook Street|Fox Court|Mr\\. Burbridge|Mary Pegler|Mrs\\. Pheasant|Mrs\\. Lee|St\\. Andrew's, Holborn|Careless Husband|Sir Charles|Lady Easy|Edging|Miscellaneous Observations|Proposals|Shakespear|向女王求情|吉伯|汉默的《莎士比亚》" chapters/src chapters/translated chapters/final glossary
```

若修复了重音接口、法律登记接口、称谓误判或广告题名接口，该轮不能 PASS，必须追加整章复查；最新一轮无新问题时才可关闭。

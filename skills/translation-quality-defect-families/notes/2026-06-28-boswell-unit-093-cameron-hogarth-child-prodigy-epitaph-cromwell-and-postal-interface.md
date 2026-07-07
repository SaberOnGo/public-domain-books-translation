# 鲍斯威尔第93单元：卡梅伦案、霍加斯评价、神童、墓志、克伦威尔改写与邮政接口

## 可复用问题族

传记脚注连续处理政治案件、文学归属、墓志文本、议会辩论改写和制度史时，专名接口和说话层级很容易错乱。尤其是编者续注开头、作品名、比较对象、拉丁题名和制度名，需要保留来源证据而不破坏中文阅读。

## 发现方式

- 扫描未清理或需接口的原名：`Redgauntlet`、`Titian`、`Hudson`、`J. S. Mill`、`Charles of Sweden`、`Irene`。
- 检查明显混写残留，如 `洛克hart`。
- 检查词典/拉丁题名接口：`Anti-Artemonius`、`sive`、`consort`。
- 检查制度词：`penny-post`、`Royal Society`、`Society for the encouragement of learning`。

## 风险

- 人名或书名若只音译中文，读者难以辨认跨文本索引；若混入半英文拼写，会直接成为成稿缺陷。
- 墓志、演说改写和原文对照若层级不清，会让读者分不清“原文”“《绅士杂志》改写”和编者评论。
- `consort` 作为词典定义对象，不应只译义而丢失词形。
- 便士邮政、鼓励学问学会等制度名若误并为皇家学会，会改写史实。

## 修复模式

- 作品名/重要人名首次自然出现用“译名（原文）”，后文用译名。
- 明显半英文残留必须修净，如“洛克hart”改为“洛克哈特”。
- 词典定义对象保留源词，如 `consort`，并在中文中说明其定义。
- 对照段落用引号和引导语分清改写文本与原文文本。

## 低 token 审计

```powershell
rg -n "Redgauntlet|Titian|Hudson|J\\. S\\. Mill|Charles of Sweden|Irene|洛克hart|Anti-Artemonius|sive|consort|penny-post|Royal Society|Society for the encouragement of learning" chapters/final chapters/translated
```

若修复专名接口、混写残留或制度名，该轮不能 PASS，必须追加整章复查。

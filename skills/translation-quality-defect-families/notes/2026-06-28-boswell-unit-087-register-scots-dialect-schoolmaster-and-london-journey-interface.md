# 鲍斯威尔第87单元：登记簿、方言、教育制度与伦敦初旅接口

## 可复用问题族

十八世纪传记脚注常把事实校勘、旧登记簿、方言讥语、货币数量和制度头衔压缩在同一单元里。若只追求中文顺读，容易把证据性拼写洗掉；若只保留原形，又会让正文像资料摘录。

## 发现方式

- 章节译后控制中扫描旧拼写和方言触发词：`Mar'd`、`Sam'll`、`Eliz'th`、`Burmingham`、`a dominie`、`schule`、`acaadamy`。
- 对照专名/术语接口检查 `dulcinea`、`Gelidus`、`I doubt not`、`Bishop of Killaloe`、`Little Britain`。
- 用中文独立阅读检查历史制度词是否误导，例如 `Free School` 和 `Lucasian Professor`。

## 风险

- 登记簿旧拼写被完全现代化，会丢失来源证据和校勘价值。
- 苏格兰方言若只译义，会抹平阶层讥笑和口音功能；若只留原文，中文读者无法理解。
- `Free School` 直译为“自由学校”、`Lucasian Professor` 直译为“卢卡斯数学教授”，会造成制度误读。
- 货币、旅行习语和书商职业建议若裸留源语，会破坏中文叙事；若过度解释，又会把脚注变成译者讲义。

## 修复模式

- 登记簿先给中文释义，再紧跟原登记关键旧拼写，明确它是证据接口。
- 方言讥语先译出意思和语气，再保留原文方言句，避免读者失去声音证据。
- 制度和讲席名优先用中文可理解的历史功能词，如“免费学校”“卢卡斯讲席数学教授”。
- 校勘短语如 `I doubt not` 必须配中文释义；拉丁名或外语称号以“译名（原文）”处理。
- 普通器物和职业建议直接入中文，如“搬运工肩垫”，不在正文为普通名词硬加源语括注。

## 低 token 审计

先在当前章和全书终稿中扫描：

```powershell
rg -n "Mar'd|Sam'll|Eliz'th|Burmingham|a dominie|schule|acaadamy|I doubt not|Gelidus|dulcinea|Free School|Lucasian|rode and tied|porter's knot" chapters/final chapters/translated
```

随后按类别判断：登记簿/方言/校勘原形是合理保留；制度词和普通名词若裸留源语或直译误导，应改为中文功能词。

## 复查

修复后重新跑整章注号、裸源语、异常空格和中文独立阅读检查。凡在复查中又修了制度词或接口词，该轮不能 PASS，必须追加新一轮整章复查。

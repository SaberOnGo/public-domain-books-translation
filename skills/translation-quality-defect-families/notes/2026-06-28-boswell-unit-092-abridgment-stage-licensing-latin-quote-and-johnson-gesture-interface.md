# 鲍斯威尔第92单元：删节版权、戏剧许可、拉丁引文与约翰生动作描写接口

## 可复用问题族

传记脚注中若同时出现出版版权、戏剧审查、古典引文和身体/心理描写，译文容易在“解释清楚”和“保留证据”之间失衡。外文原句、编者 `sic`、怪异动作描写和法律论证都需要读者接口。

## 发现方式

- 扫描残留和接口词：`Du Halde`、`Ad Elisam`、`Urbanus`、`Sic fatus`、`Marmor Norfolciense`、`surely`、`sic`。
- 检查版权/删节论证：`abridgment`、`copy-right`、`proprietors`、`acquisition of knowledge`。
- 检查动作描写：`convulsions`、`reverie`、`dancing the devil's jig`、`driveling effort`。
- 检查政治/司法评价：`Jacobite`、`Dr. Archibald Cameron`、`rigour`、`Prince`。

## 风险

- 拉丁原句若被只译不留，会丢失古典引文接口；但只留拉丁又会挡住读者。
- `surely`、`sic` 一类编辑性词若裸留，会造成未清理英文；若删除 `sic`，又丢失原文语法异常证据。
- 约翰生怪异动作描写若直译过硬，容易滑向滑稽或病理化过度。
- 删节版权论证若用现代版权话语替换，会改变约翰生作为凯夫辩护人的语境。

## 修复模式

- 古典引文采用“原文 + 中文释义/既有译文”双层接口。
- 编者 `sic` 用中文说明“原文如此”，不要裸留 `sic`。
- 意外残留英文如 `surely` 必须清除为自然中文。
- 身体动作描写既保留当时观察者的尖刻口吻，又避免中文自造夸张；必要时按原文的怪异隐喻重构。
- 删节论证保留“合法/正当/知识获得/所有者损失”的逻辑链，不擅自改成现代版权结论。

## 低 token 审计

```powershell
rg -n "Du Halde|Ad Elisam|Urbanus|Sic fatus|telumque|Marmor Norfolciense|surely|sic|convulsions|reverie|dancing the devil|driveling|copy-right|abridgment|Dr\\. Archibald Cameron" chapters/final chapters/translated
```

若修复外文接口、编辑性标记、动作描写或版权论证，该轮不能 PASS，必须追加整章复查。

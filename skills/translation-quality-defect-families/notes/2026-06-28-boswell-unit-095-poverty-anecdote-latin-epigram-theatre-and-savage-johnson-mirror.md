# 鲍斯威尔第95单元：贫困轶事、拉丁题诗、戏院地位与萨维奇-约翰生镜像

## 可复用问题族

十八世纪传记把私人贫困轶事、寓言典故、拉丁题诗、收据/书名页证据、戏院社会地位和长篇人物镜像比较放在同一单元时，译文容易同时出现两种风险：新/低频专名接口不足，以及源语抽象句法硬壳残留。

## 发现方式

- 扫描未接口专名：`Richard Stow`、`Apsley`、`Walter Harte`、`Life of Gustavus Adolphus`、`Dr. Maxwell's Collectanea`、`Northcote`、`The Bastard`、`Mrs. Bret`、`P. CUNNINGHAM`、`Mr. Wilks`、`Giffard`。
- 扫描需要保留文本证据的源形：`Ad Ricardum Savage`、`SAM. I.`、`MDCCXLIV`、`mint of ecstasy`。
- 目标语独立朗读长引文，找“反面天平”“对每个对象都在场”“向司法敞开受罚之门”等源语句法壳。
- 对贫困和戏院社会地位词做上下文回看，避免把 `sordid comforts`、`condition`、`to Justice open laid` 译成硬直抽象词。

## 风险

- 低频人名、地名、作品名若缺少源名接口，后续读者难以追索文献来源；但普通名词若滥加源语括注，又会打断中文传记阅读。
- 拉丁题诗、收据、罗马纪年和短语引证是证据，不只是内容；只译义不保留源形，会破坏编者注释的文献功能。
- 萨维奇与约翰生的镜像比较语段若保留英文抽象结构，会读成资料卡片，而不是一段有节奏的传记评论。
- 戏院/巡回演员语境中的法律和社会地位词若过直，会让历史社会评价失去语气和讽刺力度。

## 修复模式

- 对新/低频专名使用设置 3：中文译名后加源名，如“沃尔特·哈特先生（Mr. Walter Harte）”；已稳定高频名后文只用中文。
- 证据性源形保留并补读者接口：`MDCCXLIV（1744）`、`狂喜的铸坊（mint of ecstasy）`。
- 英文抽象句先转为中文动作和关系：`his attention never deserted him` 可译为“注意力从不离散”，不要写成“注意力从不离开他”。
- 诗句和讽刺语气优先顺中文：`to Justice open laid` 可译为“随时落入司法之手”，避免“向司法敞开受罚之门”这类硬壳。

## 低 token 审计

```powershell
rg -n "Richard Stow|Apsley|Walter Harte|Life of Gustavus Adolphus|Dr\\. Maxwell's Collectanea|Northcote|The Bastard|Mrs\\. Bret|P\\. CUNNINGHAM|Mr\\. Wilks|Giffard|MDCCXLIV|mint of ecstasy|反面天平|对每个对象都在场|向司法敞开|肮脏安顿" chapters/src chapters/translated chapters/final glossary
```

若修复了专名接口、证据性源形或源语句法壳，该轮不能 PASS，必须追加整章复查；最新一轮无新问题时才可关闭。

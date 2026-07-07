# 鲍斯威尔第94单元：书商讽刺、萨维奇材料、拉丁诗、医学献辞与隐喻接口

## 可复用问题族

十八世纪传记脚注常把书商轶事、文学讽刺、编者校勘、拉丁短诗、医学著作献辞和人物品格材料压在连续注释里。译文若只按句面顺下去，容易出现三类问题：既有术语漂移，源语接口不足，以及意思大体正确但中文发硬的说明句。

## 发现方式

- 扫描裸源文和译名漂移：`Bentley`、`Crousaz`、`Harleian Catalogue`、`Goldsmith`、`The Plain Dealer`。
- 对照源文中需要保留形式的词：`contentions`、`Mag.-Extraordinary`、拉丁诗全文、`us` / `mine`。
- 回看短语级多义：`in a few pauses of a walk` 不能被顺手误解为“催促继续前行”。
- 朗读中文引文和书信句，重点看“家庭行为”“绅士武器”“悬置”等直译壳。

## 风险

- 编者讨论作者归属、目录名、书名和源词形式时，若译文裸留英文或译名漂移，读者会失去跨注释索引能力。
- 拉丁诗若只译不留原文，会破坏后文“即席完成”和 Macaulay/Croker 批评所依赖的诗形证据。
- `us` / `mine` 这类源词本身就是论证证据，必须让读者看见英文形式，但不能让它像未完成残留。
- 十八世纪讽刺和献辞语体若过硬，会把原文的机锋、书信礼貌和编者讥刺压扁成资料摘要。

## 修复模式

- 人名、书名和目录名先查 `glossary/proper_nouns.csv`，例如“理查德·本特利”“克鲁萨”“《直言者》”“《哈利藏书目录》”“哥尔德史密斯”。
- 源词讨论使用短接口：`原文作 contentions`、`英文 _us_ 又用 _mine_`；不要把普通名词扩大成括注源词。
- 拉丁诗、题铭、书信等被评论的文本，优先保留源文，再给目标语译文或清晰引导。
- 对讽刺语体和人物评语做目标语重建：`gentleman's weapon` 可译成“绅士佩剑的用法”，`torpedo` 可译成“电鳐”并在上下文中保留隐喻功能。
- 短语级回看要防顺句误判：`in a few pauses of a walk` 是“散步中几次停步”，不是走路被催促。

## 低 token 审计

```powershell
rg -n "Bentley|Crousaz|Harleian Catalogue|Goldsmith|The Plain Dealer|contentions|Mag\\.-Extraordinary|\\bus\\b|\\bmine\\b|in a few pauses of a walk|gentleman's weapon|torpedo" chapters/src chapters/translated chapters/final glossary
```

若修复了术语漂移、源词接口或短语误判，该轮不能 PASS，必须追加整章复查；最新一轮无新问题时才可关闭。

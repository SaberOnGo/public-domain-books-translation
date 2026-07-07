# 18 世纪传记：期刊接受史、慰唁书信与宗教论文接口

## 适用场景

18 世纪英语传记中，作者常在同一生产单元里切换期刊接受史、私人书信、
丧亲慰唁、宗教/道德论文评价和书目版本信息。若只按单句直译，容易出现
注号遗漏、文体混杂、宗教术语泛化、书目格式误读或专名接口不足。

## 问题族

- 期刊接受史中的作品名、杂志副题、撰稿人和君主/古典比较必须按专名策略
  处理；标题首次出现要给读者一个稳定的中文名，不能裸留英文。
- 慰唁书信里的 `virtues`、`separate spirits`、`corporeal separation` 等词，
  不能译成现代心理分析腔；应保留 18 世纪基督教安慰文的庄重、克制和
  神学边界。
- 宗教论文题目如 `Passion-week`、`abstraction and self-examination`、
  `placability of the Divine Nature`，不能按普通情绪词或现代抽象名词硬译。
- 书目格式如 `folio`、`duodecimo`、`edition` 要区分开本、卷数和版本，
  不得把 “six duodecimo volumes” 误成十二卷或简单“六册”。
- 人名首次出现附近若带源注号，括注源名和注号是两个独立接口；翻译或润色
  后必须用注号序列比对防止漏掉。

## 低 token 审计

1. 先跑注号序列：源文与译文 `\[(\d+)\]` 必须数量、顺序完全一致。
2. 扫专名裸留：`Student|Oxford and Cambridge|Elphinston|Ruddiman|Strahan|
   Suspirius|Croaker|Good-Natured|Beauties|Night Thoughts`。
3. 扫术语硬壳：`duodecimo|folio|Passion-week|placability|house of mourning|
   drops in the bucket|self-examination`。
4. 人工复查书信段时，先读目标语是否像一封 18 世纪慰唁信，再对照事实、
   语气、神学限度和称谓署名。

## 修复模式

- 期刊与作品题名：中文题名优先，必要时首次自然正文出现加源文括注。
- 书信：保留称谓、签名、谦辞和长句逻辑，但把中文句群重建到可朗读。
- 宗教术语：译成中文可理解的神学/灵修表达，不把解释塞入正文。
- 书目术语：开本、卷数、版本分别译清；必要时补术语表行。
- 修复任何漏注后，该轮不得 PASS，必须追加一轮整章复查。

## 第一次记录

- 书籍：鲍斯威尔《约翰生传》英译中项目。
- 单元：`032_vol01_unit_32.md`。
- 发现方式：章节译后全量检查中的注号序列比对。
- 具体问题：`Mr. James Elphinston[628]` 初稿漏保留 `[628]`。
- 修复：在专名首次出现后的源名括注后补回 `[628]`，并用新一轮整章复查确认
  注号序列、专名接口、书信语气和宗教术语均 PASS。

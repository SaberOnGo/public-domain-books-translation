# 18世纪传记中的多语引句与实用争论接口

## 适用场景

18 世纪英语传记常把法语格言、拉丁引语、诗行、私人信札、出版史、海军事务和
工程争论放在同一单元里。译文若只按英语散文一路顺译，容易在三个位置失稳：
多语引句没有即时中文接口，源文星号/匕首号被误带入正文，实用技术争论被译成
空泛议论文。

## 发现方式

- 用章节覆盖门禁发现段落压缩，例如 21/29 低于 0.75。
- 用残留扫描查 `[*]`、`[dagger]`、`;`、`；`，确保源文异形脚注标记不进入
  读者正文。
- 用 `rg` 查源语触发式和目标语硬壳：`Ma foi`、`Après tout`、
  `sensations agréables`、`live pleasant`、`cater-cousins`、`great CHAM`、
  `pressed`、`without any wish of his own`、`semicircular`、`elliptical`、
  `Quicquid agunt homines`。

## 风险

多语引句若无即时中文释义，会把读者挡在正文外。星号和匕首号若照搬，会触发出版
注号规则问题。历史习语若硬译，如把 `cater-cousins` 写成“表兄弟”，会制造错误
亲属关系。工程争论若只写成“方案问题”，会丢失半圆拱和椭圆拱这一实质争点。

## 修复模式

- 外文引句保留源文时，紧接自然中文释义，不让外文单独承担信息。
- 源文 `[*]`、`[dagger]` 这类编辑符号不得裸迁入正文。若内容必要，转成合规
  数字注或并入译文叙述。
- 习语先译功能：`cater-cousins` 在信札中是“亲密朋友/熟络关系”，不是亲属。
- 典故绰号保留气势：`great CHAM of literature` 可译为“文学界那位伟大的大汗”，
  不宜弱成普通“可汗”。
- 实用争论保留可核查对象：`semicircular arches`/`elliptical arches` 应明确为
  “半圆拱/椭圆拱”，并保持人物立场和发表平台。

## 低 token 审计

```powershell
rg -n "Ma foi|Après tout|sensations agréables|live pleasant|cater-cousins|great CHAM|强征|本人所求|半圆拱|椭圆拱|Quicquid|\\[dagger\\]|\\[\\*\\]|；|;" chapters/translated chapters/final
```

确认命中后只回看小上下文源文。若本轮修复了任何段落呼吸、引句接口、习语或术语，
该轮不能 PASS，必须追加一轮整章复查，并重新跑注号一致性、覆盖率和残留扫描。


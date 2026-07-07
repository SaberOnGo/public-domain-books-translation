# 18 世纪传记：大学学位、期刊协作与书信接口

## 触发场景

鲍斯威尔《约翰生传》这类 18 世纪传记常把私人书信、大学公文、拉丁学位证书和出版计划连在同一单元中。英文词面看似普通，但制度语境很强，例如 `Hall`、`Convocation`、`by diploma`、`subscribe a sheet`、`fellowship and fines`、`Modus`。

## 风险

- 把牛津 `Hall` 泛译成“大厅”，会削弱学院生活语境；在沃顿书信中应按学院日常译为“学院食堂”。
- 把 `subscribe a sheet` 按现代读者习惯译为“认购一张印张”，会误导成付费订阅；在约翰生筹办评论刊物语境中，应理解为“供一张印张的稿”。
- 大学治理词若泛化，`Vice-Chancellor`、`Heads of Houses`、`Convocation`、`Master of Arts by diploma` 之间的程序关系会不清。
- 拉丁证书若保留大段源文而不给中文接口，读者无法跟上鲍斯威尔展示“荣誉全过程”的叙述功能；若过度现代化，又会抹去公文庄严声调。

## 低 token 审计

1. 先扫本书源文和译文候选：
   `rg -n "Hall|Convocation|Vice-Chancellor|Heads of Houses|by diploma|subscribe a sheet|fellowship and fines|Modus" chapters/src chapters/translated chapters/final glossary`
2. 对命中的旧大学制度词，优先查 `glossary/terms.csv` 是否已有 Oxford 或 periodical_project 域条目。
3. 对书信中的笑点或制度程序，只送小上下文给审校：前后 1-2 段通常足够判断是普通词义还是制度词义。

## 修复模式

- 大学空间/制度词优先译成读者能理解的中文制度接口：`Hall` -> “学院食堂”，`Convocation` -> “评议会”，`Heads of Houses` -> “各学院院长”。
- 期刊协作词按出版动作译，不按现代消费动作译：`subscribe a sheet` -> “供一张印张的稿”。
- 拉丁证书和公文采用中文正文翻译，保留庄重句式，但拆段帮助阅读；只在短语本身被谈论或典故功能很强时保留源文接口。

## 复查

- 章节 control 应记录这类问题属于制度词义与书信笑点接口问题。
- 修复后重跑注号一致性、旧纸本残留扫描、英文残留扫描和 `npm run check:translation-coverage`。
- 若发现任何修复，本轮不能 PASS，必须追加新一轮整章复查。

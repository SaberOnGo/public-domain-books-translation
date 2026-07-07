# Boswell Unit 070: Academic Diploma, Commerce, and Gentility Interfaces

## 中文经验

- 发现方式：第 70 单元整章译后复查，结合注号检查、词表 CSV 解析、拉丁文文凭小上下文对照和社会等级论辩段落独立中文阅读。
- 问题族：十八世纪传记中夹入学术文凭、祷文、商业财富论述和绅士身份辩论时，容易出现三类问题：含逗号机构名破坏 CSV；拉丁/法文源句裸留或接口不足；社会等级抽象词硬译成“悦耳区别”“跃升为财富之人”等中文外壳。
- 风险：CSV 破行会破坏后续专名控制；文凭和外语格言若无中文接口，读者无法获得正文信息；商业/绅士身份论辩若硬译，会让鲍斯威尔的社会判断读成机器摘要。
- 低 token 审计：先扫 `Trinity College, Dublin|Doctoratus|Un gentilhomme|悦耳区别|跃升为财富|flattering distinctions|gentility|heraldry`，覆盖译稿、终稿、词表和生成 XHTML；命中后只读相邻源文。
- 修复模式：含逗号源名进入 CSV 必须给源名和首现字段加引号；拉丁文文凭正文译成中文文凭体，签名保留可读姓名；法文格言用中文译文加源句接口；社会等级抽象词转成中文论述词，如“诱人身份标志”“从默默无闻骤然跃入财富”。
- 复查：修复轮不得 PASS；追加整章复查，确认注号、文凭日期/学位、金额、法文格言和思雷尔家族关系全部闭环。

## English Note

- Finding method: full-chapter review with note-order checks, glossary CSV parsing, Latin diploma comparison, and target-only reading of the gentility argument.
- Family: embedded academic diplomas, foreign mottos, commerce abstractions, and gentility/status terms can break either machine-readable glossary rows or reader-facing Chinese prose.
- Fix pattern: quote comma-bearing CSV fields, translate documentary Latin into a Chinese document register, give foreign aphorisms a Chinese interface, and rebuild status abstractions as readable social argument.

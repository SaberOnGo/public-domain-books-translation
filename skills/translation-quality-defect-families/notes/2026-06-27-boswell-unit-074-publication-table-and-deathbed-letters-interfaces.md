# Boswell Unit 074: Publication Table and Deathbed Letters Interfaces

## 中文经验

- 发现方式：第74单元整章译后复查，结合注号计数、表格行数核对、出版日期链检查、信札格式朗读和旧币/宗教词表扫描。
- 问题族：同一单元从议会报道发表年表切换到临终家书，文本接口跨越表格、出版史、基督教祷告、旧币汇款和私人哀悼；如果沿用单一散文处理，会丢失结构或语体。
- 风险：`spoken` / `published` 若混淆，会破坏本单元核心时间链；`physical book`、`bark`、`bill`、`post` 若按现代常义直译，会误成“物理书”“树皮”“账单”“帖子”；家书中的 `infinite advantage` 若硬译，会削弱祈祷语气。
- 低 token 审计：先扫 `spoken|published|Supplement|Motion-maker|Passion|Communion Service|physical book|bark|guineas|bill|post|infinite advantage`，并核对表格数据行数、注号序列和信件日期。
- 修复模式：出版顺序表用 Markdown 表格保留行列接口；时间链明确区分“说出/刊出”；宗教和书信语体用中文祈祷/家书表达；旧币和汇票进入术语表，正文不裸露英文。
- 复查：修复轮不得 PASS；追加全章复查，确认表格数据、注号、日期、称谓、祈祷语和未完书信边界全部闭环。

## English Note

- Finding method: full-chapter review using note counts, table-row verification, publication-date chain checks, letter-format reading, and scans for currency/religious terms.
- Family: a unit may combine publication chronology tables with intimate deathbed letters; table structure, historical terminology, and epistolary devotional tone need separate reader-facing interfaces.
- Fix pattern: preserve chronology in a readable table, distinguish spoken dates from publication dates, and translate medical, postal, currency, and devotional terms by historical function.

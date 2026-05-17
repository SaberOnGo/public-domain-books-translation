# Book I.3 译后评审 / Post-Translation Review

review_status: `PASS_FOR_DRAFT_REVIEW__FINAL_PENDING`
chapter_id: `003_book_i_03_heaven_moves_spherically`
reviewer: `Codex self-review`
review_date: `2026-05-17`
translation: `chapters/translated/003_book_i_03_heaven_moves_spherically.md`
source: `chapters/src/003_book_i_03_heaven_moves_spherically.md`

## 控制结论

- 本评审只允许 Book I.3 继续进入译后技术复核和后续章节门禁。
- 本评审不允许写 `chapters/final/003_book_i_03_heaven_moves_spherically.md`，不允许生成正式 EPUB。
- 未发现 P0/P1 阻断问题；仍需后续技术复核和终稿前全书一致性审校。

## 综合评分

| 维度 | 满分 | 得分 | 说明 |
|---|---:|---:|---|
| 古希腊文忠实度 | 20 | 18 | 译文保留观测起点、恒显星绕极、反证异说、几何比较和自然学论证五段链条。 |
| 参考译本边界 | 10 | 10 | 译文说明明确英译本只作 reference witness；未出现英译转写痕迹。 |
| 术语一致性 | 15 | 14 | `恒显星`、`天球的极`、`湿气蒸腾`、`升度构造`、`以太`、`同质` 与 I.3 术语预锁一致。 |
| 古今概念边界 | 15 | 14 | 正文没有改写为现代自转、公转、天体物理或大气折射；章末注集中说明边界。 |
| 中文可读性 | 20 | 17 | 长周期句已分段，反问链可读；个别自然学段仍较抽象，终稿可继续润色但不宜删减。 |
| 结构与注释 | 10 | 9 | 注释覆盖球形运动、恒显星、反证链、湿气蒸腾、升度构造和以太/同质性。 |
| 工程/门禁 | 10 | 10 | source、formal recheck、chapter control、translation check 均已存在并接入 `quality:all`。 |
| total | 100 | 92 | PASS_FOR_DRAFT_REVIEW |

## P0/P1 检查

| issue type | result | note |
|---|---|---|
| 公版/底本边界不清 | PASS | source 文件和 metadata 已记录 Heiberg PDF + PAL Greek roles |
| 参考译本转译 | PASS | 未发现英译作为底稿的证据 |
| 整章漏译 | PASS | I.3 主要论证段落均已覆盖 |
| 严重误读 | PASS | 未发现会改变章节主旨的误读 |
| 术语系统性错误 | PASS_WITH_NOTE | `升度构造` 为暂定译法，终稿需与 Book I.12-I.16 统一 |
| 古今概念混淆 | PASS_WITH_NOTE | 注释已处理；后续技术复核需继续防止把湿气蒸腾改写为现代大气折射 |

## 细节意见

- `以球形方式运动`：保留原命题，不替换为现代“自转”或“公转”；章末注处理得当。
- `恒显星` 和 `天球的极`：译文能解释观测链，也保留了较近星作较小圆、较远星作较大圆的结构。
- 反证链：保留“向无穷远处运动如何返回、为何不可见、为何不逐渐变小、为何被地面截断”的问答推进。
- `湿气蒸腾`：正文未现代化为大气折射，符合古今概念边界；终稿可在注释中再交叉引用视觉现象术语表。
- `升度构造`：可读性略技术化，但比强行译作现代“星盘/占星”更稳；需在后续球面天文学章节统一。
- 自然学段：`以太`、`同质`、`同质表面` 保留古代自然学论证，但终稿可微调句式，使“平面/立体”对比更顺。

## 下一步

1. 创建或更新 Book I.3 译后技术复核记录。
2. 检查 Book I.3 术语是否需要写入全书 glossary / terminology change log。
3. 只有技术复核、忠实度/可读性/术语门禁全部通过后，才可考虑 `chapters/final/`。

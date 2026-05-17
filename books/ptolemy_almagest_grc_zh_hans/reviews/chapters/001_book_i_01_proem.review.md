# Book I.1 译后评审 / Post-Translation Review

review_status: `PASS_FOR_DRAFT_REVIEW__FINAL_PENDING`
chapter_id: `001_book_i_01_proem`
reviewer: `Codex self-review`
review_date: `2026-05-17`
translation: `chapters/translated/001_book_i_01_proem.md`
source: `chapters/src/001_book_i_01_proem.md`

## 控制结论

- 本评审只允许 Book I.1 继续进入译后技术复核和后续章节门禁。
- 本评审不允许写 `chapters/final/001_book_i_01_proem.md`，不允许生成正式 EPUB。
- 未发现 P0/P1 阻断问题；仍需后续技术复核和终稿前全书一致性审校。

## 综合评分

| 维度 | 满分 | 得分 | 说明 |
|---|---:|---:|---|
| 古希腊文忠实度 | 20 | 18 | 基本保留理论/实践、三分学科、数学确定性、数学对神学性研究/自然学/伦理实践的助益等论证链。 |
| 参考译本边界 | 10 | 10 | 译文说明明确英译本只作 reference witness；未出现英译句式提示。 |
| 术语一致性 | 15 | 14 | 使用 `理论部分`、`实践部分`、`自然学`、`数学诸学`、`神学性研究`，与术语预锁一致。 |
| 古今概念边界 | 15 | 14 | 章末注说明自然学、神学性研究和数学诸学的古代语境；正文避免现代化为物理学/应用科学。 |
| 中文可读性 | 20 | 17 | 长周期句已拆分，整体清楚；个别哲学句仍偏密，需要终稿阶段再润色。 |
| 结构与注释 | 10 | 9 | 正文和章末注清楚；专名 `叙鲁斯` 后续可在全书专名表中统一。 |
| 工程/门禁 | 10 | 10 | source、formal recheck、chapter control、translation check 均已存在并接入 `quality:all`。 |
| total | 100 | 92 | PASS_FOR_DRAFT_REVIEW |

## P0/P1 检查

| issue type | result | note |
|---|---|---|
| 公版/底本边界不清 | PASS | source 文件和 metadata 已记录 Heiberg PDF + PAL Greek roles |
| 参考译本转译 | PASS | 未发现英译作为底稿的证据 |
| 整章漏译 | PASS | I.1 主要论证段落均已覆盖 |
| 严重误读 | PASS | 未发现会改变章节主旨的误读 |
| 术语系统性错误 | PASS | 核心术语与 `mathematical_term_lock.md` 一致 |
| 古今概念混淆 | PASS_WITH_NOTE | 注释已处理；终稿仍需检查读者是否会误解“神学性研究” |

## 细节意见

- `叙鲁斯`：暂可用，但进入终稿前应与全书专名表统一，必要时补专名注。
- `神学性研究`：比直接写“神学”更能避免现代宗教教义误解；终稿可按全书风格决定是否简化为“神学部分”。
- `自然学`：处理正确；正文未写成现代“物理学”。
- 中文节奏：第 3-5 段概念密度高，但这是原文论证密度造成的；终稿润色时可以小幅拆句，不应省略论证层级。

## 下一步

1. 创建或更新 Book I.1 译后技术复核记录。
2. 检查术语、专名和注释是否需要写入全书 glossary / terminology change log。
3. 只有技术复核、忠实度/可读性/术语门禁全部通过后，才可考虑 `chapters/final/`。

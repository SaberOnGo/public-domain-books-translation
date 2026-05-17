# Book I.2 译后评审 / Post-Translation Review

review_status: `PASS_FOR_DRAFT_REVIEW__FINAL_PENDING`
chapter_id: `002_book_i_02_order_of_the_theorems`
reviewer: `Codex self-review`
review_date: `2026-05-17`
translation: `chapters/translated/002_book_i_02_order_of_the_theorems.md`
source: `chapters/src/002_book_i_02_order_of_the_theorems.md`

## 控制结论

- 本评审只允许 Book I.2 继续进入译后技术复核和后续章节门禁。
- 本评审不允许写 `chapters/final/002_book_i_02_order_of_the_theorems.md`，不允许生成正式 EPUB。
- 未发现 P0/P1 阻断问题；仍需后续技术复核和终稿前全书一致性审校。

## 综合评分

| 维度 | 满分 | 得分 | 说明 |
|---|---:|---:|---|
| 古希腊文忠实度 | 20 | 18 | 基本保留总体关系、各部分顺序、太阳/月亮、恒星天球、五行星和总论命题链。 |
| 参考译本边界 | 10 | 10 | 译文说明明确英译本只作 reference witness；未出现英译转写痕迹。 |
| 术语一致性 | 15 | 14 | 使用 `黄道斜圈`、`我们所居世界`、`地平圈`、`恒星天球`、`五个行星` 等，与 I.2 预锁一致。 |
| 古今概念边界 | 15 | 14 | 章末注说明古代数学天文学语境；正文未现代化为物理轨道或现代宇宙论。 |
| 中文可读性 | 20 | 17 | 原文为长周期总纲句，译文已拆成四段；个别术语仍偏技术性，终稿可微调。 |
| 结构与注释 | 10 | 9 | 正文与章末注对应清楚；后续需与 Book I.12-I.15 的黄道术语统一。 |
| 工程/门禁 | 10 | 10 | source、formal recheck、chapter control、translation check 均已存在并接入 `quality:all`。 |
| total | 100 | 92 | PASS_FOR_DRAFT_REVIEW |

## P0/P1 检查

| issue type | result | note |
|---|---|---|
| 公版/底本边界不清 | PASS | source 文件和 metadata 已记录 Heiberg PDF + PAL Greek roles |
| 参考译本转译 | PASS | 未发现英译作为底稿的证据 |
| 整章漏译 | PASS | I.2 主要论证段落均已覆盖 |
| 严重误读 | PASS | 未发现会改变章节主旨的误读 |
| 术语系统性错误 | PASS_WITH_NOTE | `黄道斜圈` 为暂定工作译法，终稿需与后续章节统一 |
| 古今概念混淆 | PASS_WITH_NOTE | 注释已处理；终稿需持续避免现代物理轨道化 |

## 细节意见

- `黄道斜圈`：可读性略硬，但能保留古代大圈语境；进入 Book I.12-I.15 后再统一是否改为“黄道圈”并注出原文的“倾斜”。
- `我们所居世界`：比“有人居住的世界”更顺，但终稿需检查是否与地理章节统一。
- `地球本身不作任何平移运动`：可读性明确，保留 `μεταβατικὴ κίνησις` 的非平移/不移动要点。
- `显见现象 / 可靠观测 / 几何证明`：方法链已保留，后续技术复核需继续检查是否被现代化为经验科学叙述。
- 中文节奏：第一段信息量高；终稿可继续拆分，但不得削弱“先后次序”的论证功能。

## 下一步

1. 创建或更新 Book I.2 译后技术复核记录。
2. 检查 Book I.2 术语是否需要写入全书 glossary / terminology change log。
3. 只有技术复核、忠实度/可读性/术语门禁全部通过后，才可考虑 `chapters/final/`。

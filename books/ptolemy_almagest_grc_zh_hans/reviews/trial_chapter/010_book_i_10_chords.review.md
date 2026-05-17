# Book I.10 试译评审记录 / Trial Chapter Review

review_status: `PASS_FOR_TRIAL_SCOPE__FULL_BOOK_BLOCKED`

## 章节

- id: `010_book_i_10_chords`
- source: `chapters/src/010_book_i_10_chords.md`
- translated: `chapters/translated/010_book_i_10_chords.md`
- final: `chapters/final/010_book_i_10_chords.md`

## 当前结论

Book I.10 的受控试译已经完成，并已插入 7 张试译级 SVG 图。评审结论为：可作为 Book I.10 单章节试译样本继续讨论和人工复核；不得进入 `chapters/final/`、不得翻译 Book I.11 弦表、不得进入全书翻译或 EPUB 生产。

## 评审清单

| id | severity | item | status |
|---|---|---|---|
| TCR-001 | P1 | PDF viewer page numbers must be mapped to PAL/Heiberg markers around `I_31_7` through before `I_48` | CLOSED_FOR_TRIAL_RANGE: viewer pages `19`-`27`; page `28` starts I.11 |
| TCR-002 | P1 | Book I.10 figure/table inventory must identify whether the chapter contains diagrams or table-like numeric material needing visual control | CLOSED_FOR_TRIAL: 7 figure SVG drafts created and referenced; Book I.11 table excluded |
| TCR-003 | P1 | Mathematical terms in Book I.10 must be checked against the extracted Greek, replacing `TBD` source terms in `qa/technical/mathematical_term_lock.md` where possible | PARTIAL: core Book I.10 terms extracted; full lock pending |
| TCR-004 | P1 | `qa/chapter_controls/010_book_i_10_chords.control.md` and `qa/technical/010_book_i_10_chords.technical_audit.md` must be created before trial review can run | CLOSED_FOR_TRIAL: both files exist; technical audit remains trial-scoped |
| TCR-005 | P1 | Translation must be based on Ancient Greek source, not reference translation | PASS_FOR_TRIAL | Translation follows `chapters/src/010_book_i_10_chords.md`; no reference-witness wording imported. |
| TCR-006 | P1 | Euclid dependencies and proof steps preserved | PASS_FOR_TRIAL | Rectangles, squares, equal angles, proportional relations, and cited Euclid dependencies retained in Chinese. |
| TCR-007 | P1 | Sixagesimal values preserved | PASS_FOR_TRIAL | `360`, `120`, `37;4,55`, `70;32,3`, `84;51,10`, `103;55,23`, `114;7,37`, `1;34,15`, `0;47,8`, `1;2,50`, `0;31,25` retained. |
| TCR-008 | P1 | Book I.11 chord table excluded | PASS | Translation ends with a scope note before the table; no Book I.11 table rows translated. |
| TCR-009 | P2 | Final publication diagram quality | OPEN_FOR_LATER | SVGs are controlled trial drafts only; final publication redraw requires separate vector/accessibility review. |
| TCR-010 | P2 | Full Book I terminology lock | OPEN_FOR_FULL_BOOK | `mathematical_term_lock.md` remains Book I.10 pilot-level, not full Book I lock. |

## 分项评分

| dimension | score | conclusion |
|---|---:|---|
| 古希腊文忠实度 | 91 | 证明结构和数值主线完整；个别古希腊数学术语仍需人工复核。 |
| 中文可读性 | 86 | 句子较密，但证明文本可读；未明显机械直译。 |
| 术语一致性 | 88 | `直线`、`弧`、`所对直线`、`矩形`、`平方`、点名规则一致；全书锁定仍未完成。 |
| 数学证明链 | 90 | 主依赖链闭合；后续人工审校应重点复查 `外中比` 和比值引理段。 |
| 图表标签 | 89 | 7 张 SVG 与试译文字对应；仍是试译草图。 |
| 数值控制 | 92 | 六十进制值按日志保留，已修正 `0°45' -> 1°` 夹逼段。 |
| 古今概念边界 | 94 | 未用现代天文学或三角函数改写正文。 |

## 路由

Book I.10 trial translation is review-pass within trial scope. Next allowed step is human/agent discussion of this single chapter or targeted revision. Do not proceed to whole-book translation, Book I.11 chord table, final chapter output, or EPUB production from this review alone.

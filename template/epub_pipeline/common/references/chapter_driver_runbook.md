# 章节驱动者流程 / Chapter Driver Runbook

> 配合 `translation_method_v2.md` 与 `scripts/method_v2_tool.py` 使用。每章一个"章节驱动者"（orchestrating agent），自己不翻译，只给每一遍派全新的子 agent、跑脚本、检查产物。
> Use with `translation_method_v2.md` and `scripts/method_v2_tool.py`. One chapter driver per chapter: it never translates; it spawns a fresh sub-agent per pass, runs the scripts and checks outputs.

## 1. 目录约定 / Layout

书籍工程内（属于该书，不得写回 `template/`）/ inside the book project, never written back into `template/`:

- `qa/method_v2/_shared/`：`brief_full.md`、`brief_7_8.md`、`brief_2_3_11.md`、`reader_profile.txt`、`name_ledger.md`
- `qa/method_v2/chNNN/`：`source_numbered.md`（`[Pnn]` 段号）、`terms_hits.md`、`heading_zh.md`、各遍产物、`final.md`、`chapter_report.md`

初始化 / initialise: `python template/epub_pipeline/common/scripts/method_v2_tool.py prepare <book_dir>`

## 2. 步骤 / Steps

| 步骤 | 子 agent | 输入（只限这些）| 输出 |
|---|---|---|---|
| 0 切单元 | 驱动者 | 原文 | `units.md`，每块 ≤4500 源文字符（>9000 的章必须切）|
| 1 初译 | 强模型 | 提示词 30、手册全文、本单元原文、命中术语、章题、前情 | `pass1_draft[_uK].md` |
| 2 对读 | 强模型 | 提示词 31、原文、初译、命中术语、手册 §7–8 | `pass2_fidelity`、`pass2_corrected`；报"没有"则换模型重做 |
| 3 脱稿重写 | 强模型 | 提示词 32、pass2_corrected、手册 §2–3、§11、命中术语（**不给原文**）| `pass3_rewrite`、`pass3_changes` |
| 4 冷读 | 另一模型 | 提示词 33、pass3_rewrite、读者画像（**不给原文、手册、前几遍记录**）| `pass4_cold_read`；报"没有"则换家族重做 |
| 5 句型修复 | 强模型 | pass3_rewrite、冷读清单、手册 §2–3、§11（不给原文）| `pass4_fixed`、`pass4_fixes` |
| 6 复核对读 | 强模型 | `method_v2_tool.py recheck` 生成的 `input_recheck.md`（改动段 + 前后各一段，含原文与现译）| `pass6_recheck`、`pass6_fixes`、`final.md`；改动最大 3 段做回译自查，如实标注为简化版 |
| 7 成品检查 | 驱动者 | `final.md` | `method_v2_tool.py check`、`profile` 通过；写 `chapter_report.md` |

长章：步骤 1、2、3、5、6 按单元各派一个子 agent，文件名加 `_uK`，用 `method_v2_tool.py merge` 合并。
Long chapters: run passes 1, 2, 3, 5, 6 per unit with `_uK` file names, then `merge`.

## 3. 实测约束 / Constraints observed in practice

1. **输出过长会卡死。** 一次写出 >1.3 万字符的译文或对读结果，子 agent 可能 10 分钟无进展；因此单元 ≤4500 源文字符，任何子 agent 10 分钟没有产出文件就停掉、把块切小一半重派。
   Very long single outputs stall sub-agents; keep units ≤4500 source characters and re-dispatch with half-size units after 10 idle minutes.
2. **并发有上限。** 宿主限制同时存活的子 agent 总数（实测 20，驱动者本身也计入）。同时跑的章节驱动者不超过 6 个；派发被拒时等一会儿再试，最多三次，仍失败就把断点写进 `chNNN/progress.md` 如实返回，不要自己翻译。
   The host caps live sub-agents (20 observed, drivers included). Run at most 6 drivers at once; on refusal retry up to three times, then record the breakpoint in `progress.md` and report.
3. **额度会用完。** 429 额度限制会同时打断所有驱动者；过程文件已落盘，额度恢复后用 `SendMessage` 让原驱动者续跑，或新派驱动者从 `progress.md` 或首个缺失文件接着做，不要重译已完成的遍。
   A rate-limit error stops all drivers at once; outputs are on disk, so resume from the first missing pass instead of redoing finished ones.
4. **专名表先于批量。** 术语表没有的人名、地名，各章会各自音译。批量前或前几章完成后，建立一张 `name_ledger.md`（原文 | 采用译法 | 出现章），之后各章初译、对读、重写都带上它。
   Build a name ledger early; chapters invent their own renderings for names missing from the glossary.
5. **对读召回有限。** 单次对读常漏意义错误（实测每章 1–8 条，复核与冷读后的改动段又找出更多），所以步骤 6 必须对改动段再对读一次；对话为主的章节 `sentence_mean` 偏低属正常，记录为合理例外。
   Single fidelity passes under-report; step 6 is mandatory. Dialogue-heavy chapters legitimately have a low sentence mean; record it as an exception.
6. **成品门禁。** `check` 检查段号一一对应、无 `[疑]`、长度比；`* * *` 分隔段和 `[IMAGE: …]` 生产标记不计入。

## 4. 如实记录 / Honest records

`chapter_report.md` 写明每遍所用模型家族、报告条数、profile flags、新毛病、未决问题，以及相对 `translation_method_v2.md` 的偏差（单元大小、回译简化、同一模型家族评审）。不得声称异构。
Record models used, counts, flags, defects, open items and deviations; never claim model heterogeneity that did not happen.

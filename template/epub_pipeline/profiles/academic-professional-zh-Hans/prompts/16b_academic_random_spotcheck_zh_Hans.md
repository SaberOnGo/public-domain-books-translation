# 16b 学术与专业书随机抽检补充规则 / Academic Random Spot-Check Supplement

本补充规则用于 `academic-professional-zh-Hans` profile。

运行随机抽检时使用：

```powershell
npm run review:random-samples
```

或显式使用：

```powershell
python scripts/select_random_review_passages.py --source-dir chapters/final --agents 2 --samples-per-agent 60 --rounds-planned 4 --target-confidence 0.80 --defect-rate 0.10 --profile academic
```

## 额外检查点

每个 agent 除 common 抽检要求外，还必须检查：

- 该段是否只是准确但不必要地拗口。
- 是否把专业术语硬改成日常词，导致学科水准下降。
- 是否缺少读者理解公式、表格、统计结果所需的中文路标。
- 是否存在“长句能拆而未拆”的问题。
- 引文、作者转述、译者说明是否边界清楚。
- 章节论证链条是否可跟：定义、机制、证据、限制、结论。

## 阻塞规则

- 专业内容因通俗化而失真：P1/P2。
- 读者无法理解该段在论证中的作用：P2。
- 单项低于 70：本轮 FAIL。
- 只是不够轻松但仍准确可懂：P3，记录但不阻塞。

## 随机抽检同类问题全书审计 / Book-Wide Similar-Issue Audit

随机抽检一旦发现任何需要修复或可能系统性复现的问题，包括但不限于 P0/P1/P2、单项 <70、读者不可理解、事实/术语/图表/公式/注释错误，或本模板硬门禁失败，主执行 AI 不得只修被抽中的样本，也不得等到第二轮才全书检查。必须先把发现归纳为问题族，再对整本读者可见书稿执行全书同类问题审计，覆盖 `chapters/final/`、frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML；修复所有确认命中，记录合理例外，并在该轮 `fix_log.md` 与 `closure_check.md` 中关闭该问题族后，才能使用新 seed 复抽。

If a random sample exposes any issue that needs correction or may recur systemically, treat it as a possible systemic defect family immediately in the current round. Audit the whole reader-facing book for similar cases, fix all confirmed matches, document justified exceptions, and close the family in the same round before a new-seed resample.

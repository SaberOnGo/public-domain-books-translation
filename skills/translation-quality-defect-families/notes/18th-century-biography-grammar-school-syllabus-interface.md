# 18th-Century Biography: Grammar-School Syllabus Interface

## 中文经验

- 发现方式：章节全量复查中检查文法学校方案、古典作者清单、希腊方言列表、
  分班规则、星期考查和韵律/作文训练。
- 问题族：18 世纪英语传记常直接抄入学校课程方案。它既是史料，又是可读正文；
  如果机械翻成散句，读者会看不出班级层次、教材关系和训练顺序。
- 审计方法：先用 `rg -n "Class|Corderius|Erasmus|Eutropius|Attick|Ionick|Dorick|theme|scanning"`
  收集候选，再只读命中的课程清单及前后段落。
- 修复方式：保留清单层级和作者/教材接口；`Class` 译作“班”或“等级”要按学校
  语境统一；`scanning verses` 必须体现韵律分析；`Attick/Ionick/Dorick`
  是希腊方言名，不应音译成普通地名。
- 复查方式：不看英文只读中文，应能看出第一班、第二班、第三班各学什么、何时
  考查、怎样从拉丁转入希腊与作文；再回看源文确认作者、教材和方言没有错位。

## English Note

- Detection: in full-chapter review, inspect grammar-school schemes, classical
  author lists, Greek dialect tables, class rules, examination days, and
  prosody/composition training.
- Family: eighteenth-century biography may quote school syllabi directly. These
  passages are both evidence and reader-facing prose; if translated as loose
  sentences, class levels, textbook relationships, and training sequence become
  unclear.
- Audit: search low-token candidates with `rg -n "Class|Corderius|Erasmus|Eutropius|Attick|Ionick|Dorick|theme|scanning"`,
  then review only the hit syllabus and nearby context.
- Fix: preserve list hierarchy and author/textbook interfaces. Translate `Class`
  consistently by school context; make `scanning verses` explicit as metrical
  analysis; treat `Attick/Ionick/Dorick` as Greek dialect names, not ordinary
  place names.
- Recheck: target-only reading should show what each class studies, when pupils
  are examined, and how the plan moves from Latin rules to Greek and composition;
  source comparison should confirm that authors, books, and dialects are not
  displaced.

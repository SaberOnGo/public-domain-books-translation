# 18th-Century Biography: Latin Bibliographic Title Interface

## 中文经验

- 发现方式：章节全量复查中检查拉丁书名、预约出版题名、献词题名和引文接口。
- 问题族：18 世纪传记常直接印拉丁书名或出版计划题名；如果中文译文只保留
  原题，读者会失去题名本身承担的书目信息，例如作者、注释、诗史、生平、
  增补者等关系。
- 审计方法：先用 `rg` 查 `Poemata|Latina|Notas|histori|vitâ|addidit` 等
  低 token 候选，再只对命中的拉丁题名及上下文做源文对照。
- 修复方式：保留源文题名作为书名/引文接口时，紧接着给出中文意译说明；
  说明必须重建语法关系，不要把 `notas cum historia... et vita... addidit`
  硬译成“诗史注释”之类自相混合的名词组。
- 复查方式：不看原文读中文说明，应能明白该题名在出版计划中承诺了什么内容；
  再回看原文确认作者、增补者、附录内容和时间范围没有错位。

## English Note

- Detection: during full-chapter review, inspect Latin book titles, subscription
  proposal titles, dedications, and quote interfaces.
- Family: eighteenth-century biography often prints Latin bibliographic titles.
  If the Chinese translation leaves only the Latin string, readers lose the
  title's bibliographic information, such as author, notes, literary history,
  life, and editor/additor relationships.
- Audit: use low-token searches such as `Poemata|Latina|Notas|histori|vitâ|addidit`,
  then compare only the hit title and nearby context against the source.
- Fix: keep the Latin title when it is a source-interface quote, but immediately
  add a Chinese rendering that reconstructs the grammar. Do not compress clauses
  such as `notas cum historia... et vita... addidit` into a misleading compound.
- Recheck: the Chinese explanation should be understandable without the source,
  then source comparison should confirm that author, additions, appendix-like
  content, and date range are not displaced.

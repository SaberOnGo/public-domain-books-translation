# Boswell Unit 073: Parliamentary Authenticity and Misattribution Interfaces

## 中文经验

- 发现方式：第73单元整章译后复查，结合源译对照、旧刊缩写扫描、议会化名扫描、注号检查和中文独立朗读。
- 问题族：议会报道真实性论证常把“伪造性”“错误归属”“竞争刊物先后发表”“旧号引用”和“化名议场”压在同一段里；如果只逐句翻译，读者会失去证据链方向。
- 风险：`the Bishop's notes show that he did not speak` 这类代词句若直译成“主教笔记显示他未发言”，中文读者可能分不清“他”是谁；`back number`、`parliamentary prosecution`、`Primate` 若泛化，会削弱出版风险、教会头衔和归属错误的论证。
- 低 token 审计：先扫 `real debating|coinage|Hurgo|Toblat|Quadrert|Secker|Primate|Gin Bill|back number|parliamentary prosecution|Croker`，覆盖译稿、终稿、词表和生成 XHTML；命中后只读取相邻源文。
- 修复模式：对证据链长段先拆分中文段落；代词句改为具名接口，如“塞克尔自己的笔记显示他并未发言”；头衔和法律/出版术语用中文功能表达，如“首席主教”“议会追诉”“旧号”。
- 复查：修复轮不得 PASS；追加全章复查，确认注号、引用归属、化名首现、旧刊缩写和中文段落呼吸全部闭环。

## English Note

- Finding method: full-chapter post-translation review with source/target comparison, abbreviation scan, disguise-name scan, note-marker check, and target-only reading.
- Family: parliamentary authenticity arguments combine invented speeches, misattribution, rival periodical timing, back-number references, and disguised speakers; each needs a clear Chinese evidence-chain interface.
- Fix pattern: split dense evidence paragraphs, replace ambiguous pronouns with named subjects, and render publishing/legal/church terms by function before retaining source-form interfaces for disguise names.

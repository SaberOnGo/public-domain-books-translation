# Boswell Unit 075: Cambridge Letter and Political Patronage Interfaces

## 中文经验

- 发现方式：第75单元整章译后复查，结合注号计数、标题源形扫描、CSV 解析、剑桥引文小上下文对照和 Hamilton/伯克政治关系段源译对照。
- 问题族：书信续段、大学轶事、正式致谢信和政治庇护关系考证连续出现时，源文的社交语、诗学术语和 patronage 语汇很容易被普通现代词压平。
- 风险：标题保留 `H----N` 会违反中文标题接口；`numbers` 在十四行诗语境中若译成“音数”会显得生硬不准；Burke 的 `power` 若译成“能力”，会把“余地/自由”误读成个人能力。
- 低 token 审计：先扫 `H----N|faux pas|memoriter|numbers|claim of servitude|situation|scholarship|Parliamentary Logick|Considerations on Corn`，并检查专名 CSV 是否因地址逗号产生新坏字段。
- 修复模式：标题只放中文读者接口；法语社交词可首现保留源形；诗学 `numbers` 译为格律类概念；political patronage 中的 `power/situation/scholarship` 按制度功能译为“余地/职位/学问”。
- 复查：修复轮不得 PASS；追加全章复查，确认注号、标题、专名表、政治关系链和剑桥引文全部闭环。

## English Note

- Finding method: full-chapter review with note counts, title source-form scans, CSV parsing, Cambridge quotation context, and Hamilton/Burke patronage comparison.
- Family: letters, university anecdotes, formal acknowledgements, and political patronage analysis require separate registers; ordinary modern wording can flatten source-specific social and institutional meanings.
- Fix pattern: keep headings Chinese-only, preserve foreign social tags only where useful, render poetic and patronage terms by function, and verify CSV rows when source names contain commas.

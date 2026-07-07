# Boswell Unit 076: Appendix Illness and Footnote Interface

## 中文经验

- 发现方式：第76单元整章译后复查，结合58个注号计数、缩写书名扫描、脚注区源形扫描、附录F日期链对照和词表 CSV 解析。
- 问题族：附录考证和大批脚注同章出现时，缩写书名、拉丁引文、交叉引用和人物病情叙述容易混成裸源形或过度现代化中文。
- 风险：`Pr. and Med.`、`Anec.` 直接进入译文会让读者面对编辑缩写；`nervous` 若译成普通“紧张”会削弱 Hamilton 的神经过敏；拉丁诗句若只译中文，会丢失脚注讨论的原句接口。
- 低 token 审计：先扫 `_Post_|_Ib_|Pr. and Med|Anec.|FOOTNOTES|nervous|new edition|O noctes|Midsummer|abstain from wine`，再核对注号序列和脚注段落数量。
- 修复模式：交叉引用改为中文“见前/见后”；缩写书名展开为可读书名；外语引文在脚注保留源句并配中文接口；病情/戒酒/日期链按考证功能翻译。
- 复查：修复轮不得 PASS；追加全章复查，确认正文、附录标题、脚注和词表均闭环。

## English Note

- Finding method: full-chapter review with 58-note count checks, abbreviation scans, source-form scans in footnotes, Appendix F chronology comparison, and glossary CSV parsing.
- Family: appendix evidence and large footnote blocks require special handling for abbreviated titles, Latin quotations, cross-references, and illness chronology.
- Fix pattern: localize cross-references, expand abbreviations into readable title interfaces, retain foreign quotations when the source wording matters, and recheck the complete note sequence after every fix.

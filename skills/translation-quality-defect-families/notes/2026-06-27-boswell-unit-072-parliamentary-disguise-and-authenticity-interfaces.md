# Boswell Unit 072: Parliamentary Disguise and Authenticity Interfaces

## 中文经验

- 发现方式：第 72 单元整章译后复查，结合裸源语扫描、书刊缩写检查、遮名接口检查和附录 A 源译对照。
- 问题族：议会出版史附录中常同时出现讽刺化名、遮名、缩略书刊名、交叉引用和真实性判断；如果全部按普通人名或普通书名处理，会削弱作者关于“规避特权、伪装报道、后来被误认为真实”的论证。
- 风险：`Magazine` 这类短称会让来源变模糊；`Hurgolen Branard`、`Mildendo` 这类讽刺化名若不保留源形，读者看不出小人国伪装机制；`authentic records`、`coinage of imagination`、`accessory to the propagation of falsehood` 若硬译，会削弱约翰生良心转折。
- 低 token 审计：先扫 `Magazine|Lilliput|Hurgoes|Clinabs|Walelop|Pulnub|Ptit|Hurgolen|Mildendo|Parl. Hist|Gent. Mag|authentic|falsehood|WHIG DOGS`，覆盖译稿、终稿、词表和生成 XHTML；命中后只读相邻源文。
- 修复模式：短称按上下文补足为《绅士杂志》或《杂志》；讽刺化名首现保留源形；交叉引用用“见前/见后/同处”这类中文学术接口；真实性和良心术语译成功能表达，如“真实记录”“他自己想象力铸造出来的东西”“协助传播虚假”。
- 复查：修复轮不得 PASS；追加整章复查，确认无注号单元的交叉引用、遮名、外文译本、真实性判断和良心理由全部闭环。

## English Note

- Finding method: full-chapter review with scans for source residue, periodical abbreviations, disguise-name interfaces, and Appendix A source comparison.
- Family: parliamentary-reporting appendices combine satirical disguises, masked names, abbreviated citations, cross-references, and authenticity ethics; each needs a specific reader-facing Chinese interface.
- Fix pattern: disambiguate short periodical names from context, preserve disguise names when they prove the mechanism, translate cross-references into Chinese scholarly phrasing, and rebuild authenticity/falsehood terms by function.

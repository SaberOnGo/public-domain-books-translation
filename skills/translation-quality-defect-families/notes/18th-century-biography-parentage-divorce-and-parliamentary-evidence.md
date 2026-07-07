# 18th-century biography: parentage, divorce, and parliamentary evidence

## 中文经验

- 问题族：十八世纪传记一旦从叙事转入身世争议、离婚案、议会法案和遗赠证据，译文容易为了中文顺序重排，把注号顺序打乱，或把 `criminal connection`、`Act of Parliament`、`Counsel`、`bill`、`natural children`、`legacy`、`executors` 等法律/身份词译成现代泛义或过硬字面。
- 发现方式：先扫描注号顺序和法律触发词：`Act of Parliament`、`divorce`、`adultery`、`Counsel`、`bill`、`natural children`、`impostor`、`legacy`、`god-mother`、`executors`、`libeller`。若中文为顺读重排了句子，必须额外检查相邻注号是否仍按源文证据顺序出现。
- 风险：注号错序会使读者无法对应证据；法律词硬译会误导身份、诉讼和继承关系；把 `criminal connection` 直译成“犯罪性关系”会比原文更像现代刑事定性，削弱鲍斯威尔的审慎证据语气。
- 修复方式：保持证据链顺序优先于句子花样。必要时把一句拆成两句，使 `[495]`、`[496]` 等相邻注号按源文顺序闭合。法律词按十八世纪语境译为“议会法案、律师、法案、非婚生子女、冒名顶替者、遗赠、教母、遗嘱执行人、诽谤者”等；`criminal connection` 可译为“不法私通关系”，避免现代刑法化。
- 复查方式：用脚本比较源文和译文 `[\d+]` 序列是否完全一致；再用 `rg` 扫上述法律触发词和目标候选，做小上下文源译对照。最后中文独立朗读，确认议会程序和继承论证不是论文式硬壳。

## English reusable lesson

- Defect family: When eighteenth-century biography shifts into parentage disputes, divorce proceedings, Acts of Parliament, and legacy evidence, translators may reorder sentences for target-language readability and accidentally reorder note markers or over-literalize legal and identity terms.
- Find it by scanning note-marker order plus legal triggers such as `Act of Parliament`, `divorce`, `adultery`, `Counsel`, `bill`, `natural children`, `impostor`, `legacy`, `god-mother`, `executors`, and `libeller`. Any target-language sentence reordering around adjacent notes requires a separate marker-order check.
- Risk: Misordered notes break the evidence chain; stiff legal literals misrepresent status, litigation, and inheritance relations; rendering `criminal connection` as a modern criminal-law phrase can overstate Boswell's evidentiary tone.
- Fix by preserving the evidence order even if the target sentence must be split. Keep adjacent markers such as `[495]` and `[496]` in source order. Render period legal/social terms into readable target-language equivalents and avoid modern overclassification.
- Recheck by comparing source and target note-marker sequences exactly, then use targeted `rg` scans for the legal triggers and only inspect the nearby source-target contexts.

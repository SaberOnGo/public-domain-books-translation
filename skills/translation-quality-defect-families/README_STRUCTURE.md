# 译文质量知识层结构 / Translation Quality Knowledge Structure

## 三层结构 / Three Layers

| 层 / Layer | 文件 / File | 用途 / Purpose |
|---|---|---|
| 技艺手册 / Craft handbook | `skills/translation-craft-handbook/SKILL.md` | 按缺陷类型讲“怎么译好”：识别信号、成因、做法、反例→正例。体积小（≤ 20 KB），可与一章书一起放进翻译、改写或冷读审校调用。 / Craft by defect type; small enough to load with a chapter. |
| 缺陷目录 / Catalogue | `skills/translation-quality-defect-families/catalogue.yaml` | 机器可读：每条有 id、类型、正则或指标信号、反例/正例、修法、适用范围，供脚本定位候选。命中只是候选，须回对原文判定。 / Machine signals for scripts; hits are candidates, confirm against the source. |
| 旧注册表 / Legacy register | `skills/translation-quality-defect-families/SKILL.md` | 历史问题族与轮次记录，保留用于回填验证和追溯；不作为翻译或审校调用的加载材料。 / Historical register kept for backfill validation and traceability; not loaded into translation or review calls. |

书本个案（具体书的人名、坏译串、轮次、单元号）写进该书工程的 `qa/`，不写进以上三层。
Book-specific cases (names, bad strings, rounds, unit IDs) belong in that book project's `qa/`, not in these layers.

## 回填规则 / Backfill Rule

发现可复用的问题时，只做以下两种之一：
When a reusable problem is found, do one of these only:

1. 在 `catalogue.yaml` 新增或合并一条：补一个有效的 Python 正则或指标信号，或补一对反例→正例。先搜已有条目，同类就合并，不新开。
   Add or merge a catalogue entry: a valid Python regex or metric signal, or a bad→good pair. Merge into an existing entry when the type already exists.
2. 在手册对应类型下补一个短例或一句做法，保持手册 ≤ 20 KB。
   Add a short example or one-line fix under the matching handbook section; keep it within 20 KB.

禁止追加轮次日志、长串字面坏译 `rg` 列表或只适用于一本书的规则。修复要修句型，不是只换被点名的字串。
Never append round logs, long literal bad-string `rg` lists, or single-book rules. Fix sentence patterns, not just flagged strings.

## 校验 / Validation

修改 `catalogue.yaml` 后，确认 YAML 可解析、每条字段齐全、`type` 属于 `syntax|lexical|register|punctuation|structure|notes|bilingual|fidelity`、所有 `regex` 能被 Python `re.compile` 编译。
After editing the catalogue, confirm it parses, required fields are present, `type` is valid, and every `regex` compiles with Python `re`.

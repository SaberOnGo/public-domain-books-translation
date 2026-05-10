# 预翻译报告

## 结论

PASS。

预翻译阶段已完成四个样本：旗帜收束句、开篇身份段、冰上修雪橇段、历史称谓与公共论辩段。冰上修雪橇段 V1 因过度发挥失败，V2 因“省字式翻译”失败，V3 已通过。现在可进入正式分章翻译/重译阶段。

## 通过样本

| 样本 | 文件 | 结论 |
| --- | --- | --- |
| 旗帜收束句 | `qa/pretranslation/trial_symbolic_old_glory.md` | PASS |
| 开篇身份段 | `qa/pretranslation/trial_opening_identity.md` | PASS |
| 冰上修雪橇段 V1 | `qa/pretranslation/trial_ice_sledge_repair.md` | FAIL |
| 冰上修雪橇段 V2 | `qa/pretranslation/trial_ice_sledge_repair_v2.md` | FAIL |
| 冰上修雪橇段 V3 | `qa/pretranslation/trial_ice_sledge_repair_v3.md` | PASS |
| 历史称谓与公共论辩段 | `qa/pretranslation/trial_historical_terms.md` | PASS |

## 失败回溯规则

后续如预翻译失败：

- 如果失败是“美国国旗”替代“星条旗”这类意象判断问题，回到 `metadata/book_specific_translation_research.md` 强化本书专项规则。
- 如果失败是句子节奏、直译腔、中文不成立，回到 `translation_quality_framework/references/quality_standard.md` 强化通用质量标准。
- 如果失败只是某个句子没有打磨到位，留在 `qa/pretranslation/` 继续生成新版本。

## 本次失败与修复判断

本次失败属于预翻译阶段内部问题：V1 越界发挥，V2 又过度省字。已把“意象增强边界”和“省字式翻译警报”补入通用质量标准。V3 在不新增外来意象的前提下恢复了中文叙述气息，本阶段恢复 PASS。

## 允许进入正式翻译的条件

本阶段已满足进入正式分章翻译/重译的条件。但此前 `chapters/final/001-012` 未经过本预翻译门禁，不能视为合格终稿，必须按新规则重译或重审。

## 正式翻译必须继承的规则

1. `Old Glory` 正文译“星条旗”，关键句可用“旗影”等有画面的表达；“美国国旗”只用于译注解释。
2. 核心身份处 `Negro` 译“黑人”，不弱化为泛称。
3. `Esquimo` 暂译“爱斯基摩人”，首次出现加译注。
4. 动作段落用中文短句保留劳动节奏，不概括为“很冷”“很困难”。
5. 意象增强必须有原文依据；可以强化体感，不能凭空添加原文没有的比喻物、声音或情节。
6. 每章必须生成意象词检查和章节门禁报告，再写入 `chapters/final/`。

# 数学与天文学证明控制 / Math and Astronomy Proof Control

## 适用范围 / Scope

本文件专门约束含大量几何证明、角度计算、弦表、天文模型、图表和数值表的古典科学书。

It applies to works where a plausible sentence translation can still be technically wrong because the mathematical or astronomical structure was misunderstood.

## 核心风险 / Core Risks

- 几何证明步骤被译断。
- `设/作/连结/延长/交于/等于/相似/成比例/证毕` 等证明动作词不稳定。
- 弦表、角度、六十进制数值、比例和表格字段漂移。
- 天文模型术语混乱，例如本轮、均轮、偏心圆、等分点、黄道、赤道、黄经、赤纬。
- 古代模型被现代化解释覆盖，导致读者误以为原文使用现代天文学概念。
- 图中点、线、圆、弧、中心、方向和正文说明不一致。

## 翻译前硬门禁 / Pre-Translation Hard Gates

批量翻译前必须完成：

- `qa/technical/astronomical_model_registry.csv`
- `qa/technical/mathematical_term_lock.md`
- `qa/technical/chord_angle_calculation_policy.md`
- `qa/technical/proof_dependency_map.md`
- `qa/technical/equation_notation_registry.csv`
- `qa/technical/diagram_redraw_workflow.md`
- `npm run quality:translation`

未完成这些文件，相关章节不得进入正式翻译。
`npm run quality:translation` 是全书读者版翻译门禁，会扫描 `chapters/translated/`、`chapters/final/` 和 `frontmatter/`，拦截裸 `Eucl.`、内部六十进制记法、伪角分秒写法、十进制化风险、未注释《几何原本》依据和典型古典作图语硬译。

## 证明链规则 / Proof Rules

- 每个定义、命题、证明、推论必须记录来源位置和依赖对象。
- 证明步骤必须保留“作图动作”和“逻辑根据”的区别。
- 不得把构造步骤翻成结论。
- 不得把“由前命题可得”的依赖省略成中文顺口句。
- 若前文术语或图形标签变更，必须回查所有依赖该术语或标签的证明。
- 作图动作必须译成读者能复原图形的现代中文。古典术语若字面简短但中文不明，例如“割某线”“超过某线”，正文应明确为“交某线于某点”“交于某线延长线”等关系。
- 简洁不等于硬译，清楚也不等于啰嗦。优先使用一条现代中文证明句说明几何关系；只有当省略会导致证明链断裂时，才加解释句或章末注。
- 对《几何原本》等外部证明依据，正文保留小号依据标记，章末集中说明该命题、定义或系的大意。不得只裸写 `Eucl. VI.33` 或只写编号而不解释其作用。

## 数值规则 / Numeric Rules

- 角度、弧度、弦长、比例、半径、时间、星表和弦表字段必须进入数值校验记录。
- 六十进制数值不得未经说明改成十进制。
- 表格行列不得散文化。
- 原文、参考译本和现代校验结果不一致时，必须记录差异和取舍。
- 读者版正文中的非角度六十进制值必须保留原文结构，不得转成十进制小数；显示方式应由本书 `units_symbols_policy.md` 明确锁定，并由脚本扫描旧记法。

## 古今概念边界 / Ancient-Modern Boundary

- 正文译文优先呈现古代模型自身的说法。
- 现代解释只能放入译注、技术注或导读，不能冒充原文。
- 可以用现代术语帮助中文读者理解，但必须标明“现代说明”。
- 不能把古代几何天文学直接改写成现代物理学解释。

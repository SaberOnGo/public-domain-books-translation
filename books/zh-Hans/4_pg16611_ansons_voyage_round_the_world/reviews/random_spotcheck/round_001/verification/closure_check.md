# round_001 闭环复查 / Closure Check

status: PASS
open_p0_p1_p2_count: 0

## 定点复查

| issue | verification | result |
| --- | --- | --- |
| 外文残留 `აღარ` | `rg -n "აღარ" chapters/final chapters/translated` 无命中。 | PASS |
| Saumarez 译名不一致 | `rg -n "苏亚马雷斯|苏亚马雷兹" chapters/final chapters/translated` 无命中；抽检涉及处统一为 `苏阿马雷斯`。 | PASS |
| 破损脚注标记 `切尔西学院*`、`** 他们` | `rg -n "切尔西学院\\*|\\*\\* 他们" chapters/final chapters/translated` 无命中。 | PASS |
| 桑威奇群岛年份 | 译文改为 `1778 年首次抵达并命名；原注作 1779 年，疑误`，同时保留原注差异说明。 | PASS |

## 构建复查

- `npm run build:epub`: PASS。
- `npm run check:epub`: PASS, EPUBCheck `fatal=0`, `error=0`, `warning=0`。


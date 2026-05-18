# round_001 修复记录 / Fix Log

status: PASS

## 修复清单

| priority | source | file | fix |
| --- | --- | --- | --- |
| P1 | Agent A Sample 33 | `chapters/final/025_chapter_24_bound_for_china.md` | 将外文残留 `也 აღარ有进一步打算` 修为 `也不再有进一步打算`；同步修复 `chapters/translated/025_chapter_24_bound_for_china.md`。 |
| P2 | Agent B Samples 6/31 | `chapters/final/035_chapter_34_capture_of_the_galleon.md`; `chapters/final/028_chapter_27_landing_the_sick.md`; adjacent Saumarez mentions | 将 Saumarez 相关读者可见译名统一为 `苏阿马雷斯`；同步修复 `chapters/translated/` 对应章节。 |
| P2 | Agent B Sample 12 | `chapters/final/002_chapter_01_purpose_of_the_voyage.md` | 删除破损脚注/Markdown 标记 `切尔西学院*` 和 `** 他们`，保留后续注释段；同步修复 `chapters/translated/002_chapter_01_purpose_of_the_voyage.md`。 |
| P1 | Agent B Sample 56 | `chapters/final/023_chapter_22_manila_trade.md` | 将桑威奇群岛注释改为 `库克船长于 1778 年首次抵达并命名；原注作 1779 年，疑误`；同步修复 `chapters/translated/023_chapter_22_manila_trade.md`。 |

## 重建验证

- `npm run build:epub`: PASS；publication lint hard errors = 0。
- `npm run check:epub`: PASS；EPUBCheck `fatal=0`, `error=0`, `warning=0`。


# 《Almagest》数值校验记录 / Numeric Validation Log

numeric_validation_status: `BOOK_I10_TRIAL_NUMERIC_CONTROL_PASS__BOOK_I_CONTROLS_OPEN`

| id | scope | value_or_table | required_check | status | notes |
|---|---|---|---|---|---|
| I.11-chord-table | Book I.11 | chord table | Re-key table from source, validate sexagesimal entries, compare first/middle/last rows, and keep table separate from prose translation. | OPEN | No AI-generated table may be accepted without manual/numeric checksum. |
| I.13-ecliptic-arc-table | Book I.13 | ecliptic/equator arc table | Re-key and validate all degree/minute values; record interpolation rule if present. | OPEN | Do not modernize values silently. |
| I.15-obliquity | Book I.15 | obliquity value | Preserve ancient value in text; add explanatory note separately if modern comparison is useful. | OPEN | Translator note must not rewrite the original claim. |
| sample-001-proof | Book I.10 sample | no table value | Check whether the proof translation preserves ratio, equality, and construction dependency. | PENDING_REVIEW | See `qa/pretranslation/samples/book_i_math_proof_sample_001.md`. |
| I.10-sexagesimal-method | Book I.10 | circumference `τξ`; diameter `ρκ`; half-degree increments; thirtieth parts of increments | Preserve sexagesimal framework and approximation language before trial translation. | PASS_FOR_TRIAL | Controlled below; not a full Book I numeric pass. |

book_i_full_numeric_validation_status: `PLANNED_NOT_COMPLETE`

| id | chapter | source_location | value_type | source_value | target_value | check_method | status | notes |
|---|---|---|---|---|---|---|---|---|
| BookI-angles | Book I | TBD | angle/sexagesimal_value | TBD | TBD | manual + possible script | TODO | must preserve original format |
| BookI-chords | Book I | TBD | chord/table_entry | TBD | TBD | table validation | TODO | formal translation blocked |

## 当前结论

Book I.10 的试译前数值控制已达到 `PASS_FOR_TRIAL_TRANSLATION`：可写一个受控 Book I.10 试译章节，但不得进入 Book I.11 弦表、不得批量翻译 Book I，也不得把本记录视为全书数值校验通过。

## Book I.10 六十进制数值控制 / Sexagesimal Controls

Audit date: `2026-05-17`

Notation rule: keep original sexagesimal values in the Chinese body. If a modern decimal or trigonometric check is useful, put it in a translator/technical note, never as a replacement for the source value.

| id | source_location | source expression | controlled Chinese form | check | status | notes |
|---|---|---|---|---|---|---|
| I10-N001 | `I_31_11`-`I_31_16` | perimeter/circumference `τξ`; diameter `ρκ` | 圆周为 `360` 分；直径为 `120` 分 | Greek numerals: `τξ=360`, `ρκ=120` | PASS_FOR_TRIAL | This defines the Book I.10 numeric scale. |
| I10-N002 | `I_32_4`-`I_32_9` | `τῆς ἑξηκοντάδος τρόπον`; approximation to sense | 六十进制法；近似到感觉上无显著差异 | policy check only | PASS_FOR_TRIAL | Preserve approximation wording such as `ἔγγιστα`; do not silently over-precision. |
| I10-N003 | `I_34_5`-`I_34_12` | `ΔΕ=30`; `ΒΔ=60`; `EB/EZ≈67;4,55`; `DZ≈37;4,55` | `ΔΕ` 为 `30` 分；`ΒΔ` 为 `60` 分；`ΕΖ` 约 `67;4,55`；`ΔΖ` 约 `37;4,55` | `sqrt(30^2+60^2)=67;4,55`; subtract `30` -> `37;4,55` | PASS_FOR_TRIAL | Supports decagon side. |
| I10-N004 | `I_34_13`-`I_34_18` | decagon chord for arc `36°`; `DZ^2≈1375;4,15`; `BZ^2≈4975;4,15` | `36°` 所对直线约 `37;4,55`；平方值按原文保留 | independent check gives close value; source rounding is accepted as ancient approximation | PASS_FOR_TRIAL | Do not "correct" source rounded square values in body. |
| I10-N005 | `I_35_1`-`I_35_6` | pentagon chord for `72°`: `70;32,3`; hexagon chord for `60°`: `60` | `72°` 所对直线约 `70;32,3`; `60°` 所对直线为 `60` | `sqrt(60^2 + 37;4,55^2) ≈ 70;32,3` | PASS_FOR_TRIAL | `60°` chord equals radius under diameter `120`. |
| I10-N006 | `I_35_7`-`I_35_16` | square chord for `90°`: `84;51,10`; triangle chord for `120°`: `103;55,23` | `90°` 所对直线约 `84;51,10`; `120°` 所对直线约 `103;55,23` | `60*sqrt(2)=84;51,10`; `60*sqrt(3)=103;55,23` | PASS_FOR_TRIAL | Keep source square relations before modern formula note. |
| I10-N007 | `I_36_1`-`I_36_8` | complement of `36°` to semicircle: `144°`; chord `114;7,37` approximately | `144°` 所对直线约 `114;7,37` | `sqrt(120^2 - (37;4,55)^2) ≈ 114;7,36/37` | PASS_FOR_TRIAL | Difference at final second is rounding tolerance. |
| I10-N008 | `I_39_1`-`I_40_21` | from `60°` and `72°` get `12°`; halving gives `6°`, `3°`, `1°30'`, `0°45'` | Preserve arc sequence and half-arc method | dependency check with proof map | PASS_FOR_TRIAL | No table row belongs here. |
| I10-N009 | `I_41_1`-`I_41_3` | `1°30'` chord `1;34,15`; `0°45'` chord `0;47,8` | `1°30'` 所对直线约 `1;34,15`; `0°45'` 所对直线约 `0;47,8` | modern check: `1;34,15` and `0;47,7/8` depending rounding | PASS_FOR_TRIAL | Preserve source `0;47,8`; note only if needed. |
| I10-N010 | `I_45_9`-`I_46_14` | `0°45'`, `1°`, `1°30'`; bound `1;2,50`; half-degree chord `0;31,25` | `1°` 所对直线约 `1;2,50`; `0°30'` 所对直线约 `0;31,25` | modern check: `1°` chord `1;2,50`; `0°30'` chord `0;31,25` | PASS_FOR_TRIAL | Depends on ratio inequality lemma; preserve bracketing logic. |
| I10-N011 | `I_47_1`-`I_47_21` | `45` rows, half-degree increments, thirtieth part of each increment | State that the actual chord table begins after I.10, in Book I.11 | page boundary and source marker check | PASS_FOR_TRIAL | Viewer page `28` / printed page `48` starts Book I.11 chord table; do not include it in I.10 trial translation. |

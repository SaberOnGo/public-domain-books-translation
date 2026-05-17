# 《Almagest》证明依赖图 / Proof Dependency Map

proof_dependency_status: `BOOK_I10_TRIAL_DEPENDENCIES_MAPPED`

## 规则

- 预翻译样本涉及证明时，必须先补本图。
- 正式翻译前，Book I 定义、命题、证明、推论必须有依赖记录。
- 本文件当前只完成 Book I.10 试译级依赖图；不得据此进入全书翻译。

## Book I.10 Trial Dependency Map

| id | chapter | source_location | statement_type | depends_on | summary | status | notes |
|---|---|---|---|---|---|---|---|
| I.10-setup-sexagesimal | Book I.10 | `I_31_9`-`I_32_9` | method policy | N/A | Circumference divided into `360` parts, diameter into `120` parts; calculations use sexagesimal approximations. | PASS_FOR_TRIAL | Controls numeric wording before any proof translation. |
| I.10-decagon-pentagon-setup | Book I.10 | `I_32_10`-`I_32_22` | construction | I.10-setup-sexagesimal | Constructs semicircle `ΑΒΓ`, diameter `ΑΔΓ`, center `Δ`, perpendicular `ΔΒ`, midpoint `Ε`, and lines `ΕΒ`, `ΕΖ`, `ΖΒ`. | PASS_FOR_TRIAL | Figure `I.10.fig.01`; labels audited in diagram audit. |
| I.10-decagon-golden-section | Book I.10 | `I_33_1`-`I_33_17` | proof | Eucl. II.6; Eucl. I.47; Eucl. VI def.3; Eucl. XIII.9; Eucl. IV.15 coroll.; I.10-decagon-pentagon-setup | Shows `ΖΓ` cut in extreme and mean ratio at `Δ`; therefore `ΔΖ` equals the side of the decagon in the same circle. | PASS_FOR_TRIAL | Preserve rectangle/square relations; do not translate as a modern algebra derivation only. |
| I.10-pentagon-side | Book I.10 | `I_33_18`-`I_34_4` | proof | Eucl. XIII.10; Eucl. I.47; I.10-decagon-golden-section | Shows `ΒΖ` equals the side of the pentagon by combining hexagon and decagon side squares. | PASS_FOR_TRIAL | Depends on `ΒΔ` as radius/hexagon side and `ΔΖ` as decagon side. |
| I.10-primary-chord-values | Book I.10 | `I_34_5`-`I_36_8` | numerical derivation | I.10-setup-sexagesimal; I.10-decagon-golden-section; I.10-pentagon-side | Derives chord values for `36°`, `72°`, `60°`, `90°`, `120°`, and complement to `144°`. | PASS_FOR_TRIAL | Numeric details are controlled in `numeric_validation_log.md`; keep `ἔγγιστα` as approximation. |
| I.10-cyclic-quadrilateral-lemma | Book I.10 | `I_36_13`-`I_37_18` | lemma/proof | Eucl. III.21; Eucl. VI.4; Eucl. VI.16; Eucl. II.1 | For cyclic quadrilateral `ΑΒΓΔ`, proves `ΑΓ·ΒΔ = ΑΒ·ΔΓ + ΑΔ·ΒΓ`. | PASS_FOR_TRIAL | Figure `I.10.fig.02`; this is the local proof form of Ptolemy's theorem. |
| I.10-difference-of-arcs | Book I.10 | `I_37_19`-`I_39_3` | construction/proof | I.10-cyclic-quadrilateral-lemma; I.10-complement-rule from `I_35_17`-`I_36_8` | Given two arcs and their subtending straight lines, obtains the straight line subtending their difference; example: `60°` and `72°` give `12°`. | PASS_FOR_TRIAL | Figure `I.10.fig.03`; translation must preserve "difference" relation, not only result. |
| I.10-half-arc-lemma | Book I.10 | `I_39_4`-`I_40_15` | construction/proof | Eucl. III.27; Eucl. I.4; Eucl. I.26; Eucl. VI.8; I.10-complement-rule | Given a chord, constructs the chord subtending half its arc; uses `ΖΓ` as half the excess of `ΑΓ` over `ΑΒ`. | PASS_FOR_TRIAL | Figure `I.10.fig.04`; source `I_40_3` reads `ΥΓ`, controlled as `ΖΓ` from diagram/context. |
| I.10-half-arc-values | Book I.10 | `I_40_16`-`I_41_3` | numerical derivation | I.10-half-arc-lemma; I.10-difference-of-arcs; I.10-primary-chord-values | Uses halving from `12°` to obtain `6°`, `3°`, `1°30'`, and `0°45'`; records values `1;34,15` and `0;47,8` approximately. | PASS_FOR_TRIAL | Numeric check logged separately. |
| I.10-sum-of-arcs | Book I.10 | `I_41_4`-`I_42_6` | construction/proof | I.10-cyclic-quadrilateral-lemma; I.10-complement-rule | Given two successive arcs and their subtending straight lines, obtains the straight line subtending their sum. | PASS_FOR_TRIAL | Figure `I.10.fig.05`; depends on diameter `ΒΖΕ` and complements. |
| I.10-remaining-half-degree-strategy | Book I.10 | `I_42_7`-`I_43_5` | method transition | I.10-sum-of-arcs; I.10-difference-of-arcs; I.10-half-arc-values | Explains how known `1°30'` and interval operations leave only the half-degree chord to complete the half-degree table. | PASS_FOR_TRIAL | This is a method statement, not an independent proof. |
| I.10-chord-arc-ratio-lemma | Book I.10 | `I_43_6`-`I_45_8` | lemma/proof | Eucl. III.26,29; Eucl. VI.3; Eucl. VI.1; Eucl. VI.33 | Proves the larger chord has a smaller ratio to the smaller chord than the corresponding larger arc has to the smaller arc. | PASS_FOR_TRIAL | Figure `I.10.fig.06`; must preserve sector-vs-triangle comparison and ratio order. |
| I.10-one-degree-bracket | Book I.10 | `I_45_9`-`I_46_14` | numerical proof | I.10-chord-arc-ratio-lemma; I.10-half-arc-values | Brackets the 1-degree chord between bounds and accepts `1;2,50`; derives half-degree chord `0;31,25` approximately. | PASS_FOR_TRIAL | Figure `I.10.fig.07`; numeric check logged separately. |
| I.10-table-transition | Book I.10 | `I_46_15`-`I_47_21` | method/table handoff | I.10-sum-of-arcs; I.10-difference-of-arcs; I.10-one-degree-bracket | Explains use of half-degree increments and thirtieth parts of increments before the chord table begins in Book I.11. | PASS_FOR_TRIAL | No Book I.10 table should be translated as part of I.10; table starts on viewer page 28 / Book I.11. |

## Book I Full-Book Items Still Open

| id | chapter | source_location | statement_type | depends_on | summary | status | notes |
|---|---|---|---|---|---|---|---|
| BookI-definitions | Book I | TBD | definition | N/A | foundational definitions to inventory | OPEN_FOR_FULL_BOOK | required before full Book I translation |
| BookI-propositions | Book I | TBD | proposition/proof | BookI-definitions | complete Book I proof chain to map | OPEN_FOR_FULL_BOOK | not required for the limited Book I.10 trial translation |

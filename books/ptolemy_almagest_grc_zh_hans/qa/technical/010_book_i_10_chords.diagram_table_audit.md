# Book I.10 图表/表格审计 / Diagram and Table Audit

audit_status: `BOOK_I10_TRIAL_FIGURE_LABEL_AUDIT_PASS`

## Scope

- chapter_id: `010_book_i_10_chords`
- source: `chapters/src/010_book_i_10_chords.md`
- PDF facsimile: `source/facsimile/Almagest_Complete_Heiberg_1898.pdf`
- PAL range: `I_31_7` through before `I_48`
- PDF viewer range: pages `19` through `27`
- boundary check: viewer page `28` begins Book I.11 and the chord table

## Evidence

| item | path | status |
|---|---|---|
| contact sheet | `qa/technical/page_screenshots/book_i10_pdf_pages_019_028_contact_sheet.jpg` | AVAILABLE |
| page 19 | `qa/technical/page_screenshots/almagest-pdf-page-019.png` | AVAILABLE |
| page 20 | `qa/technical/page_screenshots/almagest-pdf-page-020.png` | AVAILABLE |
| page 21 | `qa/technical/page_screenshots/almagest-pdf-page-021.png` | AVAILABLE |
| page 22 | `qa/technical/page_screenshots/almagest-pdf-page-022.png` | AVAILABLE |
| page 23 | `qa/technical/page_screenshots/almagest-pdf-page-023.png` | AVAILABLE |
| page 24 | `qa/technical/page_screenshots/almagest-pdf-page-024.png` | AVAILABLE |
| page 25 | `qa/technical/page_screenshots/almagest-pdf-page-025.png` | AVAILABLE |
| page 26 | `qa/technical/page_screenshots/almagest-pdf-page-026.png` | AVAILABLE |
| page 27 | `qa/technical/page_screenshots/almagest-pdf-page-027.png` | AVAILABLE |
| page 28 | `qa/technical/page_screenshots/almagest-pdf-page-028.png` | AVAILABLE_BOUNDARY_ONLY |

## Figure Inventory

| figure_id | PDF viewer page | printed page | status | required next check |
|---|---:|---|---|---|
| I.10.fig.01 | 20 | 32 | PASS_FOR_TRIAL | trial SVG: `assets/figures/drafts/i10_fig01_decagon_pentagon.svg` |
| I.10.fig.02 | 22 | 37 | PASS_FOR_TRIAL | trial SVG: `assets/figures/drafts/i10_fig02_cyclic_quadrilateral_lemma.svg` |
| I.10.fig.03 | 23 | 38 | PASS_FOR_TRIAL | trial SVG: `assets/figures/drafts/i10_fig03_difference_of_arcs.svg` |
| I.10.fig.04 | 23 | 39 | PASS_FOR_TRIAL | trial SVG: `assets/figures/drafts/i10_fig04_half_arc.svg` |
| I.10.fig.05 | 24 | 41 | PASS_FOR_TRIAL | trial SVG: `assets/figures/drafts/i10_fig05_sum_of_arcs.svg` |
| I.10.fig.06 | 25 | 43 | PASS_FOR_TRIAL | trial SVG: `assets/figures/drafts/i10_fig06_chord_arc_ratio.svg` |
| I.10.fig.07 | 26 | 45 | PASS_FOR_TRIAL | trial SVG: `assets/figures/drafts/i10_fig07_one_degree_bracket.svg` |

## Figure Label Audit

Audit date: `2026-05-17`

Method: visual check against the stored PDF viewer screenshots plus Greek source line markers in `chapters/src/010_book_i_10_chords.md`. This is sufficient to allow one controlled Book I.10 trial translation. It is not a publication redraw approval.

| figure_id | labels visible in scan | required segments / arcs / constructions | source lines | trial-level translation control |
|---|---|---|---|---|
| I.10.fig.01 | `Α, Β, Γ, Δ, Ε, Ζ` | semicircle `ΑΒΓ`; diameter `ΑΔΓ`; center `Δ`; perpendicular `ΔΒ`; midpoint `Ε` of `ΔΓ`; joined `ΕΒ`, `ΕΖ = ΕΒ`, `ΖΒ`; conclusions `ΖΔ` side of decagon and `ΒΖ` side of pentagon | `I_32_10`-`I_34_4` | Keep point labels as Greek capitals. Do not collapse `ΖΔ`/`ΒΖ` into unlabeled "the chord"; preserve polygon-side conclusions. |
| I.10.fig.02 | `Α, Β, Γ, Δ, Ε` | cyclic quadrilateral `ΑΒΓΔ`; diagonals `ΑΓ`, `ΒΔ`; auxiliary point/line `Ε`; angle equality `∠ΔΒΓ = ∠ΑΒΕ`; rectangles/products `ΑΓ·ΒΔ`, `ΑΒ·ΔΓ`, `ΑΔ·ΒΓ` | `I_36_13`-`I_37_18` | Translate as the quadrilateral product lemma. Preserve the two triangle-comparison branches through `ΒΓΕ` and `ΑΒΕ`; do not convert to a bare modern Ptolemy theorem statement without proof steps. |
| I.10.fig.03 | `Α, Β, Γ, Δ` | semicircle `ΑΒΓΔ` on diameter `ΑΔ`; given straight lines `ΑΒ`, `ΑΓ`; joined `ΒΓ`; auxiliary `ΒΔ`, `ΓΔ`; use prior cyclic quadrilateral lemma to obtain `ΒΓ` from difference of arcs | `I_37_19`-`I_39_3` | This is the "difference of two arcs" construction. Keep `ΑΔ` as diameter and mark `ΒΔ`, `ΓΔ` as complements to the semicircle. |
| I.10.fig.04 | `Α, Β, Γ, Δ, Ε, Ζ` | semicircle `ΑΒΓ`; given `ΓΒ`; arc `ΓΒ` bisected at `Δ`; joined `ΑΒ`, `ΑΔ`, `ΒΔ`, `ΔΓ`; perpendicular `ΔΖ` to `ΑΓ`; set `ΑΕ = ΑΒ`; joined `ΔΕ` | `I_39_4`-`I_40_15` | This is the half-arc construction. Preserve `ΖΓ` as half the excess of `ΑΓ` and `ΑΒ`; note source line `I_40_3` has `ΥΓ`, controlled as `ΖΓ` by diagram and context. |
| I.10.fig.05 | `Α, Β, Γ, Δ, Ε, Ζ` | circle `ΑΒΓΔ`; diameter `ΑΔ`; center `Ζ`; successive arcs `ΑΒ`, `ΒΓ`; joined straight lines `ΑΒ`, `ΒΓ`; through `Β` diameter `ΒΖΕ`; joined `ΒΔ`, `ΔΓ`, `ΓΕ`, `ΔΕ`; conclusion `ΑΓ` given by composition | `I_41_4`-`I_42_6` | This is the "sum of two arcs" construction. Keep center `Ζ` distinct from endpoint `Ε`; preserve diameter `ΒΖΕ`. |
| I.10.fig.06 | `Α, Β, Γ, Δ, Ε, Ζ, Η, Θ` | circle `ΑΒΓΔ`; unequal chords `ΑΒ` and `ΒΓ`; angle `ΑΒΓ` bisected by `ΒΔ`; line `ΑΕΓ`; joined `ΑΔ`, `ΓΔ`; perpendicular `ΔΖ`; auxiliary circle with center `Δ` and radius `ΔΕ`, meeting/using `ΗΕΘ`; extension `ΔΖΘ` | `I_43_6`-`I_45_8` | This is the chord/arc ratio inequality lemma. Preserve auxiliary-sector labels `Η` and `Θ`; do not omit sector-vs-triangle comparison. |
| I.10.fig.07 | `Α, Β, Γ` | circle `ΑΒΓ`; unequal straight lines `ΑΒ`, `ΑΓ`; first setup uses `ΑΒ` subtending `0°45'` and `ΑΓ` subtending `1°`; second setup uses same figure with `ΑΒ` subtending `1°` and `ΑΓ` subtending `1°30'` | `I_45_9`-`I_46_14` | This is the numerical bracketing for the 1-degree chord and half-degree chord. It depends on the ratio lemma in fig.06; keep arc values in sexagesimal form. |

## Table Inventory

No Book I.10 numeric table is visible in the mapped range. Viewer page `28`, printed page `48`, begins Book I.11 and contains the chord table; this belongs to `I.11-chord-table`, not Book I.10.

## Redraw Rules

- GPT-image-2 may be used only for exploratory visual drafts.
- The publishable diagram must be reconstructed as controlled SVG/TikZ or equivalent structured vector artwork.
- Every point label, line segment, chord, arc, center, diameter, and equality/proportion relation must be checked against the Greek source and PDF screenshot.
- Redrawn figures must not modernize the proof or introduce labels not present in the source unless marked as editorial additions in notes.

## Current Gate

This audit is `PASS_FOR_TRIAL_TRANSLATION` for Book I.10 only. It does not approve final publication diagrams, final SVG/TikZ redraw, or full-book figure handling. Book I.10 may proceed to one controlled trial translation after the matching proof dependency map and sexagesimal numeric control are also PASS.

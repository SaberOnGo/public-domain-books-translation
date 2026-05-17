# 《Almagest》文本不确定性记录 / Textual Uncertainty Log

textual_uncertainty_status: `BOOK_I_RESEARCH_OPEN`

| id | location | uncertainty_type | lemma_or_source_text | witnesses_or_evidence | decision | translation_impact | status |
|---|---|---|---|---|---|---|---|
| source-download | whole work | full_source_split_not_established | N/A | Heiberg PDF downloaded; SHA256 `b5115c91265e7997236d54bb6e421eff6308ef3639681e4a6ab6bcfc37a1c32b`; PAL Greek transcription ingested as auxiliary source control | PDF facsimile and PAL auxiliary transcription preserved, but formal full-book source text and split not established | still blocks formal translation | RESOLVED_FOR_RESEARCH |
| hash-mismatch-2026-05-16 | whole work | file_history_hash | N/A | a previously noted Wikimedia SHA1 did not match local downloaded file | use local SHA256 as preservation hash until Wikimedia file history is rechecked | blocks publication, not research | OPEN |
| book-i-page-offset | Book I | page_offset | N/A | PAL/Heiberg structure located; local PDF page-image offset not visually confirmed | use only as research cut | blocks formal Book I split | OPEN |
| OCR-policy | whole work | ocr_transcription_role | N/A | no independent OCR selected; PAL transcription available as auxiliary Greek transcription | use PAL for searchable Greek control and PDF/PAL discrepancy checks; do not use English translation as OCR authority | blocks formal translation until full-book policy is recorded | OPEN |
| reference-translation-boundary | whole work | reference_witness_boundary | N/A | Toomer modern English translation is copyrighted; Taliaferro public-domain candidate not full-view verified | English translation may only prompt疑点 and summary differences; any source correction must return to PDF/PAL Greek evidence | blocks any pivot-translation workflow | RESOLVED_POLICY |
| pal-transcription-license | whole work | auxiliary_transcription_rights | N/A | PAL `LICENSE.md` checked from `pal-texts` commit `368c5f1f6555679f2d7ab84062839e921a6293cb` | CC BY 4.0 applies to Almagest transcription; use with attribution as auxiliary source control | enables trial source extraction after attribution | RESOLVED_FOR_TRIAL_SOURCE |
| BookI-variants | Book I | variant/conjecture | TBD | Heiberg apparatus to review | not reviewed | blocks Book I PASS | TODO |

## 规则

- 任何影响术语、数值、图表或证明的异文必须同步到 `qa/technical/textual_variant_log.csv`。
- `UNRESOLVED` 项存在时，不得进入 `chapters/final/`。

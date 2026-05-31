---
name: academic-professional-zh-Hans
description: Use this profile after a language-pair EPUB template when translating academic monographs, thesis-like books, or professional books into Simplified Chinese, where the translation must stay technically precise while becoming clear, natural, and reader-friendly.
---

# academic-professional-zh-Hans Profile

当一本书具有以下任一特征时，使用本 profile：

- 学术专著、论文型书籍、研究报告式章节。
- 计算机、机械、电子、生物、化学、医学、法律、政治学、经济学、社会科学等专业领域书籍。
- 含大量定义、模型、证明、统计结果、图表说明、公式、术语或长引文。
- 用户明确要求“准确表达的基础上，读得顺、有趣、不费劲”。

Use this profile for professional books where precision and readability must both be treated as quality gates.

## Overlay Order

```text
common -> {source-target} -> profiles/academic-professional-zh-Hans -> books/zh-Hans/{number}_{book_id_slug}/
```

For private-use projects, overlay `modes/private_use` last.

## Required Reading

1. `prompts/00_profile_integration_zh_Hans.md`
2. `references/academic_professional_readability_policy.md`
3. `metadata/academic_professional_style_profile.md`
4. `qa/readability/_TEMPLATE.chapter_academic_readability_audit.md`
5. The target-language framework under `template/epub_pipeline/targets/zh-Hans/`

## Required Work

- Build or revise `metadata/style_profile.md` so it names the book's professional level, intended reader, and explanation strategy.
- Keep a stable glossary for domain terms; do not paraphrase locked terms for style.
- For every chapter, run a readability audit that checks long sentences, proof/model/statistical explanation, table and figure lead-ins, quote boundaries, transitions, and source-term placement.
- For every chapter, run the chapter completion gate immediately after translation/refinement. It must check metadata, nav/TOC impact, body, notes, figures, formulas, tables, images, styles, reader-facing text, readability, terminology, comments/notes, and generated XHTML/EPUB risk.
- Fix awkward Chinese where it is not needed for precision.
- Preserve technical terms, variables, formulas, table values, citations, and necessary qualifications.
- Do not default to inline `Chinese term (source term)` in body text. Prefer footnotes, endnotes, chapter-end terminology notes, or glossary entries when the original term is useful but not immediately needed in the sentence.
- During random spot-check, use `--profile auto` or `--profile academic`; `auto` detects this profile when copied into a book project.

## Done Definition

- Every chapter has `PASS` academic readability evidence.
- Every chapter has `PASS` chapter completion gate evidence.
- No unresolved item says the reader cannot understand the argument.
- No reader-facing body text contains avoidable source-term parentheses or unexplained foreign terms.
- No professional term or formula was weakened for the sake of making the text sound casual.
- `npm run review:random-validate:pass` passes when used as part of release/private artifact closure.

## 随机抽检同类问题全书审计 / Book-Wide Similar-Issue Audit

随机抽检一旦发现任何需要修复或可能系统性复现的问题，包括但不限于 P0/P1/P2、单项 <70、读者不可理解、事实/术语/图表/公式/注释错误，或本模板硬门禁失败，主执行 AI 不得只修被抽中的样本，也不得等到第二轮才全书检查。必须先把发现归纳为问题族，再对整本读者可见书稿执行全书同类问题审计，覆盖 `chapters/final/`、frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML；修复所有确认命中，记录合理例外，并在该轮 `fix_log.md` 与 `closure_check.md` 中关闭该问题族后，才能使用新 seed 复抽。

If a random sample exposes any issue that needs correction or may recur systemically, treat it as a possible systemic defect family immediately in the current round. Audit the whole reader-facing book for similar cases, fix all confirmed matches, document justified exceptions, and close the family in the same round before a new-seed resample.

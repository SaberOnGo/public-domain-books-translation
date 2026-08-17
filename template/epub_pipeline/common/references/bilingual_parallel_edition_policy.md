# 双语对照版 EPUB 规则 / Bilingual Parallel Edition Policy

本文件定义 `edition_type: bilingual_parallel` 的成书规则。双语对照版不是目标语 EPUB 中的源语残留，也不是 lint 例外；它是一种正式读者版本，服务两个强需求：

- 读者怀疑译文时，可以就近核对源文。
- 读者想学习源语言时，可以用目标语辅助阅读。

This file defines the `edition_type: bilingual_parallel` book rules. A bilingual parallel edition is not source-language residue inside a target-language EPUB and not a lint exception. It is a first-class reader edition for source-text verification and language study.

## Edition Contract / 版本契约

- `target_only`：只输出目标语言读者版。目标语正文中的无授权源语长段通常是错误。
- `bilingual_parallel`：同时输出目标语言读者版和源语-目标语双语对照版。源语块和目标语块共同构成正式读者内容。

For `English-to-Simplified-Chinese` projects, the default is `edition_type: bilingual_parallel`: produce both the target-only Simplified Chinese EPUB and the English-Chinese bilingual parallel EPUB. This output-edition decision is independent from publication mode. Public-domain, licensed, and `private_use` projects follow the same bilingual default; publication mode only decides rights boundaries, storage location, and whether the versioned artifact is a public release or a private artifact. This is not a default translation direction for the whole repository.

对 `English-to-Simplified-Chinese` 项目，默认使用 `edition_type: bilingual_parallel`：同时输出单简体中文 EPUB 和中英双语对照 EPUB。这个输出版本决定与 `publication_mode` 解耦；公版、授权和 `private_use` 项目都使用同一双语默认值，发布模式只决定权利边界、存放目录，以及版本化产物是公开 release 还是私人 artifact。这不代表整个仓库把英译中当作默认翻译方向。

For other source-target pairs, produce `bilingual_parallel` only when the user explicitly requests it.

其他源语言和目标语言组合，只有用户明确要求时才输出 `bilingual_parallel`。

## User Prompt Sentence / 用户指定句

For non-English-to-Simplified-Chinese pairs, the concise user sentence is:

```text
请输出 edition_type: bilingual_parallel，同时生成目标语言版 EPUB 和源语言-目标语言双语对照版 EPUB。
```

## State Fields / 状态字段

The book-local `state/pipeline_state.json` must record the edition decision. Recommended shape:

```json
{
  "edition_type": "bilingual_parallel",
  "output_editions": [
    {
      "edition_type": "target_only",
      "enabled": true,
      "artifact": "output/book.epub",
      "release_artifact_suffix": ""
    },
    {
      "edition_type": "bilingual_parallel",
      "enabled": true,
      "artifact": "output/book_bilingual_parallel.epub",
      "release_artifact_suffix": "_中英双语"
    }
  ],
  "bilingual_parallel": {
    "order": "source_then_target",
    "alignment_unit": "closed_source_target_paragraph_mapping",
    "source_visibility": "full_text",
    "target_visibility": "full_text",
    "alignment_map": "qa/bilingual_parallel/alignment_map.json",
    "check_report": "output/bilingual_parallel_check.json",
    "default_for": {
      "source_language": "en",
      "target_language": "zh-Hans"
    }
  }
}
```

The versioned release/private artifact filename must use a reader-facing bilingual suffix, not the internal enum name. The suffix format is `{target language short label}{source language short label}双语`, with target language first. For English-to-Simplified-Chinese, use `_中英双语`, so a release artifact can be `林伯洛斯特的女孩_中英双语_v0.0.4.epub`.

带版本号的 release/private artifact 文件名必须使用读者可见的双语后缀，不得使用内部枚举名。后缀格式为 `{目标语言简称}{源语言简称}双语`，目标语言在前。英译简中使用 `_中英双语`，例如 `林伯洛斯特的女孩_中英双语_v0.0.4.epub`。

`edition_type: bilingual_parallel` means the book must still preserve a target-only output. It does not allow source text to be inserted into `chapters/final/` and degrade the target-only edition.

`edition_type: bilingual_parallel` 表示必须保留单目标语输出；不得把源文块塞进 `chapters/final/`，从而损害单目标语 EPUB。

Rights and publication mode are separate from the edition decision. A public or licensed project writes versioned public release artifacts under `output/release/`; a `private_use` project writes versioned local artifacts under `output/private_artifacts/`. Either mode may contain target-only and bilingual EPUB artifacts when `output_editions` enables both.

版权/发布模式与输出版本决定彼此独立。公版或授权项目把版本化公开产物写入 `output/release/`；`private_use` 项目把版本化本地产物写入 `output/private_artifacts/`。只要 `output_editions` 同时启用单目标语和双语版，两种发布模式都可以包含这两个 EPUB 产物。

## Alignment Integrity / 对齐完整性

双语分块必须以完整的源段落到目标段落映射为边界。切块大小可以上下浮动，以便刚好在段落边界结束并从新段落开始。

Hard rules:

- A reader-visible paired unit must contain material from exactly one source natural paragraph. It must never combine `S0...Sn` from multiple source natural paragraphs.
- Every visible unit has exactly one source block followed immediately by exactly one target block. The target block must completely translate that source unit.
- If a source natural paragraph is too long, split it only at complete-sentence boundaries into several short source units, and create one complete target block for each short source unit. Never split or merge by page boundaries.
- Several source natural paragraphs must never be merged into one reader-visible target paragraph. Repair or retranslate them as distinct pairs.
- Do not split a paired unit merely to hit a word-count target.
- Do not emit source paragraphs whose complete target translation is missing.
- Do not emit target paragraphs whose source counterpart is missing, except documented translator notes, editorial notes, frontmatter, or target-only supplements.

硬规则：

- 一个读者可见对齐单元只能包含一个原著自然段的内容，严禁把多个原著自然段 `S0...Sn` 合并成一个源语块。
- 每个读者可见 unit 必须恰有一个 source block，并立即跟随恰有一个 target block；target block 必须完整翻译该 source unit。
- 源自然段过长时，只能在完整句群边界内拆成多个短 source unit，并为每个短 source unit 建立一个完整 target block；不得按页面边界拆分或合并。
- 多个原著自然段不得合译成一个读者可见目标段；必须修复或重译为各自独立、紧邻的配对。
- 不得为了凑字数切断对齐关系。
- 不得输出缺少完整目标语对应的源语段落。
- 不得输出缺少源语对应的目标语段落；译者注、编辑说明、前置页或目标语补充内容必须另有记录。

Required machine-readable model:

```json
{
  "alignment_units": [
    {
      "id": "persistent-unit-uuid-1",
      "source_parent_id": "persistent-parent-uuid-1",
      "source_text": "complete short source paragraph",
      "target_text": "完整目标语短段",
      "source_sha256": "...",
      "target_sha256": "...",
      "global_order": 1
    },
    {
      "id": "persistent-unit-uuid-2",
      "source_parent_id": "persistent-parent-uuid-1",
      "source_text": "next complete sentence group from the same long natural paragraph",
      "target_text": "同一长自然段内下一完整句群的完整译段",
      "source_sha256": "...",
      "target_sha256": "...",
      "global_order": 2
    }
  ]
}
```

The default alignment map path is `qa/bilingual_parallel/alignment_map.json`. It is book-local QA evidence and must not be written back to `template/`.

默认对齐映射路径是 `qa/bilingual_parallel/alignment_map.json`。它是具体书籍工程内的 QA 证据，不得写回 `template/`。

`npm run build:bilingual` reads the canonical unit manifest and the deterministic alignment projection. Unit IDs are persistent UUIDs retained across harmless insertions; sequential paragraph numbers and source-text hashes are not durable IDs. The builder must reject duplicate IDs, missing IDs, order drift, source/target hash drift, unregistered reader text, and anything other than direct source-then-target children.

`npm run build:bilingual` 读取 canonical unit manifest 与确定性 alignment projection。unit ID 是可跨无害插入保持的 persistent UUID；顺序段号和 source-text hash 都不能充当持久 ID。构建器必须拦截重复/缺失 ID、顺序漂移、source/target hash 漂移、未注册读者文字，以及非直接 source-then-target 子节点结构。

## Reading Chunk Size / 阅读块大小

The canonical reading unit is a complete short paragraph pair, not a page or screen. Screen size and word counts are risk signals only and must never merge source natural paragraphs.

EPUB 的 canonical 阅读单位是“完整源文短段 + 完整目标短段”，不是页或屏幕。屏幕尺寸和字数只用于风险提示，绝不能据此合并原著自然段。

Advisory segmentation inside one source natural paragraph:

- Prefer complete short-paragraph units of roughly 60-160 source words for ordinary English prose, but never pad, omit, merge natural paragraphs, or cut an incomplete sentence to meet a number.
- A naturally short paragraph remains one unit; do not join it to the next paragraph.
- Dialogue, verse, notes, lists, tables, code, and quotations preserve their Markdown AST block boundary. Do not group multiple natural paragraphs into a scene-sized screen chunk.

单个原著自然段内部的建议尺寸：

- 普通英文散文优先采用约 60-160 source words 的完整短段 unit，但不得为凑数而补写、少译、跨自然段合并或切断不完整句子。
- 原著自然短段保持一个 unit，不得并入下一段。
- 对话、诗歌、注释、列表、表格、代码和引文保持 Markdown AST block 边界，不得把多个自然段按场景或屏幕大小聚成一块。

## Reader-Facing Layout / 读者版式

Default order:

```text
source chunk
target chunk

source chunk
target chunk
```

Do not add repeated visible labels such as `原文` / `译文`. Do not add chapter-opening explanatory sentences such as "本章采用原文在前，译文在后". These make the book feel like a QA artifact or textbook interface.

不要反复加入 `原文` / `译文` 标签，也不要在每章开头写“本章采用原文在前，译文在后”。这会让成书像 QA 产物或教材界面。

The target language is the primary reading text. The source language is auxiliary comparison text:

- Keep target-language blocks at normal body size, normal rhythm, and normal paragraph style.
- Make source-language blocks slightly smaller and lighter, but still readable.
- Recommended source size: `0.92em`; do not go below `0.88em`.
- Do not rely on font family, italics, or color as the only distinction.
- Avoid long-running italics. They are tiring for English and unnatural for Chinese.
- Use spacing, block structure, and restrained color/size differences. A reading system may override fonts and colors.

目标语言是主阅读文本，源语言是辅助对照文本：

- 目标语块保持正常正文字号、节奏和段落样式。
- 源语块略小、略淡，但仍必须可读。
- 源语推荐字号为 `0.92em`，不得低于 `0.88em`。
- 不得依赖字体族、斜体或颜色作为唯一区分。
- 避免长篇斜体。英文长斜体会疲劳，中文斜体不自然。
- 优先使用间距、块结构和克制的颜色/字号差异。阅读器可能覆盖字体和颜色。

Recommended CSS intent:

```css
.bitext-unit {
  margin: 0 0 1.15em;
}
.bitext-source {
  font-size: 0.92em;
  line-height: 1.5;
  color: #555;
  margin: 0 0 0.35em;
  text-indent: 0;
}
.bitext-target {
  font-size: 1em;
  line-height: 1.72;
  color: inherit;
  margin: 0;
  text-indent: 2em;
}
```

## Non-Regression Boundary / 非退化边界

The canonical target store remains the only target-language truth. `chapters/translated/` and `chapters/final/` are identical deterministic projections of it. A bilingual EPUB is a separate edition and must not weaken target-only publication lint, chapter gates, random review, or release requirements.

canonical target store 是唯一目标语事实源；`chapters/translated/` 与 `chapters/final/` 是目标文本完全一致的确定性投影。双语 EPUB 是独立版本，不得削弱单目标语 EPUB 的出版 lint、章节门禁、随机抽检或 release 要求。

Adaptive parallel orchestration may distribute canonical chapters among translation producers, but it must never assign a second producer to create a separate bilingual translation. Target-only and bilingual artifacts consume the same target unit IDs, text, order, and hashes. Independent audit consumers review that canonical target before either edition is released.

自适应并行编排可以把 canonical 章节分配给不同 translation producer，但绝不能另派一组 producer 为双语版重新翻译。单目标语和双语产物必须消费完全相同的目标 unit ID、文本、顺序和 hash；独立 audit consumer 审核的也是这份 canonical target，两个版本通过后才能发布。

Target-only and bilingual outputs may share the same translation-quality evidence for `chapters/final/`, but bilingual output requires additional checks:

- alignment map exists and covers all reader-facing bilingual body units;
- every source block has complete target correspondence;
- every target block has complete source correspondence or a documented target-only reason;
- source and target blocks have correct `lang` / `xml:lang`;
- the bilingual EPUB package metadata includes the primary source and target languages as separate `dc:language` entries;
- source text is rights-cleared for reader-facing publication;
- no repeated `原文` / `译文` labels or QA joiners enter the reader edition;
- the bilingual EPUB passes EPUBCheck, reader-facing policy checks, and `npm run check:bilingual`.

单目标语和双语输出可以共享 `chapters/final/` 的译文质量证据，但双语输出还必须额外检查：

- 对齐映射存在，并覆盖所有读者可见双语正文单元；
- 每个源语块都有完整目标语对应；
- 每个目标语块都有完整源语对应，或有目标语-only 的记录理由；
- 源语和目标语块有正确的 `lang` / `xml:lang`；
- 双语 EPUB 的 package metadata 必须把主要源语言和目标语言分别写入 `dc:language`；
- 源文具备读者可见出版权利；
- 读者版不得出现反复的 `原文` / `译文` 标签或 QA 拼接符；
- 双语 EPUB 通过 EPUBCheck、读者可见内容检查和 `npm run check:bilingual`。

## Script Gate / 脚本门禁

`npm run check:bilingual` runs `scripts/check_bilingual_parallel.py`. It is intentionally edition-driven, not copyright-mode-driven: the checker reads only `state/pipeline_state.json.edition_type`, `output_editions`, and `bilingual_parallel`. It must not decide bilingual output from `publication_mode`.

`npm run build:bilingual` runs `scripts/build_bilingual_epub.py`. It is edition-driven and is a no-op when disabled. When enabled, it builds from canonical units and their deterministic alignment projection; it must not mutate either target projection.

When the bilingual edition is disabled, the gate is a no-op PASS. When enabled, it checks:

- enabled `target_only` and `bilingual_parallel` edition entries and artifacts;
- `qa/bilingual_parallel/alignment_map.json` structure and duplicate paragraph mappings;
- bilingual EPUB OPF `dc:language` entries for source and target languages;
- bilingual XHTML `bitext-source` / `bitext-target` counts and `lang` / `xml:lang` attributes;
- absence of repeated reader-facing labels such as `原文` / `译文` and chapter layout explanations.

`npm run check:bilingual` 执行 `scripts/check_bilingual_parallel.py`。它只按输出版本状态判断，不按版权模式判断：脚本只读取 `state/pipeline_state.json.edition_type`、`output_editions` 和 `bilingual_parallel`。不得从 `publication_mode` 推断是否输出双语版。

`npm run build:bilingual` 执行 `scripts/build_bilingual_epub.py`。它同样只按输出版本状态判断；双语版未启用时直接 no-op。双语版启用时，它从源文段落、目标语段落和 `qa/bilingual_parallel/alignment_map.json` 生成独立双语 EPUB；不得修改 `chapters/final/`。

双语版未启用时，该门禁直接 PASS。双语版启用时，它检查：

- `target_only` 与 `bilingual_parallel` 两个启用版本项和产物；
- `qa/bilingual_parallel/alignment_map.json` 结构和重复段落映射；
- 双语 EPUB OPF 中源语言、目标语言的 `dc:language`；
- 双语 XHTML 的 `bitext-source` / `bitext-target` 数量，以及 `lang` / `xml:lang` 属性；
- 不得出现反复的 `原文` / `译文` 标签或每章版式说明。

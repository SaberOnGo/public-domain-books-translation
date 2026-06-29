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

- If a source block contains source paragraphs `S0...Sn`, the following target block must contain all target paragraphs that translate `S0...Sn`.
- If one source paragraph translates into several target paragraphs, all those target paragraphs must remain in the same paired target block.
- If several source paragraphs translate into one target paragraph, all those source paragraphs and the single target paragraph must remain in the same paired unit.
- Do not split a paired unit merely to hit a word-count target.
- Do not emit source paragraphs whose complete target translation is missing.
- Do not emit target paragraphs whose source counterpart is missing, except documented translator notes, editorial notes, frontmatter, or target-only supplements.

硬规则：

- 源语块包含哪些源段落，紧随其后的目标语块必须完整包含这些源段落对应的全部目标语译文。
- 一个源段落译成多个目标语段落时，这些目标语段落必须绑定在同一个目标语块内。
- 多个源段落合译成一个目标语段落时，这些源段落和该目标语段落必须绑定在同一个对齐单元内。
- 不得为了凑字数切断对齐关系。
- 不得输出缺少完整目标语对应的源语段落。
- 不得输出缺少源语对应的目标语段落；译者注、编辑说明、前置页或目标语补充内容必须另有记录。

Required machine-readable model:

```json
{
  "alignment_units": [
    {
      "id": "u0001",
      "source_paragraphs": ["s0001", "s0002"],
      "target_paragraphs": ["t0001", "t0002", "t0003"]
    },
    {
      "id": "u0002",
      "source_paragraphs": ["s0003"],
      "target_paragraphs": ["t0004", "t0005"]
    }
  ]
}
```

The default alignment map path is `qa/bilingual_parallel/alignment_map.json`. It is book-local QA evidence and must not be written back to `template/`.

默认对齐映射路径是 `qa/bilingual_parallel/alignment_map.json`。它是具体书籍工程内的 QA 证据，不得写回 `template/`。

`npm run build:bilingual` reads `chapters/src/*.md`, `chapters/final/*.md`, and the alignment map to build `output/book_bilingual_parallel.epub`. Paragraph IDs can be explicit or generated:

- explicit marker before or inside a paragraph: `<!-- id: s0001 -->`, `[id:s0001]`, or `{#s0001}`;
- generated source IDs: `s0001`, `s0002`, ... in sorted `chapters/src/*.md` paragraph order;
- generated target IDs: `t0001`, `t0002`, ... in sorted `chapters/final/*.md` paragraph order;
- local aliases: `{chapter_stem}:p0001`, `s:{chapter_stem}:p0001`, and `t:{chapter_stem}:p0001`.

For durable book production, explicit paragraph IDs are preferred because later chapter edits can change generated sequential IDs.

`npm run build:bilingual` 读取 `chapters/src/*.md`、`chapters/final/*.md` 和对齐映射，生成 `output/book_bilingual_parallel.epub`。段落 ID 可以显式标注，也可以使用生成 ID：

- 段落前或段落内显式标注：`<!-- id: s0001 -->`、`[id:s0001]` 或 `{#s0001}`；
- 源文生成 ID：按 `chapters/src/*.md` 排序后的段落顺序生成 `s0001`、`s0002`；
- 目标文生成 ID：按 `chapters/final/*.md` 排序后的段落顺序生成 `t0001`、`t0002`；
- 本地别名：`{chapter_stem}:p0001`、`s:{chapter_stem}:p0001` 和 `t:{chapter_stem}:p0001`。

正式书籍制作推荐使用显式段落 ID，因为后续章节编辑可能改变自动生成的顺序 ID。

## Reading Chunk Size / 阅读块大小

The EPUB equivalent of a print "one source page, one target page" is a reflowable "one phone-screen-ish source chunk, then one phone-screen-ish target chunk." Do not depend on fixed pages.

纸书“一页原文、一页译文”在 reflowable EPUB 中应转换为“接近一屏的源语块，然后接近一屏的目标语块”。不得依赖固定页。

Default sizing for phone reading:

- Target-language block recommendation: about 350-550 Chinese characters for Simplified Chinese prose.
- Soft lower bound: about 150-250 Chinese characters, unless a chapter, scene, poem stanza, or alignment unit naturally ends.
- Soft upper bound: about 700-900 Chinese characters, unless a single indivisible alignment unit exceeds it.
- English source block recommendation: about 150-230 words.
- Dialogue-heavy prose: group a full exchange or small scene, not each line.
- Poetry: group a stanza or complete poem unit; do not alternate source line, target line, source line, target line unless the source itself is alternating bilingual text.
- Scholarly, technical, or philosophical prose: group a complete argument unit.

手机阅读默认尺寸：

- 简体中文目标语块建议约 350-550 字。
- 软下限约 150-250 字，除非章节、场景、诗节或对齐单元自然结束。
- 软上限约 700-900 字，除非单个不可拆对齐单元已经超过。
- 英文源语块建议约 150-230 words。
- 对话密集文本按完整对话轮或小场景成块，不逐句切。
- 诗歌按诗节或完整诗歌单元成块；除非原文自身就是交替双语文本，否则不做源语一行、目标语一行的交错排法。
- 学术、技术、哲学文本按完整论点单元成块。

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

`chapters/final/` remains the target-language finished manuscript. A bilingual EPUB must be generated as a separate edition from source text, target text, and an alignment map. It must not weaken target-only publication lint, chapter gates, random review, or release requirements.

`chapters/final/` 仍然是目标语成书稿。双语 EPUB 必须作为独立版本，由源文、目标文和对齐映射生成。它不得削弱单目标语 EPUB 的出版 lint、章节门禁、随机抽检或 release 要求。

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

`npm run build:bilingual` runs `scripts/build_bilingual_epub.py`. It is also edition-driven and is a no-op when the bilingual edition is disabled. When enabled, it builds the separate bilingual EPUB from source paragraphs, target paragraphs, and `qa/bilingual_parallel/alignment_map.json`; it must not mutate `chapters/final/`.

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

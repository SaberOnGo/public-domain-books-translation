# Proper-Noun Display Policy / 专有名词显示策略

This policy controls reader-facing display of important proper nouns. It is separate from footnotes/endnotes.

本规则控制重点专有名词在读者正文中的显示方式，和脚注/尾注是两个不同功能。

## User Prompt Setting / 用户 Prompt 设置

Users may set the book-level default in a prompt:

用户可以在 prompt 中设置全书默认值：

```text
[重点专有名词(人名、地名、术语、罕见名词、音译后体验很差的名字等) 的翻译格式] 设置 = 3
```

If the user does not set it, use `3`.

用户未设置时，默认使用 `3`。

## Allowed Values / 允许值

| value | meaning |
| --- | --- |
| `1` | Translate directly into the target language. / 直接翻译成目标语言。 |
| `2` | Keep the source form and do not translate. / 保留原文不翻译。 |
| `3` | First natural body occurrence: target（source）; later use target. / 第一次正文自然出现：译名（原文），后续用译名。 |
| `4` | First natural body occurrence: target（source）; later use source. / 第一次正文自然出现：译名（原文），后续用原文。 |
| `5` | First natural body occurrence: target（source） plus an approved note marker from `references/note_marker_policy.md`; later use target. / 第一次正文自然出现：译名（原文），并使用 `references/note_marker_policy.md` 规定的合规注号；后续用译名。 |

## Scope / 适用范围

Use this only for important names whose target-language rendering needs a source-form interface:

仅对需要原文接口的重点名词使用：

- people, places, dynasties, institutions, titles, mythic names, rare terms, and culturally loaded terms;
- 人名、地名、王朝、机构、题名、神话名、罕见术语和文化负载词；
- names whose target-language transliteration feels like hard phonetic approximation and would hurt reading if used alone;
- 音译后像硬凑谐音字、单独使用会影响阅读体验的名字；
- terms where readers need the source form to disambiguate scholarship, spelling, transliteration, or competing translations.
- 读者需要原文来区分学术称法、拼写、转写或译名分歧的词。

Do not apply it mechanically to every ordinary word. Directly translatable common nouns should remain natural target-language prose.

不要机械套用到所有普通词。能自然翻译的普通名词应直接进入目标语正文。

## First Occurrence / 首次出现

Titles, subtitles, and EPUB navigation labels do not count as first body occurrences. The first occurrence rule applies only when the name first appears naturally in body prose.

标题、副标题和 EPUB 目录题名不计入正文首次出现。首次出现规则只在该名词第一次自然进入正文叙述时生效。

Title-like positions use the row's locked `subsequent_rendering` without consuming the first-body occurrence. Therefore policy `1`/`3`/`5` normally displays the target form in titles, while policy `2`/`4` displays the source form. Do not impose a Chinese-only title rule when the user selected source-form display.

标题性位置使用该行已锁定的 `subsequent_rendering`，但不消耗正文首次出现。因而策略 `1`/`3`/`5` 的标题通常显示目标语形式，策略 `2`/`4` 显示原文形式。用户选择保留原名时，不得再用“标题一律中文”覆盖用户决策。

For policy `3`, the standard zh-Hans rendering is:

策略 `3` 的简体中文标准形式为：

```text
尼禄（Nero）
```

For policy `5`, keep the proper-noun parenthetical source display and the note marker as two separate functions:

策略 `5` 中，专有名词原文括注和注号仍是两个不同功能：

```text
尼禄（Nero）[1]
尼禄（Nero）（1）
尼禄（Nero）注1
```

The note body belongs in a footnote, chapter-end note, book-end note, or another approved note layer. Do not replace it with a raw inline label such as `译注：`.

注释正文应放入脚注、章末注、书末注或其他合规注释层；不得用 `译注：` 这类裸行内标签替代。

## Repeat Source Form / 后文再次出现原文

After first occurrence, source forms may appear again only when the local passage is discussing spelling, transliteration, source-language form, or competing translations. Record the reason in `glossary/proper_nouns.csv`.

首次出现后，只有在局部段落讨论拼写、转写、原文形式或译名分歧时，才可再次显示原文。理由写入 `glossary/proper_nouns.csv`。

## Machine-Readable Register / 机器可读译表

Each book must keep important proper-noun decisions in:

每本书的重点专名决策写入：

```text
glossary/proper_nouns.csv
```

The book-level value is a default, not permission to flatten every entity into one rendering. In a mixed book, each locked row records its own `display_policy`, `display_strategy`, `first_rendering`, and `subsequent_rendering`. Stable conventional Chinese names may use policy `1`; uncommon names may use policy `2` or `4`; policy `4` may choose either `target（source）` or source-first `source（中文释义）` for the first body occurrence, but later occurrences must use the source form. The renderer validates these fields as one decision and rejects disagreements.

全书设置是默认值，不得据此把所有实体机械压成一种显示形式。混合策略书籍的每个锁定行都要分别记录 `display_policy`、`display_strategy`、`first_rendering` 与 `subsequent_rendering`。已有稳定通行中文名可用策略 `1`；罕见名称可用策略 `2` 或 `4`；策略 `4` 的正文首次形式可选 `译名（原文）`，也可选原名优先的 `source（中文释义）`，但后续必须使用原名。渲染器把这些字段作为同一个裁决校验，彼此不一致时拒绝处理。

Canonical-unit projects require entity identity and occurrence evidence. Required columns:

canonical-unit 工程必须保存实体身份和出现证据。必备列：

```csv
entity_id,source_name,target_name,category,display_policy,first_rendering,subsequent_rendering,note_required,repeat_original_allowed_when,notes,source_aliases,target_aliases,scope,status,chinese_gloss,display_strategy,first_occurrence_rule,same_name_disambiguation
```

The file is user-editable during preproduction. Before body translation, agents must complete book-wide discovery, bind every occurrence to an `entity_id`, and lock the register. If a missing high-risk name is found later, invalidate the current batch and return to discovery; do not append it while continuing the same translation batch.

该文件在预生产阶段允许用户修改。正文翻译前必须完成全书发现，把每次出现绑定到 `entity_id` 并锁定译表。正文阶段发现漏项时，必须使当前批次失效并回到发现阶段；不得一边继续翻译一边临时追加。

Canonical-unit projects must also keep `glossary/proper_noun_occurrences.csv` and a source-hash-bound `glossary/proper_noun_discovery_manifest.json`. Multiple entities may share the same `source_name`; uniqueness is enforced on `entity_id`, not spelling.

canonical-unit 工程还必须保存 `glossary/proper_noun_occurrences.csv` 和绑定全书源文哈希的 `glossary/proper_noun_discovery_manifest.json`。多个实体可以共享同一 `source_name`；唯一键是 `entity_id`，不是拼写。

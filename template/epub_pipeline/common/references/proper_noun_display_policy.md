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

Required columns:

必备列：

```csv
source_name,target_name,category,display_policy,first_rendering,subsequent_rendering,note_required,repeat_original_allowed_when,notes
```

The file is user-editable. Agents must follow it and update it when a new high-risk name is introduced.

该文件允许用户修改。Agent 必须遵守，并在新增高风险专名时更新。

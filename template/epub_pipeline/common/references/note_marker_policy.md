# Note Marker Policy / 注号格式规则

This policy controls footnote, endnote, translator-note, and editorial-note markers. It is separate from proper-noun parenthetical source display such as `尼禄（Nero）`.

本规则控制脚注、尾注、译注和编辑注的注号格式。它不同于 `尼禄（Nero）` 这类专有名词原文括注。

## Allowed Marker Families / 允许的注号体系

Use only one approved marker family per book or per clearly documented section:

每本书或每个明确记录的章节范围只能使用一种合规注号体系：

| family | examples | notes |
| --- | --- | --- |
| Square brackets / 方括号 | `[1]`, `[2]` | Good default for multilingual horizontal text. / 适合作为多语言横排默认值。 |
| Parentheses / 括号 | `(1)`, `(2)` | In Chinese body text, fullwidth `（1）` is equivalent and usually more natural. / 中文正文中，全角 `（1）` 与 `(1)` 等价，通常更自然。 |
| Note prefix / “注”字前缀 | `注1`, `注2` | Keep it numbered; do not use a raw tiny `注` label. / 必须带编号，不得只用很小的“注”字。 |

Allowed examples:

```text
尼禄（Nero）[1]
尼禄（Nero）（1）
尼禄（Nero）注1
```

## Disallowed Forms / 禁用形式

- Circled numbers or circled note labels such as `①`, `②`, `❶`, `㊟`.
- 小圆圈数字或带圈注号，例如 `①`、`②`、`❶`、`㊟`。
- Bare trailing note digits such as `……。3`.
- 裸露尾随数字注号，例如 `……。3`。
- Raw inline labels such as `译注：`, `脚注：`, `尾注：`, or `附注：`.
- 直接裸写的行内标签，例如 `译注：`、`脚注：`、`尾注：`、`附注：`。
- Mixed marker families without a documented section boundary.
- 没有记录章节边界时混用多套注号。

Every visible marker must resolve to exactly one note body, and every reader-facing note body must have a visible marker unless it is explicitly an unreferenced editorial note.

每个读者可见注号必须对应一条注释正文；每条读者可见注释正文也必须有注号，除非明确记录为无引用编辑说明。

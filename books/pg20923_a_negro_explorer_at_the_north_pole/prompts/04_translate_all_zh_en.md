# 04 全章翻译 / Translate All Chapters

【中文】
输入：chapters/src/*.md + glossary/terms.csv
输出：chapters/translated/{same_filename}.md
保持标题与段落结构一致。
强制规则：章节标题、副标题和目录题名中的人名只使用中文译名；标题中的人名不计入“正文首次出现”；英文原名必须放在正文第一次自然出现该人名的位置。
普通名词、器物名、衣物名、材料名和动作名必须译成中文；不得写成“原文词（中文释义）”。确需保留原文词时，只在首次出现处用“中文词（原文词）”。旧纸书分隔符如 `* * * * *`、`*****`、`----`、`---` 直接删除。

[EN]
Input: chapters/src/*.md + glossary/terms.csv
Output: chapters/translated/{same_filename}.md
Preserve heading and paragraph structure.
Mandatory rule: names in chapter titles, subtitles, and navigation titles must use the Chinese translated name only. A title occurrence does not count as the first body occurrence; keep the English original name at the first natural body occurrence.
Translate common nouns, object names, clothing names, material names, and action terms into Chinese. Do not write source-term-first glosses. Delete printed-book separators such as `* * * * *`, `*****`, `----`, or `---`.

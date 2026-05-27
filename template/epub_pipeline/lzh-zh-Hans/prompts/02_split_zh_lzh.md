# 02 分章与 passage 切分 / Split

## 输入

- `source/source_text_clean.*`
- `metadata/classical_chinese_source_profile.md`

## 任务

1. 按原书卷、篇、章、节或条目结构切分到 `chapters/src/`。
2. 为每个 reader-facing passage 规划稳定 id。
3. 记录原文篇名、目录短题名、页面题名和必要副标题到 `metadata/chapter_title_map.yaml`。
4. 古文段落过长时按语义、话语轮次、事件动作或论证单位拆分。
5. 不把现代题解、站点说明或版权样板切入正文。

## 输出

- `chapters/src/*.md`
- `metadata/chapter_title_map.yaml`
- `qa/textual/classical_chinese_textual_notes.md`

## 门禁

每个切分单元必须能回查到底本来源；疑难断句必须登记。

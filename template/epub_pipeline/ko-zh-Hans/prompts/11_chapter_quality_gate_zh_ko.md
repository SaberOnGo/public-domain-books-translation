# 11 章节终稿门禁 / Chapter Quality Gate

## 输入 / Input

- `chapters/src/{NNN_slug}.md`
- `chapters/translated/{NNN_slug}.md`
- `qa/fidelity/{NNN_slug}.md`
- `qa/readability/{NNN_slug}.md`
- `qa/imagery/{NNN_slug}.imagery.md`
- `qa/terminology/{NNN_slug}.md`
- `metadata/style_profile.md`
- `metadata/korean_source_profile.md`
- `qa/textual/korean_textual_notes.md`

## 任务 / Tasks

逐章判断是否可以进入终稿。

## 一票否决 / Veto

任一出现则 `FAIL`：

- 重大误译或漏译。
- 关键术语错误。
- 明显直译腔。
- 关键句只说明、不成像。
- 越界发挥。
- 省字式翻译。
- 标题错误：半截标题、目录题名过长、韩文/朝鲜文原题/读音/罗马字/解释性括注进入 EPUB 目录，或无题/编号章节被自创可见小标题。
- 标题人名错误：章节标题、副标题或目录题名中出现韩文/朝鲜文原名、读音、罗马字或括注，或把标题中的人名当作“正文首次出现”。标题只用中文译名或本书确定的中文呈现方式；必要原文信息必须放在正文第一次自然出现处、译注、术语表或书籍信息页。
- 普通名词未翻译：器物名、衣物名、材料名、动作名等普通名词仍写成 `source term（中文释义）` 或 `中文词（source term）`，而不是直接译成中文正文。
- 韩语/朝鲜语汉字词误用：字形相同但现代中文语义漂移，仍被机械照搬。
- 敬语/称谓错误：人物关系、亲疏、阶层、时代语气或叙述姿态被译错。
- 官能/暴力/心理边界错误：比原文更露骨、更猎奇、更净化，或添加原文没有的道德评语。
- 文本形态污染：底本注、编者注、输入者说明、韩国 Wikisource工作说明、OCR 注记或版权说明混入作者正文。
- 分号滥用：把韩语/朝鲜语连接关系机械处理成大量 `；`，或普通中文正文出现 ASCII `;`。
- 排版污染：中文字符之间出现连续空格、旧纸书页码目录/插图页码目录原样进入正文、出现乱码或编码污染。
- 旧纸书分隔符污染：正文中出现 `* * * * *`、`*****`、`----`、`---` 等可见分隔符。
- 随机朗读 10 句，有 2 句以上明显拗口。
- QA 文件缺失。

## 输出 / Output

- `qa/gates/{NNN_slug}.gate.md`

如果 PASS：

- 写入 `chapters/final/{NNN_slug}.md`

如果 FAIL：

- 不得写入 `chapters/final/`
- 报告必须说明回到哪个阶段：
  - 翻译阶段
  - 忠实度审校
  - 可读性/意象审计
  - 术语审校

## 状态 / State

所有章节 PASS 后：

- `status = CHAPTER_GATES_PASS`
- `chapters_reviewed = 章节数`
- `current_step = chapter_quality_gates_pass`

## 专家级与多义词硬门禁 / Expert Quality and Polysemy Hard Gate

章节进入 `chapters/final/` 前，必须确认 `qa/chapter_controls/{chapter}.control.md` 最近 PASS 轮记录 `expert_translation_skill_used: true`、`expert_level_review_status: "PASS"`、`polysemy_context_review: "PASS"`、`polysemy_unresolved_count: 0`。若后文线索推翻前文选义，或译文只是良好但未达专家级出版质量，本章 FAIL，回到翻译、译后控制或相应审校节点。

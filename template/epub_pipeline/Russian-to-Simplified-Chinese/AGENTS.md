# Russian-to-Simplified-Chinese Agent Instructions / 俄语到简体中文 Agent 指令

本文件供使用 `template/epub_pipeline/Russian-to-Simplified-Chinese/` 的 AI agent 读取。

## 强制规则

- 必须先读取仓库根目录 `AGENTS.md`、`template/epub_pipeline/README.md`、`template/epub_pipeline/common/README.md`、`template/epub_pipeline/targets/zh-Hans/quality_framework/README.md`，再读取本目录规则。
- 所有具体书籍原文、译文、QA、EPUB 输出和 metadata 只能写入 `books/zh-Hans/{number}_{目标语言书名}_{目标语言作者名}/`，不得写回本模板。
- 俄语公版项目必须记录来源、作者生卒年、原书初版/所用版本、来源站点权利声明和中国/美国/life+70 地区初步版权风险。
- 不得使用现代中文译本、现代商业删节本、盗版 EPUB 或权利不清楚的 OCR 作为底本。
- 俄语原文是底本；英译、中文介绍、百科条目只能用于理解背景和核查，不得作为转译来源。
- 面向人的重要文件必须以简体中文为主；英文或俄文可以并列用于精确标注，但不能只写英文或俄文。

## 俄语专项红线

- 不得把俄语抽象名词链硬搬成中文名词堆叠；必须改写成自然中文的动作、因果和关系。
- 不得把俄语自由词序、格关系、分词/副动词结构和插入语逐词贴译；必须先找到谓语骨架和实际施受关系，再按中文信息顺序重组。
- 不得把俄语抽象名词链按词面机械拼接成中文名词串；必须根据语境锁定读者可理解的中文表达。
- 不得忽略体貌、运动动词、反身动词、无人称结构、否定词作用域和反问语气；这些结构可能改变事实强度、人物判断和叙述距离。
- 不得把俄语长周期句逐逗号贴译；必须保留逻辑层级并拆成中文可读句群。
- 军阶、官职、社会制度、宗教/民族称呼、帝国边疆语境、身份称谓、父称/昵称和地名等词必须进入术语表，正文默认用中文译名，原词优先放脚注、章末说明或术语表。
- 涉及殖民、民族、性别、阶级、宗教或时代偏见时，忠实呈现原文语气；必要时用译注说明语境，不用现代判断替作者改写。

## 必读文件

- `references/russian_source_notes.md`
- `references/russian_title_strategy.md`
- `references/russian_to_chinese_literary_refinement.md`
- `references/translation_research_universal.md`
- `references/quality_standard.md`
- `references/quality_gate_framework.md`
- `references/stratified_random_spotcheck.md`
- `template/epub_pipeline/common/references/quality_gate_framework.md`
- `template/epub_pipeline/common/references/cover_design_policy.md`
- `template/epub_pipeline/common/references/book_info_frontmatter_policy.md`
- `template/epub_pipeline/common/references/epub_assets_figures_tables.md`
- `template/epub_pipeline/common/references/release_versioning.md`

# de-zh-Hans Agent Instructions / 德语到简体中文 Agent 指令

本文件供使用 `template/epub_pipeline/de-zh-Hans/` 的 AI agent 读取。

## 强制规则

- 必须先读取仓库根目录 `AGENTS.md`、`template/epub_pipeline/README.md`、`template/epub_pipeline/common/README.md`、`template/epub_pipeline/targets/zh-Hans/quality_framework/README.md`，再读取本目录规则。
- 所有具体书籍原文、译文、QA、EPUB 输出和 metadata 只能写入 `books/zh-Hans/{number}_{book_id_slug}/`，不得写回本模板。
- 德语公版项目必须记录来源、作者生卒年、原书初版/所用版本、来源站点权利声明和中国/美国/life+70 地区初步版权风险。
- 不得使用现代中文译本、现代商业删节本、盗版 EPUB 或权利不清楚的 OCR 作为底本。
- 德语原文是底本；英译、中文介绍、百科条目只能用于理解背景和核查，不得作为转译来源。
- 面向人的重要文件必须以简体中文为主；英文或德文可以并列用于精确标注，但不能只写英文或德文。

## 德语专项红线

- 不得把德语抽象名词链硬搬成中文名词堆叠；必须改写成自然中文的动作、因果和关系。
- 不得把德语框架结构、长前置定语、关系从句和分词结构逐词贴译；必须先找到谓语骨架，再按中文信息顺序重组。
- 不得把德语复合词按构词成分机械拼接成中文名词串；必须根据语境锁定读者可理解的中文译名。
- 不得忽略可分动词、否定词作用域、情态动词、虚拟式和被动态度；这些结构可能改变事实强度、人物判断和叙述距离。
- 不得把德语长周期句逐逗号贴译；必须保留逻辑层级并拆成中文可读句群。
- 科学技术、天文学、社会制度、殖民语境、身份称谓和火星文明设定等词必须进入术语表，正文默认用中文译名，原词优先放脚注、章末说明或术语表。
- 涉及殖民、民族、性别、阶级、宗教或时代偏见时，忠实呈现原文语气；必要时用译注说明语境，不用现代判断替作者改写。

## 必读文件

- `references/german_source_notes.md`
- `references/german_title_strategy.md`
- `references/german_to_chinese_literary_refinement.md`
- `references/translation_research_universal.md`
- `references/quality_standard.md`
- `template/epub_pipeline/common/references/quality_gate_framework.md`
- `template/epub_pipeline/common/references/cover_design_policy.md`
- `template/epub_pipeline/common/references/book_info_frontmatter_policy.md`
- `template/epub_pipeline/common/references/epub_assets_figures_tables.md`
- `template/epub_pipeline/common/references/release_versioning.md`

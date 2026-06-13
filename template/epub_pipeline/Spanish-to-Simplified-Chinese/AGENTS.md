# Spanish-to-Simplified-Chinese Agent Instructions / 西班牙语到简体中文 Agent 指令

本文件供使用 `template/epub_pipeline/Spanish-to-Simplified-Chinese/` 的 AI agent 读取。

## 强制规则

- 必须先读取仓库根目录 `AGENTS.md`、`template/epub_pipeline/README.md`、`template/epub_pipeline/common/README.md`、`template/epub_pipeline/targets/zh-Hans/quality_framework/README.md`，再读取本目录规则。
- 每一本新书必须通过 `books/scripts/create_book_project.py --source-target Spanish-to-Simplified-Chinese` 创建；脚本先复制 `common`，再覆盖本模板。具体书籍的原文、译文、QA、metadata、EPUB 输出只能写入 `books/zh-Hans/{number}_{目标语言书名}_{目标语言作者名}/`。
- 面向人的重要文件必须以简体中文为主；英文或西班牙语可以并列用于精确标注，但不能只写英文或西班牙语。
- 翻译前必须记录西班牙语来源证据、作者/匿名状态、初版/所用版本、文本形态、来源站点权利声明，以及美国、中国和 life+70 地区初步版权风险。
- 公开发布项目不得使用现代中文译本、现代校注本、商业电子书、影视/改写文本、盗版站或权利不清楚的 OCR/EPUB 作为底本或隐藏参考。
- 西班牙语原文是底本；英译、中文介绍、百科条目只能用于背景核对，不能作为转译来源。
- 每章译后必须立即执行 `qa/chapter_controls/{chapter}.control.md` 全章质量控制；发现并修复问题的轮次只能记为 `FIXED_RECHECK_REQUIRED`，必须追加新一轮整章复查，最后一轮零问题 PASS 后才可继续。
- 第一版全书 EPUB 后必须执行分层随机抽检；最终发布前必须通过 `npm run review:random-validate:pass` 并创建 `output/release/` 下的版本化 release。

## 西班牙语专项红线

- 不得把早期近代西班牙语长周期句逐逗号贴译；必须先拆清主句、插入语、让步、转折、因果和叙述推进，再重组为自然中文。
- 不得把 `vuestra merced`、`merced`、`señor`、`amo`、`escudero`、`clérigo` 等称谓和身份词随意现代化；必须按语境进入术语表并稳定处理。
- 流浪汉小说的一人称自述带有申诉、辩解、讽刺和求生机智；中文不能翻成平铺说明文，也不能为“好读”擅自替叙述者补现代心理动机。
- 宗教制度、食物、货币、官职、阶层、血统/名誉观念、旧地名和法律习俗必须进入术语表；正文默认用自然中文译名，原词优先放译注或术语表。
- 涉及时代偏见、宗教讽刺、贫穷、暴力、欺骗、性暗示或阶层羞辱时，忠实呈现原文语气；必要时用短注说明语境，不净化、不猎奇化、不加现代评判。

## 必读文件

- `references/spanish_source_notes.md`
- `references/spanish_title_strategy.md`
- `references/spanish_to_chinese_literary_refinement.md`
- `references/translation_research_universal.md`
- `references/quality_standard.md`
- `template/epub_pipeline/common/references/quality_gate_framework.md`
- `template/epub_pipeline/common/references/cover_design_policy.md`
- `template/epub_pipeline/common/references/book_info_frontmatter_policy.md`
- `template/epub_pipeline/common/references/epub_assets_figures_tables.md`
- `template/epub_pipeline/common/references/release_versioning.md`

# it-zh-Hans Agent Instructions / 意大利语到简体中文 Agent 指令

本文件供使用 `template/epub_pipeline/it-zh-Hans/` 的 AI agent 读取。

## 强制规则

- 必须先读取仓库根目录 `AGENTS.md`、`template/epub_pipeline/README.md`、`template/epub_pipeline/common/README.md`、`template/epub_pipeline/targets/zh-Hans/quality_framework/README.md`，再读取本目录规则。
- 每一本新书必须通过 `books/scripts/create_book_project.py --source-target it-zh-Hans` 创建；脚本先复制 `common`，再覆盖本模板。具体书籍的原文、译文、QA、metadata、EPUB 输出只能写入 `books/zh-Hans/{number}_{book_id_slug}/`。
- 面向人的重要文件必须以简体中文为主；英文或意大利语可以并列用于精确标注，但不能只写英文或意大利语。
- 翻译前必须记录意大利语来源证据、作者生卒年、初版/所用版本、文本形态、来源站点权利声明，以及美国、中国和 life+70 地区初步版权风险。
- 公开发布项目不得使用现代中文译本、现代校注本、商业电子书、影视改编文本、盗版站或权利不清楚的 OCR/EPUB 作为底本或隐藏参考。
- 意大利语原文是底本；英译、中文介绍、百科条目、影视剧情梗概只能用于背景核对，不能作为转译来源。
- 任何涉及殖民时代、民族称谓、宗教、性别、暴力、奴役、海盗/私掠、帝国机构或地名变迁的内容，必须忠实呈现原文语气，并用术语表/短注控制现代误读风险。
- 每章译后必须立即执行 `qa/chapter_controls/{chapter}.control.md` 全章质量控制；发现并修复问题的轮次只能记为 `FIXED_RECHECK_REQUIRED`，必须追加新一轮整章复查，最后一轮零问题 PASS 后才可继续。
- 第一版全书 EPUB 后必须执行分层随机抽检；最终发布前必须通过 `npm run review:random-validate:pass` 并创建 `output/release/` 下的版本化 release。

## 意大利语专项红线

- 不得把意大利语长周期句逐逗号贴译；必须先拆清主句、插入语、让步、转折、动作推进，再重组为自然中文。
- 不得把 `egli/ella/esso/essa/costui`、省略主语和密集指代机械译成重复人名；必须按中文阅读需要控制指代。
- 不得把冒险小说中的动作链译成动作清单。中文要顺、有现场感、有节奏，但不得新增原文没有的物体、心理或暴力强度。
- Salgari/Sandokan 类殖民冒险文本中的族群、宗教、地理和英殖民机构称谓必须进入术语表，正文默认用中文译名，原词优先放译注或术语表。
- 时代偏见必须忠实呈现并克制说明；不得净化、扩写、猎奇化或用现代立场替作者改写。

## 必读文件

- `references/italian_source_notes.md`
- `references/italian_title_strategy.md`
- `references/italian_to_chinese_literary_refinement.md`
- `references/translation_research_universal.md`
- `references/quality_standard.md`
- `template/epub_pipeline/common/references/quality_gate_framework.md`
- `template/epub_pipeline/common/references/cover_design_policy.md`
- `template/epub_pipeline/common/references/book_info_frontmatter_policy.md`
- `template/epub_pipeline/common/references/epub_assets_figures_tables.md`
- `template/epub_pipeline/common/references/release_versioning.md`

## 随机抽检同类问题全书审计 / Book-Wide Similar-Issue Audit

随机抽检一旦发现任何需要修复或可能系统性复现的问题，包括但不限于 P0/P1/P2、单项 <70、读者不可理解、事实/术语/图表/公式/注释错误，或本模板硬门禁失败，主执行 AI 不得只修被抽中的样本，也不得等到第二轮才全书检查。必须先把发现归纳为问题族，再对整本读者可见书稿执行全书同类问题审计，覆盖 `chapters/final/`、frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML；修复所有确认命中，记录合理例外，并在该轮 `fix_log.md` 与 `closure_check.md` 中关闭该问题族后，才能使用新 seed 复抽。

If a random sample exposes any issue that needs correction or may recur systemically, treat it as a possible systemic defect family immediately in the current round. Audit the whole reader-facing book for similar cases, fix all confirmed matches, document justified exceptions, and close the family in the same round before a new-seed resample.

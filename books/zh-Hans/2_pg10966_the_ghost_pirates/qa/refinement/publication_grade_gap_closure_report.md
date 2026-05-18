# 出版级查漏补缺闭环报告

## 目标来源

- `/goal`：`goal/2026-05-13_pg10966_publication_grade_gap_closure_goal.md`
- 模板依据：`template/epub_pipeline/common/PIPELINE_SPEC.md`、`template/epub_pipeline/common/references/literary_refinement_policy.md`、`template/epub_pipeline/en-zh-Hans/references/english_to_chinese_literary_refinement.md`
- 本书依据：`metadata/book_specific_translation_research.md`、`metadata/chapter_title_map.yaml`、`glossary/terms.csv`、`glossary/style_guide.md`

## 标题工程

- 终稿 `chapters/final/*.md` 的一级标题已重新对照 `metadata/chapter_title_map.yaml`。
- `004_i.md` 至 `019_xvi.md` 正文章节导航均使用“第一章”至“第十六章”；2026-05-13 二次总审确认拆章正文中存在源文真实小题，已转入 `chapter_title_map.yaml` 的页面副标题。
- `019_xvi.md` 保留 `## 附录` 与 `## 寂静之船`，因为源文存在 `APPENDIX / The Silent Ship`。
- 旧章节 QA 中出现过的副题需区分来源：源文真实小题应作为页面副标题保留；AI 自拟或未落入标题映射的题名不得进入成书。

## 术语与译注统一

已修复：

- `Jaskett` 统一为“贾斯克特”，终稿和 QA 中不再混用另一译名。
- `log-reel` 统一为“测程绳盘”，修复第 4 章相关回指中的旧误写。
- `glossary/terms.csv` 补入 `Tom`、`Jock`、`Quoin`、`Jaskett`、`Jacobs`、`Toppin`、`Mr. Tulipson`、`Mr. Grainge`、`Sangier` 和附录署名人物。
- `glossary/terms.csv` 补入 `t'gallant`、`fore royal`、`courses`、`buntline`、`gasket`、`foot-rope`、`jackstay`、`log-reel`、`crosstrees`、`jibboom`、`taffrail` 等高风险航海术语。
- `glossary/style_guide.md` 更新人名统一要求：已经进入终稿的人名必须补入术语表。

保留说明：

- `Mortzestus` 仅在正文首次自然出现处保留为“莫尔腾号（Mortzestus）”，符合本书首次出现策略。
- 署名 `J. E. G. 亚当斯` 和 `杰克·T. 埃文` 保留拉丁首字母，因为源文为签名缩写，不属于中文正文术语漂移。

## 长段落处理

- 第十六章高潮段落原超过 500 字，已按“船身倾斜 / 船首入水 / 杰索普落水逃生”三个动作阶段拆分。
- 第三章 `The Hell O! O! Chaunty` 的长块由短行号子组成，不按普通散文段落拆分；保留为诗歌/船歌格式例外。

## 出版范围清洁

- 已清理批量改写时产生的 UTF-8 BOM；原始来源证据 `source/source_text_raw.txt` 不作为出版文本清理目标。
- 后续验证应以 `frontmatter/`、`chapters/final/`、`metadata/`、生成 XHTML 和 EPUB 为出版范围。

## 当前结论

本次查漏补缺修复了实质性术语不一致和一个普通叙述长段落问题。剩余长文本为船歌格式例外；剩余拉丁字符为正文首次船名括注或附录署名缩写。

## 验证结果

- `npm run lint:publication`：PASS；`asciiSemicolon=0`、`zhSemicolon=0`、`cjkMultiSpace=0`、`mojibake=0`、`targetTitleLatinResidue=0`。
- `node scripts/refinement_check.js`：出版范围 `bomFiles=0`、`mojibakeFiles=0`、`cjkMultiSpaceFiles=0`、`zhSemicolon=0`；全局 BOM 仅在 `source/source_text_raw.txt`，保留为 raw source evidence；脚本自身包含 mojibake 检测正则，属工具代码命中。
- 标题扫描：终稿一级标题与 `metadata/chapter_title_map.yaml` 一致；EPUB XHTML 中保留源文真实小题为页面副标题，导航保持短章号。
- 术语扫描：EPUB XHTML 中无旧译名或 `log-reel` 旧误写残留。
- `npm run build:epub`：已重新生成 `output/book.epub` 和 `output/幽灵海盗.epub`。
- `npm run check:epub`：EPUBCheck `fatal=0`、`error=0`、`warning=0`。
- 最终 EPUB SHA256：`B198384764206C52CAFCF72751423204F4628F44DA9318749ABA1C8A72429D1C`。

# 18 最终输出 / Final EPUB Output

## 目的 / Purpose

在所有翻译、预制作、样章、全书制作、双 Agent 评审、回退修复都通过后，输出正本 EPUB。

## 输入 / Input

- `output/book.epub`
- `reviews/scorecards/final_quality_score.md`
- `reviews/revision_route.md`
- `output/publication_lint.json`
- `output/epubcheck.json` 或 `output/epubcheck.log`

## 最终检查 / Final Checks

必须确认：

1. EPUBCheck：fatal=0，error=0；warning 必须解释或修复。
2. EPUB 内有封面，且 OPF manifest 标记 `cover-image`。
3. 版本说明页存在，并含 `LifeBook 书坊`、译制时间、公版来源 URL、公版说明。
4. 无旧品牌名残留。
5. 标题层级、字体策略、正文排版符合 `production_spec.md`。
6. 章节标题已按 `references/chapter_title_policy.md` 和 `references/english_chapter_title_strategy.md` 检查：无半截标题、无机械破折号长链，EPUB 目录使用短题名。
7. 文件体积合理，封面和字体未异常膨胀。
8. 双 Agent 评审分数达到 PASS。
9. `output/publication_lint.json` 无硬错误；不存在分号滥用、异常连续空格、旧纸书页码目录或乱码。
10. 如本书存在系统性精修问题，`goal/` 下已有本书目标或完成记录，且可复用经验已回填到 common、zh-Hans 或 en-zh-Hans 模板。

## 输出 / Output

- `output/book.epub`
- 可选中文文件名副本：`output/{中文书名}.epub`
- `output/publication_lint.json`
- `output/final_manifest.md`

## 状态 / State

通过后：

- `state/pipeline_state.json.status = FINAL_OUTPUT_PASS`

注意：此状态还不是 `DONE`，必须进入第 19 阶段复审和经验沉淀。

# 《环球航海记》精修目标 / Literary Refinement Goal

日期：2026-05-13

## /goal 定义

在已有可构建 EPUB 的基础上，对《环球航海记》执行编辑级精修，不重新粗糙生成，而是按《黑人北极探险家》的处理经验做多轮检查、分析、修复和重新校验。

## 必须完成

- 全书静态扫描：章节数量、标题、段落完整性、长段、异常英文残留、Gutenberg 工件、mojibake、异常标点、术语风险。
- 全书“信达雅”分析：忠实、通达、文学性、历史语境、出版排版五项同时检查，不只看中文通顺。
- 重点章节精查：风暴、坏血病、韦杰号失事、派塔袭击、马尼拉大帆船、提尼安危机、澳门/广州交涉、返航和术语表。
- 重要段落精修：删除来源工件，修正明显机械句、术语不稳、叙事节奏弱、历史称谓风险。
- 按模板补齐预制作规格、封面和书籍首页信息。
- 译者/译制者统一为 `LifeBook 书坊 SaberOnGo`；后续默认格式为 `LifeBook 书坊 + 个人名`。
- 重建 `output/book.epub` 和 `output/环球航海记.epub`，并通过 `publication_lint` 与 `epubcheck`。

## PASS 条件

- `metadata/book.yaml`、OPF metadata、版本说明页、封面文字中译者名一致。
- `output/cover.svg` 存在，封面文字可读，并随 EPUB 打包。
- `preproduction/stage1/production_spec.md` 明确 PASS。
- `qa/refinement/` 下有全书静态检查、信达雅分析、重点章节复核和修复记录。
- `output/publication_lint.json` 无硬错误。
- `output/epubcheck.json` 为 fatal=0、error=0、warning=0。

## 质量口径

“信”优先于润色，事实、时间、船名、地名、数量、动作链不得错。“达”要求中文自足，避免英文句法拖拽。“雅”不是文言化，而是准确、节制、有海上远征现场感。涉及殖民战争和旧时代对中国/西班牙/当地居民的评价时，保留原文历史视角，但不扩大为现代判断。

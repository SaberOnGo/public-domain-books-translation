# 非公版私人自用翻译执行 Prompt：没有语言方向模板

适用场景：用户提供本地电子书/文本文件，明确声明“仅个人学习自用、不传播、不商业使用”，但仓库里还没有对应语言方向模板，例如想做 `French-to-Simplified-Chinese`，而 `template/epub_pipeline/French-to-Simplified-Chinese/` 不存在。

这个 prompt 允许创建可复用的语言方向模板并提交到 GitHub，但具体非公版书籍工程必须创建在 `books/private/{target}/{number}_{目标语言书名}_{目标语言作者名}/` 下。`books/private/` 被 Git 忽略，里面的原文、译文、QA、EPUB 和 book-specific metadata 不得发布到 GitHub。

用户入口必须包含：

- 我要翻译的书：`{本地文件路径；可附书名、作者}`
- 目标语言：`{例如 简体中文 / English / 日本語 / Español}`
- 私人自用声明：`仅供个人学习自用；不传播；不用于商业。`

把上面内容和下面 prompt 一起发给 AI Agent。

```text
你是在 public-domain-books-translation 仓库内工作的 EPUB 私人自用翻译 Agent。

这是非公版私人自用任务，不是公开发布任务。用户已提供本地书源，并声明仅供个人学习自用、不传播、不用于商业。你可以创建或修改可复用的语言方向模板、脚本和配置；但该书的原文、译文、QA、EPUB 输出和 book-specific metadata 必须只写入被 Git 忽略的 `books/private/`。

用户入口：
- 我要翻译的书：{用户填写的本地文件路径、书名、作者}
- 目标语言：{用户填写}
- 私人自用声明：仅供个人学习自用；不传播；不用于商业。

第一阶段：读取规则与确认缺口

1. 第一件事必须读取仓库根目录 `AGENTS.md`。
2. 读取 common、目标语言框架和现有语言方向模板作为结构参考：
   - `template/epub_pipeline/README.md`
   - `template/epub_pipeline/common/README.md`
   - `template/epub_pipeline/common/PIPELINE_SPEC.md`
   - `template/epub_pipeline/common/metadata/rights_checklist.md`
   - `template/epub_pipeline/common/metadata/source_evidence.md`
   - `template/epub_pipeline/common/metadata/private_use_declaration.md`
   - `template/epub_pipeline/common/references/` 中与来源、版权、封面、book-info、图表资产、质量门禁、随机抽检、release 有关的文件
   - `template/epub_pipeline/common/prompts/08a_chapter_post_translation_control.md`
   - `template/epub_pipeline/common/prompts/16a_stratified_random_spotcheck.md`
   - `skills/translation-quality-defect-families/SKILL.md`
   - `template/epub_pipeline/modes/private_use/README.md`
   - `template/epub_pipeline/modes/private_use/references/private_use_cover_policy.md`
   - `template/epub_pipeline/modes/private_use/references/private_use_frontmatter_policy.md`
   - `template/epub_pipeline/modes/private_use/references/private_use_artifact_policy.md`
   - 匹配的 `template/epub_pipeline/targets/{target}/`
   - 至少一个现有语言方向模板，例如 `English-to-Simplified-Chinese`、`Japanese-to-Simplified-Chinese`、`Ancient-Greek-to-Simplified-Chinese`，只用于学习目录结构，不得照搬源语言规则
3. 根据本地文件、书名、作者和目标语言，自动判断源语言、目标语言标签、语言方向模板名和目录名。目录名必须使用目标语言书名和目标语言作者名。
4. 确认 `template/epub_pipeline/{language-pair-template}` 不存在。若已存在，改用 `doc/public/user_prompt/book_translation_private_existing_template.md`。
5. 如果 `template/epub_pipeline/targets/{target}/` 不存在，先停止并报告需要创建目标语言质量框架；不能把 `zh-Hans` 规则当默认规则。

第二阶段：创建最小语言方向模板

6. 在 `template/epub_pipeline/{language-pair-template}/` 创建可复用语言方向模板。模板、脚本和配置可以发布到 GitHub。
7. 模板只放可复用规则，不得放该非公版书的原文、译文、QA、EPUB、release 或 book-specific metadata。
8. 可参考现有模板的目录骨架，但必须逐项改写为当前 `{source} -> {target}` 的真实规则；不得留下其他语言方向的继承残留。
9. 语言方向模板的重要文件必须包含该模板贡献者预期能读懂的本地语言。英文可并列用于精确说明，但重要说明不能只用英文，除非目标贡献者语言就是英文。
10. 若需要源语言专项脚本、数据或探索文件，放到 `research/{language-pair-template}/...` 或该语言方向模板内，不得放仓库根目录。
11. 不得在脚本或 prompt 中写死 Windows 盘符、本机绝对路径或某个贡献者的工作目录。

第三阶段：创建私人书籍工程

12. 必须使用以下模式创建工程，不得创建到公开 `books/{target}/`：

```powershell
cd books
npm run new:book -- "{目标语言书名}_{目标语言作者名}" --source-target {language-pair-template} --mode private-use --local-source-file "{用户本地文件路径}" --private-use-declaration "仅供个人学习自用；不传播；不用于商业。"
```

13. 工程必须位于 `books/private/{target}/{next_number}_{目标语言书名}_{目标语言作者名}/`。如果脚本没有创建到 `books/private/`，必须停止并修正。
14. create_book_project.py 必须先复制 common，再 overlay 新语言方向模板。所有后续具体书籍文件只能写入这个私人工程目录。
15. create_book_project.py 还必须最后 overlay `template/epub_pipeline/modes/private_use/`。如果工程内缺少 `references/private_use_cover_policy.md`、`references/private_use_frontmatter_policy.md`、`references/private_use_artifact_policy.md` 或私人门禁脚本，必须停止修正。

第四阶段：私人使用边界与来源记录

16. 必须记录：
    - `metadata/private_use_declaration.md`
    - `metadata/source_evidence.md`，source type 使用 `user_provided_local_file`
    - `metadata/rights_checklist.md`，decision 使用 `PRIVATE_USE_PASS` 或 `FAIL`
    - `state/pipeline_state.json.publication_mode = private_use`
17. `metadata/private_use_declaration.md` 和读者可见首页/前置页必须写明 `仅供个人自用，不传播，不商业使用`、风险由个人承担、LifeBook书坊仅发布 LifeBook 翻译发布系统且不承担其他个人翻译、保存、传播或使用非公版内容导致的版权风险及责任。
18. 不得自动查找非公版全文，不得使用盗版站、来源不明 EPUB、现代受版权保护译本或用户没有本地访问权的材料。
19. 如果用户没有提供本地文件，必须停止；不能用本 prompt 继续。

第五阶段：完成私人书籍制作

20. 私人自用模式只改变权利和目录边界，不降低质量要求。仍必须完成 book-specific research、style profile、预翻译 PASS、小样本 PASS。
21. 分章翻译时必须执行每章译后全量检查闭环。每章写入 `chapters/translated/{chapter}.md` 后，必须立即对照整章原文和整章译文检查并修复，覆盖忠实度、漏译误译、目标语言顺读、文学性、可读性和吸引力、术语稳定、专名/案例/标题一致性、标题/小标题、注释、图表/公式/表格/图片文字接口、源语言句法残留、过硬过直句、过度解释、无依据加戏、读者可见 AI/制作痕迹、乱码/异常空格和旧纸书残留。只要发现任何问题，该轮只能记录为 `FIXED_RECHECK_REQUIRED`，不能 PASS；必须追加新一轮整章复查，直到最新一轮零问题 PASS。只有章节 control 和章节 gate 都 PASS 的章节才能进入 `chapters/final/`。
22. 若任一章节检查、审校、抽检或修订发现可复现译文质量问题族，必须使用 `skills/translation-quality-defect-families/SKILL.md`：先在本私人工程记录发现方式、归纳、低 token 同类审计、修复、例外和复查；用 `rg`、术语表、禁用写法、标题表、章节控制记录和小上下文原文对照收集候选，只把候选片段交给 agent 复核；书内闭环后只把可复用且不暴露私人内容的通用经验合并进该 skill。
23. 完成 `preproduction/stage1/production_spec.md`、样章 EPUB、全书 EPUB。私人自用封面底部只写 `个人学习版`，不得放长版权声明；私人首页/前置页不得写公版说明，制作标识必须使用 `参考LifeBook书坊 个人自制`。
24. 构建和发布前清理或重建 staging 输出，避免旧 XHTML、链接或资产污染新门禁。
25. 必须运行并通过：
    - `npm run build:epub`
    - `npm run check:epub`
    - `npm run lint:publication` 或等价 publication lint
    - `npm run lint:assets` 或等价 asset manifest check
    - `npm run preflight:template`
    - `npm run preflight:private-use`
    - `npm run cover:check`
    - `npm run reader:private-check`
26. 第一版全书 EPUB 后必须执行分层随机抽检与问题族追杀，覆盖实际存在的 paragraphs、tables、figures、formulas/proof blocks、captions/notes，并保留 `reviews/random_spotcheck/round_XXX/` 下的样本、证据、Agent A/B 独立评审、fix_log、closure_check。任一样本或任一 Agent 发现 P0/P1/P2、单项 <80、读者读不懂、忠实度偏移、事实/术语/专名/标题/译注/图表/公式错误、源语言句法硬搬、无依据润饰、过度解释或加戏，必须在当轮归纳为问题族，对整本读者可见书稿执行全书同类审计，修复全部确认命中，记录合理例外，重建 EPUB，并用新 seed 追加下一轮；不得只修被抽中的样本。只有最近连续 N 个新 seed 抽检轮均 PASS（N 最小 1，默认 2，高质量译本可选 3），所有问题族关闭，且 `npm run review:random-validate:pass` 通过，才可退出抽检。
27. 抽检和修复完成后必须重新生成 EPUB，并运行 `npm run private:artifact:create` 或等价 private artifact 脚本。私人 EPUB 产物必须位于 `output/private_artifacts/`，不是公开 release，不得提交或发布到 GitHub。

第六阶段：最终报告

28. 最终报告必须包含：
    - 新建语言方向模板路径
    - 私人工程路径 `books/private/{target}/{number}_{目标语言书名}_{目标语言作者名}/`
    - 本地书源文件名和 SHA256，不要暴露不必要的本机绝对路径
    - `metadata/private_use_declaration.md` 路径
    - 私人 EPUB 产物路径
    - 验证命令与结果
    - 分层随机抽检轮次与最终 validation_report
    - 修复摘要
    - 模板回填摘要
    - 明确说明：该产物仅限个人学习自用，不得传播，不得商业使用，不得发布到 GitHub
```

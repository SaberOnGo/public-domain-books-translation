# 非公版私人自用翻译执行 Prompt：没有源语言模板

适用场景：用户提供本地电子书/文本文件，明确声明“仅个人学习自用、不传播、不商业使用”，但仓库里还没有对应语言方向模板，例如想做 `fr-zh-Hans`，而 `template/epub_pipeline/fr-zh-Hans/` 不存在。

这个 prompt 允许创建可复用的语言方向模板并提交到 GitHub，但具体非公版书籍工程必须创建在 `books/private/{target}/{number}_{slug}/` 下。`books/private/` 被 Git 忽略，里面的原文、译文、QA、EPUB 和 book-specific metadata 不得发布到 GitHub。

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
   - `template/epub_pipeline/modes/private_use/README.md`
   - `template/epub_pipeline/modes/private_use/references/private_use_cover_policy.md`
   - `template/epub_pipeline/modes/private_use/references/private_use_frontmatter_policy.md`
   - `template/epub_pipeline/modes/private_use/references/private_use_artifact_policy.md`
   - 匹配的 `template/epub_pipeline/targets/{target}/`
   - 至少一个现有语言方向模板，例如 `en-zh-Hans`、`ja-zh-Hans`、`grc-zh-Hans`，只用于学习目录结构，不得照搬源语言规则
3. 根据本地文件、书名、作者和目标语言，自动判断源语言、目标语言标签、source-target 名称和项目 slug。
4. 确认 `template/epub_pipeline/{source-target}` 不存在。若已存在，改用 `doc/public/user_prompt/book_translation_private_existing_template.md`。
5. 如果 `template/epub_pipeline/targets/{target}/` 不存在，先停止并报告需要创建目标语言质量框架；不能把 `zh-Hans` 规则当默认规则。

第二阶段：创建最小语言方向模板

6. 在 `template/epub_pipeline/{source-target}/` 创建可复用语言方向模板。模板、脚本和配置可以发布到 GitHub。
7. 模板只放可复用规则，不得放该非公版书的原文、译文、QA、EPUB、release 或 book-specific metadata。
8. 可参考现有模板的目录骨架，但必须逐项改写为当前 `{source} -> {target}` 的真实规则；不得留下其他语言方向的继承残留。
9. 语言方向模板的重要文件必须包含该模板贡献者预期能读懂的本地语言。英文可并列用于精确说明，但重要说明不能只用英文，除非目标贡献者语言就是英文。
10. 若需要源语言专项脚本、数据或探索文件，放到 `research/{source-target}/...` 或该语言方向模板内，不得放仓库根目录。
11. 不得在脚本或 prompt 中写死 Windows 盘符、本机绝对路径或某个贡献者的工作目录。

第三阶段：创建私人书籍工程

12. 必须使用以下模式创建工程，不得创建到公开 `books/{target}/`：

```powershell
cd books
npm run new:book -- {book_id_slug} --source-target {source-target} --mode private-use --local-source-file "{用户本地文件路径}" --private-use-declaration "仅供个人学习自用；不传播；不用于商业。"
```

13. 工程必须位于 `books/private/{target}/{next_number}_{slug}/`。如果脚本没有创建到 `books/private/`，必须停止并修正。
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
21. 分章翻译，完成每章译后控制、忠实度、可读性/意象、术语、章节 gate；只有 gate PASS 的章节进入 `chapters/final/`。
22. 完成 `preproduction/stage1/production_spec.md`、样章 EPUB、全书 EPUB。私人自用封面底部只写 `个人学习版`，不得放长版权声明；私人首页/前置页不得写公版说明，制作标识必须使用 `参考LifeBook书坊 个人自制`。
23. 构建和发布前清理或重建 staging 输出，避免旧 XHTML、链接或资产污染新门禁。
24. 必须运行并通过：
    - `npm run build:epub`
    - `npm run check:epub`
    - `npm run lint:publication` 或等价 publication lint
    - `npm run lint:assets` 或等价 asset manifest check
    - `npm run preflight:template`
    - `npm run preflight:private-use`
    - `npm run cover:check`
    - `npm run reader:private-check`
25. 第一版全书 EPUB 后必须执行分层随机抽检，覆盖实际存在的 paragraphs、tables、figures、formulas/proof blocks、captions/notes，并保留 `reviews/random_spotcheck/round_XXX/` 下的样本、证据、Agent A/B 独立评审、fix_log、closure_check。
26. 抽检和修复完成后必须重新生成 EPUB，并运行 `npm run private:artifact:create` 或等价 private artifact 脚本。私人 EPUB 产物必须位于 `output/private_artifacts/`，不是公开 release，不得提交或发布到 GitHub。

第六阶段：最终报告

27. 最终报告必须包含：
    - 新建语言方向模板路径
    - 私人工程路径 `books/private/{target}/{number}_{slug}/`
    - 本地书源文件名和 SHA256，不要暴露不必要的本机绝对路径
    - `metadata/private_use_declaration.md` 路径
    - 私人 EPUB 产物路径
    - 验证命令与结果
    - 分层随机抽检轮次与最终 validation_report
    - 修复摘要
    - 模板回填摘要
    - 明确说明：该产物仅限个人学习自用，不得传播，不得商业使用，不得发布到 GitHub
```

# 主控启动 Prompt / Master Start Prompt

把下面这段发给 AI，并替换变量：

- `{TEMPLATE_ROOT}`：语言方向模板目录，即 `template/epub_pipeline/Ancient-Greek-to-Simplified-Chinese`。
- `{COMMON_TEMPLATE_ROOT}`：共享模板目录，即 `template/epub_pipeline/common`。
- `{PROJECT_ROOT}`：复制模板后的具体书籍工程目录，默认格式为 `books/zh-Hans/{number}_{目标语言书名}_{目标语言作者名}`。
- `{SOURCE_URL}`：古希腊文公版或授权来源 URL。私人自用模式可为空。
- `{LOCAL_SOURCE_FILE}`：可选，仅用于用户提供本地书源的 `private_use` 模式。
- `{PROFILE_ROOT}`：可选，特殊书型 profile；如果不启用，写 `NONE`。
- `{REFERENCE_TRANSLATION_URLS}`：可选，第二语言参考译本 URL 列表；如果没有，写 `NONE`。

```text
你是自动化中文 EPUB 翻译出版代理，当前语言方向是古希腊文到简体中文。

PROJECT_ROOT = {PROJECT_ROOT}
TEMPLATE_ROOT = {TEMPLATE_ROOT}
COMMON_TEMPLATE_ROOT = {COMMON_TEMPLATE_ROOT}
SOURCE_URL = {SOURCE_URL}
LOCAL_SOURCE_FILE = {LOCAL_SOURCE_FILE}
PROFILE_ROOT = {PROFILE_ROOT}
REFERENCE_TRANSLATION_URLS = {REFERENCE_TRANSLATION_URLS}

第一步：如果 PROJECT_ROOT 不存在，必须优先运行 `books/scripts/create_book_project.py` 自动创建 `books/zh-Hans/{number}_{目标语言书名}_{目标语言作者名}`，由脚本先把 COMMON_TEMPLATE_ROOT 复制到 PROJECT_ROOT，再把 TEMPLATE_ROOT 覆盖复制到 PROJECT_ROOT。若 PROFILE_ROOT 不是 NONE，再把 PROFILE_ROOT 覆盖复制到 PROJECT_ROOT。

严禁直接在 COMMON_TEMPLATE_ROOT、TEMPLATE_ROOT 或 PROFILE_ROOT 内制作具体书籍。它们是只读模板，只能作为复制来源。所有抓取、研究、翻译、QA、EPUB 输出都必须写入 PROJECT_ROOT。

必须按以下顺序读取并执行：

1. README.md
2. PIPELINE_SPEC.md
3. automation_contract.md
4. prompts/00_orchestrator_zh_grc.md

然后由 `00_orchestrator_zh_grc.md` 串联执行全部 prompts。

硬性要求：

- 先核查古希腊文原文来源、底本版本、编辑者、OCR/转写状态和版权/公版/授权状态；若用户提供本地书源并声明个人自用、不传播、不商业使用，则进入 `private_use` 模式，读取并应用 `template/epub_pipeline/modes/private_use/` 覆盖层规则，记录 `metadata/private_use_declaration.md`。公开发布权利不明确且没有私人本地书源时停止。
- 未完成模板复制，不得抓取原文。
- 必须创建 `metadata/source_witness_manifest.md`，记录底本、witness、扫描/OCR/转写状态、卷册、页码/行号或章节编号体系。
- 必须创建 `qa/textual/textual_uncertainty_log.md`，记录异文、残损、脱文、拟补、OCR 不确定处和语法歧义；若没有发现，也要明确写出无发现。
- 先完成通用翻译研究和本书专项翻译研究。
- 正式翻译前必须完成 `qa/pretranslation/pretranslation_report.md`，且结论为 PASS。
- 翻译必须从古希腊文底本出发；现代英译、法译、德译等第二语言译本只能用于理解、疑难定位、差异校对和技术核验。
- 版权状态不清楚的参考译本不得使用；仍受版权保护的参考译本不得复制措辞、注释、图表、表格或编辑结构。
- 必须记录异文、残损、OCR 不确定处、编辑者拟补和语法歧义。
- 必须按 `references/ancient_greek_textual_criticism_policy.md`、`references/ancient_greek_source_types.md`、`references/ancient_greek_reference_translation_policy.md` 和 `references/ancient_greek_names_transliteration_policy.md` 执行。
- 分章译文不得直接进入 `chapters/final`。
- 每章翻译后必须创建并执行 `qa/chapter_controls/{NNN_slug}.control.md`。
- 每章必须完成 fidelity/readability/terminology/gate 报告。
- 只有 gate PASS 的章节才可写入 `chapters/final`。
- 如果 PROFILE_ROOT 启用古典科学 profile，必须额外执行参考译本政策、术语锁定、图表/表格清单、技术审计、图表/表格审计和科学评审。
- 最终生成 `output/book.epub`。公版或授权项目把可发布版本固化到 `output/release/book_vX.X.X.epub`；`private_use` 项目把本地私人产物固化到 `output/private_artifacts/`，不得作为公开 release。
- 必须运行 epubcheck 或等价校验，fatal/error 为 0 才可进入最终输出。
- 第一版全书 EPUB 完成后必须执行分层随机抽检模块：运行确定性抽样脚本，抽样正文段落、表格、图片、公式/证明块、图注和注释，保留 `reviews/random_spotcheck/round_XXX/` 下的样本、证据、评审、修复和闭环记录，并在最终输出前通过 `npm run review:random-validate:pass`。
- 随机抽检闭环通过后必须执行版本化产物模块：公版或授权项目运行 `npm run release:create`，生成 `output/release/book_vX.X.X.epub`、中英文 `release_note_vX.X.X.md`、`release_state.json` 和 `release_index.md`；`private_use` 项目运行 `npm run private:artifact:create`，生成 `output/private_artifacts/{title}_private_vX.X.X.epub`、`private_artifact_notes.md`、`private_artifact_state.json` 和 `private_artifact_index.md`。
- 完成后必须做全阶段复审，总结经验教训，写入 retrospective，并在需要时递增模板版本。

如果需要人类审阅，只能由控制文件决定；默认 human_required=false，AI 自动执行。
```

## 随机抽检同类问题全书审计 / Book-Wide Similar-Issue Audit

随机抽检一旦发现任何需要修复或可能系统性复现的问题，包括但不限于 P0/P1/P2、单项 <80、读者不可理解、事实/术语/图表/公式/注释错误，或本模板硬门禁失败，主执行 AI 不得只修被抽中的样本，也不得等到第二轮才全书检查。必须先把发现归纳为问题族，再对整本读者可见书稿执行全书同类问题审计，覆盖 `chapters/final/`、frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML；修复所有确认命中，记录合理例外，并在该轮 `fix_log.md` 与 `closure_check.md` 中关闭该问题族后，才能使用新 seed 复抽。

若该轮发现译文质量问题族，还必须在 `fix_log.md` 填写 `translation_quality_skill_backfill: "UPDATED"` 或 `"MERGED"`、`translation_quality_skill_backfill_path: "skills/translation-quality-defect-families/SKILL.md"` 和回填摘要，并在 `closure_check.md` 填写 `translation_quality_skill_backfill_verified: true`；若仅有非译文质量问题，必须填写 `NOT_APPLICABLE` 和具体理由。

If a random sample exposes any issue that needs correction or may recur systemically, treat it as a possible systemic defect family immediately in the current round. Audit the whole reader-facing book for similar cases, fix all confirmed matches, document justified exceptions, and close the family in the same round before a new-seed resample.

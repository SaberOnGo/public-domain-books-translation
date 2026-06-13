# 主控启动 Prompt / Master Start Prompt

把下面这段发给 AI，并替换变量。

```text
你是自动化中文 EPUB 翻译出版代理。

PROJECT_ROOT = {PROJECT_ROOT}
TEMPLATE_ROOT = {TEMPLATE_ROOT}
COMMON_TEMPLATE_ROOT = {COMMON_TEMPLATE_ROOT}
SOURCE_URL = {SOURCE_URL}
LOCAL_SOURCE_FILE = {LOCAL_SOURCE_FILE}

第一步：如果 PROJECT_ROOT 不存在，必须优先运行 `books/scripts/create_book_project.py` 自动创建 `books/zh-Hans/{number}_{目标语言书名}_{目标语言作者名}`，由脚本先把 COMMON_TEMPLATE_ROOT 复制到 PROJECT_ROOT，再把 TEMPLATE_ROOT 覆盖复制到 PROJECT_ROOT。

严禁直接在 COMMON_TEMPLATE_ROOT 或 TEMPLATE_ROOT 内制作具体书籍。它们是只读模板，只能作为复制来源。所有抓取、研究、翻译、QA、EPUB 输出都必须写入 PROJECT_ROOT。

必须按以下顺序读取并执行：

1. README.md
2. PIPELINE_SPEC.md
3. automation_contract.md
4. prompts/00_orchestrator_zh_it.md

硬性要求：

- 先核查意大利语原文来源、版权/公版/授权状态、底本文字形态和现代参考材料使用边界；公开发布权利不明确且没有私人本地书源时停止。
- 未完成模板复制，不得抓取原文。
- 批量翻译前必须完成 `metadata/italian_source_profile.md`、`metadata/book_specific_translation_research.md`、`metadata/style_profile.md`、`glossary/terms.csv`。
- 正式翻译前必须完成 `qa/pretranslation/pretranslation_report.md`，且结论为 PASS。
- 分章译文不得直接进入 `chapters/final`。
- 每章翻译后必须创建并执行 `qa/chapter_controls/{NNN_slug}.control.md`；发现问题并修复的轮次不能直接 PASS，必须追加新一轮整章复查。
- 每章必须完成 fidelity/readability/imagery/terminology/gate 报告，只有 gate PASS 的章节才可写入 `chapters/final`。
- 全部章节完成后必须完成预制作、封面、书籍信息页、EPUB 构建、EPUBCheck、分层随机抽检、独立评审和版本化 release。
- 译文要优秀、可读、有中文叙述气息；不得机械直译、不得越界发挥、不得省字式翻译，不得把殖民时代称谓或冒险小说动作链处理成猎奇、净化或现代说教。

如果需要人类审阅，只能由控制文件决定；默认 human_required=false，AI 自动执行。
```

## 随机抽检同类问题全书审计 / Book-Wide Similar-Issue Audit

随机抽检一旦发现任何需要修复或可能系统性复现的问题，包括但不限于 P0/P1/P2、单项 <80、读者不可理解、事实/术语/图表/公式/注释错误，或本模板硬门禁失败，主执行 AI 不得只修被抽中的样本，也不得等到第二轮才全书检查。必须先把发现归纳为问题族，再对整本读者可见书稿执行全书同类问题审计，覆盖 `chapters/final/`、frontmatter、metadata、nav、表格、图片、公式、图注、注释和生成 EPUB 中相应 XHTML；修复所有确认命中，记录合理例外，并在该轮 `fix_log.md` 与 `closure_check.md` 中关闭该问题族后，才能使用新 seed 复抽。

若该轮发现译文质量问题族，还必须在 `fix_log.md` 填写 `translation_quality_skill_backfill: "UPDATED"` 或 `"MERGED"`、`translation_quality_skill_backfill_path: "skills/translation-quality-defect-families/SKILL.md"` 和回填摘要，并在 `closure_check.md` 填写 `translation_quality_skill_backfill_verified: true`；若仅有非译文质量问题，必须填写 `NOT_APPLICABLE` 和具体理由。

If a random sample exposes any issue that needs correction or may recur systemically, treat it as a possible systemic defect family immediately in the current round. Audit the whole reader-facing book for similar cases, fix all confirmed matches, document justified exceptions, and close the family in the same round before a new-seed resample.

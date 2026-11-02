# 按角色阅读指南 / Role-Based Reading Guide

规则读得越多，译文不会越好：每次开工强制阅读约 780 KB 规则时，翻译者的注意力被流程吃掉，最省力的合规方式变成“把记录填齐”。因此从本版起，规则按角色分发。编排者（orchestrator）读流程与门禁；被派出去翻译、对读、重写、冷读的调用，只拿完成这一件事所需的材料。

Reading more rules does not make better prose. Rules are now distributed by role: the orchestrator reads workflow and gates; delegated translation and review calls receive only what their task needs.

| 角色 / Role | 必读 / Must read | 不应收到 / Must not receive |
|---|---|---|
| 编排者 Orchestrator | `AGENTS.md`、`template/epub_pipeline/README.md`、`common/README.md`、`references/translation_method_v2.md`、`references/quality_gate_framework.md`、本书 `state/`；做前置页/封面/发布时再读对应 policy | — |
| 初译 Translation call (`prompts/30_scene_translation.md`) | 本书译者手册 `preproduction/translator_brief.md`、本段命中的术语与专名、前情摘要；可附 `skills/translation-craft-handbook/SKILL.md` 中与本段相关的小节 | release、EPUB、lint、QA 文件结构、抽检与版本规则；整张术语表；问题族 skill 全文 |
| 对读 Fidelity pass (`31`) | 原文、译文、译者手册里的假朋友/习语/称谓清单 | 风格润色要求 |
| 脱稿重写 Rewrite (`32`) | 译文、译者手册（节奏、范例、易犯毛病）、手艺手册相关小节 | 原文（防止回到原文句法）、流程规则 |
| 冷读 Cold read (`33`) | 译文 | 原文、评分表、流程规则 |
| 回译 / 成对评审 (`34`, `35`) | 对应 prompt 列出的材料；成对评审应换模型家族 | 译者的自评 |
| 前置页与封面 Front matter & cover | `cover_design_policy.md`、`book_info_frontmatter_policy.md`；书籍信息页用 `scripts/generate_book_info.py` 生成 | 正文翻译规则 |
| 发布 Release | `release_versioning.md`；门禁由脚本执行（`check_final_epub.py`、`check_bilingual_alignment.py`、`check_routed_items.py`） | — |

## 预算 / Budget

- 翻译和评审调用收到的规则性文字合计不超过约 30 KB（译者手册 ≤3000 字 + 手艺手册相关小节）。
- 机械规则（标点、注号格式、空格、分隔符、占位页、文件名）只存在于脚本里，不再写进 prompt。
- `skills/translation-quality-defect-families/SKILL.md` 是历史问题登记，不整篇加载；检测信号用 `catalogue.yaml`，写作方法用手艺手册。

- Translation and review calls receive at most about 30 KB of rule text (the brief plus relevant handbook sections).
- Mechanical rules live in scripts only. The legacy defect register is not loaded whole; use `catalogue.yaml` for signals and the craft handbook for method.

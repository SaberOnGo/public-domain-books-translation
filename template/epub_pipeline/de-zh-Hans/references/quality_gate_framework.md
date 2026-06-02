# 德语到简体中文通用质量门禁

本文是在 `template/epub_pipeline/common/references/quality_gate_framework.md` 之上的项目化补充，保留通用硬门禁的同时，补充德语方向的术语与门禁落地要求。

## 必须复用（与 common 逻辑保持一致）

- 译前必须有来源与版权证据（来源可靠性、授权/公版边界、版本证据）。
- 试译通过后才能进入整章批量生产。
- 每章必须生成 `qa/chapter_controls/{chapter}.control.md`，并在译文 `chapters/translated/{chapter}.md` 产生后立即做「每章译后全量检查并修复」。
- 该全量检查必须覆盖 metadata/nav/章节标题、正文、注释、图表公式表格图片文字接口、术语、可读性、润色与语气，不得只复查用户点名项或上一轮问题。
- 修复并复检必须留痕，失败轮次不能跳过。

## 德语方向执行约束（落地细化）

- 德语源语言干扰（长前置定语、关系从句、分词、可分动词、情态、否定作用域、虚拟式、代词回指）必须在该章 control 中有证据化说明，否则不得 `PASS`。
- 术语原词不进入正文；不得出现连续大规模 `中文译名（德语原词）`，除有明确 `forbidden_body_renderings` 外必须记录并由译注/术语表支持。
- 关键技术词、制度词、方言/方位名词应进入 `glossary/terms.csv`，并在控制轮中核对新词条与正文呈现一致性。
- 对话、讽刺、说明文混合的章节必须分层核查：语气一致性、人物差异保留、术语链不打乱叙事逻辑。

## 每章可放行条件（本模板执行口径）

- `qa/chapter_controls/{chapter}.control.md` 最近轮次需满足：
  - `scope: FULL_CHAPTER`
  - `issues_found: 0`
  - `fixes_applied: 0`
  - `unresolved_blocking_issues: 0`
  - `latest_round_status: PASS`
  - `allow_next_chapter: true`
- 任一轮出现 P0/P1/P2、读者难以理解、事实误译、术语链断裂、裸外文/制作痕迹泄漏，即使其他分数达标，均需返工并追加轮次复检。
- `qa/gates/{chapter}.gate.md`、`qa/fidelity/{chapter}.md`、`qa/readability/{chapter}.md`、`qa/terminology/{chapter}.md`、`qa/imagery/{chapter}.imagery.md` 均通过后，方可进入下一章或 `chapters/final/`。

## 与随机抽检衔接

- 全书首次 EPUB 与每次 post-EPUB 精修后必须执行分层随机抽检闭环（参见 `references/stratified_random_spotcheck.md`）。
- 至少两个独立审校 Agent 复核样本；发现缺口需先建问题族，做本书同类问题全量追查与修复，再用新 seed 复抽通过。

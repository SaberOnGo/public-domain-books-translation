# 翻译方法 v2：篇章级五遍法 / Translation Method v2: Scene-Level Five Passes

> 适用于所有语言方向。目标：成书读起来像目标语作家写的书，而不是“通过门禁的译文”。本文件只讲方法；构建、发布、记录格式以现有 references 与脚本为准。
> Applies to every language pair. Goal: the book reads as if written by a native author. This file covers method only; build, release and record formats stay in existing references and scripts.

## 1. 为什么改 / Why

- 短对齐单元翻译看不到场景，代词、称谓、节奏无法承接。 / Short alignment units hide scene context.
- 风格输入只有形容词，没有范例、称谓矩阵、习语与假朋友清单、目标节奏。 / Style input was adjectives without exemplars or lists.
- 只看目标语的润色补出了原文没有的解释。 / Target-only polish invented explanations.
- 同家族模型自评、0–100 整体打分天然虚高。 / Same-family holistic scores inflate.
- 修复只换字串，同类问题反复出现；注释要么缺失，要么写成免责声明。 / String swaps recur; notes absent or disclaimer-like.

## 2. 角色 / Roles

| 角色 Role | 职责 Responsibility | 读什么 Reads |
|---|---|---|
| 编排者 Orchestrator | 切场景、组装输入、调度各遍、计算阈值、保存证据 / slice scenes, assemble inputs, schedule, compute thresholds, store evidence | 本文件与流程文档 / this file and process docs |
| 译者 Translator（第 1 遍） | 初译 / first draft | 只读 `30` 的输入 / only `30` inputs |
| 对读审校 Fidelity reviewer（第 2 遍） | 意义错误清单 / meaning-error list | 只读 `31` 的输入 / only `31` inputs |
| 目标语编辑 Target editor（第 3 遍） | 脱稿重写 / target-only rewrite | 只读 `32` 的输入 / only `32` inputs |
| 冷读读者 Cold reader（第 4 遍） | 停顿句清单 / pause list | 只读正文 / text only |
| 回译核对 Back-translator（第 5 遍） | 意义漂移 / drift | 只读 `34` 的输入 / only `34` inputs |
| 发布评审 Release reviewer | 异构成对评审 / pairwise review | `35` 的输入 / `35` inputs |
| 用户 User | 人工锚点与意见 / human checkpoint | 开篇与随机页 / opening and random pages |

## 3. 译前准备 / Before translation

1. 源文规范化：脚注结构、章节提要、拆章脚手架行、诗行与号子分行、转录说明，先清干净再翻译。 / Normalise the source first.
2. 试译若干代表性场景，跑完五遍，做翻译腔剖面。 / Trial scenes through all five passes; profile translationese.
3. 填写 `preproduction/_TEMPLATE.translator_brief.md` → 本书 `preproduction/translator_brief.md`：范例 8–12 对、称谓矩阵、方言策略、习语与构式、假朋友与旧义项、一名一法、注释正向清单、10 条易犯毛病。每节不得留空或写套话。 / Fill the brief; no blank or boilerplate sections.
4. **人工锚点**：批量翻译前，用户阅读开篇约 2000 字 + 随机 3 页（约 15 分钟）。每条意见写入手册第 12 节，并落到某条规则、毛病或范例；必要时修改手册后重译开篇。未完成人工锚点不得开始批量翻译；用户明确放弃时如实记录。 / User reads ~2000-char opening + 3 random pages before batch translation; each comment goes into the brief. Batch translation waits for this unless the user explicitly waives it (record the waiver).

## 4. 五遍顺序 / Order of passes

每个场景（800–2000 字完整段落）依次经过：
Each scene (800–2000 characters of complete paragraphs) passes through:

| 遍 Pass | Prompt | 单一目标 Single goal | 输出 Output |
|---|---|---|---|
| 1 初译 Draft | `prompts/30_scene_translation.md` | 篇章级忠实初稿 / faithful scene draft | 逐段译文 / translation by paragraph |
| 2 对读 Fidelity | `prompts/31_source_fidelity_pass.md` | 意义错误 / meaning errors | 双引文错误清单 / error list quoting both sides |
| 3 脱稿重写 Rewrite | `prompts/32_target_only_rewrite.md` | 目标语地道化 / nativeness | 全文 + 修改清单 / text + change list |
| 4 冷读 Cold read | `prompts/33_cold_read.md` | 读者停顿点 / reader pauses | 停顿句清单或有理由的“没有” / pause list or justified "none" |
| 5 回译抽查 Back-check | `prompts/34_back_translation_check.md` | 重写后意义漂移 / drift after rewrite | 三栏比对 / three-way comparison |

- 第 4 遍按整章（或 ≥3000 字连续正文）做；其余按场景做。 / Pass 4 runs per chapter; others per scene.
- 第 3 遍后逐段算长度比；超阈值或改动过半的段落必须进入第 5 遍。 / Length-ratio check after pass 3 routes paragraphs to pass 5.
- 全书译完后做一次统稿（专名、术语、称谓、章题、注释体系），并对最后四分之一与结尾章节按开篇同等深度复核。 / After all chapters: one consolidation pass, plus full-depth review of the last quarter and ending.

## 5. 每次调用收到什么 / What each call receives

**必须收到 / Must receive**：该 prompt “输入”节列出的内容，且只限本段命中的术语行。 / Exactly the inputs listed in the prompt, matched terms only.

**不得收到 / Must NOT receive**：
- 发布、版本、封面、前置页、构建规则；
- QA 记录格式、门禁字段、`issues_found`、`PASS`、分数门槛；
- 流程文档、问题族 skill 全文、其他书的手册；
- 前几遍的结论（冷读与成对评审尤其不得看到）。

Never pass release, versioning, cover, frontmatter or build rules; QA field formats or score thresholds; process docs, full defect-family skills or other books' briefs; or earlier-pass verdicts (especially to cold read and pairwise review). Rules in a translation call get read as "write another record", not as "write better prose".

## 6. 修复成本规则 / Fix-cost rule

被点名一句时 / When a sentence is flagged:

1. 重写整句，必要时整段；不得只换同义词、改标点或让某字串零命中。 / Rewrite the sentence or paragraph; no synonym swaps, punctuation swaps or string-count closure.
2. 按**句型**做同族检索（例如“副词照搬成‘X地’”“抽象名词作主语”“分号连接两个完整句”），不按字串；命中句一起重写。 / Search the same family by sentence pattern, not string; rewrite hits together.
3. 复核范围只限：改动段 + 前后各一段 + 同族命中段，重跑第 2 遍（必要时第 5 遍）。不重审整章，不换新随机种子重跑全轮。 / Re-check only changed paragraphs, one neighbour each side and family hits.
4. 改写版与原版做一次成对比较（`35`），胜出才替换。 / Replace only if the rewrite wins pairwise.
5. 新问题若属新句型，写入手册第 11 节；若来自用户，同时写入第 12 节。 / New pattern → brief §11; user-originated → also §12.

**零问题要被怀疑 / Zero issues is suspicious**：AI 初稿章节在对读、冷读或成对评审中报告零问题，必须换一个模型家族重跑该遍；零问题本身不是放行证据。发现问题不会触发整章重审，因此如实报告的成本很低。
A zero-issue report on an AI-draft chapter triggers a re-run by another model family. Finding issues is cheap by design, so honest reporting is the rational choice.

## 7. 与现有门禁共存 / Coexistence with 08a / 16a

- **08a 每章译后全量检查**：以第 2–4 遍（及适用时第 5 遍）的原始输出作为证据，不再由同一 agent 另写结论。忠实度证据 = `31` 清单；可读性证据 = `32` 修改清单 + `33` 冷读清单；漂移证据 = `34` 比对。每条证据必须逐字引用当前成书；脚本校验引文存在。自报的 `PASS` / `issues_found` 只作索引，不作放行依据。
  08a uses raw outputs of passes 2–4 (and 5) as evidence, all with verbatim quotes checked by script; self-reported PASS fields are an index, not a release basis.
- **16a 分层随机抽检**：抽检样本必须附原文；风格问题按 `35` 的每千字密度计入，不再永远是最低优先级。
  16a samples must include the source; style errors count toward per-1000-character density.
- 本方法不改变 XLIFF 单元、哈希绑定、封存与并行编排规则；场景是翻译调用单位，对齐单位仍以原书自然段为准（见 `translation_unit_xliff_policy.md`）。
  XLIFF, hash binding, sealing and orchestration rules are unchanged; scenes are the call unit, alignment remains by source paragraph.

## 8. 模型多样性 / Model diversity

- 冷读（第 4 遍）与发布前评审（`35`）**SHOULD** 使用与译者不同的模型家族；同家族多个 agent 只算一个视角。 / Cold read and release review SHOULD use a different model family.
- 回译（第 5 遍）SHOULD 不由第 3 遍执行者完成。 / Back-translation SHOULD not be done by the pass-3 rewriter.
- 零问题重跑 MUST 换模型家族（见第 6 节）。 / Zero-issue re-runs MUST switch family.
- 宿主无法提供其他家族时，如实记录约束和实际使用的模型，不得声称已异构。参见 `ai_parallel_execution_guidance.md`。 / If unavailable, record the constraint honestly; never claim heterogeneity.

## 9. 注释 / Notes

按手册第 10 节的正向清单加注：文化项、丢失的双关、时代指涉、源文事实错误、习俗含义。确有必要的解释放进注释，不塞进正文。禁止写给审校看的免责式注释。书籍信息页承诺的注释或术语表，书里必须有。
Add notes per brief §10; explanations belong in notes, not body text; disclaimer-style notes are forbidden.

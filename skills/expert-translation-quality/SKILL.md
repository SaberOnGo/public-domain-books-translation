---
name: expert-translation-quality
description: Use when translating, reviewing, revising, random-spot-checking, or responding to reader feedback for LifeBook book projects where the output must reach expert publication quality rather than merely pass. Triggers include polysemous or context-dependent source words, ambiguous grammar, downstream-context back-checking, expert-level prose polish, chapter post-translation controls, final release reviews, private-use artifact reviews, and any translation-quality issue that requires source-supported disambiguation.
---

# Expert Translation Quality / 专家级译文质量

## Boundary / 边界

Use this skill as the execution procedure for making a translation excellent, not merely acceptable.
使用本 skill，把译文推进到专家级出版质量，而不是“基本可读”“合格”或“良好”。

This skill is procedural. It does not store every recurring bad example. When a recurring quality family is discovered, record the concrete reusable lesson in `skills/translation-quality-defect-families/SKILL.md`.
本 skill 管执行流程，不堆所有坏例。发现可复用问题族时，把具体经验回填到 `skills/translation-quality-defect-families/SKILL.md`。

Do not use this skill for format-only work such as cover assets, OPF manifest errors, local-path leaks, or EPUBCheck failures unless the issue also changes reader-facing translation quality.
纯格式问题如封面资产、OPF manifest、本机路径泄漏或 EPUBCheck 错误，不用本 skill；除非它同时影响读者可见译文质量。

## Workflow / 流程

### Evidence-bearing canonical units / 带证据的 canonical units

Perform translation and review against persistent canonical unit IDs. Each target template must cover the complete source unit and may use only locked `{{pn:entity_id}}` markers for registered names. Never repair a bilingual alignment problem by shortening the target, borrowing a neighboring paragraph, merging several source paragraphs, or hand-editing the derived translated/final files. If one sample exposes omission, addition, or neighbor-boundary contamination, define the defect family and audit all units with the same signal.

翻译与审校必须基于持久 canonical unit ID。每个 target template 必须完整覆盖该 source unit；已注册专名只能使用锁定的 `{{pn:entity_id}}` 标记。不得通过缩短译文、借用邻段、合并多个源自然段或手改派生的 translated/final 文件来“修复”双语对齐。一个样本发现少译、增译或邻段串译后，必须归纳问题族并审计全书同类 unit。

A semantic PASS is evidence, not a label. For every unit, independently record source-to-target omission, target-to-source addition, neighbor-boundary contamination, and numbers/names/negation/notes checks with non-empty evidence bound to current hashes and revisions. Then run a fresh full-chapter pass over the exact ordered unit IDs. A scalar PASS, mutable summary file, stale generation, or structural coverage ratio is insufficient.

语义 PASS 是证据，不是标签。每个 unit 都要分别记录 source-to-target 遗漏、target-to-source 增译、邻段串译、数字/专名/否定/注释检查，并给出绑定当前 hash/revision 的非空 evidence；随后对精确有序 unit ID 做一次新鲜全章复核。标量 PASS、可变总表、旧 generation 或结构覆盖率都不能放行。

### 1. Orient Before Translating / 先定向再翻译

Before translating a chapter or passage, identify:
翻译章节或段落前，先识别：

- source function, narrator or argumentative voice, and genre pressure;
  原文功能、叙述/论证声音、文类压力；
- terms, names, idioms, images, grammar, or cultural references whose meaning depends on wider context;
  依赖更大上下文判断的术语、专名、习语、意象、语法和文化信息；
- words or phrases that are polysemous in the source language or target language.
  源语或目标语中可能多义的词组。

Keep this watchlist internal during translation unless the workflow asks for a QA record. Do not put watchlist notes into reader-facing text.
翻译时内部保留观察清单即可；除非流程要求写 QA 记录，不要把观察清单写进读者正文。

The translation stage is the first owner of polysemy. Do not defer obvious or locally resolvable sense choices to later review. Before producing the translated passage, actively test each watchlist item against the current sentence, paragraph, nearby context, glossary, speaker identity, argumentative role, and any available downstream context. Resolve what can be resolved now; only mark an item unresolved when source evidence is genuinely insufficient.
翻译阶段是多义词处理的第一责任节点。不得把明显或局部上下文已能判清的选义推给后续审校。输出译文前，必须用当前句、本段、邻近上下文、术语表、说话人身份、论证功能和可用后文线索主动检验每个观察项。能当场判清的当场处理；只有源文证据确实不足时，才可标为未决。

### 2. Preserve Ambiguity Until Context Resolves It / 未决歧义先保留

If the source meaning is not yet resolved:
如果源义尚未判清：

- choose a target phrase that does not falsely narrow the meaning;
  优先选不错误收窄含义的译法；
- avoid hiding a guessed sense behind smooth prose;
  不要用顺滑句子掩盖猜测；
- mark the item for downstream-context back-check in the chapter control or review notes.
  在章节 control 或审校记录中标记后文回看。

When downstream context later disambiguates the word, return to the earlier occurrence and revise it. Later clarity must repair earlier guesses.
后文给出线索后，必须回到前文多义词位置复核并必要时修订。后文清楚时，前文猜测不能继续保留。

### 3. Run The Expert Pass / 执行专家级复核

For each chapter or sampled unit, perform these passes in order:
每章或每个抽检单元按顺序执行：

1. Target-only reading: read the target text without the source. It must sound like a finished book written by an expert target-language author or translator.
   目标语独立阅读：不看原文读译文；它必须像专家级目标语作者或译者写成的书。
2. Source fidelity pass: compare against source for facts, causal links, voice, implication, metaphor, tone, and unresolved ambiguity.
   原文忠实复核：对照事实、因果、声音、暗示、隐喻、语气和未决歧义。
3. Polysemy back-check: revisit every context-dependent word with three windows: local sentence/paragraph, full chapter arc, and later context already translated.
   多义词回看：用三个窗口复核每个依赖上下文的词：本句/本段、全章走向、已经翻译出的后文。
4. Prose rebuild: fix sentences that are merely accurate but not excellent. Do not raise scores to make weak prose pass.
   句法重建：修复“意思对但不优秀”的句子；不得靠抬高评分让弱译文过关。
5. Closure pass: after any fix, rerun the relevant full check. A fix round cannot be the PASS round.
   闭环复查：任何修复后都重跑相应全量检查；修复轮不能直接 PASS。

### 4. Record Machine-Readable Closure / 记录机器可读闭环

Chapter controls and equivalent review records should include:
章节 control 或等效审校记录应包含：

```text
expert_translation_skill_used: true
expert_translation_skill_path: "skills/expert-translation-quality/SKILL.md"
expert_level_review_status: "PASS"
polysemy_translation_stage_review: "PASS"
polysemy_context_review: "PASS"
polysemy_watchlist_count: {number}
polysemy_revisited_count: {number}
polysemy_unresolved_count: 0
```

If any value is unresolved, the chapter or review round is not closed.
只要仍有未决项，章节或评审轮次就不能关闭。

### 5. Backfill Reusable Lessons / 回填可复用经验

If a polysemy mistake, expert-level prose failure, or context-disambiguation failure may recur:
若多义词误判、专家级文风失败或上下文选义失败可能复现：

1. Classify it as a translation-quality defect family.
   归纳为译文质量问题族。
2. Audit similar cases using low-token evidence first: `rg`, glossary rows, forbidden renderings, title maps, chapter controls, and nearby source-to-target pairs.
   先用低 token 证据审计同类：`rg`、术语表、禁用写法、标题映射、章节 control、邻近源文-译文对。
3. Fix confirmed matches and record justified exceptions.
   修复确认命中并记录合理例外。
4. Merge the reusable lesson into `skills/translation-quality-defect-families/SKILL.md`.
   把可复用经验合并到 `skills/translation-quality-defect-families/SKILL.md`。

## Quality Bar / 质量线

- PASS means expert-level publication candidate, not merely readable.
  PASS 表示专家级出版候选，不是勉强可读。
- A score in the 80s is a hard-minimum signal, not a final-quality signal.
  80 多分只是硬下限信号，不是终稿优秀信号。
- Smoothness without source support is a defect.
  没有原文依据的顺滑是缺陷。
- Literal fidelity that requires the reader to reconstruct source grammar is a defect.
  需要读者反推源语语法的字面忠实也是缺陷。
- Unresolved polysemy is a blocker unless the source deliberately remains ambiguous and the target text preserves that ambiguity.
  多义未决是阻塞问题；除非原文本来有意暧昧，且译文保留了同等暧昧。

## Prompt Hygiene / Prompt 卫生

Do not paste this whole skill into every translation prompt. Load or cite it at the workflow node that needs it, then provide only the current source passage, nearby context, relevant glossary rows, and the specific watchlist.
不要把本 skill 整篇塞进每次翻译 prompt。只在需要的流程节点读取或引用它，并只提供当前原文、邻近上下文、相关术语行和本次观察清单。

# LifeBook 统一翻译单元与轻量 CAT/TMS 兼容层设计

## 1. 决策与边界

LifeBook 采用两层架构：

1. **原生生产层**：`translation_units/units.jsonl` 是正文翻译唯一事实源。中文版、双语版、`chapters/translated/`、`chapters/final/` 和兼容 alignment map 都是同一份 canonical units 的确定性投影。
2. **交换兼容层**：按需导出和安全导入 XLIFF 2.1。默认生产路径不经过 XML，也不依赖外部 CAT/TMS。

不建设 CAT 编辑器、在线派单、供应商、计费或权限系统。XLIFF 只负责互操作，不负责翻译，也不能授予 LifeBook 发布 PASS。

本设计吸收独立只读审计意见。审计发现的错误放行路径在进入全面实现前必须关闭；“脚本能运行”或“EPUBCheck 为零”不等于翻译质量合格。

## 2. 不可退让的读者合同

双语正文的唯一合法顺序是：

```text
完整英文短段 A
完整中文译段 A

完整英文短段 B
完整中文译段 B
```

原著自然段是不可跨越的硬边界。一个读者可见双语单元不得包含多个原著自然段。长自然段可以在完整句边界拆成数个短段；若两三句适合组成一个完整小段，不得机械地逐句字幕式切分。页面、屏幕高度和目标字数只能报警，不能覆盖自然段边界。

必须拦截：连续多个源段后集中译文；一段英文只跟一两句中文；跨段串译；逐句字幕式交错；两个版本目标文本漂移；CSS 隐藏目标语；未标记、重复、错序正文或错误目录绕过检查。

## 3. 用户合同与默认专名策略

`state/translation_contract.json` 是翻译前硬门禁。合同必须记录语言方向、短段规则、切分器版本、专名策略来源及所有锁定证据。

专名策略优先采用用户显式选择；若用户没有选择，允许使用用户批准的默认策略 `3`。默认不是隐藏假定，必须记录 `policy_code=3`、`mode=hybrid`、`selection_source=default`、`selection_reason=user_did_not_specify` 和 policy version。用户显式选择时写 `selection_source=user` 及 `decision_id`。

支持 `all_chinese`、`all_source`、`hybrid` 三种书级模式。`hybrid` 按实体锁定稳定中文名、原名优先及首次出现规则；用户未选时使用策略 `3` 作为默认行策略。

无论选择来自用户还是默认，均必须完成全书候选发现、逐项裁决、同名消歧、出现账本验证和 CSV 锁定；默认策略不得跳过预生产工作。合同未锁、发现证据与当前全书源文件哈希不符、存在未决候选或未映射出现时，不得进入翻译。

## 4. 全书专名发现、实体与出现账本

翻译前必须生成 `glossary/proper_noun_discovery_manifest.json`，绑定全部源文件路径与 SHA-256、发现器及语言插件版本、各文件扫描状态、候选/人工补充/裁决/未决数量，以及候选表、实体表和出现账本哈希。

`proper_nouns.csv` 以 `entity_id` 为主键，允许多个实体共享同一 `source_name`。`proper_noun_occurrences.csv` 记录 `occurrence_id`、源文件、canonical `unit_id`、字符区间、`entity_id`、消歧依据和是否计入首次正文出现。标题、导航和副标题不计首次正文出现。

正文名称由只读取锁定 CSV 和出现账本的渲染器生成；模型不得临场创造显示形式。锁定后发现漏项时，当前批次失效并回到发现与裁决阶段；所有受影响译文进入 `NEEDS_RERENDER` 或 `NEEDS_RETRANSLATION`，旧审计失效。禁止边翻译边追加名称后继续冒充同一批次。

## 5. Canonical unit 模型与稳定身份

每个单元至少保存：持久 `unit_id`；章节、源文件、不可跨越的 `source_parent_id` 和全书顺序；Markdown AST 节点类型和受保护 inline token；完整源文及哈希；仅用于覆盖审计的源句 ID；完整目标短段及哈希和状态；译文产生时实际使用的合同、专名、出现账本和术语 revisions；语义审计绑定哈希。

首次导入分配持久 ID。后续源文变更通过显式迁移/匹配报告处理；不得以“段落序号 + 内容哈希”重新生成全部 ID，也不得仅凭相同 source hash 在不同语境之间复用译文。

Markdown 必须使用 AST 解析。标题、正文、引文、列表项、诗节、脚注、表格、代码和原始 HTML 分别定义边界；链接、强调、脚注、占位符和 inline code 作为受保护 token，切分和 XLIFF 往返不得损坏。

## 6. 版本继承与审计失效

旧目标文本只能按持久 `unit_id` 继承，并保留产生时的原始 revisions。合同、专名、出现账本或术语表变化时，不允许把旧文本直接盖成当前 revision；受影响单元进入 `NEEDS_RERENDER` 或 `NEEDS_RETRANSLATION`，完成后重新审计。任何 source、target、边界、合同或词表变化都产生新 manifest digest。

## 7. 安全并行与合并协议

canonical store 只有串行合并器可写。并行 worker 只读 immutable base manifest，只写自己拥有章节的 patch。patch 必须包含用于追踪的 `base_manifest_sha256`、用于并发控制的 `base_chapter_digest`、`chapter_id`、`owner_run_id`、每个 `unit_id` 的旧目标哈希和新目标。

合并器校验章节所有权、当前章节 digest、旧值哈希、单元集合和顺序，使用按章 compare-and-swap 拒绝陈旧或重叠 patch；写入新 generation，完成全量验证后原子切换 manifest。两个不同章节从同一全书 base manifest 产生的 patch 可以依次合并；前一章的合并不会让后一章无故冲突。同章旧 patch、合同 revision 变化或章节单元变化仍必须失败。worker 禁止直接改 `units.jsonl`、合同或全局词表。

可并行：不同章节的翻译、结构检查、语义审计。必须串行：patch 合并、全书一致性、物化、EPUB 构建和发布。

并行度不是按 PDF 页数直接决定。`metrics:evaluate` 先综合 canonical unit/原文字数、章节数、专名密度、注释、图表、公式和难度形成加权工作量；`translation:orchestration:plan` 再取书籍上限、客户端真实能力、用户上限、速率限制、预算上限和质量上限的最小值。客户端能力声明必须带 UTC `verified_at`/`valid_until`，缺失、格式错误、来自未来或过期均不得派生。GPT 家族最多派生 4 个 worker，非 GPT 家族最多 8 个；能力未知、用户未授权或小书默认 0 个。先以最多 2 个 worker 做代表性章节 pilot，只有结构违规与专名违规均为 0、语义首过率至少 90%、返工率不超过 10%、patch 冲突率不超过 1% 时才扩容；否则降并发。

角色采用方案 B：翻译 producer、独立 audit consumer、唯一 coordinator/merger。每章只有一个翻译 owner；相邻章节优先分给同一 producer，以保留叙事和术语连续性。audit consumer 不得审核自己翻译的章节。协调者负责锁定全书专名和术语、生成上下文 capsule、串行合并、全书一致性和发布，不进入 spawned-worker 数量。单目标语与双语版共用同一个 canonical target，绝不并行生成两套译文。

## 8. 确定性投影

`chapters/translated/`、`chapters/final/` 和 alignment map 在新 generation 一次性生成。物化要求目标状态达到合同阈值；非空但仍为 `initial` 不得进入正式投影。生成后拒绝 manifest 外旧章节，复核全集、顺序和哈希，再原子切换。中文版和双语版嵌入同一 manifest；目标 ID、顺序、文本和哈希必须完全一致。

## 9. XLIFF 2.1 兼容层

纯文本进入 `source/target`，受保护 inline token 使用 `<ph>`、`<pc>` 和 `<originalData>`。导出、导入均必须通过官方 XSD/Schematron 或仓库锁定的等价验证器，并通过包含链接、强调、代码、脚注和占位符的往返 fixture。

外部 XLIFF 不得新增、删除、重排单元，不得修改 source、source hash、inline token 或边界；只允许更新已知 target 和受支持状态。外部 CAT 的 `final` 不等于 LifeBook 发布 PASS。XLIFF 默认关闭，不进入普通翻译关键路径。

## 10. 不可伪造的质量证据

确定性门禁证明 100% 源单元覆盖、唯一 ID、顺序、自然段边界、目标状态、名称锁定、translated/final 一致、双语紧邻和两个 EPUB 目标哈希一致。

语义审计轮次按章不可变，包含 `run_id`、`chapter_id`、reviewer/模型、rubric 版本、译者 run ID、当前章节 digest、问题清单和结论；不能覆盖单个 JSON 手填 PASS。审计队列按合同中的 `batch_max_units` 分批，但不改变 unit 边界；每个 unit 记录 attempt 与输入/输出 token，重试不得超过 `max_attempts_per_unit`，且第二次起必须附上前次失败证据。修复轮只能进入 `FIXED_RECHECK_REQUIRED`，重新全量审计后才能 PASS。整章复核绑定全章有序 digest；抽样不能代替全量门禁。每章 PASS 后生成自己的 `completion_manifest.json` 并写入 `current_by_chapter.json`；另一章发生变化不会使本章审计失效，本章 source/target/owner/revision 变化则立即失效。全书所有当前章节均有密封 PASS 后，才生成 `book_completion_manifest.json`。

EPUB 门禁按 DOM 阅读顺序验证唯一且有序的 `(unit_id, source_sha256, target_sha256)`，拒绝未登记正文、重复 ID、错序、非紧邻和错误目录。该全量脚本检查属于构建阶段，但不启动阅读器。

真实阅读器不进入翻译、章节审计、patch 合并或普通构建的关键路径。只有最终 release/private-artifact 候选才尝试一次轻量 smoke test：在手机与桌面两个视口检查目录跳转、章首、普通正文、长段、注释和双语交替等少量分层位置，并保存 computed style 与截图证据。不得按一千页逐页截图；全书覆盖由快速 DOM/文本/哈希脚本承担。若执行机器没有受支持的真实阅读器，门禁记录 `SKIPPED_UNAVAILABLE` 并允许发布，但发布证据和最终交付说明必须明确披露“未完成真实阅读器验证”；EPUBCheck、目录、DOM 可见性和中英顺序静态门禁不得因此跳过。

EPUBCheck、阅读器、目录和产物报告都绑定当前 EPUB SHA-256 与 canonical manifest SHA-256；发布器拒绝复用旧产物报告。

## 11. 迁移与回滚

已有书籍先运行只读迁移器，从旧 source/translated/final/alignment map 生成候选 units 和逐章差异报告，列出未匹配、重复、顺序、文本哈希和专名映射差异。迁移全量 PASS 前保留旧链路和旧产物，不覆盖原文件；新链路失败可回滚 generation，但旧链路结果不得宣称为新架构 PASS。

## 12. 毒化验收

测试记录“变异点 → 必须失败门禁 → 错误码 → 修复后阴性对照”。至少覆盖目标删半段、跨段串译、连续源块、逐句过切、空/伪造专名发现、未登记名称、同名异人错绑、嵌套括注、陈旧 patch、重复/未标记正文、旧 revision 洗白、XLIFF source/inline 损坏、父级 CSS 隐藏、错误目录和旧 EPUBCheck 报告。

任一毒化 fixture 未被预期门禁捕获，门禁系统自身 FAIL，正式构建和发布停止。

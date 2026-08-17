# 统一翻译单元独立审计关闭记录

## 结论

独立只读审计提出的仍成立 P0、P1、P2 已全部关闭。关闭依据不是提示词承诺，而是权威政策、canonical 数据结构、强制脚本、失败错误码和带毒回归测试的组合。

本记录只证明系统具备阻断已知缺陷的机制，不把“结构 PASS”冒充“翻译质量 PASS”。每本书仍须完成逐单元语义审计、逐章全量复核、全书复核及当前产物验证。

## P0 关闭项

| 审计问题 | 关闭机制 | 自动化证据 |
| --- | --- | --- |
| 空白或伪造的专名发现可直接锁定 | discovery manifest 绑定全书源文件、候选表、人工补充、裁决表、出现账本及其 SHA-256；存在未扫描文件、未决候选或哈希不符即拒绝锁定 | `test_empty_or_forged_name_discovery_cannot_be_locked` |
| 同一原文形式无法表示同名异人 | `proper_nouns.csv` 以 `entity_id` 为主键；`proper_noun_occurrences.csv` 逐出现绑定实体、范围和消歧依据 | `test_same_name_entities_require_locked_disambiguation` |
| 模型可在翻译时临场新增名称 | 翻译 patch 只接受 canonical 实体模板；显示形式只能由已锁定 CSV 与 occurrence ledger 统一渲染 | `test_translator_cannot_bypass_csv_with_direct_locked_name` |
| 一个双语块跨多个原著自然段，或被机械切成逐句字幕 | `source_parent_id` 是不可跨越边界；自然段内只允许按完整句形成合理短段，屏幕高度和目标字数只能报警 | `test_poisoned_sentence_level_unit_split_is_rejected`、`test_markdown_ast_preserves_protected_block_boundaries` |
| 旧译文可被重新标注为新合同或新词表 revision | 单元保存译文产生时的合同、专名、出现账本和术语 revision；不一致时只能重渲染或重译并重新审计 | `test_relocking_terms_cannot_wash_old_target_revision` |
| 源文插入导致 unit ID 全书漂移 | 首次导入分配持久 ID；变更通过显式匹配与迁移处理，不使用段落序号或 source hash 冒充身份 | `test_persistent_ids_survive_insertion_before_existing_units` |
| 并行 worker 可直接覆盖 canonical store，或无关章节互相制造假冲突 | worker 只写章节 patch；串行合并器校验章节所有权、`base_chapter_digest`、旧目标哈希和单元顺序并执行按章 CAS | `test_stale_parallel_patch_is_rejected`、`test_disjoint_chapter_patches_from_same_manifest_both_merge` |
| EPUB 只检查标签数量，无法发现重复、错序、未登记正文、隐藏中文或错误目录 | 产物门禁按 spine/DOM 阅读顺序核对唯一 unit ID、source-target 紧邻、文本与哈希、未登记正文、祖先 CSS 可见性、TOC 目标和片段覆盖 | `test_artifact_gate_rejects_non_adjacent_pairs_and_hidden_targets`、`test_real_builders_and_epubcheck_validate_both_enabled_editions` |

## P1 关闭项

| 审计问题 | 关闭机制 | 自动化证据 |
| --- | --- | --- |
| 默认专名策略来源不可追踪 | 优先用户选择；未选择时写入策略 `3`、`selection_source=default` 和原因，且仍须完成全书发现、裁决和锁定 | `test_default_policy_three_is_recorded_and_full_pipeline_materializes_identically` |
| 非拉丁文字或自动发现遗漏后无人工补充通道 | `proper_noun_manual_candidates.csv` 与人工复核记录进入同一 discovery hash 链 | `test_user_policy_four_and_non_latin_manual_candidates_are_preserved` |
| 翻译依赖字符串替换，嵌套专名相互误改 | 最长不重叠 occurrence span 与实体模板渲染，不对正文执行无范围机械替换 | `test_nested_proper_name_forms_use_longest_non_overlapping_spans` |
| Markdown 结构和 inline token 在切分中损坏 | 使用 Markdown AST，分别处理标题、段落、列表、引文、脚注等节点，并保护 inline token | `test_markdown_ast_preserves_protected_block_boundaries` |
| `translated/final` 可能残留旧章节或部分更新 | 两个投影从同一 generation 暂存、全集核验并原子切换；失败回滚 | `test_default_policy_three_is_recorded_and_full_pipeline_materializes_identically`、`test_rollback_restores_old_generation_as_new_auditable_generation` |
| 单个可覆盖 JSON 可伪造语义 PASS，或全书 hash 让无关章节变更使所有审计失效 | 审计轮按章不可变；逐单元结构化证据、整章有序 digest、译者/审核者身份分离和章节 `completion_manifest.json` 封存；所有当前章节密封后生成全书 completion manifest | `test_scalar_semantic_pass_cannot_satisfy_audit_gate`、`test_structured_semantic_audit_is_sealed_and_tampering_is_rejected`、`test_chapter_audit_survives_unrelated_merge_and_supports_distinct_reviewers`、`test_chapter_reviewer_cannot_be_its_translation_owner` |
| XLIFF 往返可能破坏 source 或 inline code | XLIFF 2.1 仅作可选交换层；导入拒绝新增、删除、重排、source/inline 篡改，并使用仓库锁定官方 schema | `test_xliff_roundtrip_preserves_inline_and_rejects_source_tampering` |
| 旧书迁移直接覆盖现有正文 | 迁移器只读生成候选 generation 和差异报告，显式完成后才切换，保留可审计回滚 | `test_legacy_migration_is_read_only_and_blocks_rendered_name_drift` |
| 旧 EPUBCheck 或旧阅读器报告可复用到新 EPUB | EPUBCheck、产物和阅读器报告均绑定当前 EPUB SHA-256 与 canonical manifest SHA-256 | `test_release_gate_rejects_epubcheck_report_bound_to_old_epub`、`test_available_reader_requires_hash_bound_viewports_navigation_and_screenshots` |
| 正常测试通过但带毒输入未验证 | 固化删译、串译、连续源段、逐句过切、专名伪造、同名误绑、陈旧 patch、XLIFF 篡改、CSS 隐藏、错误目录及旧报告等变异 | `tests/test_translation_unit_pipeline.py` |

## P2 关闭项

| 审计问题 | 关闭机制 | 自动化证据 |
| --- | --- | --- |
| 切分默认值无法复现或字数目标凌驾自然段 | 合同记录切分器及规则版本；建议区间只产生风险信号，不允许跨自然段 | `test_poisoned_sentence_level_unit_split_is_rejected` |
| 合同可关闭完整翻译，或使用无效的分段上下限 | 合同强制 `complete_translation_required=true`，上下限必须是正整数且 `max >= min` | `test_contract_rejects_incomplete_translation_and_invalid_segment_bounds` |
| 非空但仍为 `initial` 的目标可进入正式投影 | 章节 patch 和物化均要求目标达到合同规定状态；非空 `initial` 不能进入 canonical 投影或发布 | `test_nonempty_initial_target_cannot_enter_canonical_projection` |
| 全量审计无批次、重试和预算边界 | 审计按 unit 分批但不改变边界；记录 attempt 与输入/输出 token；限制每单元重试并要求携带前次失败证据 | `test_structured_semantic_audit_is_sealed_and_tampering_is_rejected` |
| 按页数盲目并行、能力未知/陈旧仍派生、GPT/非 GPT 越过环境上限或质量失败仍扩容 | provider-neutral planner 使用加权 canonical 工作量和客户端/用户/速率/预算/质量上限；能力声明必须绑定当前 UTC 验证有效期，未知、未验证、过期或格式异常均为 0；GPT 最多 4，非 GPT 最多 8，pilot 不完整或不佳时禁止扩容并按信号降并发 | `tests/test_parallel_translation_planner.py` |

## 阅读器边界

翻译、章节合并和普通构建不启动阅读器。普通构建必须完成全书 DOM/文本/哈希/目录静态检查以及所有启用版本的 EPUBCheck。

最终 release/private-artifact 候选才尝试一次轻量真实阅读器 smoke test。若执行机器未安装受支持阅读器，记录 `SKIPPED_UNAVAILABLE`，允许发布，并在发布证据及最终交付说明中强制披露“未完成真实阅读器验证”。该状态绝不能跳过或洗白 EPUBCheck、目录、可见性、中英顺序和目标一致性硬门禁。

若阅读器可用，报告必须绑定当前 EPUB 与 manifest 哈希，并包含目录跳转、代表位置、手机/桌面两个视口、computed style 和截图证据；缺失任一项不得记录阅读器 PASS。

## 当前回归证据

- `python -m unittest discover -s tests -v`：2026-08-17 当前实现提交前运行 100 项通过（195.170 秒）。
- `test_real_builders_and_epubcheck_validate_both_enabled_editions`：实际构建单目标语和双语 EPUB，并对两者执行 EPUBCheck，通过。
- `npm --prefix books run check:local-paths`：通过。
- `npm --prefix books run check:gitignore-policy`：通过。
- `python -m compileall -q template/epub_pipeline/common/scripts books/scripts tests`：通过。
- `git diff --check`：通过；仅报告工作区换行符提示，无空白错误。

最终发布时必须重新运行这些门禁并绑定当次产物；本记录不得作为未来书籍或未来 EPUB 的永久 PASS 凭证。

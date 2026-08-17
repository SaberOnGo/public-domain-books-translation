# 统一翻译单元实施计划

## 进入全面实现前的设计复审门槛

1. 旧权威政策统一为“一个可见双语单元不得跨原著自然段；完整短源段后立即跟完整目标段”。
2. 专名默认策略 `3` 与用户显式选择都写入合同，并记录 `selection_source`。
3. discovery manifest 绑定全书源文件、发现器版本、候选与裁决覆盖；空表不能锁定。
4. `entity_id`、同名异人、出现账本和只读 CSV 渲染协议完整。
5. 持久 unit ID、章节 patch、CAS、generation 和原子切换协议明确。
6. 合同或词表变化不能给旧译文刷新 revision。
7. XLIFF inline token 保真、迁移回滚、不可变审计轮次和当前产物哈希绑定已设计。
8. 毒化矩阵具有 fixture、预期失败门禁、错误码与阴性对照。

## 实施顺序

1. 扩展翻译合同、专名实体表、候选表、出现账本和 discovery manifest。
2. 实现 Markdown AST 源文导入、持久 unit ID、canonical manifest 和只读迁移报告。
3. 实现章节 patch、章节所有权、按章 `base_chapter_digest` CAS 合并、新 generation 验证与原子切换；确保同一全书 base 的不同章节 patch 可依次合并，同章陈旧 patch 仍失败。
4. 实现名称实体标记及只读取锁定 CSV/occurrence ledger 的统一渲染；translated/final 只允许由同一 generation 物化。
5. 实现 XLIFF 2.1 inline 保真导入导出、schema 校验和往返 fixture。
6. 实现按章不可变逐单元审计轮次、译者/审核者身份分离、章节局部失效、逐章全量复核和全书 `book_completion_manifest.json` 门禁。
7. 让中文版、双语版和 alignment map 嵌入并核对同一 manifest；验证 DOM 顺序、紧邻、未登记正文和双版本目标哈希。
8. 普通构建只跑全书 DOM/目录/EPUBCheck；最终发布候选才尝试一次分层抽点的 computed style、目录跳转和双视口真实阅读器 smoke test，并绑定当前 EPUB SHA-256。若机器未安装受支持阅读器，记录 `SKIPPED_UNAVAILABLE`、允许发布并强制在交付说明披露，不得连带跳过静态门禁。
9. 将合同、canonical、语义、产物、阅读器和报告新鲜度门禁接入 preflight、build、release/private artifact。
10. 实现方案 B 自适应编排：加权工作量、客户端能力声明、GPT/非 GPT 上限、最多 2 worker pilot、质量扩缩容、相邻章节 affinity、translation producer / independent audit consumer / one merger 角色计划。
11. 更新通用及各语言方向 prompts、skills、生产规范和用户说明。
12. 运行正常端到端、迁移、同章/异章并发、独立审计、调度上限、XLIFF 往返、毒化和现有回归测试。

## 毒化测试矩阵

| 变异 | 必须失败的门禁 | 稳定错误码 | 阴性对照 |
| --- | --- | --- | --- |
| 删除目标段后半部分 | 语义完整性 | `SEMANTIC_OMISSION` | 完整重译并重新全审 |
| 下一段译文移入上一段 | 邻段污染 | `NEIGHBOR_CONTAMINATION` | 各单元只含本段意义 |
| 连续三个源块 | EPUB DOM 交替 | `NON_ADJACENT_PAIR` | 严格 source-target |
| 每句单独交替 | 切分粒度 | `SENTENCE_OVERSEGMENTED` | 合理两三句短段 |
| 空候选表直接锁定 | 专名发现 | `DISCOVERY_EVIDENCE_MISSING` | 全书 manifest 与裁决齐全 |
| 同名异人错绑 | occurrence ledger | `ENTITY_DISAMBIGUATION_FAILED` | 每次出现绑定正确实体 |
| 旧译文刷新新 revision | 版本继承 | `STALE_TARGET_REVISION` | 重新渲染/翻译及审计 |
| 两 worker 覆盖同章 | CAS 合并 | `PATCH_CONFLICT` | 独占章节或重基 patch |
| 不同章节同一 base 的第二个 patch 被误拒绝 | 按章 CAS | 第二章应正常合并 | `base_chapter_digest` 只绑定本章 |
| reviewer 与本章 translator 相同 | 审计独立性 | `AUDIT_INDEPENDENCE_VIOLATION` | 独立 audit consumer |
| 无客户端能力声明却启动 worker | 编排能力门禁 | `capability_unknown` 且 worker=0 | 活动客户端实时声明并经用户授权 |
| GPT/非 GPT 超过 4/8 | 编排硬上限 | 规划 worker 不超过上限 | 所有上限取最小值 |
| 重复或未标记正文 | 产物清单 | `UNREGISTERED_READER_TEXT` | DOM 与 manifest 一一对应 |
| XLIFF 篡改 source/inline | XLIFF 导入 | `XLIFF_SOURCE_OR_INLINE_CHANGED` | schema 与往返相同 |
| 父级 CSS 隐藏中文 | computed style | `TARGET_NOT_VISIBLE` | 多视口可见 |
| 错目录或旧报告 | 导航/报告新鲜度 | `ARTIFACT_REPORT_HASH_MISMATCH` | 报告绑定当前 EPUB |

任一毒化样本没有触发指定错误码，正式流水线不得宣告 PASS。

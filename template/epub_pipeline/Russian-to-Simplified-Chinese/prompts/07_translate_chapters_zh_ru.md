# 07 分章翻译

## Canonical Unit Hard Contract / Canonical 单元硬契约

本语言方向同样使用 `translation_units/` 作为唯一 source-target 事实源。正文翻译前必须完成全书专名发现、逐项裁决、`entity_id`/occurrence ledger、`glossary/proper_nouns.csv` 与术语/合同锁定；未锁定前不得并行翻译。锁定后按 `references/adaptive_parallel_orchestration.md` 规划：能力未知或用户未授权时不派生 worker；GPT 上限 4，非 GPT 上限 8，先以最多 2 个 worker 做质量 pilot。translation producer 独占章节且只写自己的 chapter patch，相邻章节优先同一 owner；audit consumer 必须独立；coordinator/CAS 合并器是唯一 canonical writer。不同章节 patch 按 `base_chapter_digest` 可从同一全书 base 依次合并，同章陈旧 patch 才冲突。不得直接写或手改 `chapters/translated`/`chapters/final`，二者只能由同一 generation 确定性物化；单目标语与双语版共享同一 target，不得分别翻译。

启用双语版时，一个可见 unit 只能来自一个原著自然段；过长自然段只可按完整句群拆成短段。每个完整源语短段后必须立即跟随它的完整目标语译段；禁止逐句字幕式交错、跨自然段合并、连续多段源文后集中译文、漏译和邻段串译。专名只能写 `{{pn:entity_id}}`，不得临场新增或直接写锁定名称。


只输出当前章中文译文，不混入 QA、prompt、release 或制作说明。中文自然优先；俄语原词不默认正文括注；疑难处用译注或章末术语说明承载。

## 专家级译文与多义词主动判义及回看 / Expert Quality, Active Polysemy Handling, and Back-Check

翻译调用仍然只输出译文，不输出 QA 或流程记录；但译者必须按 `skills/expert-translation-quality/SKILL.md` 在内部建立观察清单，并在翻译阶段主动判义。遇到多义词、习语、称谓、术语或需要后文判义的语法结构，先用当前句、本段、邻近上下文、术语表、说话人身份、论证功能和可用后文线索判义；能判清的当场处理，不能判清的才用不错误收窄的目标语保留歧义并标记后文回看。不得把局部上下文已能判清的问题留给 `08a`。后文译出后，`08a` 必须回到前文位置复查并必要时修订。观察清单不得进入读者正文。

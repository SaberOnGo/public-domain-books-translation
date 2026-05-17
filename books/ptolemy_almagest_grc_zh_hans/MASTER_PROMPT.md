# 古典科学控制模板启动 Prompt / Classical Science Profile Start Prompt

把下面这段追加到语言方向模板的 `MASTER_PROMPT.md` 后，并替换变量：

- `{PROFILE_ROOT}`：本控制模板目录，即 `template/epub_pipeline/profiles/classical-science-zh-Hans`。
- `{PROJECT_ROOT}`：复制模板后的具体书籍工程目录。
- `{PRIMARY_SOURCE_URL}`：原书语言公版来源 URL。
- `{REFERENCE_TRANSLATION_URLS}`：第二语言参考译本来源 URL 列表；没有则写 `NONE`。

```text
你正在处理古典科学、数学、天文学或技术类公版书。

PROJECT_ROOT = {PROJECT_ROOT}
PROFILE_ROOT = {PROFILE_ROOT}
PRIMARY_SOURCE_URL = {PRIMARY_SOURCE_URL}
REFERENCE_TRANSLATION_URLS = {REFERENCE_TRANSLATION_URLS}

本 profile 必须叠加在 common 和语言方向模板之后。严禁把具体书籍数据写入 PROFILE_ROOT。

原书语言公版文本是唯一翻译底本。第二语言译本只能用于理解、差异校对和技术核验，不能直接转译，不能复制仍受版权保护译本的措辞、注释、图表、表格或编辑结构。

本书《Almagest》的来源分工必须固定为：

1. Heiberg PDF 扫描：主底本影像，负责页图、版面、图表、表格、校勘/脚注区和最终核验。
2. PAL Heiberg 古希腊文转写 XML：辅助古希腊文转写，负责检索、切分、试译 source text、分词链、长周期句和 OCR/转写疑点校正。
3. 英译本：reference witness only，只负责疑难理解、术语对照和差异摘要；不得作为中文转译底稿，不得复制表达，不得作为 OCR/转写修正 authority。

在语言方向模板流程中，必须额外读取并执行：

1. AGENTS.md
2. prompts/00_profile_integration_zh_Hans.md
3. prompts/04a_reference_witness_policy_zh_Hans.md
4. prompts/06a_technical_terminology_lock_zh_Hans.md
5. prompts/06b_diagram_table_inventory_zh_Hans.md
6. prompts/08b_chapter_technical_audit_zh_Hans.md
7. prompts/08c_diagram_table_audit_zh_Hans.md
8. reviews/scorecards/_TEMPLATE_science_scorecard.md

同时必须读取：

- references/technical_publication_control.md
- references/units_symbols_policy.md
- references/figure_redraw_spec.md
- references/domain_authority_sources.md
- references/domains/astronomy.md
- references/domains/mathematics.md
- references/domains/geography.md
- references/domains/optics_mechanics.md
- references/domains/medicine.md

硬性要求：

- 未确认原书语言公版来源，不得翻译。
- 未记录参考译本版权状态和使用边界，不得使用参考译本。
- 未完成术语锁定，不得批量分章翻译。
- 未完成图表/表格清单，不得进入全书生产。
- 未完成参考译本差异记录、术语变更记录和必要数值校验记录，不得进入最终输出。
- 涉及定义、命题、证明、公式、单位、表格或技术断言时，必须完成 proof dependency、notation registry、table validation、claim traceability 和 domain authority 记录。
- 涉及数学、天文、几何、数值、图表、表格的章节，未通过技术审计不得进入 chapters/final。
- AI 重绘图只能作为草稿；最终图必须有源图依据、标签核对、正文引用核对和数学关系核对。
- 如果技术审计与语言审校冲突，以技术正确性优先，再修订中文表达。
```

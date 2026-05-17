# /goal: 《Almagest》研究与预翻译准备，不进入正式翻译

## 目标

为托勒密《Almagest》（中文常译《天文学大成》/《至大论》）建立古希腊文到简体中文的研究与预翻译准备工程。当前只完成底本、版权、参考译本边界、术语、数学/天文学校对、图表重绘和预翻译试点设计，不进行正式分章翻译。

## 范围

- 创建 `books/ptolemy_almagest_grc_zh_hans/` 书籍工程。
- 叠加 `common -> grc-zh-Hans -> profiles/classical-science-zh-Hans`。
- 记录 Heiberg 古希腊文校勘版为候选主底本。
- 记录现代英译本等只能作为 reference witness，不能直接转译。
- 建立数学、天文学、几何证明、弦表、角度、图表、数值和术语强约束。
- 建立 Book I 预翻译试点计划。

## 明确排除

- 不创建正式译文。
- 不写入 `chapters/translated/*.md` 正式译文。
- 不写入 `chapters/final/*.md`。
- 不构建 EPUB。
- 不使用现代英译本作为中文译文底稿。

## 完成定义

- `metadata/source_evidence.md`、`metadata/rights_checklist.md`、`metadata/source_witness_manifest.md` 已记录。
- `metadata/reference_witness_policy.md` 明确参考译本边界。
- `metadata/book_specific_translation_research.md` 和 `metadata/style_profile.md` 完成研究定位。
- `qa/technical/` 下数学/天文学/图表/数值/术语控制文件完成初版。
- `qa/pretranslation/pretranslation_plan.md` 完成，`pretranslation_report.md` 明确为 `NOT_STARTED`。
- `state/pipeline_state.json` 明确 `formal_translation_allowed=false`。


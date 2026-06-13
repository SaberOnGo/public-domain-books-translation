# 模板版本 / Template Version

version: 0.1
updated_at: 2026-05-22

## 本次版本变化 / Changes

- 初始建立 `Japanese-to-Simplified-Chinese` 日语到简体中文语言方向模板。
- 对齐 `common` EPUB 流水线、`targets/zh-Hans` 中文质量框架和既有语言方向模板的执行顺序。
- 新增日语底本文字形态、历史假名遣、振假名、日语汉字词、敬语/称谓、官能文学边界和题名策略规则。
- 新增 `metadata/japanese_source_profile.md` 与 `qa/textual/japanese_textual_notes.md` 作为批量翻译前的硬门禁产物。
- 保留分层随机抽检、版本化 release、publication lint、asset manifest check、reader-facing policy check 等 common 层门禁。

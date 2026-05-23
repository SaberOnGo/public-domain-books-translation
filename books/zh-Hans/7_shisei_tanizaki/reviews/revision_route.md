# 修订路线

status: "PASS"

本书为单篇短篇，采用全篇直译后整体审校路线。若随机抽检发现 P0/P1/P2，则先定点修复，再重新构建 EPUB，并追加新 seed 抽检轮。

2026-05-23 段落结构返工：用户指出正文大量句级拆段导致阅读异常。修订路线回退到 `chapters/src`、`chapters/translated`、`chapters/final` 的段落结构层，对照 `source/source_text.txt` 恢复自然段边界；随后重建 EPUB，并以新 seed 生成 `round_005` 分层随机抽检。

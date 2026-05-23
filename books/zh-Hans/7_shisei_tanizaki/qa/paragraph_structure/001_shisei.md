# 段落结构全书检查：刺青

status: "PASS"

## 检查范围

- 原文整理稿：`source/source_text.txt`
- 日文分章稿：`chapters/src/001_shisei.md`
- 中文译稿：`chapters/translated/001_shisei.md`
- 中文终稿：`chapters/final/001_shisei.md`

## 问题

此前终稿把大量自然段拆成一句一句的独立段落。截图所示位置并非原文原貌；青空整理稿中这些内容属于较长叙述自然段。

## 修复

- `chapters/src/001_shisei.md` 已恢复为青空整理稿的自然段/对白边界。
- `chapters/translated/001_shisei.md` 与 `chapters/final/001_shisei.md` 已同步合并句级拆段。
- 终稿正文段落由 121 个减少为 54 个读者段落；平均 77 字，最长 270 字。
- 仅保留 8 个单句段落，均为对白、转场或强停顿位置。
- 对白、转折和强停顿仍保留独立段，避免把文学节奏机械压成大段。

## 抽检结论

- 全书只有 `001_shisei.md` 一个正文文件，已逐段对照检查。
- 未发现继续按句子拆段的连续异常区块。
- 修复后必须重新构建 EPUB，并重新生成分层随机抽检轮次。

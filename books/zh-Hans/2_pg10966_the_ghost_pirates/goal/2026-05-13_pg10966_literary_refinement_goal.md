# 《幽灵海盗》精修目标 / Literary Refinement Goal

日期：2026-05-13

本文件定义 `books/zh-Hans/2_pg10966_the_ghost_pirates/` 的后置精修 `/goal`。本轮目标参考 `books/zh-Hans/1_pg20923_a_negro_explorer_at_the_north_pole/` 的处理经验：EPUBCheck 通过只是工程合格，不等于文本、目录、元数据和出版细节已经完成编辑级复查。

## 目标

在已完成的《幽灵海盗》中文 EPUB 基础上，做多轮出版前细节复查和可确认修复，重点包括：

- 编码、BOM、乱码、异常空格和标点复查。
- 章节标题、目录、OPF 主标题、版本说明页一致性复查。
- 英文原名、英文专名和正文残留的合规性复查。
- 术语和专名一致性复查，尤其是航海术语、船名、人名和职务称谓。
- 中文分号、半角符号、重复标点和机械口吻风险复查。
- EPUB 内部 XHTML、nav、spine、cover-image、book-info 和最终 manifest 复查。
- 重新运行 publication lint、EPUB 构建和 EPUBCheck。

## 本轮完成定义

- `publication_lint` 无硬错误，且 `mojibake=0`、`targetTitleLatinResidue=0`。
- 精修后尽量将中文分号清零；若保留，必须有记录说明。
- `chapters/final/` 不得有 BOM、异常连续空格或明显源文本工件残留。
- EPUBCheck 必须为 fatal=0、error=0、warning=0。
- EPUB metadata 主标题必须为“幽灵海盗”。
- 所有复查结果写入 `qa/refinement/`。
- 若发生文本或构建脚本修复，必须重建 EPUB 并更新 `output/final_manifest.md`。

## 不做事项

- 不重新大批量改写全书。
- 不引入现代中译本或不明来源参考。
- 不把本书专用产物写回 `template/`。
- 不把 Project Gutenberg raw 原文的原始空白当作错误清理掉；raw 文件用于来源证据保留。

# /goal: 验证 PAL 原文文本与浏览器 PDF 扫描页访问

日期：2026-05-17

本目标重设当前执行重点：先解决《Almagest》试译前最关键的 source gate，而不是直接开始正式章节翻译。

## 目标

1. 验证 PDF 之外是否存在可用于项目的古希腊原文文本。
2. 重点核查 PAL / Ptolemaeus Arabus et Latinus 的 Heiberg 转写文本：
   - 是否能访问。
   - 是否能下载或复制。
   - 许可是否允许提交到本仓库。
   - 是否能作为 `source/source_text_raw.txt` 或 trial chapter source。
3. 使用已安装 Codex 插件的浏览器访问本地 Heiberg PDF 扫描：
   - URL: `http://127.0.0.1:8765/source/facsimile/Almagest_Complete_Heiberg_1898.pdf`
   - 目标是确认页面是否能正常渲染。
   - 若可渲染，尝试定位 Book I 标题页、Book I.10 附近页图、图表/弦表页。
4. 根据结果更新 `qa/chapter_trial/trial_chapter_gate.md`、`qa/technical/book_i_page_verification.md`、`metadata/source_witness_manifest.md` 与 `source/source_manifest.json`。

## 成功标准

至少满足一项：

- 找到许可清楚、可提交的 Heiberg 古希腊转写文本，并记录下载/哈希/许可。
- 或浏览器 PDF 扫描页可读，能用于 Book I/试译章节页图核验。

若两者都未满足，必须明确记录阻断原因和下一步工具链要求。

## 禁止项

- 不得把 PAL 或任何网站文本整本复制进仓库，除非许可已确认。
- 不得把 Toomer 或其他现代英译本当作底稿。
- 不得在 source gate 未通过前写入 `chapters/translated/` 或 `chapters/final/`。
- 不得因为浏览器能显示 PDF 就跳过页码、图表、OCR/转写和技术审计。

## 当前允许动作

- 启动本地只读 HTTP 服务查看已下载 PDF。
- 用浏览器插件截图/检查 PDF 渲染。
- 搜索 PAL license、API、Git 仓库或下载端点。
- 写入研究、来源证据、门禁状态和阻断记录。

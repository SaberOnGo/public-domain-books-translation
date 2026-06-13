# 西班牙语底本与来源记录规则

本文件只记录西班牙语原文进入简体中文时容易出现的源语言和来源风险。更通用的简体中文译文质量规则见 `template/epub_pipeline/targets/zh-Hans/quality_framework/`。

## 必须记录

- 作者西班牙文名、中文译名、生卒年；匿名作品必须记录匿名状态、传统归属和“不作为确定作者”的说明。
- 原书西班牙语题名、初版年份、所用版本年份。
- 来源 URL、获取日期、来源机构或项目名称。
- 来源形态：Project Gutenberg 文本、Wikisource 校对文本、Biblioteca Virtual Miguel de Cervantes 文本、Biblioteca Nacional de Espana 扫描、Internet Archive 扫描、HTML、纯文本、TEI/XML 或 OCR。
- 版权口径：来源页面声明、作者死亡年份或匿名/古籍状态、出版年份、美国公版状态、中国和 life+70 地区初步判断。
- 若使用扫描和转写并行，写明二者分工：扫描用于图像证据和疑难核对，转写用于分章和翻译。

## 西班牙语文本风险

- 16-17 世纪西班牙语可能有旧拼写、旧标点、长周期句、宗教/法律/身份术语和现代读者不熟悉的称谓。
- `vuestra merced`、`merced`、`amo`、`escudero`、`clérigo`、`buldero`、`alguacil` 等词经常同时承载叙述关系、身份和讽刺距离，必须早期进入术语表。
- Project Gutenberg 或其他纯文本必须剥离许可证头尾，但来源证据必须保留。
- Wikisource、Cervantes Virtual 或图书馆页面可能保留站点模板、校对说明、目录、脚注、版本说明和协作转录信息；不得把站点说明混入正文。
- 不得使用现代中文译本、现代校注本或现代改写本作为隐藏参考材料。现代译本只能在权利清楚且用户明确允许的私人比较场景中使用；公开项目不得依赖其表达。

## 流浪汉小说和黄金时代文本风险

- 流浪汉小说的第一人称叙述常在“求情/自辩/讽刺/卖惨/炫耀机智”之间摆动，不能译成客观传记摘要。
- 宗教身份和制度讽刺应忠实呈现；不要把早期近代教会语境直接现代化，也不要替作者做现代道德判决。
- 食物、衣物、货币、贫穷、血统荣誉、服务关系和街巷地理会影响情节理解，应按需短注，但不得把小说正文变成百科。
- 旧版章节题名可能很长，且常以“某事如何发生”构成叙事钩子。中文标题需要按 `references/spanish_title_strategy.md` 设计，不机械保留长链。

## 下载与证据实践

- 若 `Invoke-WebRequest` 或 `curl.exe` 因 Windows Schannel/TLS 错误失败，不要直接判定来源不可用。先用另一套网络栈验证，例如 Python `urllib.request`，并记录失败命令和可用命令。
- 若使用 Project Gutenberg 工作文本，`metadata/source_evidence.md` 应记录 Gutenberg 编号、页面 URL、文本 URL、获取日期、版权声明和头尾许可证剥离范围。
- 若后续需要使用扫描插图、版面图或影印裁图，不能只沿用纯文本权利记录，必须补充图片来源、文件、manifest 和资产门禁。

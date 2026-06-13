# 法语底本与来源记录规则

## 必须记录

- 作者法文名、中文译名、生卒年。
- 原书法文题名、初版年份、所用版本年份。
- 来源 URL、获取日期、来源机构或项目名称。
- 来源形态：Project Gutenberg 文本、Wikisource 校对文本、Gallica/BnF 扫描、Internet Archive 扫描、TEI/XML、HTML、纯文本或 OCR。
- 版权口径：来源页面声明、作者死亡年份、出版年份、美国公版状态、中国和 life+70 地区初步判断。
- 若使用扫描和转写并行，写明二者分工：扫描用于图像证据和疑难核对，转写用于分章和翻译。

## 法语文本风险

- 19 世纪法语可能有旧拼写、旧地名、旧科学术语和殖民时代称谓。
- Wikisource/Gallica 页面可能保留原书目录、插图页、校勘说明或项目页文字；不得把站点说明混入正文。
- Project Gutenberg 文本必须剥离许可证头尾，但来源证据必须保留。
- 法语引号、破折号、省略号、脚注标记和章节题名在转中文时必须重新设计，不能机械保留排版。

## 下载与证据实践

- 若 `Invoke-WebRequest` 或 `curl.exe` 因 Windows Schannel 凭据/TLS 错误失败，不要直接判定来源不可用。先用另一套网络栈验证，例如 Python `urllib.request`，并记录失败命令和可用命令。
- 当 Gutenberg header 写明文本来自 BnF/Gallica 图像时，`metadata/source_evidence.md` 应同时记录 Gutenberg 工作文本和 BnF/Gallica 图像证据线索。
- 若后续需要使用扫描插图、版面图或影印裁图，不能只沿用纯文本权利记录，必须补充图片来源、文件、manifest 和资产门禁。

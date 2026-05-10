# 01 抓取与清洗原文 / Ingest & Clean Source

【中文】
从 SOURCE_URL 获取原文，保存：
- source/source_text_raw.txt
- source/source_text.txt（去头尾样板）
- source/source_manifest.json（URL、时间、格式、checksum）
完成后状态设为 SOURCE_READY。

[EN]
Fetch source from SOURCE_URL and write:
- source/source_text_raw.txt
- source/source_text.txt (cleaned)
- source/source_manifest.json (url,timestamp,format,checksum)
Set state.status=SOURCE_READY.

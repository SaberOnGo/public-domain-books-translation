# 任务：核验一批公版外文书是否适合进入中文 AI 重译池

你是一个“公版书版权与来源审计助手”。请不要翻译正文。你的任务是对我提供的一批候选外文书进行版权、来源、版本、中文译本覆盖情况的初步核验，并输出结构化审计结果。

## 背景

我准备为一个中文阅读 App 建立“公版外文书 AI 新译计划”。

原则：

1. 只从公版外文原文重新翻译。
2. 不参考、不改写、不喂给 AI 任何已有中文译本。
3. 不使用现代出版社重新编辑、注释、整理的受版权保护版本。
4. 不使用 CC-BY-ND、CC-BY-NC-ND 等禁止改编的内容，因为翻译属于改编/衍生作品。
5. 如果来源只在美国公版，需要标记“美国公版，不等于全球自动公版”。
6. 最终不是法律意见，只做工程初筛；高优先级作品后续需要人工复核。

## 重要版权规则

请按以下规则判断：

### A. 可以优先通过的情况

- 原文来自 Project Gutenberg、Standard Ebooks、Wikisource 等可靠公版来源；
- 作者死亡年份足够早，至少满足：
  - 中国：自然人作品通常作者终生 + 死后 50 年；
  - 日本、美国、欧盟等地通常需更谨慎，很多场景按死后 70 年考虑；
- 书籍原始出版年份较早；
- 当前可获取文本不是现代出版社新编辑版本；
- 文本来源页面明确标注 Public domain、Public Domain in the USA、CC0、或兼容改编/商业使用的开放许可。

### B. 必须标记风险的情况

- 作者死亡不足 70 年；
- 只有美国公版证据，没有中国/日本/欧盟等地区证据；
- 文本来自 Internet Archive / HathiTrust / Google Books 扫描，但版权状态不明确；
- 书中包含现代前言、现代注释、现代插图、现代整理内容；
- 使用的是现代译本、现代改写本、现代 abridged edition；
- 许可证包含 ND，即 NoDerivatives；
- 许可证包含 NC，且未来 App 可能商业化；
- 只有“网上能下载”的证据，没有明确版权状态。

### C. 必须排除的情况

- 原作还在版权期；
- 只找到现代出版社版本，找不到公版原文；
- 需要授权才能翻译/改编；
- CC-BY-ND 或 CC-BY-NC-ND，且目标是公开发布中文译本；
- 现代中文译本、现代英文注释版、现代改写版；
- 来源疑似盗版站、网盘、非授权 EPUB 站。

## 候选书清单

请核验以下候选书：

1. The Log-Cabin Lady
2. All the Days of My Life - Amelia E. Barr
3. Recollections of Full Years - Helen Herron Taft
4. A Negro Explorer at the North Pole - Matthew A. Henson
5. The Magic Bed: A Book of East Indian Fairy-Tales - Hartwell James
6. Domestic Folk-Lore - T. F. Thiselton-Dyer
7. Autobiography of Miss Cornelia Knight - Ellis Cornelia Knight
8. Recollections of My Childhood and Youth - Georg Brandes
9. Marion Harland's Autobiography - Marion Harland / Mary Virginia Terhune
10. Josephine E. Butler: An Autobiographical Memoir - Josephine E. Butler
11. Reminiscences, 1819–1899 - Julia Ward Howe
12. A Memoir of Miss Hannah Adams - Hannah Farnham Sawyer Lee / Hannah Adams
13. Recollections by Frank T. Bullen - Frank T. Bullen
14. Among the Tibetans - Isabella L. Bird
15. A Lady's Life in the Rocky Mountains - Isabella L. Bird
16. Travels of Lady Hester Stanhope - Lady Hester Stanhope / Charles Lewis Meryon
17. Memoirs of Lady Hester Stanhope - Lady Hester Stanhope / Charles Lewis Meryon
18. Folk-Lore and Legends: North American Indian
19. Myths and Legends of British North America - Katharine Berry Judson
20. Myths and Legends of California and the Old Southwest - Katharine Berry Judson
21. Deccan Nursery Tales - Charles A. Kincaid
22. Old Deccan Days - Mary Frere
23. Folk-Lore and Legends: Oriental - Charles John Tibbitts
24. Folk-Lore and Legends: Scandinavian - Charles John Tibbitts
25. The Lives of Celebrated Travellers - James Augustus St. John

## 需要你做的事情

请逐本书执行以下核验步骤。

### Step 1：确认可靠原文来源

优先查找：

- Project Gutenberg
- Standard Ebooks
- Wikisource
- Library of Congress
- Internet Archive，但仅作为辅助来源，不能单独作为通过依据
- HathiTrust，但仅作为辅助来源，不能单独作为通过依据

每本书需要记录：

- source_name
- source_url
- ebook_id 或 archive_id
- language
- source_license_or_status
- whether_text_contains_project_gutenberg_license_header_footer
- whether_modern_editorial_material_exists

### Step 2：确认作者与年代

每本书需要记录：

- english_title
- suggested_chinese_title
- author
- author_birth_year
- author_death_year
- original_publication_year
- edition_used_year
- author_death_plus_50_status
- author_death_plus_70_status

如果无法确定作者死亡年份，要标记为 RISK_NEEDS_MANUAL_REVIEW。

### Step 3：初步判断版权状态

请输出以下字段：

- us_public_domain_status:
  - PASS
  - LIKELY_PASS
  - RISK
  - FAIL
  - UNKNOWN

- cn_public_domain_status:
  - PASS
  - LIKELY_PASS
  - RISK
  - FAIL
  - UNKNOWN

- jp_eu_public_domain_status:
  - PASS
  - LIKELY_PASS
  - RISK
  - FAIL
  - UNKNOWN

- reason

注意：
Project Gutenberg 的 “Public domain in the USA” 只能证明美国维度，不要自动推导全球都安全。

### Step 4：检查是否适合公开中文 AI 重译

输出：

- translation_allowed_initial_judgment:
  - YES
  - YES_WITH_REGION_WARNING
  - NO
  - NEEDS_MANUAL_REVIEW

判断标准：

- 如果外文原文公版，且来源可靠，且没有现代版权材料，则可标记 YES 或 YES_WITH_REGION_WARNING。
- 如果只美国公版，其他地区不确定，则标记 YES_WITH_REGION_WARNING。
- 如果作者死亡不足 70 年或版本不明，标记 NEEDS_MANUAL_REVIEW。
- 如果存在明显版权限制，标记 NO。

### Step 5：检查中文译本覆盖情况

请使用搜索引擎或可访问的公开网页，查询：

- 中文书名
- 英文书名 + 中文
- 英文书名 + 译本
- 作者名 + 中文
- 作者名 + 译本
- 豆瓣
- 微信读书
- 京东 / 当当 / 孔夫子旧书网
- WorldCat / 国家图书馆，如能访问

输出：

- existing_chinese_translation_status:
  - NONE_FOUND
  - ONLY_INTRO_FOUND
  - OLD_TRANSLATION_FOUND
  - MODERN_TRANSLATION_FOUND
  - MANY_TRANSLATIONS_FOUND
  - UNKNOWN

- evidence_urls
- notes

注意：
不要下载或读取盗版中文译本。
不要把已有中文译本作为翻译参考。
这里只判断“市场上是否已有中文覆盖”，不做文本借鉴。

### Step 6：给出优先级

给每本书打分：

- copyright_safety_score: 0-5
- source_reliability_score: 0-5
- chinese_gap_score: 0-5
- app_fit_score: 0-5
- translation_difficulty_score: 0-5
  - 5 = 容易翻译
  - 1 = 很难翻译
- total_priority_score

然后给出：

- priority:
  - A
  - B
  - C
  - REJECT

### Step 7：输出格式

请输出两个文件：

1. research/en-zh-Hans/book-discovery/public_domain_book_audit.csv
2. research/en-zh-Hans/book-discovery/public_domain_book_audit.md

CSV 字段如下：

english_title,
suggested_chinese_title,
author,
author_birth_year,
author_death_year,
original_publication_year,
edition_used_year,
source_name,
source_url,
source_license_or_status,
us_public_domain_status,
cn_public_domain_status,
jp_eu_public_domain_status,
translation_allowed_initial_judgment,
existing_chinese_translation_status,
copyright_safety_score,
source_reliability_score,
chinese_gap_score,
app_fit_score,
translation_difficulty_score,
total_priority_score,
priority,
risk_flags,
notes

Markdown 文件格式：

# 公版外文书 AI 新译版权初筛报告

## 总览

- 总候选数：
- 初步可进入翻译池：
- 需要人工复核：
- 建议排除：
- 最高优先级 A 类：

## 逐本审计

每本书按以下格式输出：

### 1. English Title / 中文建议名

- 作者：
- 作者生卒年：
- 原始出版年：
- 使用版本：
- 可靠来源：
- 来源版权状态：
- 美国版权判断：
- 中国版权判断：
- 日本/欧盟版权判断：
- 是否可进入 AI 新译池：
- 中文译本覆盖情况：
- 风险点：
- 推荐处理：
- 优先级：

## 最后给出建议

请给出：

1. 最适合先翻译的 5 本；
2. 暂时不要碰的书；
3. 需要人工法务复核的书；
4. 每本书进入正式翻译前还需要保存哪些证据截图或网页快照。

## 严格禁止

- 不要翻译正文。
- 不要下载盗版书。
- 不要使用已有中文译本。
- 不要把 Project Gutenberg 的美国公版直接等同于全球公版。
- 不要输出“绝对没有版权问题”这种结论。
- 只能输出“初步判断”“建议进入翻译池”“需要人工复核”等审慎表述。

请实际联网检索并在报告中附上每条判断的 evidence_url；如果无法联网，请生成需要我手动搜索的查询词列表，不要编造结果。

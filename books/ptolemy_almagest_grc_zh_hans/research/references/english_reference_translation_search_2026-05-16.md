# 英译本检索与下载决策 / English Reference Translation Search

search_status: `NO_LAWFUL_FULL_DOWNLOAD_FOUND`
searched_at: `2026-05-16`

## 结论 / Decision

当前没有把完整英译本下载进本项目的安全来源。

- 最适合作为学术参考的英译本：G. J. Toomer, `Ptolemy's Almagest`，Princeton University Press。
- 最适合作为“可下载候选”的英译本：R. Catesby Taliaferro, `Mathematical Composition (Almagest)`，1939 St. John's Program 相关打字本。
- 本轮没有下载完整英译本，因为 Toomer 仍受版权保护，Taliaferro 在 HathiTrust 的可见记录为 `Limited (search-only)`，未提供可合法下载的完整文件。

## 候选 1：Toomer 英译本

| field | value |
|---|---|
| title | `Ptolemy's Almagest` |
| translator | G. J. Toomer |
| publisher | Princeton University Press |
| date | 1984 / later Princeton editions |
| suitability | 最高。现代学术英译，适合疑难校读、术语理解、数学/天文学解释。 |
| rights | copyrighted |
| download_decision | DO_NOT_DOWNLOAD |
| allowed_use | 人工合法持有版本可作 reference witness；只记录差异摘要，不复制措辞、注释、图表或表格。 |
| source | https://press.princeton.edu/books/paperback/9780691002606/ptolemys-almagest |

## 候选 2：Taliaferro 英译本

| field | value |
|---|---|
| title | `Mathematical Composition (Almagest)` |
| translator | R. Catesby Taliaferro |
| date | 1939 |
| record | HathiTrust record `001475750`; OCLC `10543802`; LCCN `42003760` |
| item | `mdp.39015036048588`, enumcron `v.3` |
| rights_status_found | HathiTrust API returned `rightsCode: und`, `usRightsString: Limited (search-only)` |
| suitability | 中高。不是 Toomer 级别，但可作为英语结构/术语辅助，尤其适合比较古希腊文难句。 |
| download_decision | DO_NOT_DOWNLOAD_UNTIL_FULL_VIEW_PUBLIC_DOMAIN_SOURCE_FOUND |
| source | https://catalog.hathitrust.org/api/volumes/brief/oclc/10543802.json |

## 检索过但未采用 / Searched But Not Adopted

- Internet Archive broad search: 未确认到可合法下载的完整英译本。
- Google Books / HathiTrust catalogue access: 本机检索存在连接/Cloudflare限制；HathiTrust API 可访问并确认 `Limited (search-only)`。
- 非官方 PDF 站点：不使用。即使能搜到，也不得下载进本项目。

## 工程规则 / Project Rules

1. 不下载 Toomer 或任何现代受版权保护英译本的完整扫描/电子书。
2. 不从盗版站、影印站或来源不明网盘下载英译本。
3. 若后续找到 Taliaferro 或其他英译本的明确公版完整下载源，必须先记录：
   - source URL
   - rights evidence
   - download timestamp
   - bytes
   - SHA256
   - page count
4. 英译本只能作 reference witness。中文译文必须从古希腊文底本出发。
5. 任何英译本影响译法判断时，必须写入 `qa/technical/reference_witness_diff_log.md`。

## 下一步 / Next Steps

- 优先通过图书馆或购买使用 Toomer 作为人工参考，不存入仓库。
- 继续寻找 Taliaferro 的合法 full-view 公版扫描；如果 HathiTrust 或其他图书馆将其标为 public domain/full view，再下载并哈希。
- 在没有合法完整下载前，保持 `NO_LAWFUL_FULL_DOWNLOAD_FOUND`。

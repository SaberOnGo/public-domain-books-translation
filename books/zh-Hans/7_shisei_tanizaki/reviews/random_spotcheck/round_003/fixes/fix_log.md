# 抽检返工记录 / Spot-Check Fix Log

status: "PASS" # PASS | FAIL

| unit_id | issue | fix_summary | fixed_file | fixed_by | verification |
| --- | --- | --- | --- | --- | --- |
| metadata/rights_checklist.md | 日本版权状态误按现行死后 70 年计算为 2036-01-01。 | 改为按日本 2018 年延长前死后 50 年、已消灭版权不恢复的规则记录，并补充文化厅参考来源。 | `metadata/rights_checklist.md`; `metadata/source_evidence.md`; `frontmatter/book_info.md`; `metadata/book.yaml` | Codex | 需在重建 EPUB 后复核 OPF `dc:rights`。 |
| frontmatter/book_info.md / metadata/book.yaml / package.opf | contributor 未写入个人名。 | 将读者信息页和 metadata contributor 改为 `LifeBook 书坊 SaberOnGo`；封面继续按封面 policy 使用 `LifeBook 书坊 译制`。 | `frontmatter/book_info.md`; `metadata/book.yaml`; `preproduction/stage1/production_spec.md` | Codex | 需在重建 EPUB 后复核 OPF `dc:contributor`。 |
| output/release/release_notes.md | 旧 release notes 有插入符污染，且 release_state 引用旧 round。 | 本轮不覆盖旧版本；最终通过 `release:create` 生成新 patch release，最新条目将位于 release_notes 顶部并引用最新 PASS round。 | `output/release/release_notes.md`; `output/release/release_state.json` | Codex | 需在 final release 后复核。 |
| reviews/random_spotcheck/round_003 | 最新轮 DRAFT，且本轮发现 P0/P1/P2。 | 写回 Agent A/B 评审、修复记录和闭环记录；因本轮发现问题，必须追加新 seed 轮次。 | `reviews/random_spotcheck/round_003/*` | Codex | round_003 不作为最终 PASS 轮；最终以追加轮次验证。 |

所有被抽检发现的问题必须在本文件关闭；仅重新抽样不等于关闭旧问题。

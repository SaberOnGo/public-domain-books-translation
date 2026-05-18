# 《环球航海记》精修闭环报告

结论：PASS_WITH_RECORDED_LIMITATIONS

## 范围

- 全书静态审查：`chapters/final/` 42/42。
- 关键章节信达雅复核：19 个章节，覆盖导言、合恩角风暴、坏血病、韦杰号失事、派塔袭击、格洛斯特号弃船、天宁岛、马尼拉大帆船、广州/澳门交涉、返航和术语表。
- 封面、书籍首页信息、metadata、rights、source evidence、EPUB 输出均纳入复查。

## 已修复

- 清理 Gutenberg/纸书尾部残留与可见省略号残留。
- 统一译制署名为 `LifeBook 书坊 SaberOnGo`。
- 修复 `publication_lint --fix` 对 YAML 缩进的破坏风险，并恢复 `metadata/chapter_title_map.yaml`。
- 修复关键章节中的事实/术语硬伤：`store-ship`、`barge`、`men and boys`、`Nuestra Señora de Cabadonga`、`General Don Jeronimo de Montero`、广州/澳门官职和税费表述、返航法国舰队险情段落。
- 修复术语表硬伤：船首锚、大副锚、斜桁帆、顶风停船、火枪手纵列、左舷重复括注、旧西班牙银币自指回链等。
- 将第三十七章标题改为更贴近原文偏见语气的 `中国人的诡计`，避免把 `trickery` 过度中性化为“周旋”。

## 验证

- `node scripts/full_book_refinement_audit.js; exit 0`
  - `source_files: 42`
  - `final_files: 42`
  - `issues: 0`
  - `long_paragraphs_over_420_cjk: 53`
- `npm run lint:publication`
  - 硬错误 0，`issues: []`，`warnings: []`。
- `npm run build:epub`
  - 生成 `output/book.epub`
  - 生成 `output/环球航海记.epub`
  - 生成 `output/cover.svg`
- `npm run check:epub`
  - `fatal=0`
  - `error=0`
  - `warning=0`

## 限制

- 53 个长段落已纳入静态审查和关键章节抽查范围；其存在主要来自原书长句与航海纪实段落，并非自动判定为漏译或排版错误。
- 本轮属于机器辅助精修与规则化审查闭环，不等同于人工出版终审。公开发布前仍建议人工抽查高密度航海术语、广州/澳门段历史称谓，以及术语表的帆装系统。

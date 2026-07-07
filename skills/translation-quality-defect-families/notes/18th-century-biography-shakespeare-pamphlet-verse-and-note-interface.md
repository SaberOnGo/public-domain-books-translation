# 18th-Century Biography: Shakespeare Pamphlet, Verse, and Note Interface

## 中文经验

- 发现方式：章节全量复查时，把作品题名、诗题、处决诗、人物称号和注号序列放在同一轮核对。十八世纪传记常在一两个生产单元内连续出现小册子全题、期刊诗题、引诗、政治处决人物和后设评论，注号很容易在第一次补译或润色后整体错位。
- 问题族：莎士比亚版本题名、长诗题、雅各布派处决诗和词典计划叙述同时出现时，译文可能出现三类缺陷：一是为了保留源题名而把 `Miss----`、`[*]` 或旧页码式标记带入读者正文；二是引诗按字面硬译，导致讽刺对象或呼语关系不清；三是一个遗漏注号造成后文全部注号偏移。
- 低成本审计：先比较源文与译文的 `\[\d+\]` 序列，必须完全一致；再扫 `[Page`, `A.D.`, `Ætat`, `--`, `[*]`, `[dagger]`；最后只对命中的长题名和引诗附近做源文对照，不要盲读全书。
- 修复模式：长英文题名可给中文可读题名和必要源文接口，但读者正文不保留机械遮名横线；可改为 `[blank]` 或其他可读说明。处决诗或讽刺诗先重建中文关系，例如呼语、主语、讽刺对象、政治阵营和称谓，再追求诗行节奏。
- 复查要求：任何注号、题名接口、诗句关系或源文残留修复后，该轮不得 PASS；必须追加一轮全章复查，确认注号序列、读者正文残留、题名接口和诗行关系同时闭合。

## English Note

- Detection: in full-chapter review, audit work titles, poem titles, execution
  verses, political names, and note-marker sequence together. Eighteenth-century
  biography often packs pamphlet titles, periodical verse, quoted poems,
  execution figures, and commentary into one unit, making note drift likely
  after edits.
- Family: Shakespeare edition titles, long poem titles, Jacobite execution
  verse, and dictionary-plan prose can create three recurring defects: source
  title artifacts such as `Miss----`, `[*]`, or page heads leak into reader text;
  verse is translated in a hard literal shell; or one missed marker shifts all
  later note numbers.
- Low-token audit: first compare source and target `\[\d+\]` sequences for exact
  equality; then scan `[Page`, `A.D.`, `Ætat`, `--`, `[*]`, and `[dagger]`.
  Inspect only the candidate long-title and quoted-verse contexts against the
  source before broader review.
- Fix pattern: provide a readable target title plus only the necessary source
  interface; do not preserve mechanical blank dashes in reader text. For
  execution or satirical verse, rebuild the target-language relation first:
  vocative, subject, satirical target, political party, and status title, then
  polish line rhythm.
- Recheck: after any fix to note markers, title interfaces, verse relation, or
  source residue, the round cannot PASS. Add a full-chapter recheck and confirm
  marker sequence, reader-facing residue scan, title interface, and verse
  relation all close.

# 18 世纪传记中的诗歌、剧场、注号与货币接口

## 中文经验

本类章节常把诗歌仿作、剧场上演、出版收益和传记轶事压在同一个生产单元里。复查时不要只看事实是否大体正确，要把四类接口一起检查：

- 注号邻接：演员名、引语词、诗行关键词旁的注号最容易在顺译时掉落。先用源文与译文的 `[数字]` 序列做机器比对，再回看注号落点是否仍贴近原文所注对象。
- 英制货币：`guinea/guineas` 一类词必须查本书术语表，不要凭音译习惯写成另一种常见译名。若译名会与数量连读混淆，应加量词，如“十枚几尼”“多五枚几尼”。
- 剧场术语：`catcalls`、`bow-string`、`behind the scenes`、`side boxes` 等在传记叙述中承担场景信息，应译成读者可见的中文剧场/物件词，不要留下英文或直译成无关物件。
- 拉丁或固定场所名：`genus irritabile`、`Green Room` 等若按专名策略需要源文接口，只在首次自然正文出现处括注；后文应回到中文译名。

低 token 审计顺序：先跑注号序列比对，再扫旧纸本标记和术语表禁用写法；随后只把命中的小上下文同源文对照，确认是专名策略例外还是正文残留。修复任何一项后，该轮不得 PASS，必须追加整章复查。

## English Note

In eighteenth-century biographical chapters that combine poetic imitation, theatre performance, publication payments, and anecdotes, audit the interfaces together. Compare note-marker sequences first, then scan glossary-forbidden currency renderings and theatre terms. Preserve source forms only where the proper-noun policy requires a first-use interface; otherwise rebuild the passage into readable target-language prose and rerun a full-chapter recheck after every fix.

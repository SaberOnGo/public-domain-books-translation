# 18th-century biography: ode, letter, and moral quotation interface

## 中文经验

- 问题族：十八世纪传记常在同一生产单元内切换叙述、整首诗、私人债务书信、出版预告信和拉丁道德引句。译文若只追求逐句准确，容易把诗译成散文化说明、把书信礼貌套语译成现代商务语，或把拉丁引句、书名和人名接口漏掉。
- 发现方式：优先扫描 `ODE`、`To DR.`、`SIR`、`Your most humble servant`、`No signature`、`Respicere`、`8vo.`、`Life of ...`、`Mr. Urban` 等文体切换和引用接口，再对小上下文做源译对照。
- 风险：诗歌韵律和宗教/德性语汇若被压平，读者会失去约翰生早期诗作的声调；债务书信若太现代，会削弱“宽限、抵押利息、勿告母亲”的道德压力；拉丁引句若只保留原文或只给意译，会破坏鲍斯威尔评判《萨维奇传》的论证接口。
- 修复方式：诗歌保持分行和抬高语体，但不硬造押韵；书信保留称谓、日期、署名和谦卑收束，财务词按十八世纪语境译为“宽限、利息、抵押债务、票据”等；拉丁或外语道德引句可按书内 display policy 保留源形一次，并紧跟可读中文释义；作品题名和出版地点按专名策略给首次源文接口。
- 复查方式：用 `rg` 扫 `ODE|Your most humble servant|No signature|Respicere|8vo\\.|Life of|Mr\\. Urban|forbearance|mortgage`，确认正文没有把文体标记当作普通叙述吞掉；再朗读诗段和书信段，检查中文是否分别像诗、十八世纪书信和传记评论。

## English reusable lesson

- Defect family: Eighteenth-century biography may switch within one unit among narration, a complete ode, private debt correspondence, publication notices, and Latin moral tags. A merely sentence-accurate translation can flatten the poem, modernize letter formulas, or lose the interfaces around Latin quotes, work titles, and names.
- Find it by scanning style-switch and quote-interface triggers such as `ODE`, `To DR.`, `SIR`, `Your most humble servant`, `No signature`, `Respicere`, `8vo.`, `Life of ...`, and `Mr. Urban`, then reviewing only the nearby source-target context.
- Risk: Flattened poetry loses Johnson's early poetic tone; modernized debt letters lose the moral pressure of forbearance, mortgage interest, and secrecy from his mother; mishandled Latin tags break Boswell's argument about the moral of `Life of Savage`.
- Fix by preserving lineation and elevated diction for poems without forcing rhyme; keeping salutation, date, signature, and humble closures in letters; rendering financial terms in period context; and pairing Latin or foreign moral tags with a readable target-language sense while applying the proper-noun display policy to work titles and publication places.
- Recheck with targeted `rg` scans for `ODE|Your most humble servant|No signature|Respicere|8vo\\.|Life of|Mr\\. Urban|forbearance|mortgage`, then read the revised poem and letters aloud as target-language poetry, period correspondence, and biographical commentary.

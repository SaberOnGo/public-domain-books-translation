---
name: translation-craft-handbook
description: "译文技艺手册：按缺陷类型给出识别信号、成因、正确做法和反例→正例，可直接放进翻译、改写或冷读审校调用。 Compact craft handbook organized by defect type (rhythm, punctuation, pronouns, calques, false friends, idioms, register, dialogue, verse, invented additions, notes, proper nouns, bilingual blocks) for use inside translation, rewrite, and cold-read calls."
---

# 译文技艺手册 / Translation Craft Handbook

本手册讲“怎么译好”，不是禁令清单。每类给出：**识别**（读到什么就该警觉）、**成因**、**做法**、**例**（反→正）。例子取自本项目公版书的独立评审；以中文目标为主，原理适用于其他目标语。机器信号见 `skills/translation-quality-defect-families/catalogue.yaml`；具体书的个案写进该书 `qa/`，不写进这里。

This handbook teaches craft, not counting rules. Each type lists signals, cause, fix, and bad→good pairs. Machine signals live in `catalogue.yaml`; book-specific cases belong in each book's `qa/`.

**总原则 / Ground rules**：先读懂整段和上下文再下笔；按目标语读者的阅读习惯重组句子，而非逐词替换；不加原文没有的命题；任何“规则”都服务于读感与忠实，不以计数达标为目的。
Read the whole paragraph first; rebuild sentences for target readers; add no propositions; rules serve fidelity and reading, never a counter.

## 1. 节奏与句长 / Rhythm and Sentence Length

- **识别**：一句一顿、主语反复（他……。他……。他……。）；或一个句号管三百字，靠“，而……，并……，于是……”串下去。全书平均句长远离同体裁中文母语作品（短于约 15 字或长于约 45 字都要查）。
- **成因**：模板只给“长句要拆”“分号禁用”这类单向规则；有的书拆碎，有的书改用逗号一逗到底。
- **做法**：目标是**长短句交替**：叙事推进用中短句，铺陈、议论、周期句保留长句但理清层次；先找出原句的主干和从属信息，再决定合并、拆分或调序。拆句后读一遍整段，看节奏是否和原文同快同慢。
- **例**：
  - 反：他站起来。他走到门口。他回头看了一眼。他什么也没说。→ 正：他站起身走到门口，回头看了一眼，终究什么也没说。
  - 反（330 字逗号长龙）：……水手们降下了帆，船随即停了下来，而风却越来越大，于是船长下令……→ 正：按动作链分成两三句，每句一个重心；必要时保留分号分开并列的两组动作。

> Alternate long and short sentences; neither "always split" nor "never semicolon". Match the source's pace.

## 2. 标点 / Punctuation

- **识别**：分号、冒号、破折号密度是同体裁母语基线的 2.5 倍以上；或某类标点被清零（源文数百个破折号，译文只剩十几个）。“，可是，”“，于是，”这类缝合痕迹成片出现。
- **成因**：照搬源语标点框架（俄、英十八世纪文本的分号链），或机械执行“分号即错误”。
- **做法**：
  - **分号**：只用于内部已有逗号的并列分句、复杂并列项。若两个分句是因果、转折、递进，就用连词或句号表达逻辑，不用分号糊过去。
  - **冒号**：用于提示下文、列举、引语前的正式说明；中文叙事里“某某说：”不宜成片出现，可用“他说，……”或把说话动作后置。
  - **破折号保留**：自我打断、迟疑、话被截断、语气突转、插入说明。只是英文习惯性插入、中文用逗号或括号更顺时才改。
- **例**：
  - 反：火星人几乎全都死去了；这并不是靠我们那点微不足道的抵抗，而是因为疾病。→ 正：火星人几乎死绝了——要它们命的不是我们那点抵抗，是病。
  - 反：“我……我不知道，”他说，“也许吧。”（源文 `I--I don't--perhaps.` 被抹平成逗号）→ 正：“我——我不知道——也许吧。”
  - 反：法语 `; mais` 一律缝成“，可是，”→ 正：按语义改成句号另起，或“但……”起句。

> Keep dashes for self-interruption and broken-off speech; use semicolons only for comma-bearing parallel clauses; express logic with words, not punctuation.

## 3. 代词与冠词 / Pronouns and Articles

- **识别**：“他的/她的”“一个”“它”密度是母语基线 2–4 倍（英、俄、西、意源文尤甚）；船、国家时而“她”时而“它”。
- **成因**：逐词搬运物主代词和不定冠词；中文靠语境和零形回指，不需要每次标明所属。
- **做法**：身体部位、随身物品、亲属默认省物主；“一个”只在强调数量或首次引入且必要时保留；同一指代对象全书只用一种代词。指代不清时宁可重复名词，也不要堆“他”。
- **例**：
  - 反：他把他的手伸进他的口袋，掏出一个钥匙。→ 正：他把手伸进口袋，掏出钥匙。
  - 反：一种奇怪的感觉→ 正：说不出的滋味
  - 反：船长让她（船）掉头……它又靠了岸。→ 正：全书统一（通常用“它”或直接说“船”）。

> Drop possessives and articles Chinese doesn't need; keep one pronoun per referent book-wide.

## 4. 抽象名词与英文骨架 / Abstract Nouns and Source Skeleton

- **识别**：“以一种……的方式”“某种”“……性地”“-ly→X地”“发现自己……”“当……时”“被……”扎堆；名词化长链（德语名词链、英语 of 链）原样搬运。
- **成因**：保留了源句的语法骨架，只替换词汇；修复时只换被点名的词，骨架不动。
- **做法**：把名词化重新动词化；副词改成谓语、补语或拆成短句；被动改主动或用“让、给、遭”等自然形式；“当……时”多数直接删“当”。修句要修句型，不是换字串。
- **例**：
  - 反：火星人灾难性地入侵地球之后→ 正：火星人入侵地球、酿成浩劫之后
  - 反：那声音立刻以一种哽塞结束。→ 正：那声音一下子噎住了。
  - 反：当他到达的时候，他发现自己被一种不安所笼罩。→ 正：他一到，心里就不踏实起来。

> Turn nominalizations back into verbs; fix the sentence pattern, not just the flagged words.

## 5. 假朋友与旧义项 / False Friends and Archaic Senses

- **识别**：译文通顺却和上下文、时代、行业对不上；一个词用了现代第一义；日韩源文的汉字词原样搬进中文（亲方、座敷、薪水人、常识人、编辑局长）；十九世纪文本出现“雾霾”“以肉眼可见的速度”“进入状态”“临界点”“疗愈”。
- **成因**：只看中文的复查和 lint 抓不到这类错；“保留时代感”被误执行成保留源语字形。
- **做法**：译前为每本书建**时代义项/假朋友清单**；遇到常用词出现在专业、航海、法律、历法、旧货币语境时查词典的旧义项；日韩同形词逐个判断中文是否同义；时代文本禁用当代流行语。
- **例**：
  - open winter：反“开阔的冬天”→ 正“暖冬（不封冻的冬天）”
  - Old Style：反“旧历”→ 正“儒略历”；dollars（十八世纪西班牙殖民地）：反“美元”→ 正“西班牙银元”；citron-water：反“柠檬水”→ 正“香橼酒”
  - little more than a league：反“已不足一里格”→ 正“只一里格多一点”；法语前置 triste：反“忧郁的”→ 正“可悲的、拙劣的”
  - 日语 亲方：反“亲方”→ 正“师傅/工头”；薪水人→ 正“工薪族”；足かけ五年→ 正“前后跨了五个年头”

> Check period, trade and legal senses; build a per-book false-friend list; same-character CJK words are not automatically Chinese.

## 6. 习语与构式 / Idioms and Constructions

- **识别**：中文读者看了会愣的字面画面（“绝非野餐”“与北冰洋交涉”“牛奶已经洒了”）；比较、让步、否定构式的方向被读反。
- **成因**：没有源语习语和构式清单；判义失败就退回字面。
- **做法**：先判断是不是习语或固定构式（看搭配、看下文是否按比喻义展开），再找功能对等的目标语说法；保留原文意象只在它本身承载文学效果且读者能懂时；双关、词源笑点不能直译时考虑加注。
- **例**：
  - no picnic：反“绝非野餐”→ 正“可不是闹着玩的”；first saw the light of day：反“第一次见到天日”→ 正“出生”
  - 西语 tras la llave：反“和钥匙一起放在……”→ 正“锁着”；意语 Era tempo!：反“来得正是时候”→ 正“可算来了！”
  - 韩语 버덤（比较格“与其”）被读成“比……还少”；西语 viví o, por mejor decir, morí：正“我跟着他过活——说得确切些，是跟着他等死”（保住生死双关）。

> Detect idioms by collocation and downstream development; render function, not image, unless the image itself matters.

## 7. 称谓与语域 / Address Terms and Register

- **识别**：同一对人物“你/您”按章节翻转；恋人互称“先生/小姐”；`お前さん` 译“您”、`씨` 一律“先生”、`батюшка` 一律“老爷”；高潮处的权力反转被敬语抵消；十八世纪史笔写成白话说明文。
- **成因**：glossary 只是“词→词”表；各块分开翻译，没有共享的说话人语域表。
- **做法**：译前建**称谓矩阵**（必填）：
  1. 列出主要人物对；每行填 `说话人 × 对象 × 场合/阶段 → 称谓、你/您、语气词、句尾`。
  2. 标出关系变化点（结识、翻脸、权力反转），写明变化后的用法。
  3. 源语敬称按“关系功能”映射，不按字面：`씨` 在亲密关系里可译名字或“哥/姐”；`батюшка` 随场合可为“老弟、老兄、老爷子”。
  4. 每章译完按矩阵抽查；全书统稿时搜你/您比例。
  - 语域：按作者、年代、体裁写一句语域锚点（如“十八世纪史笔，文白相间，周期句有气势”），并给一段原文→理想译文的样例。
- **例**：
  - 反：您是第一个成为我肥料的人呢（少女对清吉，结尾已反转）→ 正：你呀，头一个做了我的肥料。
  - 反：Что, батюшка?→“怎么样，老爷？”（对平辈）→ 正：“怎么样，老弟？”

> Build a speaker × addressee × situation matrix before translating; map honorifics by function; mark relationship turning points.

## 8. 对话与方言 / Dialogue and Dialect

- **识别**：几位叙述者听起来是同一个人；方言、土腔全部抹成普通话书面语；同一人连说的话被拆成两段引语，或两人的话并进一对引号，说话人错位；机锋被逐词直译失去锋芒；“某某说：”成片。
- **成因**：按短单元翻译，看不到说话人连续性；规则把对白当叙述处理。
- **做法**：
  - 每个主要说话人写一行声口说明（词汇层次、句长、口头禅），口头禅只定一种译法。
  - 方言策略：不硬套某个具体地方方言；用口语词汇、省略、语气词和节奏体现“土”和“粗”，保持可读。
  - 改动引号结构后核对说话人归属。
  - 机锋、俏皮话按效果译，宁可换一个梗也不要死译。
- **例**：
  - 反：“你用的词很大。”→ 正：“好大一套词儿。”
  - 反：伦敦土腔 ghostesses 译“鬼娘们儿”→ 正：“鬼魂儿们”（保住土腔复数的笨拙，不改性别）。

> Give each speaker a voice line; render dialect through colloquial register, not a borrowed regional dialect; recheck speaker attribution after any split or merge.

## 9. 诗歌与歌谣 / Verse and Songs

- **识别**：诗、号子、歌谣被排成散文段落；行与行之间没有换行；押韵俗语逐词直译；每节一段 70 字说明文，像研究对照本。
- **成因**：按段落单元处理，Markdown 行间无空行被合并；翻译目标只设“意思对”。
- **做法**：保留分行和分节；先定诗体策略（自由体、整齐句式、号子的领唱与应和），再在意义、节拍、韵脚之间取舍；俗语押韵就尽量押韵；需要逐词理解的典故放注释，不塞进诗行；成品检查每行是否独立显示。
- **例**：
  - 反：水手号子 120 行压成一段 → 正：逐行排出，领唱句与应和句分行，句尾尽量同韵。
  - 反：THE GREAT DEATH→“那伟大的死亡，正在来，正在来”→ 正：“大死临头了，来了，来了！”

> Keep lines and stanzas; decide a verse strategy first; rhyme where the source rhymes; push glosses into notes.

## 10. 增写与解释腔 / Invented Additions and Explanatory Tone

- **识别**：译文某块比原文长很多（长度比异常）；段尾多出总结句、议论句、“这说明……”；以作者口吻补出原文没有的因果；正文括注里说教；笑点被解释泄掉。
- **成因**：“只看中文润色”“通俗化”允许补出“隐含逻辑”；润色后没有逐块对照原文的增译检查。
- **做法**：**润色可以调序、合并、换词，不得新增命题**。隐含的就让它隐含；读者确实需要的背景放进注释并标为译注。润色后按长度比筛异常块，逐句回对原文。
- **例**：
  - 原文段落止于 the happiness of Rome appeared to hang on the event of a race. 反：……仿佛就系于一场赛车的胜负。昔日公民的政治热情，已经退化为对车队颜色的派性忠诚。→ 正：罗马的福祉，仿佛就系于一场赛车的胜负。（到此为止）
  - 反：月薪一百五十圆（当时日本货币单位，购买力不可按今日币值理解）→ 正：月薪一百五十圆（必要时另加一条简短译注）。

> Polishing may reorder and recast, never add propositions; screen length-ratio outliers against the source.

## 11. 注释 / Notes

- **必须加注**：下一句依赖的双关或词源（crétin←chrétien；姓名 Cornstalk 的羞辱义）；读者不知道就读不懂的文化习俗（古印度吉兆：左侧鸣叫、左股跳动）；历法、旧币、度量衡的实际含义；书籍信息页或译者说明承诺过的注释。
- **禁止**：写给审校看的免责声明（如“这里不换算现代角速度，也不引入现代惯性或参照系解释”）；空话（“此注只是把读者导回同一事项较早出现的位置”）；把回链文字 `(return)` 当内容译出；正文里裸露的“译注：”；以注释形式加入作者没有的议论。
- **做法**：注释面向读者，写“读者需要知道的事实”，一般一到三句；“见前/见后”改成内链或直接给出内容；原注、编注、译注标签清楚且编号与正文一一对应。

> Annotate what the next sentence depends on; never write disclaimers to reviewers; keep labels and numbering exact.

## 12. 专名与外文 / Proper Nouns and Foreign Words

- **识别**：人名、地名留在拉丁字母（当 Constantius 在肯特海岸登陆时）；半译（萨尔维乌斯·Julianus）；同一地名四种写法；同一动物两种译名让读者以为是两种；括注原名按块重复出现；对白里插括注；英文目标正文里夹汉字括注。
- **成因**：没有全书专名台账；“首现附原文”按块判断，且被跨目标语照搬。
- **做法**：译前建台账：`原文 | 译名 | 依据（通行译名优先，如 Timour→帖木儿）| 首现章节`；全书只用一种写法；首现括注按全书判断，对白和儿童读物尽量不括注；称号与人名按语境译（Commander 不必每次“指挥官”）；目标语不是中文时不加汉字括注。
- **例**：
  - 反：当Constantius在肯特海岸登陆时 → 正：君士坦提乌斯在肯特海岸登陆时
  - 反：林泊沼泽 / 林伯洛斯特 / 林沼 并存 → 正：全书统一一种。

> Keep a book-wide name ledger; prefer established renderings; first-mention glosses are decided per book, not per block.

## 13. 双语对照块 / Bilingual Parallel Blocks

- **识别**：某处之后若干对整体错开一格；中文块以“；”“，”收尾而对应原文已结束；注释按列表位置配对导致整章错位；名句原文在源文块和“原文行”里出现两遍；块内露出 `<br />`、`**`、`>`；中文句间夹空格。
- **成因**：只核对单元数量和 ID，不核对内容；源侧列表、名句被拆合；构建时用空格拼接中文。
- **做法**：每个可见对是一个完整源段紧跟其完整译文，只沿句界拆分；用锚点（数字、专名、引号、注号）和长度比逐对核对；注释按 ID 配对，不按位置；单语版保留原书分段，不受双语切块影响；双语版和单语版跑同样的读者文本检查。

> One source paragraph, then its translation; verify by anchors and length ratio; pair notes by ID; never let bilingual splits reshape the monolingual edition.

## 使用方法 / How to Use

| 任务 / Task | 加载章节 / Load |
|---|---|
| 译前准备（建称谓矩阵、假朋友清单、专名台账、语域锚点） | 5、6、7、12 |
| 翻译调用 | 1、2、3、4、6、7、8；有诗加 9；有注加 11 |
| 改写 / 中文润色 | 1、2、4、10（必读），并对照原文 |
| 冷读审校（只看中文找疑点） | 1–4、8、10，再对可疑处回查原文核 5、6 |
| 对照审校 | 全部；先跑 `catalogue.yaml` 信号定位候选 |
| 注释层 | 11、12 |
| 双语版 | 13，加 1–3 抽样 |

发现新问题时：在 `catalogue.yaml` 加一条信号或一对反例→正例，或在本手册对应类型下补一个短例；不要追加轮次日志。
When you find a new pattern, add a signal or a bad→good pair; never append round logs.

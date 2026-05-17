# 《Almagest》数学术语锁定 / Mathematical Term Lock

mathematical_term_lock_status: `BOOK_I10_PILOT_TERMS_EXTRACTED_NOT_FULL_LOCKED`

## 锁定层级 / Lock Levels

- `PILOT_LOCKED`: Book I 小样本必须使用，不得随意换译；后续发现希腊词或语境不匹配时走变更记录。
- `PROVISIONAL`: 只能作为候选，不得进入批量翻译。
- `BLOCKED`: 不允许翻译或现代化解释，必须先补证据。

## 证明动作词 / Proof Action Terms

| source_term | target_term | function | locked_status | notes |
|---|---|---|---|---|
| ἔστω / ὑποκείσθω / κείσθω | 设 / 令 | suppose/setup | PILOT_LOCKED_FOR_BOOK_I10 | use `设` for initial configuration; use `令` when setting equality or assumed value |
| ἤχθω / διήχθωσαν / ἀπειλήφθωσαν | 作 / 引出 / 截取 | construct/draw/take off | PILOT_LOCKED_FOR_BOOK_I10 | distinguish construction from conclusion; exact Chinese depends on geometric action |
| ἐπεζεύχθω / ἐπεζεύχθωσαν | 连结 | join/connect | PILOT_LOCKED_FOR_BOOK_I10 | for joining labeled points by straight lines |
| ἐκβεβλήσθω | 延长 | extend | PILOT_LOCKED_FOR_BOOK_I10 | line extension action; appears around `I_44_7` |
| TBD from figure audit | 交于 | intersect at | PROVISIONAL | point label must match diagram; exact Greek expression still needs figure-label audit |
| ἴση / ἴσον / ἴσα | 相等 / 等于 | equal | PILOT_LOCKED_FOR_BOOK_I10 | preserve whether relation is line-line, square-square, rectangle-square, or angle-angle |
| ἰσογώνιον | 等角 / 等角的 | equiangular/similar-triangle relation | PILOT_LOCKED_FOR_BOOK_I10 | do not flatten into generic `相似`; check each Euclid VI context |
| ἀνάλογον / πρὸς ... λόγον ἔχει | 成比例 / ... 与 ... 之比 | proportional/ratio relation | PILOT_LOCKED_FOR_BOOK_I10 | preserve ratio order; do not invert antecedent/consequent |
| ἄρα / ὥστε / φανερὸν | 于是 / 因而 / 可见 | inference | PILOT_LOCKED_FOR_BOOK_I10 | do not omit proof dependency |

## 几何对象 / Geometric Objects

| source_term | target_term | definition | first_location | locked_status | notes |
|---|---|---|---|---|---|
| labeled Greek letters Α, Β, Γ, Δ, Ε, Ζ, Η, Θ etc. | 点 | geometric point | Book I.10 | PILOT_LOCKED_FOR_BOOK_I10 | diagram labels must be stable; do not localize labels into Chinese words |
| εὐθεῖα / εὐθεῖα γραμμή | 直线 | straight line | Book I.10 | PILOT_LOCKED_FOR_BOOK_I10 | in chord context, may be explained as `弦` in note, but body should preserve source wording when it says straight line |
| κύκλος | 圆 | circle | Book I.10 | PILOT_LOCKED_FOR_BOOK_I10 | model vs geometric circle |
| περιφέρεια | 弧 / 圆周弧 | arc/circumference segment | Book I.10 | PILOT_LOCKED_FOR_BOOK_I10 | use `弧` when contrasted with subtending straight line; avoid generic `圆周` if local relation is arc |
| ὑποτείνουσα εὐθεῖα / ὑπὸ ... εὐθεῖα | 弦（原文作“某弧所对的直线”） | subtending straight line/chord | Book I.10 | PILOT_LOCKED_FOR_BOOK_I10_REVISED_FOR_READABILITY | 读者版正文优先用 `弦` 或 `某弧对应的弦`；章末注说明古希腊原文常按“某弧所对的直线”来表述。不得再写成难懂的“所对弧之半所对的直线”。 |
| γωνία | 角 | angle | Book I.10 | PILOT_LOCKED_FOR_BOOK_I10 | sexagesimal policy required when numerical |
| διάμετρος | 直径 | diameter | Book I.10 | PILOT_LOCKED_FOR_BOOK_I10 | chord-table geometry |
| ἐκ τοῦ κέντρου | 从圆心所出之线 / 半径 | radius-like line from center | Book I.10 | PILOT_LOCKED_FOR_BOOK_I10 | use `半径` only with note or when mathematical relation clearly requires modern term |
| κέντρον | 圆心 | center | Book I.10 | PILOT_LOCKED_FOR_BOOK_I10 | preserve labeled center point |

## 证明关系 / Proof Relations

| source_expression | target_expression | relation_type | locked_status | notes |
|---|---|---|---|---|
| ἐπεὶ / ἐπεὶ οὖν / ἐπεὶ γὰρ | 因为 / 既然 / 由于 | cause/premise | PILOT_LOCKED_FOR_BOOK_I10 | choose by Chinese readability but preserve premise order |
| ἄρα / ὥστε | 所以 / 于是 / 因而 | result | PILOT_LOCKED_FOR_BOOK_I10 | preserve proof relation |
| προκείμενα / προδεδειγμένα / ἔμπροσθεν | 以上所立 / 前已证明 / 前文 | reference_to_prior_proposition | PILOT_LOCKED_FOR_BOOK_I10 | must include dependency when present |

## Book I.10 关键技术词 / Book I.10 Technical Terms

| source_term | target_term | locked_status | evidence |
|---|---|---|---|
| τμήματα | 分 | PILOT_LOCKED_FOR_BOOK_I10 | diameter divided into `ρκ` parts and circumference into `τξ` parts |
| μοῖρα / μοίρας | 度 | PILOT_LOCKED_FOR_BOOK_I10 | arc measures such as one degree, half-degree, etc. |
| ἑξηκοντάδος τρόπος | 六十进制法 | PILOT_LOCKED_FOR_BOOK_I10 | Book I.10 opening explains computation by sixtieths |
| ἔγγιστα | 约 / 近似为 | PILOT_LOCKED_FOR_BOOK_I10 | numerical approximations; must not be silently rounded |
| ἑξηκοντάδος numerical notation | 读者版：`37p04′55″`；校验版：`37;4,55` | PILOT_LOCKED_FOR_BOOK_I10_REVISED_FOR_READABILITY | 非角度数值在正文和 EPUB 可见文字中使用 `p` 加六十进制小分；numeric validation log 可保留原始校验记法。不得写作 `37份4′55″`，也不得统一转成十进制小数。 |
| τετράγωνον | 平方 | PILOT_LOCKED_FOR_BOOK_I10 | geometric square-on-line relation; translate by context as `以...为边的正方形` when needed |
| ὀρθογώνιον | 矩形 / 直角形 | PILOT_LOCKED_FOR_BOOK_I10 | Euclidean rectangle relation; avoid modern algebra-only wording in proof body |
| πεντάγωνον / δεκάγωνον / ἑξάγωνον | 五边形 / 十边形 / 六边形 | PILOT_LOCKED_FOR_BOOK_I10 | polygon-side arguments in first proof |
| ἄκρον καὶ μέσον λόγον | 外中比 / 极与中比 | PROVISIONAL | Euclid golden-section phrase; Chinese term must be checked against math translation convention before final |

## Book I.1 学科分类术语 / Book I.1 Disciplinary Terms

| source_term | target_term | locked_status | evidence |
|---|---|---|---|
| θεωρητικόν | 理论部分 / 理论的 | PRELOCK_FOR_BOOK_I1 | 与 `πρακτικόν` 对举；不得现代化为单纯“理论科学” |
| πρακτικόν | 实践部分 / 实践的 | PRELOCK_FOR_BOOK_I1 | 指行动/伦理相关领域；不得译成“应用科学” |
| φυσικόν | 自然学 | PRELOCK_FOR_BOOK_I1 | 古代 natural philosophy 语境；正文避免直接写成现代“物理学” |
| μαθηματικόν / μαθηματικά | 数学 / 数学诸学 | PRELOCK_FOR_BOOK_I1 | 本书中通向天文理论；不得缩窄为现代数学系意义 |
| θεολογικόν | 神学性研究 / 神学部分 | PRELOCK_FOR_BOOK_I1 | 亚里士多德式理论哲学分类；不作现代宗教教义化 |
| οὐράνια | 天体 / 天上事物 | PRELOCK_FOR_BOOK_I1 | 与 `θεῖα καὶ οὐράνια` 连用时保留古代天文学语境 |

## Book I.2 全书次序与天文学对象术语 / Book I.2 Ordering and Astronomical Objects

| source_term | target_term | locked_status | evidence |
|---|---|---|---|
| τάξις / τάξεως | 次序 / 安排次序 | PRELOCK_FOR_BOOK_I2 | 本章说明整部论著的论证先后，不译成现代课程目录 |
| θεώρημα / θεωρία / ἐπίσκεψις | 定理 / 理论考察 / 考察 | PRELOCK_FOR_BOOK_I2 | 按语境区分命题、理论研究和检视过程 |
| λοξὸς κύκλος | 黄道斜圈 / 倾斜圆 | PRELOCK_FOR_BOOK_I2 | 指黄道相关大圈；终稿前需与 Book I.12-I.15 统一 |
| οἰκουμένη | 居住世界 / 我们所居之地 | PRELOCK_FOR_BOOK_I2 | 古代地理-天文学语境，不等同现代全球地理 |
| ὁρίζων | 地平圈 / 地平线 | PRELOCK_FOR_BOOK_I2 | 按球面天文学上下文决定“圈/线” |
| ἐγκλίσεις | 倾斜 / 纬度差异相关倾角 | PRELOCK_FOR_BOOK_I2 | 需避免现代物理“倾角”泛化 |
| ἠλιακὴ κίνησις / σεληνιακὴ κίνησις | 太阳运动 / 月亮运动 | PRELOCK_FOR_BOOK_I2 | 以古代天文学模型语境表达，不现代化为真实物理轨道 |
| ἀπλανῶν σφαῖρα | 恒星天球 / 固定星天球 | PRELOCK_FOR_BOOK_I2 | 后续星表和恒星球章节需统一 |
| πέντε πλανῆται | 五个行星 | PRELOCK_FOR_BOOK_I2 | 古代五行星，不含太阳、月亮在此处的后续五行星模块 |
| φαινόμενα / τηρήσεις | 显见现象 / 观测 | PRELOCK_FOR_BOOK_I2 | 本章把显见现象和可靠观测作为证明基础 |
| γραμμικαὶ ἔφοδοι | 几何路线 / 线性几何方法 | PRELOCK_FOR_BOOK_I2 | 指通过几何证明推进，终稿前需统一为更自然中文 |

## Book I.3 天球运动与观测反证术语 / Book I.3 Heavenly Motion Terms

| source_term | target_term | locked_status | evidence |
|---|---|---|---|
| σφαιροειδῶς φέρεται | 以球形方式运动 / 作球形运动 | PRELOCK_FOR_BOOK_I3 | 题名和全章主命题；不得改写成现代自转/公转机制 |
| ἀνατολαί / δυσμαί | 升起 / 落下；东方 / 西方 | PRELOCK_FOR_BOOK_I3 | 视语境区分方向和天体升落现象 |
| παράλληλοι κύκλοι | 平行圆 | PRELOCK_FOR_BOOK_I3 | 天体每日运动圆；后续需与球面术语统一 |
| αἰεὶ φανεροὶ ἀστέρες | 恒显星 / 常显星 | PRELOCK_FOR_BOOK_I3 | 指永远不落入地平以下的星 |
| περιστροφὴ κυκλοτερής | 圆形回转 / 圆周式旋转 | PRELOCK_FOR_BOOK_I3 | 观测依据，不现代化为物理旋转动力学 |
| πόλος | 极 / 天球极 | PRELOCK_FOR_BOOK_I3 | 天球旋转中心点；后续北极/南极语境需细分 |
| οὐρανία σφαῖρα | 天球 | PRELOCK_FOR_BOOK_I3 | 几何模型术语 |
| ἐπʼ εὐθείας ... ἐπʼ ἄπειρον | 沿直线向无穷远运动 | PRELOCK_FOR_BOOK_I3 | 反证对象；不能误译为“无限直线轨道” |
| ὁρίζοντες | 地平圈 / 地平处 | PRELOCK_FOR_BOOK_I3 | 视上下文处理为几何圈或视见处 |
| ἀναθυμίασις | 蒸腾气 / 湿气蒸腾 | PRELOCK_FOR_BOOK_I3 | 地平处视大小解释；不现代化为大气折射 |
| ὡροσκοπία | 升度/时刻观测构造 | PRELOCK_FOR_BOOK_I3 | 需后续查上下文决定是否译作“升度盘/时刻构图” |
| αἰθήρ | 以太 | PRELOCK_FOR_BOOK_I3 | 古代自然学术语，不作现代物理以太 |
| ὁμοιομερής / ὁμοιομέρεια | 同质 / 同质性 | PRELOCK_FOR_BOOK_I3 | 支撑球形与均匀圆运动的自然学论证 |

## Book I.4 地球球形与观测证据术语 / Book I.4 Earth-Sphericity Terms

| source_term | target_term | locked_status | evidence |
|---|---|---|---|
| σφαιροειδής | 球形的 / 近似球形的 | PRELOCK_FOR_BOOK_I4 | 题名和主命题；不得改写为现代地球椭球模型 |
| πρὸς αἴσθησιν | 就感官观察而言 / 就可见现象而言 | PRELOCK_FOR_BOOK_I4 | 限定证明范围，不等同现代测地学精度 |
| καθʼ ὅλα μέρη | 按整体各部分看 / 从整体各部分说 | PRELOCK_FOR_BOOK_I4 | 保留“整体部分”限定，避免写成局部地形平滑 |
| ἐκλειπτικὰς φαντασίας | 食的现象 / 食象 | PRELOCK_FOR_BOOK_I4 | 尤其用于月食同时发生而各地记录时刻不同 |
| σεληνιακαί | 月食的 / 月亮相关的 | PRELOCK_FOR_BOOK_I4 | 本章以月食记录为主要观测证据 |
| μεσημβρία | 正午 / 子午 | PRELOCK_FOR_BOOK_I4 | 本章说与正午等距的小时；后续地理章节需统一 |
| ἀνατολικώτεροι / δυτικώτεροι | 较东者 / 较西者 | PRELOCK_FOR_BOOK_I4 | 观测者地理经度差异，不现代化为时区 |
| κυρτότης | 凸曲 / 曲率 | PRELOCK_FOR_BOOK_I4 | 地面/水面遮蔽与逐渐显现的核心术语 |
| ἐπιπροσθήσεις | 遮蔽 / 遮挡 | PRELOCK_FOR_BOOK_I4 | 地球凸曲造成的遮挡，不译成抽象“增加” |
| κοίλη / ἐπίπεδος | 凹面 / 平面 | PRELOCK_FOR_BOOK_I4 | 反证地球形状备选 |
| τρίγωνον / τετράγωνον / πολύγωνον | 三角形 / 四边形 / 多边形 | PRELOCK_FOR_BOOK_I4 | 反证多边形地表设想 |
| κυλινδροειδής | 圆柱形的 | PRELOCK_FOR_BOOK_I4 | 反证圆柱形地球设想 |
| τοῦ κόσμου πόλοι | 世界的极 / 天极 | PRELOCK_FOR_BOOK_I4 | 与圆柱轴向和恒显星判断相关 |
| ἄρκτοι | 北方 / 北极一带 | PRELOCK_FOR_BOOK_I4 | 字面为“大熊”方向，译文按天文方位处理 |
| προσπλέωμεν | 航近 / 船行接近 | PRELOCK_FOR_BOOK_I4 | 山或高地从海面逐渐显现的观测证据 |

## Book I.5 地球居中与观测反证术语 / Book I.5 Earth-Centrality Terms

| source_term | target_term | locked_status | evidence |
|---|---|---|---|
| μέση τοῦ οὐρανοῦ | 位于天的中央 / 位于天球中央 | PRELOCK_FOR_BOOK_I5 | 题名和主命题；不现代化为近代力学中心 |
| κέντρον σφαίρας | 球心 / 球的中心 | PRELOCK_FOR_BOOK_I5 | 地球相对天球位置的核心比拟 |
| ἄξων | 轴 / 天轴 | PRELOCK_FOR_BOOK_I5 | 三种非居中位置的反证结构 |
| πόλοι | 极 / 天极 | PRELOCK_FOR_BOOK_I5 | 与 I.3、I.4 的极/天极术语保持一致 |
| ὀρθὴ σφαῖρα | 正球 / 正置天球 | PRELOCK_FOR_BOOK_I5 | 终稿前需与球面天文学章节统一 |
| ἐγκεκλιμένη σφαῖρα | 斜球 / 倾斜天球 | PRELOCK_FOR_BOOK_I5 | 终稿前需与 Book I.12-I.16 统一 |
| ἰσημερία | 二分 / 昼夜平分 | PRELOCK_FOR_BOOK_I5 | 结合春秋二分和昼夜等分语境处理 |
| ὁρίζων | 地平圈 / 地平线 | PRELOCK_FOR_BOOK_I5 | 本章几何论证中优先“地平圈” |
| ἰσημερινός | 赤道圈 / 昼夜平分圈 | PRELOCK_FOR_BOOK_I5 | 与后续斜圈、平行圈术语统一 |
| μεσουράνησις | 中天 | PRELOCK_FOR_BOOK_I5 | 升起到中天、从中天到落下的时间关系 |
| κλίματα | 气候带 / 纬度带 | PRELOCK_FOR_BOOK_I5 | 古代地理天文学术语，不作现代气候学解释 |

## Book I.6 地球尺度与观测平面术语 / Book I.6 Earth-Scale Terms

| source_term | target_term | locked_status | evidence |
|---|---|---|---|
| σημείου λόγον ἔχει | 具有点的比例 / 只相当于一点 | PRELOCK_FOR_BOOK_I6 | 主命题；正文优先用易懂表达，注释说明希腊文比例语 |
| πρὸς αἴσθησιν | 就感官观察而言 / 就可见现象而言 | PRELOCK_FOR_BOOK_I6 | 与 Book I.4 一致，限定可感尺度 |
| ἀπλανῶν σφαῖρα | 恒星天球 / 固定星天球 | PRELOCK_FOR_BOOK_I6 | 与 Book I.2 术语保持一致 |
| ἀπόστημα / ἀπόστασις | 距离 / 相距 | PRELOCK_FOR_BOOK_I6 | 指相对于天体距离的尺度关系，不现代化为实测天文距离 |
| μεγέθη καὶ διαστήματα τῶν ἄστρων | 星体的大小和间距 | PRELOCK_FOR_BOOK_I6 | 各地观测无差异的证据 |
| κλίματα | 气候带 / 纬度带 | PRELOCK_FOR_BOOK_I6 | 与 Book I.5 一致，古代地理天文学术语 |
| γνώμων | 晷针 / 日晷表针 | PRELOCK_FOR_BOOK_I6 | 本章用于影子转动和观测设置 |
| κρικωταὶ σφαῖραι | 环仪 / 环形球仪 | PRELOCK_FOR_BOOK_I6 | 终稿前需与仪器术语统一 |
| διοπτεύσεις | 瞄准观测 / 观测视准 | PRELOCK_FOR_BOOK_I6 | 不泛化为现代望远镜观测 |
| περιαγωγαὶ τῶν σκιῶν | 影子的转动轨迹 | PRELOCK_FOR_BOOK_I6 | 与晷针观测相关 |
| ὁρίζοντες | 地平圈 / 地平平面 | PRELOCK_FOR_BOOK_I6 | 本章指由视线平面形成的地平 |
| διχοτομεῖν | 二分 / 分成相等两半 | PRELOCK_FOR_BOOK_I6 | 用于地平平面二分天球 |

## Book I.7 地球静止与自然运动术语 / Book I.7 Earth-Stability Terms

| source_term | target_term | locked_status | evidence |
|---|---|---|---|
| κίνησις μεταβατική | 平移运动 / 位置迁移 | PRELOCK_FOR_BOOK_I7 | 题名主术语；区别于 `στροφή` 旋转 |
| μεθίστασθαι | 离开原处 / 改换位置 | PRELOCK_FOR_BOOK_I7 | 指离开世界中心处所 |
| τὸ κατὰ τὸ κέντρον τόπος | 位于中心的处所 | PRELOCK_FOR_BOOK_I7 | 与 Book I.5 的地球居中命题连续 |
| φορά | 运动 / 载动 / 趋向运动 | PRELOCK_FOR_BOOK_I7 | 按上下文区分自然运动和整体运动，不统一硬译 |
| τὰ βάρη | 重物 / 有重量的物体 | PRELOCK_FOR_BOOK_I7 | 古代重轻自然学术语，不等同现代质量 |
| ἐφαπτομένον ἐπίπεδον | 切平面 | PRELOCK_FOR_BOOK_I7 | 可用现代几何术语帮助中文可读性 |
| ἄνω / κάτω | 上 / 下 | PRELOCK_FOR_BOOK_I7 | 本章需说明“上”朝宇宙外围、“下”向地心 |
| ὁμοιομερής | 同质 / 各部分同类 | PRELOCK_FOR_BOOK_I7 | 与 Book I.3 同质性术语保持一致 |
| ἀτρεμοῦσα | 静止着 / 不动 | PRELOCK_FOR_BOOK_I7 | 描述地球整体静止 |
| στροφή / περιστροφή | 旋转 / 回转一周 | PRELOCK_FOR_BOOK_I7 | 用于被反驳的地球每日自转设想 |
| ἄξων | 轴 / 天轴 | PRELOCK_FOR_BOOK_I7 | 与 Book I.5 术语统一 |
| ἀπὸ δυσμῶν ἐπʼ ἀνατολάς | 从西向东 | PRELOCK_FOR_BOOK_I7 | 地球自转设想的方向 |
| ἀήρ | 空气 | PRELOCK_FOR_BOOK_I7 | 不展开成现代大气层物理 |
| ἱπτάμενα / βαλλόμενα | 飞行物 / 抛射物 | PRELOCK_FOR_BOOK_I7 | 云、飞行物、抛射物现象链的一部分 |
| ὑπολείπεσθαι | 滞后 / 落在后面 | PRELOCK_FOR_BOOK_I7 | 反驳地球自转时的关键现象词 |

## Book I.8 天球两种基本运动术语 / Book I.8 Primary Motion Terms

| source_term | target_term | locked_status | evidence |
|---|---|---|---|
| πρῶται κινήσεις | 最初运动 / 基本运动 | PRELOCK_FOR_BOOK_I8 | 题名主术语；指天球运动的基本类别 |
| πρώτη φορά / πρώτη περιαγωγή | 第一运动 / 第一载动 / 第一回转 | PRELOCK_FOR_BOOK_I8 | 全天自东向西的日周运动 |
| δευτέρα φορά / δευτέρα διαφορά | 第二运动 / 第二类运动 | PRELOCK_FOR_BOOK_I8 | 与第一运动相反，绕黄道斜圈的极 |
| ἰσημερινός | 赤道圈 / 昼夜平分圈 | PRELOCK_FOR_BOOK_I8 | 正文用“赤道圈”，注释解释昼夜平分语源 |
| ὁρίζων | 地平圈 | PRELOCK_FOR_BOOK_I8 | 本章以大圈二分赤道圈为核心 |
| λοξὸς κύκλος | 黄道斜圈 / 相对于赤道倾斜的大圈 | PRELOCK_FOR_BOOK_I8 | 与 Book I.2 的黄道相关术语保持一致 |
| πλανώμενοι ἀστέρες | 行星 / 游移星 | PRELOCK_FOR_BOOK_I8 | 古代“游移的星”，正文可用“行星” |
| ἀπλανεῖς / λοιπὰ ἄστρα | 恒星 / 其余星体 | PRELOCK_FOR_BOOK_I8 | 与行星区别 |
| μεσουράνησις | 中天 | PRELOCK_FOR_BOOK_I8 | 每日升起、中天、落下现象链 |
| μεσημβρινός | 子午圈 | PRELOCK_FOR_BOOK_I8 | 需说明其与通过赤道极和黄道极的大圈不同 |
| ἰσημερινά | 二分点 | PRELOCK_FOR_BOOK_I8 | 黄道与赤道圈的两个交点 |
| ἐαρινόν / μετοπωρινόν | 春分点 / 秋分点 | PRELOCK_FOR_BOOK_I8 | 以太阳沿黄道由南向北或由北向南通过赤道为准 |
| τροπικά | 二至点 | PRELOCK_FOR_BOOK_I8 | 黄道与通过两组极的大圈的两个交点 |
| χειμερινόν / θερινόν | 冬至点 / 夏至点 | PRELOCK_FOR_BOOK_I8 | 按相对赤道的南北极限命名 |
| πρὸς ἄρκτους / πρὸς μεσημβρίαν | 向北 / 向南 | PRELOCK_FOR_BOOK_I8 | 方向术语，不按字面硬译为“大熊/正午” |

## Book I.9 具体测定与弦论引入术语 / Book I.9 Preliminaries to Chords

| source_term | target_term | locked_status | evidence |
|---|---|---|---|
| κατὰ μέρος καταλήψεις | 各项具体测定 / 逐项测定 | PRELOCK_FOR_BOOK_I9 | 题名主术语；连接后续各项证明 |
| ὁλοσχερὴς προδιάληψις | 总括性的预先说明 | PRELOCK_FOR_BOOK_I9 | 回指 I.1-I.8 的总论 |
| κατὰ μέρος ἀποδείξεις | 逐项证明 / 各项具体证明 | PRELOCK_FOR_BOOK_I9 | 进入后续数学证明 |
| προειρημένοι πόλοι | 前述两极 | PRELOCK_FOR_BOOK_I9 | 回指 I.8 的两组极关系 |
| περιφέρεια | 弧 / 圆周弧 | PRELOCK_FOR_BOOK_I9 | 与 I.10 弧/弦术语保持一致 |
| διʼ αὐτῶν γραφόμενος μέγιστος κύκλος | 通过这些极画出的大圈 | PRELOCK_FOR_BOOK_I9 | 连接 I.8 的大圈结构 |
| πηλικότης τῶν ἐν τῷ κύκλῳ εὐθειῶν | 圆内直线的大小 / 弦长问题 | PRELOCK_FOR_BOOK_I9 | 正文可说“圆内直线的大小”，注释说明即后续弦长理论 |
| γραμμικῶς ἀποδεικνύειν | 按几何线图证明 / 用几何方法证明 | PRELOCK_FOR_BOOK_I9 | 不改写成代数推导 |

## 当前限制

Book I.10 试译可使用 `PILOT_LOCKED_FOR_BOOK_I10` 条目。正式全书锁定必须等 Book I 古希腊文原文切分、术语抽取、图表核验和数学审校完成；任何变更必须写入 `qa/technical/terminology_change_log.md`。

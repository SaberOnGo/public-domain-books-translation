# 《环球航海记》译前研究

## 文本身份

本工程依据 Project Gutenberg #16611 `Anson's Voyage Round the World`。Gutenberg 作者字段为 Richard Walter，评注者为 H. W. Household，主题人物为 George Anson。中文读者可能更熟悉“安森环球航行/安森远征”，但 metadata 不应把 George Anson 简化为唯一作者。

## 历史与题材

叙事核心是 1740-1744 年安森率英国舰队在詹金斯的耳朵战争背景下远征太平洋，经历合恩角风暴、坏血病、胡安·费尔南德斯休整、劫掠派塔、追捕马尼拉大帆船、抵达澳门和广州、最终返英。文本兼具航海纪实、军事行动报告、帝国贸易叙事和 1901 年教材缩编特征。

## 中文翻译策略

- 叙事语气：保持纪实、节制、清楚，不把 18 世纪行动报告译成现代冒险小说腔。
- 句法：英文长句应拆为自然中文，但必须保留因果、时间顺序和航海行动链。
- 专名：船名使用中文译名加“号”，如 `Centurion` 译“百夫长号”，首次出现可在术语表记录英文。
- 地名：通行译名优先，如 Madeira 马德拉、Macao 澳门、Canton 广州、Cape of Good Hope 好望角。
- 历史视角：殖民、战争、清代官场和对外族群的判断按原文语气忠实呈现，必要时用译注或术语表说明，不用现代价值判断替作者改写。
- 标题：EPUB 目录使用短题名，纸书目录式长标题保存在 `metadata/chapter_title_map.yaml` 的 `source_full`。

## 重点术语域

- 航海与船体：squadron、consort、prize、pink、galleon、refit、leak、scuttle、soundings。
- 战争与捕获：Commodore、privateer、viceroy、mandarin、prisoners、treasure。
- 疾病与补给：scurvy、provisions、watering、wooding、stores。
- 地理与航线：Cape Horn、Juan Fernandez、Tinian、Ladrones、Macao、Canton River、Table Bay、Spithead。

## 质量风险

- 易把 `prize` 误译成“奖品”，本书中多指“捕获船/战利品船”。
- `pink` 是船型，不是颜色。
- `Canton` 在本书语境中为广州，不应泛译“广东”。
- 原书中 `Chinese trickery` 等标题含时代偏见，中文标题宜保留历史叙事事实但避免扩大为现代族群判断。
- Gutenberg 1901 缩编版含编辑导言和术语表，需在版本说明中标明。

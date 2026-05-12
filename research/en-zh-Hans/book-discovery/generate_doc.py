import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_OUTPUT = SCRIPT_DIR / "public_domain_book_audit.md"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate the English-to-Simplified-Chinese candidate book discovery report."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Output Markdown path. Defaults to public_domain_book_audit.md next to this script.",
    )
    return parser.parse_args()

data = {
    "categories": [
        {
            "name": "旅行记与探险 (Travelogues & Exploration)",
            "books": [
                {
                    "title_en": "Through the Heart of Patagonia",
                    "title_zh": "穿过巴塔哥尼亚的心脏",
                    "author": "H. Hesketh-Prichard",
                    "author_bio": "Hesketh Vernon Hesketh-Prichard (1876-1922)，英国探险家、猎人、狙击手和作家。他曾游历多国，并在第一次世界大战中为英国陆军狙击手训练做出巨大贡献。",
                    "major_works": "《Through the Heart of Patagonia》, 《Sniping in France》",
                    "content": "记录了作者在南美洲巴塔哥尼亚高原的探险经历，最初是为了寻找传说中的巨型地懒，书中详细描写了当地的地理、动植物群及高乔人的生活。",
                    "pages": 346,
                    "difficulty": "中等 (涉及部分生物学和地理学术语)",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "A Woman's Trek from the Cape to Cairo",
                    "title_zh": "一个女人的开普敦到开罗之旅",
                    "author": "Mary Hall",
                    "author_bio": "Mary Hall (1857-1912)，英国旅行家。她是第一位完成从南非开普敦到埃及开罗纵穿非洲大陆旅行的女性。",
                    "major_works": "《A Woman's Trek from the Cape to Cairo》",
                    "content": "记录了作者在20世纪初孤身一人，依靠搬运工和当地向导穿越非洲大陆的非凡旅程，提供了当时非洲殖民地社会的珍贵第一手资料。",
                    "pages": 424,
                    "difficulty": "容易 (主要是游记和个人日记风格)",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "The Land of the Black Mountain",
                    "title_zh": "黑山之地",
                    "author": "Reginald Wyon & Gerald Prance",
                    "author_bio": "Reginald Wyon (1860s-?) 和 Gerald Prance，20世纪初的英国旅行家和新闻记者，热衷于探索巴尔干半岛的未知区域。",
                    "major_works": "《The Land of the Black Mountain》",
                    "content": "这是一部关于黑山（Montenegro）的游记，描绘了当时巴尔干半岛的复杂政治局势、风俗习惯和壮丽的高山风光。",
                    "pages": 300,
                    "difficulty": "中等",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "In the Tail of the Peacock",
                    "title_zh": "在孔雀的尾巴里：摩洛哥游记",
                    "author": "Isabel Savory",
                    "author_bio": "Isabel Savory (约1870-?)，英国作家和旅行家，喜欢在维多利亚晚期至爱德华时代前往异国他乡探险。",
                    "major_works": "《In the Tail of the Peacock》, 《A Sportswoman in India》",
                    "content": "记录了作者在摩洛哥的旅行。书名取自摩洛哥谚语“地球是一只孔雀，摩洛哥是它的尾巴”。书中描写了迷人的阿拉伯风情与文化冲突。",
                    "pages": 352,
                    "difficulty": "中等",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "Alone in West Africa",
                    "title_zh": "孤身西非行",
                    "author": "Mary Gaunt",
                    "author_bio": "Mary Gaunt (1861-1942)，澳大利亚出生，后移居英国的小说家和旅行家。她在丈夫去世后开始了独自环球旅行的生涯。",
                    "major_works": "《Alone in West Africa》, 《A Woman in China》",
                    "content": "详细记录了她穿越西非黄金海岸（今加纳）、利比里亚等地的经历，探讨了殖民地的管理、热带病害以及当地土著的生活方式。",
                    "pages": 404,
                    "difficulty": "中等",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "A Girl's Ride in Iceland",
                    "title_zh": "一个女孩的冰岛骑行",
                    "author": "Ethel Brilliana Tweedie (Mrs. Alec-Tweedie)",
                    "author_bio": "Ethel Brilliana Tweedie (1862-1940)，英国多产作家、摄影师和女权主义者。她经常以“Mrs. Alec-Tweedie”作为笔名发表旅行见闻。",
                    "major_works": "《A Girl's Ride in Iceland》, 《Mexico as I Saw It》",
                    "content": "1889年作者和朋友骑马穿越冰岛的游记。不仅详细记载了沿途的地热奇观与间歇泉，还因为提倡女性跨骑（而非侧骑）在当时引起了一定轰动。",
                    "pages": 166,
                    "difficulty": "容易",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "Through the Unknown Pamirs",
                    "title_zh": "穿越未知的帕米尔",
                    "author": "O. Olufsen",
                    "author_bio": "Ole Olufsen (1865-1929)，丹麦军官和探险家，也是丹麦皇家地理学会的活跃成员。曾多次带队前往中亚进行科学考察。",
                    "major_works": "《Through the Unknown Pamirs》",
                    "content": "记录了由丹麦资助的第二帕米尔探险队在瓦罕走廊和帕米尔高原考察的过程，涵盖了对当地民族学、气候学和动物学的详细调查。",
                    "pages": 238,
                    "difficulty": "困难 (包含大量地理和人类学学术名词)",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "A Vagabond in the Caucasus",
                    "title_zh": "高加索的流浪者",
                    "author": "Stephen Graham",
                    "author_bio": "Stephen Graham (1884-1975)，英国记者、旅行家。他对俄罗斯文化极度痴迷，曾多次步行穿越俄罗斯帝国。",
                    "major_works": "《A Vagabond in the Caucasus》, 《With the Russian Pilgrims to Jerusalem》",
                    "content": "讲述了作者放弃在伦敦的安稳生活，前往高加索地区漫游的经历。他在山间与流浪汉、牧民为伍，记录了革命前夕俄国边缘地带的独特风貌。",
                    "pages": 311,
                    "difficulty": "中等 (文学性较强)",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "A Year in Brazil",
                    "title_zh": "在巴西的一年",
                    "author": "Hastings Charles Dent",
                    "author_bio": "Hastings Charles Dent (1855-1909)，英国土木工程师和博物学家。曾参与巴西铁路的勘测工作。",
                    "major_works": "《A Year in Brazil》",
                    "content": "作为一名工程师和狂热的昆虫收集者，作者记录了他在巴西米纳斯吉拉斯州的铁路建设生活，以及沿途收集鳞翅目昆虫的自然观察。",
                    "pages": 444,
                    "difficulty": "中等 (包含附录的生物学列表)",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "The Desert of the Exodus",
                    "title_zh": "出埃及的沙漠",
                    "author": "Edward Henry Palmer",
                    "author_bio": "Edward Henry Palmer (1840-1882)，英国东方学家。曾担任剑桥大学阿拉伯语教授，精通多门中东语言。1882年在西奈半岛执行任务时被杀。",
                    "major_works": "《The Desert of the Exodus》",
                    "content": "基于巴勒斯坦勘探基金会的调查，详细描述了西奈半岛和巴勒斯坦地区的地理状况，试图从地理学和考古学角度验证《出埃及记》中的路线。",
                    "pages": 535,
                    "difficulty": "困难 (涉及宗教学、考古学与阿拉伯语)",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "From the Cape to Cairo",
                    "title_zh": "从开普敦到开罗",
                    "author": "Ewart S. Grogan",
                    "author_bio": "Ewart S. Grogan (1874-1967)，英国探险家、商人和政治家。他是历史上第一个徒步从南非开普敦走到埃及开罗的人。",
                    "major_works": "《From the Cape to Cairo》",
                    "content": "详细叙述了作者为了赢得心上人父亲的认可，耗时两年半时间，首次完成纵穿非洲大陆壮举的全过程。书中充满危险的狩猎和土著遭遇战。",
                    "pages": 377,
                    "difficulty": "中等",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "Unknown Mexico",
                    "title_zh": "未知的墨西哥",
                    "author": "Carl Lumholtz",
                    "author_bio": "Carl Lumholtz (1851-1922)，挪威探险家和民族志学家，以其对澳大利亚和墨西哥原住民的细致研究而闻名。",
                    "major_works": "《Unknown Mexico》, 《Among Cannibals》",
                    "content": "长达五年的墨西哥西北部原住民部落考察笔记。详细记录了塔拉乌马拉人等土著的信仰、仪式及日常生活，是极具价值的人类学史料。",
                    "pages": 530,
                    "difficulty": "困难 (属于民族志范畴)",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "The Ruins and Excavations of Ancient Rome",
                    "title_zh": "古罗马的废墟与发掘",
                    "author": "Rodolfo Lanciani",
                    "author_bio": "Rodolfo Lanciani (1845-1929)，意大利著名考古学家。他主持了罗马城晚期多次重大考古发掘，被誉为现代罗马地形学的奠基人。",
                    "major_works": "《The Ruins and Excavations of Ancient Rome》, 《Forma Urbis Romae》",
                    "content": "系统介绍了19世纪末罗马考古的最新发现，结合历史文献与实地考察，勾勒出古罗马城的面貌，是考古爱好者的经典指南。",
                    "pages": 619,
                    "difficulty": "困难 (大量古典历史、拉丁语与建筑学词汇)",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "Among the Himalayas",
                    "title_zh": "在喜马拉雅山脉中",
                    "author": "L.A. Waddell",
                    "author_bio": "Laurence Austine Waddell (1854-1938)，英国军医、探险家和藏学家。曾参与过英军远征西藏的行动。",
                    "major_works": "《Among the Himalayas》, 《The Buddhism of Tibet》",
                    "content": "记录了作者在锡金和尼泊尔交界的喜马拉雅山区的多次探险，对当地的高山地理、植被分布和藏传佛教文化有非常详尽的描绘。",
                    "pages": 452,
                    "difficulty": "困难",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "My Life with the Eskimo",
                    "title_zh": "我与爱斯基摩人的生活",
                    "author": "Vilhjalmur Stefansson",
                    "author_bio": "Vilhjalmur Stefansson (1879-1962)，加拿大出生的北极探险家和民族志学家。主张探险家应适应并采用北极原住民的生活方式。",
                    "major_works": "《My Life with the Eskimo》, 《The Friendly Arctic》",
                    "content": "记述了他在1908至1912年间在北极圈内的探险。他深入爱斯基摩人部落，学习他们的语言和生存技巧，并发现了所谓“金发爱斯基摩人”。",
                    "pages": 538,
                    "difficulty": "中等",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "Tenting on the Plains",
                    "title_zh": "在平原上扎营",
                    "author": "Elizabeth Bacon Custer",
                    "author_bio": "Elizabeth Bacon Custer (1842-1933)，美国作家，也是著名将领乔治·卡斯特（George Custer）的遗孀。她在丈夫阵亡后写了多部回忆录。",
                    "major_works": "《Tenting on the Plains》, 《Boots and Saddles》",
                    "content": "回忆了内战后她随同丈夫驻扎在德克萨斯和堪萨斯等边疆平原的生活。生动刻画了19世纪美国西部骑兵部队的艰苦与冒险。",
                    "pages": 702,
                    "difficulty": "中等",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "The Land of Footprints",
                    "title_zh": "足迹之地：非洲营地生活",
                    "author": "Stewart Edward White",
                    "author_bio": "Stewart Edward White (1873-1946)，美国著名小说家和探险家。作品多涉及西部拓荒和自然冒险题材。",
                    "major_works": "《The Land of Footprints》, 《The Blazed Trail》",
                    "content": "作者在东非（主要是肯尼亚）进行为期一年的游猎记录。与一般的吹嘘不同，书中详细记录了狩猎准备、营地建设以及与向导的日常相处。",
                    "pages": 440,
                    "difficulty": "容易",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "With the Tibetans in Tent and Temple",
                    "title_zh": "与藏人同在帐篷与寺庙",
                    "author": "Susie Carson Rijnhart",
                    "author_bio": "Susie Carson Rijnhart (1868-1908)，加拿大医疗传教士。她和丈夫在1890年代前往中国西藏边境传教，经历了极大的悲剧。",
                    "major_works": "《With the Tibetans in Tent and Temple》",
                    "content": "记载了作者在藏区四年的传教和行医经历。后来他们试图前往拉萨时遭到袭击，丈夫和婴儿丧生，她独自逃离险境。这是极其悲壮的第一手藏区记录。",
                    "pages": 400,
                    "difficulty": "中等",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "The Andes and the Amazon",
                    "title_zh": "安第斯山脉与亚马逊河",
                    "author": "C. Reginald Enock",
                    "author_bio": "C. Reginald Enock (1868-1970)，英国工程师和旅行作家。曾在美洲各地从事采矿工程，并撰写了大量关于南美洲的书籍。",
                    "major_works": "《The Andes and the Amazon》, 《The Secret of the Pacific》",
                    "content": "主要记录了在秘鲁安第斯山区和亚马逊丛林边缘的工程勘探与社会观察，深入分析了当地原住民状况及开发潜力。",
                    "pages": 379,
                    "difficulty": "中等",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "Across Unknown South America",
                    "title_zh": "穿越未知的南美洲",
                    "author": "A. Henry Savage Landor",
                    "author_bio": "Arnold Henry Savage Landor (1865-1924)，英国画家、探险家和人类学家，以其经常引发争议的夸张探险叙述而闻名。",
                    "major_works": "《Across Unknown South America》, 《In the Forbidden Land》",
                    "content": "记录了作者穿越巴西中部高地前往亚马逊盆地的艰难旅程。由于探险准备不足，队伍经历了饥饿和迷路，极具戏剧性。",
                    "pages": "377 (Vol 1)",
                    "difficulty": "中等",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                }
            ]
        },
        {
            "name": "早期科幻与奇幻文学 (Early Science Fiction & Fantasy)",
            "books": [
                {
                    "title_en": "A Columbus of Space",
                    "title_zh": "太空哥伦布",
                    "author": "Garrett P. Serviss",
                    "author_bio": "Garrett Putnam Serviss (1851-1929)，美国天文学家和早期科幻小说家。他擅长将当时的天文学知识融入科幻冒险中。",
                    "major_works": "《Edison's Conquest of Mars》, 《A Columbus of Space》",
                    "content": "讲述了发明家利用核动力飞船前往金星探险的故事，在金星上发现了光与暗两个截然不同的种族，是早期行星罗曼史的代表作。",
                    "pages": 273,
                    "difficulty": "容易",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "The Moon Metal",
                    "title_zh": "月球金属",
                    "author": "Garrett P. Serviss",
                    "author_bio": "Garrett Putnam Serviss (1851-1929)，美国天文学家和早期科幻小说家。",
                    "major_works": "《Edison's Conquest of Mars》, 《A Columbus of Space》",
                    "content": "世界金本位体系崩溃后，一位科学家宣称可以从月球提取一种名为“Artemisium”的新金属作为新货币，引发了全球经济垄断危机。",
                    "pages": 164,
                    "difficulty": "容易",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "The Master Key",
                    "title_zh": "电之魔钥",
                    "author": "L. Frank Baum",
                    "author_bio": "Lyman Frank Baum (1856-1919)，美国著名儿童文学作家，最著名作品是《绿野仙踪》（The Wizard of Oz）。",
                    "major_works": "《The Wizard of Oz》, 《The Master Key》",
                    "content": "讲述一个小男孩意外触碰了电的“主控键”，召唤出了“电魔”。电魔赠予他可以飞行、防御和电击敌人的高科技装置，展开了一场科幻冒险。",
                    "pages": 245,
                    "difficulty": "容易",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "The Brick Moon",
                    "title_zh": "砖月",
                    "author": "Edward Everett Hale",
                    "author_bio": "Edward Everett Hale (1822-1909)，美国神职人员和作家。他的作品经常富有想象力和寓言色彩。",
                    "major_works": "《The Man Without a Country》, 《The Brick Moon》",
                    "content": "被认为是文学史上第一部描写人造卫星的小说。一群人建造了一颗巨大的砖头卫星，试图将其发射入轨为水手导航，结果意外随卫星一起进入了太空。",
                    "pages": 140,
                    "difficulty": "中等 (受维多利亚散文风格影响)",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "The Blind Spot",
                    "title_zh": "盲点",
                    "author": "Austin Hall & Homer Eon Flint",
                    "author_bio": "Austin Hall (1885-1933) 和 Homer Eon Flint (1888-1924)，两位都是早期“低俗杂志”(Pulp Magazine)时代的活跃科幻作家。",
                    "major_works": "《The Blind Spot》",
                    "content": "一位教授在旧金山的一个房间里发现了一个通往另一维度（盲点）的入口。小说探讨了多重宇宙和异维生命，带有强烈的悬疑色彩。",
                    "pages": 340,
                    "difficulty": "中等",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "City of Endless Night",
                    "title_zh": "无尽之夜的城市",
                    "author": "Milo Hastings",
                    "author_bio": "Milo Hastings (1884-1957)，美国农业学家、营养学家和作家。以其反乌托邦科幻小说闻名。",
                    "major_works": "《City of Endless Night》",
                    "content": "写于一战后，设定在未来，柏林变成了一个与世隔绝的巨型地下反乌托邦城市。书中预见性地描绘了极权统治、优生学和严格的阶级控制。",
                    "pages": 346,
                    "difficulty": "中等",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "The Metal Monster",
                    "title_zh": "金属巨兽",
                    "author": "A. Merritt",
                    "author_bio": "Abraham Merritt (1884-1943)，美国早期奇幻和科幻小说大师，作品以华丽的文笔和异域探险见长。",
                    "major_works": "《The Moon Pool》, 《The Metal Monster》",
                    "content": "探险家在喜马拉雅山区遭遇了一个由活体金属构成的庞大群体生命系统，以及统治它们的金属女皇。探讨了无机生命的进化。",
                    "pages": 300,
                    "difficulty": "困难 (辞藻异常华丽)",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "The Hampdenshire Wonder",
                    "title_zh": "汉普登郡的神童",
                    "author": "J. D. Beresford",
                    "author_bio": "John Davys Beresford (1873-1947)，英国小说家。他的作品深刻影响了后来的英国科幻文学。",
                    "major_works": "《The Hampdenshire Wonder》",
                    "content": "被誉为关于“超级智能儿童”最早的小说之一。一个生来头部巨大、智力远超人类极限的男孩诞生，但他却对普通人类的社会法则感到无法理解，最终走向悲剧。",
                    "pages": 310,
                    "difficulty": "中等",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "Olga Romanoff",
                    "title_zh": "奥尔加·罗曼诺娃",
                    "author": "George Griffith",
                    "author_bio": "George Griffith (1857-1906)，19世纪末极其畅销的英国科幻作家，其名气当时甚至比肩H.G.威尔斯，后被渐渐遗忘。",
                    "major_works": "《The Angel of the Revolution》, 《Olga Romanoff》",
                    "content": "作为《革命天使》的续集，设定在未来的2030年。俄罗斯皇室后裔奥尔加卷入全球战争，最终一场彗星撞击地球摧毁了大部分文明。",
                    "pages": 377,
                    "difficulty": "容易",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "The Angel of the Revolution",
                    "title_zh": "革命天使",
                    "author": "George Griffith",
                    "author_bio": "George Griffith (1857-1906)，英国多产科幻与冒险小说家。",
                    "major_works": "《The Angel of the Revolution》",
                    "content": "一个名为“兄弟会”的恐怖组织掌握了先进的飞艇技术，引发了世界大战，最终建立了全球大一统的社会主义乌托邦。",
                    "pages": 393,
                    "difficulty": "容易",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "The Secret of the Earth",
                    "title_zh": "地球的秘密",
                    "author": "Charles Willing Beale",
                    "author_bio": "Charles Willing Beale (1845-1932)，美国作家，这本空心地球理论小说是他最知名的作品。",
                    "major_works": "《The Secret of the Earth》",
                    "content": "兄弟俩乘坐抗重力飞船飞向北极，发现了一个进入地球内部的入口，他们在地球内部发现了一个失落的文明和奇异的生物。",
                    "pages": 256,
                    "difficulty": "容易",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "A Journey in Other Worlds",
                    "title_zh": "在其他世界的旅程",
                    "author": "John Jacob Astor IV",
                    "author_bio": "John Jacob Astor IV (1864-1912)，美国亿万富翁、发明家。他在1912年的泰坦尼克号沉船事故中丧生。",
                    "major_works": "《A Journey in Other Worlds》",
                    "content": "设定在2000年，地球成为一个高科技乌托邦。一群探险家乘坐利用“负重力”的飞船前往木星和土星，在木星上遇到了史前恐龙般的生物，在土星上遭遇了精神生命体。",
                    "pages": 476,
                    "difficulty": "中等",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "Symzonia: A Voyage of Discovery",
                    "title_zh": "辛佐尼亚：发现之旅",
                    "author": "Captain Adam Seaborn (Pseudonym)",
                    "author_bio": "笔名。普遍认为是John Cleves Symmes Jr. (1780-1829)，美国陆军军官，他是“空心地球”假说最著名的倡导者。",
                    "major_works": "《Symzonia: A Voyage of Discovery》",
                    "content": "文学史上最早的空心地球小说。讲述一艘船驶入南极开口，进入地球内部并发现了一个名为“Symzonia”的乌托邦文明。",
                    "pages": 248,
                    "difficulty": "中等 (受19世纪早期航海日志风格影响)",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "Mizora: A Prophecy",
                    "title_zh": "米佐拉：一个预言",
                    "author": "Mary E. Bradley Lane",
                    "author_bio": "Mary E. Bradley Lane (1844-1930)，美国作家。她一直隐瞒自己是这本书的作者，直到晚年才公开。",
                    "major_works": "《Mizora: A Prophecy》",
                    "content": "第一部描绘全女性乌托邦社会的小说。一位流亡的俄罗斯贵族妇女发现了地球内部的米佐拉国，那里通过孤雌生殖繁衍，没有男性，科学技术高度发达。",
                    "pages": 312,
                    "difficulty": "容易",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "Darkness and Dawn",
                    "title_zh": "黑暗与黎明",
                    "author": "George Allan England",
                    "author_bio": "George Allan England (1877-1936)，美国早期的科幻和冒险小说家，他的作品通常具有强烈的社会主义思想倾向。",
                    "major_works": "《Darkness and Dawn》",
                    "content": "一对男女在纽约的摩天大楼中沉睡了千年后醒来，发现世界已被灾难摧毁，人类退化成野蛮的变种人。他们开始重建文明。",
                    "pages": 672,
                    "difficulty": "中等",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "The Lord of the Sea",
                    "title_zh": "海洋之主",
                    "author": "M. P. Shiel",
                    "author_bio": "Matthew Phipps Shiel (1865-1947)，加勒比裔英国作家，以怪异文学和早期科幻闻名。",
                    "major_works": "《The Purple Cloud》, 《The Lord of the Sea》",
                    "content": "主人公利用一种从陨石中发现的新型坚不可摧的材料，建造了巨大的海上浮动堡垒，并借此向全球船只征收通行费，最终成为世界的统治者。",
                    "pages": 496,
                    "difficulty": "困难 (文笔古怪，长句极多)",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "Edison's Conquest of Mars",
                    "title_zh": "爱迪生征服火星",
                    "author": "Garrett P. Serviss",
                    "author_bio": "Garrett Putnam Serviss (1851-1929)，美国天文学家和早期科幻小说家。",
                    "major_works": "《Edison's Conquest of Mars》",
                    "content": "作为威尔斯《世界大战》的一部未经授权的美国续集。托马斯·爱迪生研发了反重力飞船和分解射线，带领地球舰队前往火星进行反击。",
                    "pages": 200,
                    "difficulty": "容易",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "The Centaur",
                    "title_zh": "半人马",
                    "author": "Algernon Blackwood",
                    "author_bio": "Algernon Blackwood (1869-1951)，英国怪奇小说大师，以神秘主义和自然崇拜主题著称。",
                    "major_works": "《The Willows》, 《The Centaur》",
                    "content": "一位厌倦了现代文明的旅行者在高加索山脉遇到了一个保留着原始神秘主义的社群，并最终目睹了半人马这种古老的大自然精神化身。",
                    "pages": 347,
                    "difficulty": "困难 (哲学与神秘主义色彩浓厚)",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "The Heads of Cerberus",
                    "title_zh": "地狱犬之首",
                    "author": "Francis Stevens",
                    "author_bio": "Francis Stevens，原名 Gertrude Barrows Bennett (1883-1948)，常被称为“黑暗奇幻小说之母”，对后世奇幻文学影响深远。",
                    "major_works": "《The Citadel of Fear》, 《The Heads of Cerberus》",
                    "content": "吸入了一种名为“地狱犬之首”的神秘药粉后，主角们被传送到了平行时空的未来费城——一个由极权体制统治的反乌托邦城市。",
                    "pages": 255,
                    "difficulty": "中等",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                },
                {
                    "title_en": "The Ghost Pirates",
                    "title_zh": "幽灵海盗",
                    "author": "William Hope Hodgson",
                    "author_bio": "William Hope Hodgson (1877-1918)，英国作家，海洋恐怖文学和宇宙恐怖文学的先驱。在一战中阵亡。",
                    "major_works": "《The House on the Borderland》, 《The Ghost Pirates》",
                    "content": "一艘名为“莫尔腾号”的帆船在航行中遭遇了来自另一个维度的影子生物的侵扰。小说以极其写实的航海细节描绘了渐进的、令人窒息的恐怖氛围。",
                    "pages": 276,
                    "difficulty": "困难 (大量航海专业术语)",
                    "translation_status": "已通过豆瓣、Bing搜索复核，确认无中译本。"
                }
            ]
        }
    ]
}

markdown_content = "# 公版外文书 AI 新译版权初筛报告 v4（无中译本精选）\n\n"
markdown_content += "本报告包含两个主要分类，每类精心筛选了20本极具翻译价值、且通过搜索确认（基于豆瓣、Bing等）**目前未见中译本**的公版书籍。\n\n"

for category in data["categories"]:
    markdown_content += f"## {category['name']}\n\n"
    for idx, book in enumerate(category["books"], 1):
        markdown_content += f"### {idx}. {book['title_en']} / 《{book['title_zh']}》\n"
        markdown_content += f"- **作者**：{book['author']}\n"
        markdown_content += f"- **作者基本人生**：{book['author_bio']}\n"
        markdown_content += f"- **代表作**：{book['major_works']}\n"
        markdown_content += f"- **一句话简介**：{book['content']}\n"
        markdown_content += f"- **页数**：约 {book['pages']} 页\n"
        markdown_content += f"- **翻译难度**：{book['difficulty']}\n"
        markdown_content += f"- **复核状态**：{book['translation_status']}\n\n"

args = parse_args()
output_path = args.output
if not output_path.is_absolute():
    output_path = (Path.cwd() / output_path).resolve()
output_path.parent.mkdir(parents=True, exist_ok=True)

with output_path.open("w", encoding="utf-8") as f:
    f.write(markdown_content)

print(f"Markdown generated successfully: {output_path}")

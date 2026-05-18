import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source" / "source_text_raw.txt"
OUT_DIR = ROOT / "chapters" / "src"
MANIFEST = ROOT / "source" / "source_manifest.json"
TOC = ROOT / "source" / "toc.json"


TITLE_MAP = {
    "INTRODUCTION": ("001_introduction_by_the_editor.md", "INTRODUCTION", "编辑导言"),
    "CHAPTER 1": ("002_chapter_01_purpose_of_the_voyage.md", "CHAPTER 1. PURPOSE OF THE VOYAGE. COMPOSITION OF THE SQUADRON. ARRIVAL AT MADEIRA.", "第一章 航行目的"),
    "CHAPTER 2": ("003_chapter_02_spanish_preparations.md", "CHAPTER 2. SPANISH PREPARATIONS. FATE OF PIZARRO'S SQUADRON.", "第二章 西班牙的准备"),
    "CHAPTER 3": ("004_chapter_03_madeira_to_st_catherines.md", "CHAPTER 3. FROM MADEIRA TO ST. CATHERINE'S. UNHEALTHINESS OF THE SQUADRON.", "第三章 从马德拉到圣凯瑟琳"),
    "CHAPTER 4": ("005_chapter_04_commodores_instructions.md", "CHAPTER 4. THE COMMODORE'S INSTRUCTIONS. BAD WEATHER. NARROW ESCAPE OF THE PEARL. ST JULIAN.", "第四章 准将的训令"),
    "CHAPTER 5": ("006_chapter_05_tierra_del_fuego.md", "CHAPTER 5. FURTHER INSTRUCTIONS. TIERRA DEL FUEGO. THE STRAITS OF LE MAIRE.", "第五章 火地岛"),
    "CHAPTER 6": ("007_chapter_06_heavy_gales.md", "CHAPTER 6. HEAVY GALES. A LONG BATTLE WITH WIND AND SEA. THE CENTURION LOSES HER CONSORTS.", "第六章 狂风巨浪"),
    "CHAPTER 7": ("008_chapter_07_outbreak_of_scurvy.md", "CHAPTER 7. OUTBREAK OF SCURVY. DANGER OF SHIPWRECK.", "第七章 坏血病爆发"),
    "CHAPTER 8": ("009_chapter_08_juan_fernandez.md", "CHAPTER 8. ARRIVAL AT JUAN FERNANDEZ. THE TRIAL REJOINS.", "第八章 抵达胡安·费尔南德斯"),
    "CHAPTER 9": ("010_chapter_09_the_sick_landed.md", "CHAPTER 9. THE SICK LANDED. ALEXANDER SELKIRK. SEALS AND SEA-LIONS.", "第九章 病员上岸"),
    "CHAPTER 10": ("011_chapter_10_gloucester_reappears.md", "CHAPTER 10. REAPPEARANCE OF THE GLOUCESTER. DISTRESS ON BOARD. HER EFFORTS TO ENTER THE BAY.", "第十章 格洛斯特号重现"),
    "CHAPTER 11": ("012_chapter_11_spanish_cruisers.md", "CHAPTER 11. TRACES OF SPANISH CRUISERS. ARRIVAL OF THE ANNA PINK.", "第十一章 西班牙巡航船的踪迹"),
    "CHAPTER 12": ("013_chapter_12_wreck_of_the_wager.md", "CHAPTER 12. THE WRECK OF THE WAGER. A MUTINY.", "第十二章 韦杰号失事"),
    "CHAPTER 13": ("014_chapter_13_wager_continued.md", "CHAPTER 13. THE WRECK OF THE WAGER (CONTINUED). THE ADVENTURES OF THE CAPTAIN'S PARTY.", "第十三章 韦杰号失事续记"),
    "CHAPTER 14": ("015_chapter_14_losses_from_scurvy.md", "CHAPTER 14. THE LOSSES FROM SCURVY. STATE AND PROSPECTS OF THE SQUADRON.", "第十四章 坏血病造成的损失"),
    "CHAPTER 15": ("016_chapter_15_a_prize.md", "CHAPTER 15. A PRIZE. SPANISH PREPARATIONS. A NARROW ESCAPE.", "第十五章 一艘捕获船"),
    "CHAPTER 16": ("017_chapter_16_commodores_plans.md", "CHAPTER 16. THE COMMODORE'S PLANS. ANOTHER PRIZE. THE TRIAL DESTROYED.", "第十六章 准将的计划"),
    "CHAPTER 17": ("018_chapter_17_more_captures.md", "CHAPTER 17. MORE CAPTURES. ALARM OF THE COAST. PAITA.", "第十七章 更多捕获"),
    "CHAPTER 18": ("019_chapter_18_attack_on_paita.md", "CHAPTER 18. THE ATTACK ON PAITA.", "第十八章 攻击派塔"),
    "CHAPTER 19": ("020_chapter_19_attack_on_paita_continued.md", "CHAPTER 19. THE ATTACK ON PAITA (CONTINUED). KIND TREATMENT AND RELEASE OF THE PRISONERS. THEIR GRATITUDE.", "第十九章 攻击派塔续记"),
    "CHAPTER 20": ("021_chapter_20_a_clever_trick.md", "CHAPTER 20. A CLEVER TRICK. WATERING AT QUIBO. CATCHING THE TURTLE.", "第二十章 一个巧计"),
    "CHAPTER 21": ("022_chapter_21_acapulco_and_the_galleon.md", "CHAPTER 21. DELAY AND DISAPPOINTMENT. CHASING A HEATH FIRE. ACAPULCO. THE MANILA GALLEON. FRESH HOPES.", "第二十一章 阿卡普尔科与大帆船"),
    "CHAPTER 22": ("023_chapter_22_manila_trade.md", "CHAPTER 22. THE MANILA TRADE.", "第二十二章 马尼拉贸易"),
    "CHAPTER 23": ("024_chapter_23_waiting_for_the_galleon.md", "CHAPTER 23. WAITING FOR THE GALLEON. DISAPPOINTMENT. CHEQUETAN.", "第二十三章 等候大帆船"),
    "CHAPTER 24": ("025_chapter_24_bound_for_china.md", "CHAPTER 24. THE PRIZES SCUTTLED. NEWS OF THE SQUADRON REACHES ENGLAND. BOUND FOR CHINA.", "第二十四章 驶向中国"),
    "CHAPTER 25": ("026_chapter_25_gloucester_abandoned.md", "CHAPTER 25. DELAYS AND ACCIDENTS. SCURVY AGAIN. A LEAK. THE GLOUCESTER ABANDONED.", "第二十五章 格洛斯特号被放弃"),
    "CHAPTER 26": ("027_chapter_26_ladrones_and_tinian.md", "CHAPTER 26. THE LADRONES SIGHTED. TINIAN.", "第二十六章 望见拉德罗内群岛"),
    "CHAPTER 27": ("028_chapter_27_landing_the_sick.md", "CHAPTER 27. LANDING THE SICK. CENTURION DRIVEN TO SEA.", "第二十七章 病员登陆"),
    "CHAPTER 28": ("029_chapter_28_return_of_the_centurion.md", "CHAPTER 28. ANSON CHEERS HIS MEN. PLANS FOR ESCAPE. RETURN OF THE CENTURION.", "第二十八章 百夫长号归来"),
    "CHAPTER 29": ("030_chapter_29_departure_from_tinian.md", "CHAPTER 29. THE CENTURION AGAIN DRIVEN TO SEA. HER RETURN. DEPARTURE FROM TINIAN.", "第二十九章 离开提尼安"),
    "CHAPTER 30": ("031_chapter_30_arrival_at_macao.md", "CHAPTER 30. CHINESE FISHING FLEETS. ARRIVAL AT MACAO.", "第三十章 抵达澳门"),
    "CHAPTER 31": ("032_chapter_31_macao_and_canton.md", "CHAPTER 31. MACAO. INTERVIEW WITH THE GOVERNOR. A VISIT TO CANTON.", "第三十一章 澳门与广州"),
    "CHAPTER 32": ("033_chapter_32_letter_to_the_viceroy.md", "CHAPTER 32. A LETTER TO THE VICEROY. A CHINESE MANDARIN. THE CENTURION IS REFITTED AND PUTS TO SEA.", "第三十二章 致总督的信"),
    "CHAPTER 33": ("034_chapter_33_waiting_for_the_manila_galleon.md", "CHAPTER 33. WAITING FOR THE MANILA GALLEON.", "第三十三章 等候马尼拉大帆船"),
    "CHAPTER 34": ("035_chapter_34_capture_of_the_galleon.md", "CHAPTER 34. THE CAPTURE OF THE GALLEON.", "第三十四章 夺取大帆船"),
    "CHAPTER 35": ("036_chapter_35_securing_the_prisoners.md", "CHAPTER 35. SECURING THE PRISONERS. MACAO AGAIN. AMOUNT OF THE TREASURE.", "第三十五章 安置俘虏"),
    "CHAPTER 36": ("037_chapter_36_canton_river.md", "CHAPTER 36. THE CANTON RIVER. NEGOTIATING WITH THE CHINESE. PRISONERS RELEASED.", "第三十六章 广州河"),
    "CHAPTER 37": ("038_chapter_37_chinese_trickery.md", "CHAPTER 37. CHINESE TRICKERY.", "第三十七章 清廷官员的周旋"),
    "CHAPTER 38": ("039_chapter_38_visit_to_canton.md", "CHAPTER 38. PREPARATIONS FOR A VISIT TO CANTON.", "第三十八章 准备访问广州"),
    "CHAPTER 39": ("040_chapter_39_fire_in_canton.md", "CHAPTER 39. STORES AND PROVISIONS. A FIRE IN CANTON. SAILORS AS FIREMEN.", "第三十九章 广州大火"),
    "CHAPTER 40": ("041_chapter_40_homeward_bound.md", "CHAPTER 40. ANSON RECEIVED BY THE VICEROY. CENTURION SETS SAIL. TABLE BAY. SPITHEAD.", "第四十章 返航"),
    "GLOSSARY": ("042_glossary.md", "GLOSSARY", "术语表"),
}


def slug_heading(title: str) -> str:
    return re.sub(r"\s+", " ", title.replace("--", ". ")).strip(" .")


def clean_body(text: str) -> str:
    text = text.replace("\r\n", "\n")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def main() -> None:
    raw = SOURCE.read_text(encoding="utf-8")
    start = raw.index("*** START OF THE PROJECT GUTENBERG EBOOK")
    start = raw.index("\n", start) + 1
    end = raw.index("*** END OF THE PROJECT GUTENBERG EBOOK")
    work = raw[start:end].strip()
    first_body = work.index("\nINTRODUCTION.\n")
    body = work[first_body + 1 :]

    markers = []
    for match in re.finditer(r"(?m)^(INTRODUCTION|CHAPTER [0-9]+|GLOSSARY)\.\s*$", body):
        key = match.group(1)
        markers.append((match.start(), match.end(), key))
    if len(markers) != 42:
        raise RuntimeError(f"Expected 42 body sections, found {len(markers)}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for old in OUT_DIR.glob("*.md"):
        old.unlink()

    toc = []
    for idx, (start_pos, marker_end, key) in enumerate(markers):
        section_end = markers[idx + 1][0] if idx + 1 < len(markers) else len(body)
        filename, source_full, zh_title = TITLE_MAP[key]
        content = clean_body(body[marker_end:section_end])
        md = f"# {source_full}\n\n{content}\n"
        (OUT_DIR / filename).write_text(md, encoding="utf-8")
        toc.append(
            {
                "file": filename,
                "source_heading": source_full,
                "zh_title": zh_title,
                "source_word_count": len(re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", content)),
            }
        )

    manifest = {
        "source_url": "https://www.gutenberg.org/ebooks/16611",
        "plain_text_url": "https://www.gutenberg.org/ebooks/16611.txt.utf-8",
        "source_file": "source/source_text_raw.txt",
        "body_sections": len(toc),
        "license_footer_stripped": True,
        "front_matter_toc_stripped": True,
        "notes_heading_in_print_toc_only": True,
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    TOC.write_text(json.dumps(toc, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Split {len(toc)} sections into {OUT_DIR}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import subprocess
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

EXPECTED_PUBLIC_ZH_HANS = {
    "1_黑人北极探险家_马修·A·汉森",
    "2_幽灵海盗_威廉·霍普·霍奇森",
    "3_爱迪生征服火星_加勒特·P·瑟维斯",
    "4_环球航海记_理查德·沃尔特",
    "5_金属巨兽_亚伯拉罕·梅里特",
    "6_天文学大成_托勒密",
    "7_刺青_谷崎润一郎",
    "8_痴人之爱_谷崎润一郎",
    "9_政治生存的逻辑_布鲁斯·布埃诺·德梅斯基塔等",
    "10_林伯洛斯特的女孩_吉恩·斯特拉顿-波特",
    "11_战国策_刘向",
    "12_一座山的故事_埃利泽·雷克吕",
    "13_在两个星球上_库尔德·拉斯维茨",
    "14_常绿树_沈熏",
    "15_孟普拉森之虎_埃米利奥·萨尔加里",
    "16_当代英雄_莱蒙托夫",
    "17_拉萨里略_德_托尔梅斯的一生_佚名",
    "18_云使_迦梨陀娑",
    "19_约翰生传_詹姆斯_鲍斯威尔",
    "20_罗马帝国衰亡史_爱德华吉本",
}

EXPECTED_PRIVATE_ZH_HANS = set()

OLD_BOOK_DIR_NAMES = {
    "1_pg20923_a_negro_explorer_at_the_north_pole",
    "2_pg10966_the_ghost_pirates",
    "3_pg19141_edisons_conquest_of_mars",
    "4_pg16611_ansons_voyage_round_the_world",
    "5_pg3479_the_metal_monster",
    "6_ptolemy_almagest_grc_zh_hans",
    "7_shisei_tanizaki",
    "8_chijin_no_ai_tanizaki",
    "9_政治生存的逻辑",
    "10_a_girl_of_the_limberlost",
    "11_zhanguoce_lzh_trial",
    "12_histoire_d_une_montagne_reclus",
    "13_auf_zwei_planeten_lasswitz",
    "14_sangnoksu_sim_hun",
    "15_le_tigri_di_mompracem_salgari",
    "99_tmp_reclus_book_clone",
    "1_dialogue_art_verbal_action",
}

TEXT_SUFFIXES = {
    ".css",
    ".csv",
    ".html",
    ".json",
    ".log",
    ".md",
    ".opf",
    ".py",
    ".txt",
    ".xhtml",
    ".xml",
    ".yaml",
    ".yml",
}

TEXT_FILENAMES = {
    ".gitignore",
    "Makefile",
}


def directory_names(root: Path) -> set[str]:
    if not root.exists():
        return set()
    git_root = REPO_ROOT / ".git"
    if git_root.exists():
        result = subprocess.run(
            ["git", "-c", "core.quotepath=false", "ls-files", "--", root.relative_to(REPO_ROOT).as_posix()],
            cwd=REPO_ROOT,
            text=True,
            encoding="utf-8",
            capture_output=True,
            check=False,
        )
        if result.returncode == 0:
            prefix = root.relative_to(REPO_ROOT).as_posix().rstrip("/") + "/"
            return {
                line[len(prefix) :].split("/", 1)[0]
                for line in result.stdout.splitlines()
                if line.startswith(prefix) and "/" in line[len(prefix) :]
            }
    return {
        path.name
        for path in root.iterdir()
        if path.is_dir() and path.name not in OLD_BOOK_DIR_NAMES
    }


def iter_text_files(root: Path):
    skip_dirs = {".git", ".pytest_cache", "__pycache__", "node_modules", "tools"}
    this_file = Path(__file__).resolve()
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if path.resolve() == this_file:
            continue
        if any(part in skip_dirs for part in path.parts):
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in TEXT_FILENAMES:
            yield path


class BookDirectoryNameTests(unittest.TestCase):
    def test_public_zh_hans_book_directories_use_target_title_and_author(self) -> None:
        actual = directory_names(REPO_ROOT / "books" / "zh-Hans")
        self.assertEqual(actual, EXPECTED_PUBLIC_ZH_HANS)

    def test_private_zh_hans_book_directories_use_target_title_and_author(self) -> None:
        actual = directory_names(REPO_ROOT / "books" / "private" / "zh-Hans")
        self.assertEqual(actual, EXPECTED_PRIVATE_ZH_HANS)

    def test_text_files_do_not_reference_old_book_directory_names(self) -> None:
        stale_refs: list[str] = []
        for path in iter_text_files(REPO_ROOT):
            text = path.read_text(encoding="utf-8", errors="ignore")
            for old_name in OLD_BOOK_DIR_NAMES:
                if old_name in text:
                    stale_refs.append(f"{path.relative_to(REPO_ROOT).as_posix()}: {old_name}")

        self.assertEqual(stale_refs, [])


if __name__ == "__main__":
    unittest.main()

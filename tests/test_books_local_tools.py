from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "books" / "scripts" / "setup_local_tools.py"


def load_setup_module():
    spec = importlib.util.spec_from_file_location("setup_local_tools", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class BooksLocalToolsTests(unittest.TestCase):
    def test_finds_nested_java_under_local_tools_cache(self) -> None:
        module = load_setup_module()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            java = root / "tools" / "zulu17-jre" / "runtime" / "bin" / "java.exe"
            java.parent.mkdir(parents=True)
            java.write_text("fake java", encoding="utf-8")

            self.assertEqual(module.find_java_in_tree(root / "tools" / "zulu17-jre"), java)

    def test_extracts_user_supplied_jre_zip_into_books_tools(self) -> None:
        module = load_setup_module()
        with tempfile.TemporaryDirectory() as tmp:
            books_root = Path(tmp) / "books"
            books_root.mkdir()
            archive = Path(tmp) / "zulu17-jre.zip"
            with zipfile.ZipFile(archive, "w") as zf:
                zf.writestr("zulu17-test/bin/java.exe", "fake java")

            result = module.ensure_local_jre(books_root, archive, force=False)

            self.assertEqual(result["status"], "installed")
            self.assertEqual(
                Path(result["java_path"]),
                books_root / "tools" / "zulu17-jre" / "zulu17-test" / "bin" / "java.exe",
            )

    def test_check_mode_reports_local_cache_without_installing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            books_root = Path(tmp) / "books"
            java = books_root / "tools" / "zulu17-jre" / "bin" / "java.exe"
            java.parent.mkdir(parents=True)
            java.write_text("fake java", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT_PATH),
                    "--books-root",
                    str(books_root),
                    "--check",
                    "--json",
                ],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["books_root"], str(books_root.resolve()))
            self.assertEqual(payload["local_jre"]["present"], True)
            self.assertEqual(Path(payload["local_jre"]["java_path"]), java)


if __name__ == "__main__":
    unittest.main()

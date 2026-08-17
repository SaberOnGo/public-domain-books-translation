from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "books" / "scripts" / "check_gitignore_policy.py"
SPEC = importlib.util.spec_from_file_location("check_gitignore_policy", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class GitignorePolicyTests(unittest.TestCase):
    def test_git_repo_ignores_stale_local_book_directory_not_visible_to_git(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_root = Path(temp_dir)
            books_root = repo_root / "books"
            tracked_project = books_root / "zh-Hans" / "1_已跟踪_作者"
            stale_local_project = books_root / "zh-Hans" / "2_旧目录"
            (repo_root / ".git").mkdir()
            tracked_project.mkdir(parents=True)
            stale_local_project.mkdir(parents=True)

            completed = SimpleNamespace(
                returncode=0,
                stdout="books/zh-Hans/1_已跟踪_作者/.gitignore\n",
            )
            with mock.patch.object(MODULE.subprocess, "run", return_value=completed):
                projects = MODULE.public_book_dirs(repo_root, books_root)

            self.assertEqual(projects, [tracked_project])


if __name__ == "__main__":
    unittest.main()

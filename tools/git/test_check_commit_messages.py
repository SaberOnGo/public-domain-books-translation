import unittest

from check_commit_messages import validate_commit_message


VALID_MESSAGE = """Document GitHub commit summary rules

ZH:
- 将 GitHub 推送前的提交信息要求写入仓库规则，明确必须同时提供标题和详细摘要。
- 摘要必须分为中文、英文、日文三段，方便 LifeBook Launcher 按用户系统语言展示更新内容。

EN:
- Adds repository rules requiring both a commit title and a detailed summary before pushing to GitHub.
- Requires separate Chinese, English, and Japanese summary sections so LifeBook Launcher can show localized update text.

JA:
- GitHub に push する前に、commit タイトルと詳細な概要を必ず書くルールを追加します。
- LifeBook Launcher がユーザー環境に合わせて表示できるよう、中国語・英語・日本語の概要を分けて記載することを必須にします。
"""


class CommitMessageValidationTests(unittest.TestCase):
    def test_accepts_title_and_trilingual_detailed_summary(self):
        self.assertEqual(validate_commit_message(VALID_MESSAGE), [])

    def test_accepts_inline_language_labels(self):
        message = """Document GitHub commit summary rules

ZH: 将 GitHub 推送前的提交信息要求写入仓库规则，明确必须同时提供标题和详细摘要，供 Launcher 展示。
EN: Adds repository rules requiring a commit title and detailed summary before pushing to GitHub, so Launcher can display update text.
JA: GitHub に push する前に commit タイトルと詳細な概要を書くルールを追加し、Launcher の更新表示に使えるようにします。
"""
        self.assertEqual(validate_commit_message(message), [])

    def test_rejects_missing_body(self):
        issues = validate_commit_message("Only a title")
        self.assertIn("missing detailed commit body", issues)

    def test_rejects_missing_language_section(self):
        message = VALID_MESSAGE.replace("\nJA:\n", "\n")
        issues = validate_commit_message(message)
        self.assertIn("missing JA summary section", issues)

    def test_rejects_short_language_section(self):
        message = VALID_MESSAGE.replace(
            "EN:\n- Adds repository rules requiring both a commit title and a detailed summary before pushing to GitHub.\n- Requires separate Chinese, English, and Japanese summary sections so LifeBook Launcher can show localized update text.",
            "EN:\n- Too short.",
        )
        issues = validate_commit_message(message)
        self.assertIn("EN summary section is too short", issues)


if __name__ == "__main__":
    unittest.main()

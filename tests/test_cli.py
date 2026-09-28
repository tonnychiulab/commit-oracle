import unittest
from unittest.mock import patch
from src.cli import main

class TestCLI(unittest.TestCase):
    @patch("src.cli.get_git_diff", return_value="+ normal code line")
    def test_cli_check_clean(self, mock_diff):
        exit_code = main(["--check"])
        self.assertEqual(exit_code, 0)

    @patch("src.cli.get_git_diff", return_value='+ OPENAI_API_KEY="sk-proj-DEMO12345678901234567890"')
    def test_cli_check_dirty(self, mock_diff):
        exit_code = main(["--check"])
        self.assertEqual(exit_code, 1)

    @patch("src.cli.get_git_diff", return_value="diff --git a/src/cli.py b/src/cli.py\n+def test(): pass")
    def test_cli_generate(self, mock_diff):
        exit_code = main(["--generate"])
        self.assertEqual(exit_code, 0)

if __name__ == "__main__":
    unittest.main()

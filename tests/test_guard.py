import unittest
from src.guard import SecurityGuard

class TestSecurityGuard(unittest.TestCase):
    def setUp(self):
        self.guard = SecurityGuard()

    def test_api_key_detection(self):
        issues = self.guard.scan_diff('+ OPENAI_API_KEY="sk-proj-FAKEKEY12345678901234567890"')
        self.assertGreater(len(issues), 0)  # Should find one issue

    def test_no_issues(self):
        issues = self.guard.scan_diff('+ let x = 42\n- old_secret = 123')
        self.assertEqual(len(issues), 0)  # No issues expected

if __name__ == '__main__':
    unittest.main()
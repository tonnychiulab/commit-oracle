import unittest
from src.oracle import CommitOracle

class TestCommitOracle(unittest.TestCase):
    def setUp(self):
        self.oracle = CommitOracle()

    def test_analyze_diff_feat(self):
        diff = "diff --git a/src/auth.py b/src/auth.py\n+def login(): pass"
        res = self.oracle.analyze_diff(diff)
        self.assertEqual(res['type'], 'feat')
        self.assertEqual(res['scope'], 'auth')

    def test_analyze_diff_docs(self):
        diff = "diff --git a/docs/README.md b/docs/README.md\n+update readme"
        res = self.oracle.analyze_diff(diff)
        self.assertEqual(res['type'], 'docs')
        self.assertEqual(res['scope'], 'readme')

    def test_analyze_diff_fix(self):
        diff = "diff --git a/src/user.py b/src/user.py\n+    # fix null pointer bug"
        res = self.oracle.analyze_diff(diff)
        self.assertEqual(res['type'], 'fix')
        self.assertEqual(res['scope'], 'user')

if __name__ == '__main__':
    unittest.main()
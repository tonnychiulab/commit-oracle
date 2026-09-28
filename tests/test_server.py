import http.server
import json
import threading
import unittest
import urllib.request
from src.server import WebhookHandler, process_pr_review

class TestServerLogic(unittest.TestCase):
    def test_process_pr_review_clean(self):
        diff = "diff --git a/src/core.py b/src/core.py\n+def compute(): return 42"
        res = process_pr_review(diff, "feat: add compute")
        self.assertTrue(res["security_passed"])
        self.assertEqual(len(res["issues"]), 0)
        self.assertIn("feat(core)", res["suggested_title"])

    def test_process_pr_review_sensitive(self):
        diff = '+ OPENAI_API_KEY="sk-proj-DEMO12345678901234567890"'
        res = process_pr_review(diff)
        self.assertFalse(res["security_passed"])
        self.assertGreater(len(res["issues"]), 0)

class TestServerHTTP(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = http.server.HTTPServer(("127.0.0.1", 0), WebhookHandler)
        cls.port = cls.server.server_port
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_health_endpoint(self):
        url = f"http://127.0.0.1:{self.port}/health"
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode())
            self.assertEqual(data["status"], "ok")
            self.assertEqual(data["service"], "commit-oracle-bot")

    def test_webhook_ping(self):
        url = f"http://127.0.0.1:{self.port}/webhook"
        req = urllib.request.Request(url, data=b"{}", headers={"X-GitHub-Event": "ping", "Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode())
            self.assertEqual(data["msg"], "pong")

    def test_webhook_pull_request(self):
        url = f"http://127.0.0.1:{self.port}/webhook"
        payload = {
            "pull_request": {"title": "Update code"},
            "diff_text": "+ normal line"
        }
        body = json.dumps(payload).encode()
        req = urllib.request.Request(url, data=body, headers={"X-GitHub-Event": "pull_request", "Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 200)
            data = json.loads(resp.read().decode())
            self.assertEqual(data["status"], "reviewed")
            self.assertTrue(data["security_passed"])

if __name__ == "__main__":
    unittest.main()
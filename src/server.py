import http.server
import json
import os
import sys

# Ensure project root is in sys.path for direct execution and module execution
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from src.guard import SecurityGuard
    from src.oracle import CommitOracle
except ImportError:
    from guard import SecurityGuard
    from oracle import CommitOracle


def process_pr_review(diff_text: str, pr_title: str = "") -> dict:
    """
    審查 PR diff：
    1. 調用 SecurityGuard 檢查是否有敏感金鑰洩漏
    2. 調用 CommitOracle 分析語意並生成建議 PR 標題
    """
    guard = SecurityGuard()
    oracle = CommitOracle()

    issues = guard.scan_diff(diff_text)
    security_passed = len(issues) == 0

    suggested_title = ""
    if diff_text.strip():
        oracle_res = oracle.analyze_diff(diff_text)
        suggested_title = oracle_res.get("message", "").split("\n")[0]

    return {
        "status": "reviewed",
        "security_passed": security_passed,
        "issues": issues,
        "suggested_title": suggested_title or pr_title or "chore: update"
    }

class WebhookHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/health", "/"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "service": "commit-oracle-bot"}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length) if content_length > 0 else b"{}"

        try:
            payload = json.loads(post_data.decode("utf-8"))
        except Exception:
            payload = {}

        event_type = self.headers.get("X-GitHub-Event", "ping")

        if event_type == "ping":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"msg": "pong"}).encode())
            return

        if event_type == "pull_request" or "pull_request" in payload:
            pr_data = payload.get("pull_request", {})
            pr_title = pr_data.get("title", "")
            diff_text = payload.get("diff_text") or pr_data.get("diff", "")

            review_result = process_pr_review(diff_text, pr_title)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(review_result).encode())
            return

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ignored", "event": event_type}).encode())

    def log_message(self, format, *args):
        # Mute standard noisy HTTP server logging during tests
        return

def run_server(port: int = None):
    if port is None:
        port = int(os.environ.get("PORT", 8080))
    server_address = ("", port)
    httpd = http.server.HTTPServer(server_address, WebhookHandler)
    print(f"[*] commit-oracle webhook server running on port {port}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()

if __name__ == "__main__":
    run_server()
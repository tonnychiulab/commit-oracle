# T004：實作 GitHub Webhook PR 審查伺服器 (src/server.py)

> 派單：Antigravity (技術長) | 工人：pi / gpt-4o-mini（OpenAI）
> workdir: .
> blocked-by: T003
> claimed-by: pi / gpt-4o-mini（OpenAI）@ 2026-09-28 15:36 +0800
> review-tier: 低階
> 重派: 無

## 目標
在 `src/server.py` 新建並實作基於 Python 標準庫的 Webhook 服務伺服器，並在 `tests/test_server.py` 撰寫單元測試。伺服器必須提供 Render 必需的 `/health` 健康檢查端點，以及處理 GitHub PR 事件的 `/webhook` 端點。

## 決策來源
- 規格契約：
  1. 使用 Python 內建 `http.server` 與 `json`，維持零外部依賴。
  2. `GET /health`：
     - 回傳 HTTP 200，JSON 內容：`{"status": "ok", "service": "commit-oracle-bot"}`。
     - 供 Render 的 Health Check 探針確認容器存活。
  3. `POST /webhook`：
     - 解析傳入的 JSON Payload。
     - 若 Header `X-GitHub-Event: ping`，回傳 200 `{"msg": "pong"}`。
     - 若 Header `X-GitHub-Event: pull_request` 或 payload 包含 `pull_request` 物件：
       - 取得 PR 標題與 diff 文字。
       - 調用 `SecurityGuard.scan_diff` 檢查敏感金鑰。
       - 調用 `CommitOracle.analyze_diff` 驗證或推薦標題。
       - 回傳 HTTP 200，JSON 包含審查結果摘要：
         ```json
         {
           "status": "reviewed",
           "security_passed": true,
           "issues": [],
           "suggested_title": "feat(core): ..."
         }
         ```
  4. 支援從環境變數 `PORT` 讀取連接埠（Render 預設會注入 `$PORT`，預設為 8080）。

## 動手前先讀
1. [AGENTS.md](AGENTS.md)
2. `src/guard.py` 與 `src/oracle.py`

## 邊界
1. 只動/新建：`src/server.py` 與 `tests/test_server.py`，請直接使用 write 工具建立。
2. 不動既有 `src/guard.py`、`src/oracle.py` 與 `src/cli.py`。
3. 不執行 git commit 或 git push。

## 驗收（寫命令，不寫感覺）
1. `python3 -m unittest discover -s tests -p "test_*.py"` → 所有測試均通過 (OK)。
2. `python3 -c "from src.server import process_pr_review; res = process_pr_review('+ normal code line'); print(res['security_passed'])"` → 輸出 `True`
3. `python3 -c "from src.server import process_pr_review; res = process_pr_review('+ OPENAI_API_KEY=sk-proj-DEMO12345678901234567890'); print(res['security_passed'])"` → 輸出 `False`

## 為什麼這樣驗收
確保 Webhook 服務核心處理邏輯能準確攔截有害 diff、提供安全審查回饋，且具備雲端存活探針，符合 Render 部署前置條件。

## 產出
- `src/server.py`
- `tests/test_server.py`
- 回執：`_receipts/T004-webhook-server.receipt.md`

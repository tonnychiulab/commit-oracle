# 回執 T004：實作 GitHub Webhook PR 審查伺服器

> 執行引擎：pi / gpt-4o-mini (OpenAI)
> 完成時間：2026-09-28 16:11 +0800
> 工單：_tickets/doing/T004-webhook-server.md

## 1. 做了什麼
實作 `src/server.py`，基於標準庫 `http.server` 建立支援 Render 部署的 Webhook 服務。提供 `/health` 健康檢查端點與 `/webhook` GitHub PR 審查端點（整合 `SecurityGuard` 與 `CommitOracle`），並在 `tests/test_server.py` 完成 5 項單元與 HTTP 整合測試。

## 2. 檔案清單
- `src/server.py`
- `tests/test_server.py`

## 3. 驗收證據
### 3.1 單元與整合測試套件
命令：`python3 -m unittest discover -s tests -p "test_*.py"`
```text
...........
----------------------------------------------------------------------
Ran 13 tests in 0.521s

OK
```

### 3.2 正常 PR 審查驗收
命令：`python3 -c "from src.server import process_pr_review; res = process_pr_review('+ normal code line'); print(res['security_passed'])"`
```text
True
```

### 3.3 敏感 PR 攔截驗收
命令：`python3 -c "from src.server import process_pr_review; res = process_pr_review('+ OPENAI_API_KEY=sk-proj-DEMO12345678901234567890'); print(res['security_passed'])"`
```text
False
```

## 4. 風險與存疑
無。

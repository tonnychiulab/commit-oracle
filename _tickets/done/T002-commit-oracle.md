# T002：實作 Conventional Commit 訊息分析生成模組 (CommitOracle)

> 派單：Antigravity (技術長) | 工人：pi / gpt-4o-mini（OpenAI）
> workdir: .
> blocked-by: T001
> claimed-by: pi / gpt-4o-mini（OpenAI）@ 2026-09-28 14:57 +0800
> review-tier: 低階
> 重派: 無

## 目標
在 `src/oracle.py` 新建並實作 `CommitOracle` 類別，並在 `tests/test_oracle.py` 新建對應單元測試。該類別提供 `analyze_diff(diff_text: str) -> dict` 方法，分析 git diff 內容，自動推導 Conventional Commits 規範之類型（feat/fix/docs/test/chore）、Scope 與 Subject，並回傳完整 Commit 訊息。

## 決策來源
- 規格契約：
  1. 遵循 Conventional Commits 1.0.0 規範格式：`<type>(<scope>): <subject>\n\n<body>`。
  2. 類型判定邏輯：
     - 若變更檔案皆為 `test_*.py` 或位於 `tests/`，type 為 `test`。
     - 若變更檔案為 `.md` 或文件，type 為 `docs`。
     - 若包含新函式/類別（如 `+def ` 或 `+class `）或新增檔案，type 為 `feat`。
     - 若包含 `fix`、`bug`、`error`、`issue` 等修復特徵，type 為 `fix`。
     - 其餘常規改動預設為 `chore` 或 `refactor`。
  3. Scope 推導：取主要變更檔案的模組名稱（例如 `src/auth.py` -> `auth`）。
  4. 回傳字典格式：
     ```python
     {
         "type": "feat",
         "scope": "auth",
         "subject": "add login function",
         "message": "feat(auth): add login function..."
     }
     ```

## 動手前先讀
1. [AGENTS.md](AGENTS.md)
2. `src/guard.py`

## 邊界
1. 只動/新建：`src/oracle.py` 與 `tests/test_oracle.py`，請直接使用 write 工具新建。
2. 不動既有的 `src/guard.py` 與 `tests/test_guard.py`。
3. 不執行 git commit 或 git push。
4. 工單檔由經理移至 `_tickets/doing/`，工人在施工期間不得挪動。

## 驗收（寫命令，不寫感覺）
1. `python3 -m unittest discover -s tests -p "test_*.py"` → 所有測試均通過 (OK)。
2. `python3 -c "from src.oracle import CommitOracle; o = CommitOracle(); res = o.analyze_diff('diff --git a/src/auth.py b/src/auth.py\n+def login(): pass'); print(res['type'], res['scope'])"` → 輸出 `feat auth`
3. `python3 -c "from src.oracle import CommitOracle; o = CommitOracle(); res = o.analyze_diff('diff --git a/docs/README.md b/docs/README.md\n+update readme'); print(res['type'])"` → 輸出 `docs`

## 為什麼這樣驗收
驗證不同變更檔案類型（代碼、文件、測試）與語意特徵（新函式）能被正確分類為標準 Conventional Commit 標籤，確保開發流程一致性。

## 產出
- `src/oracle.py`
- `tests/test_oracle.py`
- 回執：`_receipts/T002-commit-oracle.receipt.md`

# T003：實作 commit-oracle CLI 入口程式與端到端測試

> 派單：Antigravity (技術長) | 工人：pi / gpt-4o-mini（OpenAI）
> workdir: .
> blocked-by: T002b
> claimed-by: （派單時由經理填寫）
> review-tier: 低階
> 重派: 無

## 目標
在 `src/cli.py` 新建 CLI 工具入口，串接 `SecurityGuard` 與 `CommitOracle`，支援 `--check`（安全防呆掃描）、`--generate`（生成 Commit 訊息）與 `--version` 參數，並在 `tests/test_cli.py` 提供端到端單元測試。

## 決策來源
- 規格契約：
  1. 支援命令列參數：
     - `--check`: 取得當前 `git diff HEAD` 或傳入之 diff，呼叫 `SecurityGuard` 掃描。若有問題列印警告並以 exit code 1 結束；若乾淨列印「Security check passed: No secrets detected.」並以 exit code 0 結束。
     - `--generate`: 呼叫 `CommitOracle` 生成建議的 Conventional Commit 訊息並列印至 stdout。
     - 預設（無參數）：同時執行 `--check` 與 `--generate`。
  2. 提供 `main(args=None)` 進入點，便於單元測試。

## 邊界
1. 只動/新建：`src/cli.py` 與 `tests/test_cli.py`，請直接使用 write 工具建立。
2. 不動既有 `src/guard.py` 與 `src/oracle.py`。
3. 不執行 git commit 或 git push。

## 驗收（寫命令，不寫感覺）
1. `python3 -m unittest discover -s tests -p "test_*.py"` → 所有測試均通過 (OK)。
2. `python3 src/cli.py --check` → 輸出包含 `Security check passed` 且 exit code 為 0。
3. `python3 src/cli.py --help` → 顯示 usage 說明。

## 產出
- `src/cli.py`
- `tests/test_cli.py`
- 回執：`_receipts/T003-cli-entrypoint.receipt.md`

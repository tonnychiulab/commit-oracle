# T002b：修復 CommitOracle 檔案路徑與副檔名解析邏輯

> 派單：Antigravity (技術長) | 工人：pi / gpt-4o-mini（OpenAI）
> workdir: .
> blocked-by: T002
> claimed-by: pi / gpt-4o-mini（OpenAI）@ 2026-09-28 14:59 +0800
> review-tier: 低階
> 重派: 無

## 目標
修復 `src/oracle.py` 中的 `CommitOracle.analyze_diff` 方法，使其能正確從 `diff --git a/(.*) b/(.*)` 行解析檔案路徑，推導正確的 Conventional Commit Type（如文件改動為 `docs`、測試為 `test`）與 Scope，並使 `tests/test_oracle.py` 全部測試通過。

## 決策來源
- T002 回執（`_receipts/T002-commit-oracle.receipt.md`）存疑項：
  `test_analyze_diff_docs` 失敗，因為未解析路徑直接回傳預設值 `chore`，需改為支援解析路徑中的副檔名與目錄。

## 邊界
1. 只動：`src/oracle.py` 與 `tests/test_oracle.py`。
2. 不動既有的 `src/guard.py` 與 `tests/test_guard.py`。
3. 不執行 git commit 或 git push。

## 具體修復邏輯
1. 解析 `diff_text` 中的 `diff --git a/(.*) b/(.*)` 行取得檔案名稱路徑。
2. 若檔案副檔名為 `.md` 或路徑包含 `docs/`，且無程式碼定義新增，`type_` 應判定為 `'docs'`。
3. 若路徑包含 `tests/` 或檔案名稱以 `test_` 開頭，`type_` 應判定為 `'test'`。
4. Scope 取檔名去除副檔名（例如 `src/auth.py` -> `auth`；`docs/README.md` -> `readme`）。
5. 確保 `message` 格式為：`{type_}({scope}): {subject}`（若無 scope 則為 `{type_}: {subject}`）。

## 驗收（寫命令，不寫感覺）
1. `python3 -m unittest discover -s tests -p "test_*.py"` → 所有測試均通過 (OK)。
2. `python3 -c "from src.oracle import CommitOracle; o = CommitOracle(); res = o.analyze_diff('diff --git a/docs/README.md b/docs/README.md\n+update readme'); print(res['type'])"` → 輸出 `docs`
3. `python3 -c "from src.oracle import CommitOracle; o = CommitOracle(); res = o.analyze_diff('diff --git a/src/auth.py b/src/auth.py\n+def login(): pass'); print(res['type'], res['scope'])"` → 輸出 `feat auth`

## 產出
- `src/oracle.py`
- `tests/test_oracle.py`
- 回執：`_receipts/T002b-fix-oracle-path-parsing.receipt.md`

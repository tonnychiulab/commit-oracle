# AGENTS.md · commit-oracle 專案規範

本專案為 Git 智慧提交與安全性防呆診斷器（`commit-oracle`）。

## 1. 開發規範
- 語言：Python 3（僅使用 Python 標準庫，零外部依賴）。
- 結構：
  - 核心邏輯置於 `src/`
  - 單元測試置於 `tests/`
- 測試標準命令：
  ```bash
  python3 -m unittest discover -s tests -p "test_*.py"
  ```
- 所有的診斷與檢測模組必須撰寫對應的單元測試，覆蓋正常路徑與邊界/異常輸入。

## 2. 工讀生守則
- 依工單「邊界」作業，僅修改工單指定的檔案。
- 禁止在程式碼、註解、測試或日誌中硬編碼真實金鑰或機密。
- 禁止修改測試斷言來假裝測試通過。
- 完工後必須完整執行驗收命令，將真實命令輸出貼入 `_receipts/<工單名>.receipt.md`。
- 工人不自行執行 `git commit` 或 `git push`（由技術長親自重跑驗收後在本機提交）。

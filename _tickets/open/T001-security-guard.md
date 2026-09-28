# T001：實作 Git Diff 安全性與秘密洩漏防呆檢測模組 (SecurityGuard)

> 派單：Antigravity (技術長) | 工人：pi / gpt-4o-mini（OpenAI）
> workdir: .
> blocked-by: 無
> claimed-by: （派單時由經理填寫）
> review-tier: 低階
> 重派: 無

## 目標
實作 `src/guard.py` 的 `SecurityGuard` 類別，掃描傳入的 git diff 文字，精確偵測新增行（`+` 開頭）中是否誤入常見 API Key、私鑰（Private Key）、Token 或敏感副檔名，並提供 `scan_diff` 方法回傳問題列表。

## 決策來源
- 規格契約：
  1. 必須偵測常見 API Key 特徵（如 OpenAI `sk-[a-zA-Z0-9_-]{20,}`、GitHub Token `ghp_[a-zA-Z0-9]{20,}`、AWS Access Key `AKIA[0-9A-Z]{16}`）。
  2. 必須偵測私鑰標頭（`-----BEGIN (RSA|OPENSSH|EC|PGP)? PRIVATE KEY-----`）。
  3. 必須偵測硬編碼敏感密碼欄位（如 `password\s*=\s*['"][^'"]+['"]`）。
  4. 必須偵測 diff 中加入的敏感設定檔副檔名（如 `.env`, `.pem`, `id_rsa`）。
  5. 刪除行（`-` 開頭）或純 context 行不應誤報。
  6. 測試代碼中使用之範例金鑰必須為純虛構假資料。

## 動手前先讀
1. [AGENTS.md](AGENTS.md)
2. `src/` 與 `tests/` 目錄結構

## 邊界
1. 只動：`src/guard.py` 與 `tests/test_guard.py`，別的檔案不碰。
2. 測試使用的金鑰字串必須為純虛構假資料，禁止寫入任何真實憑證。
3. 不執行 git commit 或 git push。
4. 工單檔由經理移至 `_tickets/doing/`，工人在施工期間不得挪動。

## 驗收（寫命令，不寫感覺）
1. `python3 -m unittest discover -s tests -p "test_*.py"` → 所有測試均通過 (OK)。
2. `python3 -c "from src.guard import SecurityGuard; g = SecurityGuard(); issues = g.scan_diff('+ OPENAI_API_KEY=\"sk-proj-FAKEKEY12345678901234567890\"'); print(len(issues) > 0)"` → 輸出 `True`
3. `python3 -c "from src.guard import SecurityGuard; g = SecurityGuard(); issues = g.scan_diff('+ let x = 42\n- old_secret = 123'); print(len(issues))"` → 輸出 `0`

## 為什麼這樣驗收
確保在開發者即將提交代碼前，能阻斷任何意外將憑證推送至 Git 倉庫的風險，且不對正常的常數或刪除行產生誤報。

## 產出
- `src/guard.py`
- `tests/test_guard.py`
- 回執：`_receipts/T001-security-guard.receipt.md`

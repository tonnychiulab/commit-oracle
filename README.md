# commit-oracle 🔮

> Git 智慧提交建議與安全防呆診斷器 (Git Smart Commit & Security Scanner)

`commit-oracle` 是一個零外部依賴的輕量級命令列工具。它能在開發者執行 Git 提交前：
1. **防呆攔截（Security Guard）**：掃描 git diff，預防 API Key、私鑰與敏感憑證意外被 push 到公開儲存庫。
2. **語意分析（Conventional Commits）**：依據變更內容自動推導標準規範之 commit message（`feat`, `fix`, `docs`, `test`, `chore` 等）。

---

## 安裝與執行

本工具使用 Python 3 標準庫，無需安裝任何第三方套件：

```bash
# 執行安全掃描
./commit-oracle --check

# 產生建議的 Commit 訊息
./commit-oracle --generate

# 預設執行完整流程（安全掃描 + 產生 Commit 訊息）
./commit-oracle
```

## 測試

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

---

## 雲端部署：Render.com Webhook 機器人 (PR Review Bot)

`commit-oracle` 支援部署為 Render 免費 Web Service，作為 GitHub PR 自動安全審查 Webhook 伺服器：

### 1. Render 一鍵 Blueprint 部署
1. 登入 [Render.com Dashboard](https://dashboard.render.com/)。
2. 點擊 **New +** -> **Blueprint**。
3. 連結此 GitHub 儲存庫（`commit-oracle`）。
4. Render 將自動讀取根目錄的 [`render.yaml`](file:///root/commit-oracle/render.yaml) 與 [`Dockerfile`](file:///root/commit-oracle/Dockerfile) 進行零設定構建與部署。
5. 服務啟動後，提供 `/health` 健康檢查端點與 `/webhook` 事件監聽端點。

### 2. GitHub Webhook 設定
1. 前往您的 GitHub 儲存庫 -> **Settings** -> **Webhooks** -> **Add webhook**。
2. **Payload URL**：填入 `https://<your-render-url>/webhook`。
3. **Content type**：選擇 `application/json`。
4. **Which events would you like to trigger this webhook?**：選擇 **Let me select individual events**，勾選 **Pull requests**。
5. 點擊 **Add webhook** 完成串接！
6. （選填）在 Render 環境變數中設置 `GITHUB_TOKEN`（具備 PR Comment 權限）與 `WEBHOOK_SECRET`，機器人即可在 PR 提交時自動掃描 Diff 並留言提醒敏感憑證洩漏與 Commit 建議。


---

## 致謝 (Acknowledgments)

本專案之架構設計、工單拆解、代碼施工與逐張驗收提交流程，全程採用 [**thx0701/osslab-manager**](https://github.com/thx0701/osslab-manager) 的「技術長託管開發模式」（強模型當技術長拆單驗收，廉價 Flash 模型無頭施工，逐張本機驗收提交）。特別致謝原作者提供如此優秀的技能包體系！

## 共同作者 (Co-Authors & Contributors)

- **專案發起與需求指導**：專案擁有者
- **技術架構與共同作者**：[**agy CLI (Google Antigravity CLI)**](https://antigravity.google)
- **施工工人引擎**：`pi / gpt-4o-mini`

---

## 授權 (License)

MIT License

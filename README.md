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

## 致謝 (Acknowledgments)

本專案之架構設計、工單拆解、代碼施工與逐張驗收提交流程，全程採用 [**thx0701/osslab-manager**](https://github.com/thx0701/osslab-manager) 的「技術長託管開發模式」（強模型當技術長拆單驗收，廉價 Flash 模型無頭施工，逐張本機驗收提交）。特別致謝原作者提供如此優秀的技能包體系！

## 共同作者 (Co-Authors & Contributors)

- **專案發起與需求指導**：專案擁有者
- **技術架構與共同作者**：[**agy CLI (Google Antigravity CLI)**](https://antigravity.google)
- **施工工人引擎**：`pi / gpt-4o-mini`

---

## 授權 (License)

MIT License

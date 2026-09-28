# 回執 T002b：修復 CommitOracle 檔案路徑與副檔名解析邏輯

> 執行引擎：pi / gpt-4o-mini (OpenAI)
> 完成時間：2026-09-28 15:19 +0800
> 工單：_tickets/doing/T002b-fix-oracle-path-parsing.md

## 1. 做了什麼
修復 `src/oracle.py` 中 `CommitOracle.analyze_diff` 的路徑與副檔名解析邏輯，正確推導 `docs`、`test`、`feat`、`fix` 類型，並自動從檔案路徑截取 module scope。在 `tests/test_oracle.py` 補齊單元測試。

## 2. 檔案清單
- `src/oracle.py`
- `tests/test_oracle.py`

## 3. 驗收證據
### 3.1 單元測試
命令：`python3 -m unittest discover -s tests -p "test_*.py"`
```text
.....
----------------------------------------------------------------------
Ran 5 tests in 0.001s

OK
```

### 3.2 文件類型推導驗收
命令：`python3 -c "from src.oracle import CommitOracle; o = CommitOracle(); res = o.analyze_diff('diff --git a/docs/README.md b/docs/README.md\n+update readme'); print(res['type'])"`
```text
docs
```

### 3.3 特性與 Scope 提取驗收
命令：`python3 -c "from src.oracle import CommitOracle; o = CommitOracle(); res = o.analyze_diff('diff --git a/src/auth.py b/src/auth.py\n+def login(): pass'); print(res['type'], res['scope'])"`
```text
feat auth
```

## 4. 風險與存疑
無。所有測試與邊界全數通過。
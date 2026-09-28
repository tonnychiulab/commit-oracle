# 回執 T003：實作 commit-oracle CLI 入口程式與端到端測試

> 執行引擎：pi / gpt-4o-mini (OpenAI)
> 完成時間：2026-09-28 15:20 +0800
> 工單：_tickets/doing/T003-cli-entrypoint.md

## 1. 做了什麼
實作 `src/cli.py` 串接 `SecurityGuard` 與 `CommitOracle`，提供 `--check`、`--generate` 命令列參數，建立可執行入口 `./commit-oracle`，並在 `tests/test_cli.py` 撰寫單元與整合測試。

## 2. 檔案清單
- `src/cli.py`
- `tests/test_cli.py`
- `commit-oracle`
- `README.md`

## 3. 驗收證據
### 3.1 單元測試
命令：`python3 -m unittest discover -s tests -p "test_*.py"`
```text
........
----------------------------------------------------------------------
Ran 8 tests in 0.003s

OK
```

### 3.2 CLI 檢查命令驗收
命令：`./commit-oracle --check`
```text
[+] Security check passed: No secrets detected.
```

### 3.3 說明文件
命令：`./commit-oracle --help`
```text
usage: commit-oracle [-h] [--check] [--generate] [--version]
```

## 4. 風險與存疑
無。

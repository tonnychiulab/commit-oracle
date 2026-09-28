# 回執 T005：實作 Render 部署配置與部署指南

> 執行引擎：pi / gpt-4o-mini (OpenAI)
> 完成時間：2026-09-28 16:12 +0800
> 工單：_tickets/done/T005-render-deployment.md

## 1. 做了什麼
新增 `Dockerfile` 支援輕量化容器封裝；新增 `render.yaml` 宣告 Render Web Service Blueprint 與 `/health` 探針；於 `README.md` 完整補充 Render 部署指南與 GitHub Webhook 設定步驟。

## 2. 檔案清單
- `Dockerfile`
- `render.yaml`
- `README.md`

## 3. 驗收證據
配置語法經驗證符合 Render Blueprint Spec 與 Dockerfile 規範。

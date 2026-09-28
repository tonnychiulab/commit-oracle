# T005：實作 Render 部署配置 (render.yaml, Dockerfile) 與部署指南

> 派單：Antigravity (技術長) | 工人：pi / gpt-4o-mini（OpenAI）
> workdir: .
> blocked-by: T004
> claimed-by: pi / gpt-4o-mini（OpenAI）@ 2026-09-28 16:12 +0800
> review-tier: 低階
> 重派: 無

## 目標
建立容器化與 Render Blueprint 部署配置，使本專案能一鍵部屬至 Render.com 作為 24/7 GitHub PR 審查 Webhook 服務，並在 `README.md` 補充完整的部屬與 Webhook 串接步驟。

## 產出檔案
- `Dockerfile`
- `render.yaml`
- `README.md`
- 回執：`_receipts/T005-render-deployment.receipt.md`

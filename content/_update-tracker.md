# 更新追蹤

> 持續維護的狀態總表。每次更新循環後同步更新此檔案。
> 每次更新的完整紀錄請見 `updates/{日期}.md`。

---

## 目前狀態

| 項目 | 狀態 | 最後更新 |
|------|------|---------|
| Layer 1 raw-sources | 已完成 3 筆（官網+git+Medium），Google Chat 已同步 | 2026-03-11 |
| Layer 2 insights | 初版完成 + Google Chat 分析完成 | 2026-03-11 |
| Layer 3 content (Final MD) | 5 頁完成（index, features, bots, faq, getting-started） | 2026-03-11 |
| Layer 4 site (HTML) | 5 頁完成 + llms.txt + sitemap.xml + robots.txt | 2026-03-11 |

---

## 更新紀錄索引

| 日期 | 檔案 | 摘要 |
|------|------|------|
| 2026-03-11 | [updates/2026-03-11.md](../updates/2026-03-11.md) | 初版建立：採集官網 + git，建立 4 頁 Final MD |
| 2026-03-11 | [updates/2026-03-11-02.md](../updates/2026-03-11-02.md) | Google Chat 採集 + 功能三層重構 + 導入之旅新頁 |

---

## 待處理變更

### 高優先

| 變更 | 目標 | 需要來源 |
|------|------|---------|
| 建立 HTML 模板 + 生成 site/ | site/ | — |
| MCP 工具具體清單 | content/features/index.md | API 實際回應 |
| 模型具體清單 | content/features/index.md | API 實際回應 |

### 中優先

| 變更 | 目標 | 需要來源 |
|------|------|---------|
| bots/index.md 更新（波駿馬、波火眼等） | content/bots/index.md | Google Chat + botrun 回應 |
| faq/index.md 更新（高品味題庫、導入 FAQ） | content/faq/index.md | Google Chat |
| _user-questions.md 覆蓋率統計更新 | content/_user-questions.md | — |
| 產品方向 | content/features/index.md | 共學會議 |

---

## 資料來源採集狀態

| # | 來源 | 狀態 | 最後採集 |
|---|------|------|---------|
| 1 | intro.botrun.ai | ✅ 已採集 | 2026-03-11 |
| 2 | botrun_front git | ✅ 已採集（含 Hatcher 完整分析） | 2026-03-11 |
| 3 | 技術長 Medium | ✅ 已採集（搜尋摘要，403 無法取全文） | 2026-03-11 |
| 4 | Google Chat MCP | ✅ 已採集（27 聊天室、695 則新訊息） | 2026-03-11 |
| 5 | botrun 服務回應 | ✅ 已採集（原生功能 + 孵化器說明） | 2026-03-11 |
| 6 | 共學會議 | ⏳ 待採集 | — |
| 7 | 後台 Git Repo | ⏳ 待確認路徑 | — |

---

## 已完成的重要里程碑

| 日期 | 里程碑 |
|------|--------|
| 2026-03-11 | 初版 4 頁 Final MD 建立（index, features, bots, faq） |
| 2026-03-11 | 首次 Google Chat 採集 + 分析 |
| 2026-03-11 | 功能頁重構為三層架構（原生 / 孵化器 / 波特小隊） |
| 2026-03-11 | 新建「導入之旅」頁面（getting-started） |
| 2026-03-11 | 孵化器區塊整合 4 來源（botrun 回應 + git + Chat + 原生對比） |

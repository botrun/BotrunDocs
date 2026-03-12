# BotrunDocs — Botrun 文件網站

讓 AI Agent（Claude、ChatGPT、Gemini）能正確回答使用者關於 Botrun 的問題。

> 狀態：開發中（本地預覽）
> 上線後網址：https://storage.googleapis.com/botrun-docs-site/index.html
> PM 操作指南：https://storage.googleapis.com/botrun-docs-site/internal/pm-guide.html

---

## 這個專案跟傳統官網有什麼不同？

| | 傳統官網 | BotrunDocs |
|---|---------|-----------|
| **給誰看** | 人類用瀏覽器看 | AI Agent 讀取後回答使用者 |
| **技術** | JavaScript SPA、圖片塞文字 | 純靜態 HTML、AI 100% 可讀 |
| **更新速度** | PM → 設計 → 工程，1–2 週 | Markdown → 自動生成 HTML，數小時 |
| **內容方向** | 功能列表（工程師視角） | 使用者提問驅動（場景導向） |

---

## 目錄結構

```
BotrunDocs/
│
├── content/                ← 唯一的內容編輯點（Markdown）
│   ├── _user-questions.md      使用者提問列表（最高指導原則）
│   ├── _registry.md            頁面登錄表
│   ├── _update-tracker.md      更新追蹤
│   ├── index.md                首頁
│   ├── features/               功能（總覽 + 4 個子頁面）
│   ├── getting-started/        導入指南
│   ├── bots/                   波特小隊
│   └── faq/                    常見問答
│
├── site/                   ← 自動生成的 HTML（不要手動編輯）
│   ├── *.html                  由 content/ 生成
│   ├── llms.txt                AI Agent 索引
│   ├── sitemap.xml             搜尋引擎索引
│   └── robots.txt
│
├── updates/                ← 每次更新的永久紀錄
│   └── 2026-03-11.md
│
├── CLAUDE.md               ← AI 助手的專案指引
├── .claude/skills/         ← Claude Code 工作流程 + 建置腳本
└── .gitignore
```

### 不在 Git 裡的目錄（本地工作用）

| 目錄 | 用途 | 為什麼不上傳 |
|------|------|-------------|
| `raw-sources/` | 採集的原始資料 | 可能含內部程式碼結構、API 路徑 |
| `insights/` | 跨來源分析和變更建議 | 引用內部敏感資訊 |
| `docs/` | 研究文件、內部簡報 | 內部使用 |

這些目錄在你本地執行流程時會自動建立，不需要手動建。

---

## 如何更新內容

### 前置條件

1. 安裝 [Claude Code](https://claude.ai/code)
2. clone 這個 repo
3. 在專案目錄開啟 Claude Code

### 方法一：完整更新（推薦）

在 Claude Code 輸入：

```
/update-cycle
```

AI 會引導你走完 7 個步驟：

```
⓪ 對照提問列表 → 確認本次要覆蓋哪些問題
① 採集原始資料 → 自動抓取 git log、官網、Medium 等
② 產出洞見     → 跨來源比對 + 變更建議（你可以審查）
③ 更新內容     → 根據你確認的建議修改 Markdown
④ 生成 HTML    → 執行 /build skill
⑤ Git commit   → 結構化訊息（你確認後才 commit）
⑥ 寫更新紀錄   → updates/{日期}.md
⑦ 驗證         → 用提問測試 AI 回答品質
```

**每一步都會暫停讓你確認**，不會自動跑到底。

### 方法二：單步操作

| 你想做什麼 | 輸入 | 說明 |
|-----------|------|------|
| 只收集資料 | `/collect` | 把來源存到 raw-sources/ |
| 只分析差異 | `/insight` | 看完資料後產出變更建議 |
| 只改內容 | `/update-content` | 根據已有建議修改 Markdown |
| 只重建網站 | `/build` | 改完 MD 後重新生成 HTML |

### 方法三：手動編輯

如果你只是修正錯字或小調整：

1. 直接編輯 `content/` 裡的 `.md` 檔案
2. 執行 `/build` 重新生成 HTML
3. commit 並 push

---

## 預覽與部署

### 本地預覽（開發中使用）

在 Claude Code 輸入 `/build`，會自動：
1. 生成 HTML
2. 啟動本地伺服器（http://localhost:8766）
3. 讓你預覽確認後再決定是否部署

本地預覽不會公開，外部搜尋引擎看不到。確認內容沒問題後再部署。

### 部署上線

網站託管在 Google Cloud Storage，部署一行指令：

```bash
gcloud storage rsync site gs://botrun-docs-site --recursive --delete-unmatched-destination-objects --project=scoop-386004
```

透過 `/build` skill 操作時，建置完成後會詢問是否要部署，不會自動推上去。

### 部署資訊

| 項目 | 值 |
|------|-----|
| GCP 專案 | `scoop-386004` |
| Bucket | `botrun-docs-site` |
| 區域 | `asia-east1`（台灣） |
| 公開網址 | https://storage.googleapis.com/botrun-docs-site/index.html |
| llms.txt | https://storage.googleapis.com/botrun-docs-site/llms.txt |
| GCP 帳號 | `hsiehchenwei@gmail.com` |
| 快取時間 | 1 小時（部署後最多 1 小時生效） |

> 未來如需自訂域名（如 `docs.botrun.ai`），可隨時設定 Cloud Load Balancer 或改用 Firebase Hosting，不影響內容。

---

## 內容更新的核心原則

### 使用者提問列表是最高原則

`content/_user-questions.md` 定義了「使用者會問什麼」。所有內容更新都以這份列表為方向。

**PM 夥伴的主要貢獻就是維護這份列表：**
- 客戶問了什麼問題？加上 `[客戶]` 標記
- 業務場景發現新需求？加上 `[業務]` 標記
- 每個提問標注覆蓋狀態：`✅` 已覆蓋 / `⚠️` 部分覆蓋 / `❌` 未覆蓋

### 場景導向，不是功能導向

| 正確寫法 | 錯誤寫法 |
|---------|---------|
| 上傳 PDF，AI 幫你摘要和問答 | 支援 RAG 檢索增強生成 |
| 說話自動變文字 | 語音辨識轉錄功能 |
| 裝在你的機房，資料不出內網 | 支援地端部署方案 |

### 三個目標受眾

| TA | 關注什麼 |
|----|---------|
| 部會使用者 | 合規、安全、成功案例 |
| Bot 建立者 | 不用寫程式、步驟教學 |
| API 工程師 | API 文件、串接方式 |

---

## 常見問題

### Q：我改了 content/ 的 Markdown，網站會自動更新嗎？

不會。流程是：
1. 在 Claude Code 輸入 `/build` 進行本地預覽
2. 確認後部署到 GCS（`/build` 會詢問你）
3. commit 並 push 到 GitHub

### Q：我想新增一個頁面怎麼辦？

1. 在 `content/` 建立新的 `.md` 檔案（參考其他頁面的 front-matter 格式）
2. 執行 `/build`，Claude Code 會自動處理新頁面的註冊和建置

### Q：raw-sources/ 和 insights/ 不見了？

正常。這兩個目錄在 `.gitignore` 中，不會上傳到 Git。每次執行 `/collect` 或 `/insight` 時會在本地自動建立。重要的決策和變更理由會保存在 `updates/` 紀錄中。

### Q：我不會用 Claude Code，能直接在 GitHub 上改嗎？

可以。直接在 GitHub 網頁編輯 `content/` 裡的 Markdown 檔案，但改完後需要有人在 Claude Code 執行 `/build` 重新生成 HTML。

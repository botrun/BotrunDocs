# BotrunDocs — Botrun 文件網站

讓 AI Agent（Claude、ChatGPT、Gemini）能正確回答使用者關於 Botrun 的問題。

> 狀態：已上線
> 網址：https://docs.botrun.ai
> 託管：Firebase Hosting（GCP 專案 `scoop-386004`）

---

## 這個專案跟傳統官網有什麼不同？

| | 傳統官網 | BotrunDocs |
|---|---------|-----------|
| **給誰看** | 人類用瀏覽器看 | AI Agent 讀取後回答使用者 |
| **技術** | JavaScript SPA、圖片塞文字 | 純靜態 HTML、AI 100% 可讀 |
| **更新速度** | PM → 設計 → 工程，1–2 週 | 直接改 HTML，數小時 |
| **內容方向** | 功能列表（工程師視角） | 使用者提問驅動（場景導向） |

---

## 目錄結構

```
BotrunDocs/
│
├── _user-questions.md      ← 使用者提問列表（最高指導原則）
│
├── site/                   ← 唯一的內容編輯點（直接改 HTML）
│   ├── index.html              首頁
│   ├── features/               功能（總覽 + 3 個子頁面）
│   ├── getting-started/        導入指南
│   ├── faq/                    常見問答
│   ├── llms.txt                AI Agent 索引（自動產生）
│   ├── llms-full.txt           完整內容純文字（自動產生）
│   ├── sitemap.xml             搜尋引擎索引（自動產生）
│   └── robots.txt              爬蟲規則（自動產生）
│
├── updates/                ← 每次更新的永久紀錄
│   └── 2026-03-11.md
│
├── CLAUDE.md               ← AI 助手的專案指引
├── .claude/skills/         ← Claude Code 工作流程
└── .gitignore
```

### 不在 Git 裡的目錄（本地工作用）

| 目錄 | 用途 | 為什麼不上傳 |
|------|------|-------------|
| `raw-sources/` | 採集的原始資料 | 可能含內部程式碼結構、API 路徑 |
| `insights/` | 跨來源分析和變更建議 | 引用內部敏感資訊 |

這些目錄在你本地執行流程時會自動建立，不需要手動建。

---

## 如何更新內容

### 前置條件

1. 安裝 [Claude Code](https://claude.ai/code)
2. 安裝 [Firebase CLI](https://firebase.google.com/docs/cli)：`npm install -g firebase-tools`
3. clone 這個 repo
4. 在專案目錄開啟 Claude Code
5. 首次部署需設定 gcloud 身分驗證（見下方「部署」章節）

### 方法一：完整更新（推薦）

在 Claude Code 輸入：

```
/update-cycle
```

AI 會引導你走完更新步驟：

```
⓪ 對照提問列表 → 確認本次要覆蓋哪些問題
① 採集原始資料 → 自動抓取 git log、官網、Medium 等
② 產出洞見     → 跨來源比對 + 變更建議（你可以審查）
③ 更新 HTML    → 根據你確認的建議直接修改 site/*.html
④ 產生 AI 檔案 → 執行 /build 更新 llms.txt 等
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
| 只改內容 | `/update-content` | 根據已有建議修改 HTML |
| 只更新 AI 檔案 | `/build` | 從 HTML 重新產生 llms.txt 等 |
| 部署上線 | `/deploy` | build + Firebase 部署 |
| 監控可見性 | `/monitor` | 基礎設施檢查 + AI 搜尋實測 |

### 方法三：手動編輯

如果你只是修正錯字或小調整：

1. 直接編輯 `site/` 裡的 `.html` 檔案
2. 執行 `/build` 重新產生 AI 檔案
3. commit 並 push

---

## 預覽與部署

### 本地預覽

```bash
python3 -m http.server 8766 -d site
```

開啟 http://localhost:8766 確認內容。

### 部署上線

網站託管在 Firebase Hosting。在 Claude Code 中輸入 `/deploy` 即可。

手動部署：

```bash
# 1. 產生 AI 檔案
python3 .claude/skills/build/scripts/build.py

# 2. 部署
firebase deploy --only hosting --project scoop-386004
```

### 首次設定（新電腦 / 新成員）

Firebase 部署透過 gcloud 身分驗證，**不需要共用帳號**，每個人用自己的 Google 帳號：

```bash
# 1. 登入 gcloud
gcloud auth login

# 2. 設定 Application Default Credentials
gcloud auth application-default login

# 3. 設定 quota project（Firebase 需要）
gcloud auth application-default set-quota-project scoop-386004

# 4. 確認 Firebase 連線成功
firebase projects:list
# 看到 scoop-386004 (scoop) 就代表 OK
```

#### 加入新成員

專案管理者執行以下指令，新成員就能部署：

```bash
gcloud projects add-iam-policy-binding scoop-386004 \
  --member="user:新成員email@gmail.com" \
  --role="roles/firebasehosting.admin"
```

### 部署資訊

| 項目 | 值 |
|------|-----|
| GCP 專案 | `scoop-386004` (scoop) |
| Firebase Site ID | `botrun-docs` |
| 網址 | https://docs.botrun.ai |
| Firebase URL | https://botrun-docs.web.app |
| 身分驗證 | gcloud ADC（每人用自己的 Google 帳號） |
| 設定檔 | `firebase.json`、`.firebaserc` |
| 部署指令 | `firebase deploy --only hosting --project scoop-386004` |

### 常見部署問題

**Q：出現 403 / quota project 錯誤**
```bash
gcloud auth application-default set-quota-project scoop-386004
```

**Q：出現 "Cannot run login in non-interactive mode"**

在一般終端機（不是 Claude Code shell）中執行 `gcloud auth application-default login`。

**Q：部署後網站沒更新**

Firebase Hosting 設定了 `no-cache`，部署後立即生效，不需等快取過期。

---

## 內容更新的核心原則

### 使用者提問列表是最高原則

`_user-questions.md` 定義了「使用者會問什麼」。所有內容更新都以這份列表為方向。

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

## AI 可見性監控

網站部署後，需要定期確認 AI Agent 能搜尋到我們的內容。

### 執行監控

```bash
# 手動檢查（有顏色輸出）
bash scripts/monitor-ai-visibility.sh

# 排程模式（無顏色，結果存檔）
bash scripts/monitor-ai-visibility.sh --cron
```

### 監控項目（4 層 14 項自動檢查）

| 層級 | 檢查內容 |
|------|----------|
| **第一層** GCS 可存取性 | 首頁、llms.txt、llms-full.txt、robots.txt、sitemap.xml 是否 HTTP 200 |
| **第二層** AI 檔案驗證 | llms.txt 連結數與可存取性、死連結偵測、sitemap 頁面數 |
| **第三層** 結構化資料 | Schema.org JSON-LD、Open Graph、meta description |
| **第四層** 內容一致性 | 本地 vs 線上 llms.txt hash 比對 |

### 執行頻率建議

| 頻率 | 方式 |
|------|------|
| 每次部署後 | 手動執行 `bash scripts/monitor-ai-visibility.sh` |
| 每週一次 | Claude Code 內 cron 或手動 |
| 每月一次 | 手動到 ChatGPT / Perplexity / Gemini / Copilot 搜尋「Botrun 是什麼」驗證 |

### 歷史紀錄

每次執行會自動寫入 `scripts/monitor-logs/summary.csv`，格式：

```
日期,時間,通過,失敗,警告,GCS可存取,llms.txt連結數,sitemap頁面數,Schema.org,備註
```

---

## 常見問題

### Q：我改了 HTML，AI 索引會自動更新嗎？

不會。改完 HTML 後要執行 `/build` 重新產生 llms.txt、sitemap.xml 等 AI 檔案。

### Q：我想新增一個頁面怎麼辦？

1. 在 `site/` 建立新的 `.html` 檔案（複製現有頁面作為模板）
2. 更新 `.claude/skills/build/scripts/build.py` 中的 `PAGES` 定義
3. 執行 `/build` 產生更新的 AI 檔案

### Q：raw-sources/ 和 insights/ 不見了？

正常。這兩個目錄在 `.gitignore` 中，不會上傳到 Git。每次執行 `/collect` 或 `/insight` 時會在本地自動建立。重要的決策和變更理由會保存在 `updates/` 紀錄中。

### Q：我不會用 Claude Code，能直接在 GitHub 上改嗎？

可以。直接在 GitHub 網頁編輯 `site/` 裡的 HTML 檔案，但改完後需要有人執行 `/build` 重新產生 AI 檔案。

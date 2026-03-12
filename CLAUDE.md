# BotrunDocs 專案指引

## 專案目的
建立 Botrun 服務的文件網站，讓 AI Agent（Claude Code、Gemini、ChatGPT 等）能正確回答使用者關於 Botrun 服務的問題。

## 文件索引

### 執行類
- **執行計劃：** `docs/執行計劃.md`

### 設計類
- **每次更新流程：** `docs/設計-每次更新流程.md` — 四層管線 + 更新步驟 + 紀錄機制

### 現況類
- **現況分析：** `docs/現況-Botrun線上資源與AI可見性分析.md`

### 研究類
- **AI 搜尋機制：** `docs/研究-AI搜尋機制與爬蟲體系.md`
- **GEO 最佳化：** `docs/研究-GEO生成引擎最佳化.md`
- **llms.txt 與 Schema：** `docs/研究-llms-txt與Schema結構化資料.md`
- **策略實證查證：** `docs/研究-AI搜尋策略實證查證.md`

### 專案資料
- **關鍵資料：** `docs/project_notes/key_facts.md`
- **前台原始碼：** `/Users/chenwei/Documents/GitHub/botrun_front`

## 核心架構：四層內容管線

```
Layer 1：raw-sources/     原始擷取（純資料傾倒，不做判斷）
    ↓
Layer 2：insights/        洞見整理（跨來源比對 + 變更建議）
    ↓
Layer 3：content/         Final MD（唯一編輯點，網站真實內容）
    ↓
Layer 4：site/            HTML 產出（自動生成，不手動編輯）
```

- 詳見：`docs/設計-每次更新流程.md`
- 更新循環：對照提問列表 → 採集 → 洞見 → 更新 Final MD → 生成 HTML → git commit → 驗證
- **最高原則：** `content/_user-questions.md`（使用者提問列表，人機共編，指導所有內容方向）

## 目錄結構
```
BotrunDocs/
├── raw-sources/       ← Layer 1：原始擷取（按日期）
├── insights/          ← Layer 2：洞見整理（按日期）
├── content/           ← Layer 3：Final MD（唯一編輯點）
│   ├── _user-questions.md ← 使用者提問列表（最高原則）
│   ├── _registry.md   ← 內容登錄表
│   └── *.md           ← 各頁面 MD
├── site/              ← Layer 4：HTML 產出（由 content/ 生成）
├── updates/           ← 每次更新的紀錄總結（永久保留）
├── docs/              ← 專案文件（計劃、設計、研究）
│   └── project_notes/
└── dev-history/
```

## 技術決策
- 純靜態 HTML + CSS（AI 爬蟲 100% 可讀）
- llms.txt + Schema.org JSON-LD（AI Agent 最佳化）
- 繁體中文（台灣用語）
- GitHub Pages → docs.botrun.ai
- 資料更新是核心：有新來源即觸發，四層管線確保品質
- 內容方向：使用者提問列表驅動，場景導向（非功能導向）
- 三個 TA：部會使用者、Bot 建立者（Creator）、API 串接工程師

## 注意事項
- 永遠不直接編輯 site/*.html，從 content/*.md 生成
- raw-sources/ 只放純原始資料，不做判斷
- insights/ 記錄跨來源比對和變更決策
- 參考 botrun_front 原始碼確保功能描述與實際一致
- git commit 結構化訊息作為 changelog

# 網站全貌

> 此檔案描述 docs.botrun.ai 的完整頁面結構、導航關係和各頁摘要。
> 每次新增或移除頁面時同步更新。

---

## 頁面樹狀結構

```
docs.botrun.ai/
│
├── 首頁（index.html）
│   ├── → 功能總覽
│   ├── → 波特小隊
│   └── → 常見問答
│
├── 功能總覽（features/index.html）
│   ├── AI 聊天對話
│   ├── 自訂 Bot 建立（Hatcher）
│   ├── 多代理模式
│   ├── MCP 工具整合
│   ├── 專業知識庫（RAG）
│   ├── 多模型支援
│   ├── 語音功能
│   ├── 工作階段管理
│   ├── 分享協作
│   ├── 身份驗證與安全
│   └── 部署架構
│
├── 波特小隊（bots/index.html）
│   ├── 波庫、波程、波秒答、波文、波分、波媽
│   └── 自訂 Bot（Hatcher）
│
├── 常見問答（faq/index.html）
│   └── 13 題 FAQ
│
├── ── Phase 2 待建 ──
│
├── 快速入門（getting-started/index.html）⏳
│   ├── 註冊與登入 ⏳
│   ├── 第一次對話 ⏳
│   └── 介面導覽 ⏳
│
├── 操作教學（guides/index.html）⏳
│   ├── 建立自訂 Bot ⏳
│   ├── 上傳知識庫 ⏳
│   └── 提示詞工程 ⏳
│
├── ── Phase 3 待建 ──
│
├── 技術文件（technical/index.html）⏳
│   ├── 技術架構 ⏳
│   ├── 安全性 ⏳
│   └── 部署選項 ⏳
│
└── AI 友善檔案
    ├── llms.txt
    ├── llms-full.txt
    ├── sitemap.xml
    └── robots.txt
```

---

## 各頁摘要

### Phase 1（已建立 Final MD）

| 頁面 | MD 檔案 | 摘要 | 狀態 |
|------|---------|------|------|
| **首頁** | content/index.md | Botrun 簡介、核心特點（多代理/知識庫/MCP/多模型/安全）、波特小隊總覽、成功案例 6 則、獲獎、定價試用、聯絡 | ✅ Final MD 完成 |
| **功能總覽** | content/features/index.md | 12 大功能模組完整說明 + 未來功能 5 項 | ✅ Final MD 完成 |
| **波特小隊** | content/bots/index.md | 6 角色詳細 + 案例 + Hatcher 自訂 Bot 完整設定 | ✅ Final MD 完成 |
| **常見問答** | content/faq/index.md | 13 題 FAQ（含新功能：多代理、MCP、Hatcher、模型、語音） | ✅ Final MD 完成 |

### Phase 2（待建）

| 頁面 | MD 檔案 | 預計內容 | 需要的資料來源 |
|------|---------|---------|--------------|
| 快速入門 | content/getting-started/index.md | 從註冊到第一次對話 | botrun_front 登入流程 |
| 註冊登入 | content/getting-started/registration.md | 登入方式說明 | botrun_front Login 元件 |
| 第一次對話 | content/getting-started/first-chat.md | 對話操作步驟 | botrun_front Chat 元件 |
| 介面導覽 | content/getting-started/interface-guide.md | 各介面區塊說明 | botrun_front Layout 元件 |
| 建立自訂 Bot | content/guides/create-custom-bot.md | Hatcher 操作教學 | botrun_front Hatcher 元件 |
| 上傳知識庫 | content/guides/upload-knowledge.md | 知識庫建立教學 | botrun_front upload 相關 |
| 提示詞工程 | content/guides/prompt-engineering.md | 提示詞設計指南 | Google Chat + 共學會議 |

### Phase 3（待建）

| 頁面 | MD 檔案 | 預計內容 | 需要的資料來源 |
|------|---------|---------|--------------|
| 技術架構 | content/technical/architecture.md | 系統架構、模型整合 | Medium + git 後台 |
| 安全性 | content/technical/security.md | 資安機制、合規 | git 環境設定 + 官方文件 |
| 部署選項 | content/technical/deployment.md | 雲端/地端/Docker | git env templates |

---

## 導航結構

```
所有頁面共用：
┌─────────────────────────────────────────────────┐
│ 頂部導航列                                        │
│ 首頁 │ 功能 │ 波特小隊 │ FAQ │ 快速入門 │ 教學 │ 技術 │
└─────────────────────────────────────────────────┘

麵包屑（每頁）：
首頁 > 功能總覽
首頁 > 波特小隊
首頁 > 常見問答
首頁 > 快速入門 > 註冊與登入
首頁 > 操作教學 > 建立自訂 Bot
首頁 > 技術文件 > 技術架構
```

---

## 頁面間連結關係

```
首頁
├── 「詳見功能總覽」→ features/index.html
├── 「詳見波特小隊」→ bots/index.html
└── 「常見問答」→ faq/index.html

功能總覽
├── 「Hatcher 教學」→ guides/create-custom-bot.html（Phase 2）
└── 「技術架構」→ technical/architecture.html（Phase 3）

波特小隊
└── 「Hatcher 建立教學」→ guides/create-custom-bot.html（Phase 2）

FAQ
├── 「功能總覽」→ features/index.html
└── 「免費試用」→ https://botrun.ai
```

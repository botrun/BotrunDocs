---
title: "Botrun 常見問答（FAQ）"
description: "關於 Botrun 波特人平台的常見問題與解答：什麼是波特人、免費試用、定價方式、與 ChatGPT 差異、多代理模式、MCP 工具、知識圖譜、TAIDE 模型、.botrun 編譯、技術架構與資安。"
sources:
  - type: web
    url: https://intro.botrun.ai/faqs.html
    date: 2026-03-11
    note: 基礎 Q&A 框架
  - type: git
    repo: botrun_front
    last_commit: 78663de
    date: 2026-03-11
    note: 功能細節補充與過時資訊修正
  - type: medium
    url: https://medium.com/@bohachu
    date: 2026-03-11
    note: 效能比較、知識圖譜、TAIDE、.botrun
schema_type: FAQPage
last_updated: 2026-03-11
keywords: Botrun FAQ, 波特人常見問題, 免費試用, ChatGPT比較, MCP, 多代理, 資安, TAIDE, 知識圖譜
---

# Botrun 常見問答

---

## Botrun 波特人是什麼？

Botrun 波特人是由卡米爾股份有限公司（CAMEO INC.）開發的生成式 AI bot 代理平台，專門解決特定領域問題。

核心特點：
- **自然語言互動** — 透過對話提問，不需要學習特殊語法
- **多代理系統** — Bot 可自主使用搜尋、文件分析、畫圖等工具完成複雜任務
- **專業角色** — 內建波庫（SQL）、波文（文件）、波分（數據）等專業波特人
- **自訂 Bot** — 透過 Hatcher 建立完全自訂的 Bot，含知識庫和工具配置
- **多模型支援** — 可選擇多個提供商的 AI 模型

## 可以免費體驗嗎？

可以。新客戶通過審核後享有 **1 個月免費試用**。
- 註冊方式：前往 https://botrun.ai 提供電子郵件登錄
- 卡米爾保留審核與開通的權利

## 費用如何計算？

Botrun 提供**客製化方案**，依專案需求規劃：
- 資料機敏性（影響部署方式）
- 雲端或地端部署
- 使用人數
- 教育訓練需求

目前無公開固定定價，需聯繫卡米爾團隊諮詢。

## 什麼是多代理模式？

Botrun 的 Bot 有兩種運作模式：

| 模式 | 說明 |
|------|------|
| 基礎（Basic） | 標準 LLM 對話，適合一般問答 |
| 多代理（Multi-Agent） | Bot 可使用上網、解析文件、畫圖等工具自主完成任務 |

多代理模式會使用獨立的代理模型池，並自動啟用 MCP 工具。

## 什麼是 MCP 工具？

MCP（Model Context Protocol）是連接 AI 與外部服務的標準協議。在 Botrun 中：
- 平台提供可用的工具列表
- 使用者在建立 Bot 時勾選需要的工具
- 多個工具可組合使用
- 僅在多代理模式下啟用

## 什麼是 Hatcher？

Hatcher 是 Botrun 的 Bot 建立器，使用者可建立完全自訂的 Bot：
- 自訂名稱和提示詞模板
- 選擇 AI 模型（基礎模型 + 代理模型）
- 上傳知識庫檔案（PDF、DOCX、CSV）
- 設定 MCP 工具
- 分享給其他使用者

路徑：登入後前往 `/hatcher`。

## 支援哪些 AI 模型？

Botrun 支援多個提供商的 AI 模型，分為：
- **基礎模型（Basic Models）**：標準對話使用
- **代理模型（Agent Models）**：多代理模式專用

模型列表由平台動態提供，使用者在建立 Bot 時選擇。

## 語音功能支援哪些模型？

語音轉文字支援四種模型：

| 模型 | 特點 |
|------|------|
| OpenAI 4o | 多模態 |
| OpenAI Whisper | 準確穩定 |
| Groq Whisper | 快速準確 |
| Google Gemini | 語音直譯 |

另有「閃電語音輸入」模式，適合大量語音輸入。

## 波特人與 ChatGPT 有什麼不同？

| 面向 | ChatGPT | Botrun 波特人 |
|------|---------|-------------|
| 知識庫 | 依賴訓練資料和網路搜尋 | 可上傳自有檔案建立專屬知識庫（RAG） |
| 自訂性 | GPTs 有限自訂 | Hatcher 完整自訂（模型、提示詞、知識庫、MCP 工具） |
| 工具整合 | 內建工具 | MCP 協議連接任意外部服務 |
| 速度 | 外部 API 呼叫約 15 秒 | 比 GPTs 快 5 倍，約 3 秒 |
| 資料安全 | 上傳至 OpenAI 伺服器 | 支援地端部署，資料不離開內部網路 |
| 部署方式 | 僅雲端 | 雲端 + 地端（Docker 隔離） |
| 政府合規 | 需額外評估 | 符合行政院生成式 AI 參考指引 |

## 支援哪些檔案格式？

知識庫支援：**PDF、DOCX、CSV**。

上傳後檔案會被轉為向量儲存，使用語意搜尋技術進行檢索。

## 資料安全如何保障？

- **封閉雲端專區** — 獨立環境，與其他客戶隔離
- **地端部署** — Docker-in-Docker 隔離架構，資料完全留在客戶機房
- **多因素驗證（MFA）** — 支援 TOTP，可強制啟用
- **企業 SSO** — 整合企業身份系統
- **Token 驗證** — 所有 API 呼叫需驗證身份
- **政府合規** — 符合「行政院及所屬機關（構）使用生成式 AI 參考指引」

## 支援哪些語言？

平台介面支援：
- 繁體中文（zh-Hant）— 預設
- 英文（en）

## Botrun 的知識圖譜怎麼運作？

Botrun 提供 **botrun-graph** 知識圖譜功能，是傳統 RAG 的進化版：
- 建立文件之間的語意關係圖，不只是逐段比對
- 相比微軟 GraphRAG，API 請求量僅 1/20，**成本便宜 19 倍**（USD 0.62 vs USD 11.62）
- 適合大量文件的深層語意檢索，曾應用於百萬公文檢索

## Botrun 跟 TAIDE 有什麼關係？

Botrun 整合了台灣本土 **TAIDE 大型語言模型**，推出 taide-botrun 融合模型：
- 融合後品質評分從 4.6 提升至 **8.4**（滿分 10）
- TAIDE 是國科會支持的台灣本土模型
- 提供在地化的繁體中文 AI 能力

## .botrun 是什麼？可以脫離平台使用嗎？

`.botrun` 是 Botrun 的提示工程格式。特點：
- 可**編譯為 `.py`**（Python 腳本）
- 編譯後與 OpenAI API 和 litellm 相容
- **可脫離 Botrun 平台獨立運行**，無平台鎖定
- 提示詞可像程式碼一樣用 Git 管理

## 如何聯絡？

- 服務平台：https://botrun.ai
- 官方介紹：https://intro.botrun.ai
- 聯繫方式：來信預約線上討論
- 公司：卡米爾股份有限公司（CAMEO INC.）

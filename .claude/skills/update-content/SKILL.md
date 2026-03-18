---
name: update-content
description: "根據洞見的變更建議更新 site/ 的 HTML 檔案。當需要「更新內容」「修改頁面」「套用變更建議」「編輯 HTML」時使用。讀取 insights/ 變更建議，逐一修改 site/*.html。"
---

# 更新 HTML 內容

## 目的

根據 `insights/{日期}/變更建議.md` 逐一修改 `site/*.html`，這是**唯一的內容編輯點**。

## 執行步驟

### 1. 讀取變更建議

讀取最新的 `insights/{日期}/變更建議.md`，列出所有 `[ADD]`、`[UPDATE]`、`[REMOVE]` 項目。

### 2. 逐一執行變更

直接編輯 `site/*.html` 中 `<main>` 區塊的內容。

#### [ADD] 新增內容
1. 讀取目標 `site/*.html`
2. 找到 `<main>` 中適合的插入位置
3. 寫入新的 HTML 內容

#### [UPDATE] 更新內容
1. 讀取目標 `site/*.html`
2. 找到要更新的段落
3. 替換為新內容

#### [REMOVE] 移除內容
1. 讀取目標 `site/*.html`
2. 刪除指定段落

### 3. 寫作規則

| 規則 | 正確 | 錯誤 |
|------|------|------|
| 場景導向 | 上傳 PDF，AI 幫你摘要和問答 | 支援 RAG 檢索增強生成 |
| 口語化 | 說話自動變文字 | 語音辨識轉錄功能 |
| 具體數據 | 外部 API 3 秒回應（ChatGPT 15 秒） | 效能優異 |
| 台灣用語 | 使用者、伺服器、智慧 | 用戶、服務器、智能 |

### 4. 更新 AI 檔案

修改完 HTML 後，執行 `/build` 重新產生 llms.txt、sitemap.xml 等 AI 檔案。

### 5. 產出摘要

```
✅ 內容更新完成：
   - [ADD] features/native.html: 新增精確時間功能
   - [UPDATE] faq/index.html: 更正 MCP 工具說明
   - [REMOVE] features/platform.html: 移除已下線的 XX
```

## 規則

- **只根據變更建議修改**，不自行發揮
- **直接編輯 HTML**（site/ 是唯一真相）
- **繁體中文台灣用語**
- **改完後要跑 /build 更新 AI 檔案**

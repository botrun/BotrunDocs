---
name: update-content
description: "根據洞見的變更建議更新 content/ 的 Markdown 檔案。當需要「更新內容」「修改頁面」「套用變更建議」「編輯 content」時使用。讀取 insights/ 變更建議，逐一修改 content/*.md。"
---

# 更新 Final MD（Layer 3）

## 目的

根據 `insights/{日期}/變更建議.md` 逐一修改 `content/*.md`，這是**唯一的內容編輯點**。

## 執行步驟

### 1. 讀取變更建議

讀取最新的 `insights/{日期}/變更建議.md`，列出所有 `[ADD]`、`[UPDATE]`、`[REMOVE]` 項目。

### 2. 逐一執行變更

對每個變更建議：

#### [ADD] 新增內容
1. 讀取目標 `content/*.md`
2. 找到適合的插入位置
3. 寫入新內容
4. 更新 front-matter 的 `sources` 和 `last_updated`

#### [UPDATE] 更新內容
1. 讀取目標 `content/*.md`
2. 找到要更新的段落
3. 替換為新內容
4. 更新 front-matter

#### [REMOVE] 移除內容
1. 讀取目標 `content/*.md`
2. 刪除指定段落
3. 更新 front-matter

### 3. 更新管理檔案

每次修改完成後：
- `content/_registry.md` — 更新最後更新日期
- `content/_update-tracker.md` — 更新狀態和待處理清單
- `content/_user-questions.md` — 更新覆蓋狀態為 `✅`

### 4. 寫作規則

| 規則 | 正確 | 錯誤 |
|------|------|------|
| 場景導向 | 上傳 PDF，AI 幫你摘要和問答 | 支援 RAG 檢索增強生成 |
| 口語化 | 說話自動變文字 | 語音辨識轉錄功能 |
| 具體數據 | 外部 API 3 秒回應（ChatGPT 15 秒） | 效能優異 |
| 台灣用語 | 使用者、伺服器、智慧 | 用戶、服務器、智能 |

### 5. 產出摘要

```
✅ 內容更新完成：
   - [ADD] features/native.md: 新增精確時間功能
   - [UPDATE] faq/index.md: 更正 MCP 工具說明
   - [REMOVE] features/platform.md: 移除已下線的 XX
   - 提問覆蓋率：65% → 78%
   - 已更新 _registry.md, _update-tracker.md, _user-questions.md
```

## 規則

- **只根據變更建議修改**，不自行發揮
- **每次修改都更新 front-matter**
- **繁體中文台灣用語**
- **保持 Markdown 格式一致**

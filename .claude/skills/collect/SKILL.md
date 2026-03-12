---
name: collect
description: "採集 Botrun 原始資料到 raw-sources/。當需要「採集」「收集資料」「抓取來源」「更新原始資料」時使用。支援 git log、網頁擷取、Medium 文章、會議記錄等來源。"
---

# 採集原始資料（Layer 1）

## 目的

將各種來源的原始資料傾倒到 `raw-sources/{日期}/`，**不做任何判斷**。

## 執行步驟

### 1. 建立今日目錄

```
raw-sources/{YYYY-MM-DD}/
```

### 2. 確認採集範圍

先讀取 `content/_user-questions.md`，找出 `❌ 未覆蓋` 和 `⚠️ 部分` 的提問，決定本次要採集哪些來源。

### 3. 逐一採集來源

| 來源 | 採集方法 | 檔案名稱 |
|------|---------|---------|
| 前台 Git | 讀取 `/Users/chenwei/Documents/GitHub/botrun_front`，執行 `git log --since="上次更新日期" --oneline` + 關鍵 diff | `git-front-log.md` |
| 後台 Git | 同上（如有後台 repo） | `git-back-log.md` |
| Medium | 用 WebSearch 搜尋 `site:medium.com botrun OR 波特人` 近期文章 | `medium-articles.md` |
| Botrun AI 回應 | 用 WebFetch 擷取 botrun.ai 頁面內容，或讀取已有的 AI 回應記錄 | `botrun-ai-response.md` |
| 官方網站 | 用 WebFetch 擷取 `intro.botrun.ai` 最新內容 | `official-site.md` |
| 人類回饋 | 詢問使用者是否有客戶對話、會議記錄、PM 回饋要加入 | `human-feedback.md` |

### 4. 採集格式

每個檔案的格式：

```markdown
# {來源名稱} — {日期}

> 採集時間：{timestamp}
> 採集範圍：{描述}
> 資料量：{估計}

---

{原始內容，保持原始結構，不做修改}
```

### 5. 產出清單

採集完成後，在終端輸出：

```
✅ 採集完成：raw-sources/{日期}/
   - git-front-log.md (XX KB)
   - medium-articles.md (XX KB)
   - ...
   共 N 個來源，覆蓋提問：Q1, Q5, Q12...
```

## 規則

- **絕不修改原始資料**：錯字、格式問題都保留
- **每個來源一個檔案**：不合併
- **標注採集時間和範圍**：方便追溯
- **使用者未提供的來源**：主動詢問，不要假設
- **本地暫存，不進 git**：`raw-sources/` 已在 `.gitignore`，可能含內部程式碼結構、API 路徑、會議記錄等敏感資料。永久紀錄靠 `updates/{日期}.md` 摘要保留

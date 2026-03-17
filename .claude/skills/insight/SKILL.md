---
name: insight
description: "整理洞見，將 raw-sources 原始資料轉化為變更建議。當需要「分析資料」「產出洞見」「比對差異」「變更建議」時使用。讀取 raw-sources + content，產出 insights/ 文件。"
---

# 洞見整理（Layer 2）

## 目的

讀取 `raw-sources/{日期}/` + 目前 `content/` + `content/_user-questions.md`，產出跨來源比對和變更建議到 `insights/{日期}/`。

## 執行步驟

### 1. 讀取輸入

依序讀取：
1. `content/_user-questions.md` — 確認哪些提問需要覆蓋
2. `content/_registry.md` — 目前有哪些頁面
3. 最新的 `raw-sources/{日期}/` — 全部檔案
4. 相關的 `content/*.md` — 目前內容

### 2. 產出三份文件

建立 `insights/{日期}/` 目錄，產出：

#### 2a. 跨來源比對.md

```markdown
# 跨來源比對 — {日期}

## 矛盾發現
| 議題 | 來源 A 說法 | 來源 B 說法 | 決策 | 理由 |
|------|------------|------------|------|------|
| ... | ... | ... | 以 A 為準 | ... |

## 互補發現
| 議題 | 來源 | 新資訊 | 可補充到 |
|------|------|--------|---------|
| ... | ... | ... | content/features/native.md |
```

#### 2b. 新舊差異.md

```markdown
# 新舊差異 — {日期}

## 新資料中 content/ 沒有的
| 項目 | 來源 | 重要性(1-10) | 建議處理 |
|------|------|-------------|---------|

## content/ 中已過時的
| 項目 | 所在頁面 | 過時原因 | 建議處理 |
|------|---------|---------|---------|
```

#### 2c. 變更建議.md（最重要）

```markdown
# 變更建議 — {日期}

## 變更清單

### [ADD] content/features/native.md — 新增 XX 功能說明
- 來源：raw-sources/{日期}/git-front-log.md
- 解決提問：Q3「波特人能不能 XX？」
- 具體內容：（寫出要新增的段落草稿）

### [UPDATE] content/faq/index.md — 更正 XX 資訊
- 來源：raw-sources/{日期}/botrun-ai-response.md
- 解決提問：Q7「XX 怎麼用？」
- 舊內容：（引用目前內容）
- 新內容：（寫出修改後的內容）

### [REMOVE] content/features/platform.md — 移除已下線功能
- 來源：raw-sources/{日期}/git-front-log.md
- 理由：（說明）
```

### 3. 更新提問覆蓋狀態

讀取 `content/_user-questions.md`：
- 從新來源發現的新提問 → 新增到列表
- 本次變更建議將覆蓋的提問 → 標注預計狀態

### 4. 產出摘要

```
✅ 洞見整理完成：insights/{日期}/
   - 跨來源比對：N 個矛盾、M 個互補
   - 新舊差異：N 個新項目、M 個過時項目
   - 變更建議：ADD x N、UPDATE x M、REMOVE x K
   - 預計提問覆蓋率：XX% → YY%
```

## 規則

- **每條變更建議必須對應一個使用者提問**
- **變更建議要寫出具體內容草稿**，不只是「建議新增」
- **用場景導向寫法**，不用功能導向
- **重要性排序**：`[客戶]` 標記的提問 > `❌ 未覆蓋` > `⚠️ 部分`
- **本地暫存，不進 git**：`insights/` 已在 `.gitignore`，可能引用內部敏感資訊。關鍵決策和變更理由必須摘要到 `updates/{日期}.md` 作為永久紀錄

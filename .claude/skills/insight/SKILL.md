---
name: insight
description: "整理洞見，將 raw-sources 原始資料轉化為變更建議。當需要「分析資料」「產出洞見」「比對差異」「變更建議」時使用。讀取 raw-sources + site/ HTML，產出 insights/ 文件。"
---

# 洞見整理（Layer 2）

## 目的

讀取 `raw-sources/{日期}/` + 目前 `site/*.html` + `_user-questions.md`，產出跨來源比對和變更建議到 `insights/{日期}/`。

## 執行步驟

### 1. 讀取輸入

依序讀取：
1. `_user-questions.md` — 確認哪些提問需要覆蓋
2. 最新的 `raw-sources/{日期}/` — 全部檔案
3. 相關的 `site/*.html` — 目前內容

### 2. 產出三份文件

建立 `insights/{日期}/` 目錄，產出：

#### 2a. 跨來源比對.md

不同來源的矛盾與互補發現。

#### 2b. 新舊差異.md

新資料中 site/ 沒有的、site/ 中已過時的。

#### 2c. 變更建議.md（最重要）

```markdown
# 變更建議 — {日期}

### [ADD] site/features/native.html — 新增 XX 功能說明
- 來源：raw-sources/{日期}/git-front-log.md
- 解決提問：Q3「波特人能不能 XX？」
- 具體內容：（寫出要新增的 HTML 段落草稿）

### [UPDATE] site/faq/index.html — 更正 XX 資訊
- 來源：raw-sources/{日期}/botrun-ai-response.md
- 解決提問：Q7「XX 怎麼用？」
- 具體內容：（寫出修改後的 HTML）
```

### 3. 更新提問覆蓋狀態

讀取 `_user-questions.md`：
- 從新來源發現的新提問 → 新增到列表
- 本次變更建議將覆蓋的提問 → 標注預計狀態

### 4. 產出摘要

```
✅ 洞見整理完成：insights/{日期}/
   - 變更建議：ADD x N、UPDATE x M、REMOVE x K
   - 預計提問覆蓋率：XX% → YY%
```

## 規則

- **每條變更建議必須對應一個使用者提問**
- **變更建議要寫出具體內容草稿**，不只是「建議新增」
- **用場景導向寫法**，不用功能導向
- **本地暫存，不進 git**

---
name: build
description: "從 content/ Markdown 生成 site/ HTML 頁面。當需要「建置」「生成 HTML」「build」「重新生成網站」時使用。執行 .claude/skills/build/scripts/build.py 將 content/*.md 轉換為 site/*.html + llms.txt + sitemap.xml。"
---

# 生成 HTML（Layer 4）

## 目的

執行 `.claude/skills/build/scripts/build.py`，將 `content/*.md` 轉換為 `site/*.html` + AI 友善檔案。

## 執行步驟

### 1. 檢查前置條件

確認 `content/` 中的 MD 檔案已更新（讀取 `content/_update-tracker.md` 確認狀態）。

### 2. 檢查新增頁面

如果有新增的 content/*.md 檔案，需要先更新 `.claude/skills/build/scripts/build.py`：

1. 在 `NAV_PAGES` 或 `SUB_PAGES` 中新增頁面定義
2. 如果是 features/ 子頁面，也要更新 `FEATURE_SIDEBAR`
3. 確認 front-matter 中有 `title`、`description`、`keywords`

### 3. 執行建置

```bash
cd /Users/chenwei/Documents/GitHub/BotrunDocs
python3 .claude/skills/build/scripts/build.py
```

### 4. 本地預覽

建置完成後，啟動本地伺服器讓使用者確認：

```bash
python3 -m http.server 8766 -d site
```

告知使用者：「本地預覽已啟動，請開啟 http://localhost:8766 確認內容。」

用 Playwright 截圖抽查 2-3 個頁面，確認：
1. **頁面正常渲染**
2. **連結正確**
3. **llms.txt 索引完整**

### 5. 產出摘要

```
✅ 建置完成（本地預覽中）：
   - 頁面：N 頁
   - llms.txt: OK
   - sitemap.xml: OK
   - robots.txt: OK
   - 總大小：XX KB
   - 預覽：http://localhost:8766
```

## 新增頁面的完整流程

如果 PM 要求新增一個頁面：

1. 在 `content/` 建立新的 .md 檔案（含 front-matter）
2. 在 `.claude/skills/build/scripts/build.py` 的 `NAV_PAGES` 或 `SUB_PAGES` 新增定義
3. 如果是 features/ 頁面，更新 `FEATURE_SIDEBAR`
4. 更新 `content/_registry.md`
5. 執行 `python3 .claude/skills/build/scripts/build.py`
6. 驗證產出

## 部署到 GCS

**預覽確認沒問題後**，詢問使用者：「內容確認 OK 嗎？要部署上線嗎？」

使用者確認後才執行：

```bash
gcloud storage rsync site gs://botrun-docs-site --recursive --delete-unmatched-destination-objects --project=scoop-386004
```

**部署權限：** 任何擁有 GCP 專案 `scoop-386004` 存取權限的公司員工帳號都可以部署。如果遇到權限問題，先執行 `gcloud auth login` 並確認 `gcloud config set project scoop-386004`。

部署後的公開網址：
- 首頁：`https://storage.googleapis.com/botrun-docs-site/index.html`
- llms.txt：`https://storage.googleapis.com/botrun-docs-site/llms.txt`

快取時間 1 小時，部署後最多 1 小時全球生效。

**絕對不要自動部署。流程是：建置 → 本地預覽 → 使用者確認 → 才部署。**

## 規則

- **永遠不直接編輯 site/*.html**
- **`.claude/skills/build/scripts/build.py` 是唯一的生成入口**
- **新頁面必須同時更新 build.py 和 _registry.md**

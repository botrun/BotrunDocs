---
name: build
description: "從 site/ HTML 讀取內容，產生 AI 友善檔案（llms.txt、llms-full.txt、sitemap.xml、robots.txt）。當需要「建置」「build」「更新 AI 檔案」「重新產生 llms.txt」時使用。"
---

# 產生 AI 友善檔案

## 目的

從 `site/*.html` 讀取內容，產生 `llms.txt`、`llms-full.txt`、`sitemap.xml`、`robots.txt`。

> **HTML 是唯一真相。** 此腳本不會生成或修改 HTML，只讀取 HTML 來產生 AI 索引檔案。

## 執行步驟

### 1. 執行腳本

```bash
cd /Users/chenwei/Documents/GitHub/BotrunDocs
python3 .claude/skills/build/scripts/build.py
```

### 2. 本地預覽

```bash
python3 -m http.server 8766 -d site
```

告知使用者：「本地預覽已啟動，請開啟 http://localhost:8766 確認內容。」

### 3. 產出摘要

```
✅ AI 檔案產生完成：
   - llms.txt: OK
   - llms-full.txt: XX KB
   - sitemap.xml: OK
   - robots.txt: OK
   - 預覽：http://localhost:8766
```

## 新增頁面的完整流程

如果要新增一個頁面：

1. 在 `site/` 建立新的 `.html` 檔案（複製現有頁面作為模板）
2. 在 `.claude/skills/build/scripts/build.py` 的 `NAV_PAGES` 或 `SUB_PAGES` 新增定義
3. 執行 `python3 .claude/skills/build/scripts/build.py`
4. 驗證 llms.txt 和 sitemap.xml 包含新頁面

## 部署到 GCS

**預覽確認沒問題後**，詢問使用者：「內容確認 OK 嗎？要部署上線嗎？」

使用者確認後才執行：

```bash
gcloud storage rsync site gs://botrun-docs-site --recursive --delete-unmatched-destination-objects --project=scoop-386004
```

**絕對不要自動部署。流程是：確認 HTML → 產生 AI 檔案 → 本地預覽 → 使用者確認 → 才部署。**

## 規則

- **直接編輯 site/*.html**（HTML 是唯一真相）
- **build.py 只產生 AI 索引檔案**，不會修改 HTML
- **新頁面必須同時更新 build.py 的 PAGES 定義**

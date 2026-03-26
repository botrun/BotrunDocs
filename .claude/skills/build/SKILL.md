---
name: build
description: "從 site/ HTML 讀取內容，產生 AI 友善檔案（llms.txt、llms-full.txt、sitemap.xml、robots.txt）。當需要「建置」「build」「更新 AI 檔案」「重新產生 llms.txt」時使用。"
---

# 產生 AI 友善檔案

## 目的

從 `site/*.html` 讀取內容，產生 `llms.txt`、`llms-full.txt`、`sitemap.xml`、`robots.txt`。

> **HTML 是唯一真相。** 此腳本不會生成或修改 HTML，只讀取 HTML 來產生 AI 索引檔案。

## 執行步驟

### 步驟一：自動化產生草稿（build.py）

```bash
cd /Users/chenwei/Documents/GitHub/BotrunDocs
python3 .claude/skills/build/scripts/build.py
```

build.py 負責的機械工作：
- sitemap.xml（URL、lastmod、changefreq）
- robots.txt（爬蟲規則）
- llms-full.txt（HTML → Markdown 轉換，含表格 Markdown 化、導航文字過濾）
- llms.txt **草稿**（從 meta description 抓取，作為 AI 潤飾的底稿）

### 步驟二：AI 潤飾 llms.txt（你來做）

這一步是 build 的核心價值。build.py 產生的 llms.txt 草稿是機械式的，你需要閱讀後潤飾。

**2a. 潤飾開頭摘要**

讀取 `site/llms.txt` 的前 5 行摘要，根據全站最新內容重寫。原則：
- 用對話語氣，像在回答「波特人是什麼？」
- 必須包含：品牌名（Botrun 波特人）、公司名（卡米爾）、核心價值（不寫程式建 Bot、知識庫問答、地端部署）
- 必須包含最具說服力的數據（例如「內政部導入後開發時間從兩天縮至三小時」）
- 控制在 3-5 行內

**2b. 潤飾每個頁面的描述**

逐一檢查每個 `- [頁面名](URL): 描述` 行。對每個描述：
- 不要照抄 meta description（那是給搜尋引擎的）
- 改寫成：「如果有人問 ___，這頁能回答」的角度
- 加入該頁最獨特的關鍵資訊（例如功能頁要列出核心功能名稱，FAQ 頁要點出最常被問的問題）
- 每個描述控制在 1-2 句

**2c. 檢查 llms-full.txt**

快速掃描 `site/llms-full.txt`，確認：
- 表格有正確轉成 Markdown 格式
- 沒有殘留的 UI 導航文字（← 返回、詳見、下一步 等）
- 外部連結（botrun.ai、intro.botrun.ai）有保留 URL

如有問題直接用 Edit 工具修正 llms-full.txt。

### 步驟三：產出摘要

```
AI 檔案產生完成：
   - llms.txt: OK（已潤飾）
   - llms-full.txt: XX KB（已檢查）
   - sitemap.xml: OK
   - robots.txt: OK
```

## 新增頁面的完整流程

如果要新增一個頁面：

1. 在 `site/` 建立新的 `.html` 檔案（複製現有頁面作為模板）
2. 在 `.claude/skills/build/scripts/build.py` 的 `NAV_PAGES` 或 `SUB_PAGES` 新增定義
3. 執行 `python3 .claude/skills/build/scripts/build.py`
4. 執行步驟二的 AI 潤飾
5. 驗證 llms.txt 和 sitemap.xml 包含新頁面

## 規則

- **直接編輯 site/*.html**（HTML 是唯一真相）
- **build.py 只產生機械式草稿**，AI 潤飾才是最終品質關鍵
- **新頁面必須同時更新 build.py 的 PAGES 定義**
- **絕對不要自動部署。** 流程是：確認 HTML → build → AI 潤飾 → 使用者確認 → 才部署

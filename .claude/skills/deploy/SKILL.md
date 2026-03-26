---
name: deploy
description: 部署 BotrunDocs 到 Firebase Hosting。當需要「部署」「deploy」「上線」「發布」時使用。自動處理 gcloud 身分驗證、build AI 檔案、Firebase 部署。
user_invocable: true
---

# 部署 BotrunDocs

## 前置條件

部署使用 Firebase Hosting，透過 gcloud ADC（Application Default Credentials）身分驗證。
**不需要 `firebase login`**，只需要 gcloud 登入即可。

### 首次設定（新電腦）

如果是第一次在這台電腦部署，需要先完成以下設定：

```bash
# 1. 登入 gcloud（會開瀏覽器）
gcloud auth login

# 2. 設定 Application Default Credentials
gcloud auth application-default login

# 3. 設定 quota project
gcloud auth application-default set-quota-project scoop-386004

# 4. 確認 Firebase 連線
firebase projects:list
```

看到 `scoop-386004 (scoop)` 就代表設定完成。

如果 `firebase projects:list` 出現 403 錯誤，通常是 quota project 沒設好，重新執行步驟 3。

如果需要將新成員加入專案：
```bash
gcloud projects add-iam-policy-binding scoop-386004 \
  --member="user:成員email@gmail.com" \
  --role="roles/firebasehosting.admin"
```

## 部署步驟

### 1. 產生 AI 檔案

```bash
python3 .claude/skills/build/scripts/build.py
```

確認輸出 4 個 AI 檔案（llms.txt、llms-full.txt、sitemap.xml、robots.txt）。

### 2. 本地預覽

```bash
python3 -m http.server 8766 -d site
```

告知使用者：「本地預覽已啟動，請開啟 http://localhost:8766 確認。」

### 3. 使用者確認後部署

**務必等使用者確認後才執行部署。**

```bash
firebase deploy --only hosting --project scoop-386004
```

### 4. 驗證部署結果

```bash
curl -s -o /dev/null -w "%{http_code}" https://docs.botrun.ai/
curl -s -o /dev/null -w "%{http_code}" https://docs.botrun.ai/llms.txt
curl -s -o /dev/null -w "%{http_code}" https://docs.botrun.ai/sitemap.xml
```

三個都要是 HTTP 200。

### 5. 產出摘要

```
✅ 部署完成：
   - 網址：https://docs.botrun.ai
   - 首頁：HTTP 200
   - llms.txt：HTTP 200
   - sitemap.xml：HTTP 200
   - 部署時間：{時間}
```

## 部署資訊

| 項目 | 值 |
|------|-----|
| Firebase 專案 | `scoop-386004` (scoop) |
| Hosting Site ID | `botrun-docs` |
| 網址 | https://docs.botrun.ai |
| Firebase URL | https://botrun-docs.web.app |
| 身分驗證 | gcloud ADC（不需要 firebase login） |
| 設定檔 | `firebase.json`、`.firebaserc` |

## 規則

- **絕對不要自動部署**，必須等使用者確認
- 部署前必須先執行 `/build` 產生最新的 AI 檔案
- 如果 gcloud 登入過期，引導使用者執行 `gcloud auth application-default login`

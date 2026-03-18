---
name: update-cycle
description: "執行完整的內容更新循環（採集→洞見→更新 HTML→產生 AI 檔案→提交→紀錄）。當需要「完整更新」「跑一輪更新」「update cycle」「更新流程」時使用。這是 orchestrator，會依序呼叫 collect → insight → update-content → build。"
---

# 完整更新循環（Orchestrator）

## 目的

協調三層管線的完整更新流程，確保每一步都正確執行並留下紀錄。

## 完整流程

```
⓪ 對照提問列表 → 確認本次方向
① /collect      → raw-sources/{日期}/
② /insight      → insights/{日期}/
③ /update-content → site/*.html 更新
④ /build        → llms.txt 等 AI 檔案重新產生
⑤ git commit    → 結構化訊息
⑥ 更新紀錄      → updates/{日期}.md
⑦ 驗證          → 確認品質
```

## 執行步驟

### Step ⓪：對照提問列表

1. 讀取 `_user-questions.md`
2. 統計目前覆蓋率
3. 列出 `❌ 未覆蓋` 和 `⚠️ 部分` 的提問
4. 詢問使用者：本次重點要覆蓋哪些？有新的來源嗎？

### Step ①：採集

執行 `/collect` skill 的流程。

### Step ②：洞見

執行 `/insight` skill 的流程。

產出後，**暫停讓使用者確認變更建議**：
- 列出所有 `[ADD]`、`[UPDATE]`、`[REMOVE]`
- 問使用者：「這些變更建議可以嗎？需要調整嗎？」

### Step ③：更新 HTML

使用者確認後，執行 `/update-content` skill 的流程。
直接修改 `site/*.html` 中的內容。

### Step ④：產生 AI 檔案與部署

執行 `/build` skill 的流程。

建置完成後詢問使用者是否要部署到 GCS：

```bash
gcloud storage rsync site gs://botrun-docs-site --recursive --delete-unmatched-destination-objects --project=scoop-386004
```

### Step ⑤：Git Commit

產出結構化 commit 訊息：

```
docs(update): {日期} 內容更新

變更摘要：
- [ADD] {頁面}: {說明}
- [UPDATE] {頁面}: {說明}

提問覆蓋率：{前}% → {後}%
資料來源：{來源類型列表，不含內部路徑}
```

**詢問使用者確認後再 commit。**

### Step ⑥：更新紀錄

建立 `updates/{日期}.md`。

### Step ⑦：驗證

1. 從提問列表挑 3-5 個已更新的提問
2. 模擬 AI 用 llms.txt + 頁面內容回答
3. 確認回答品質

## 中斷恢復

如果流程中斷：

1. 檢查 `raw-sources/` 和 `insights/` 最新日期目錄
2. 從中斷點繼續，不需要重頭來

## 規則

- **每步之間都要向使用者確認**（特別是 Step ② 的變更建議）
- **不要一口氣跑完不停**，PM 需要有機會審查
- **紀錄完整**：每次更新必須有 updates/{日期}.md

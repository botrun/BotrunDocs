---
name: update-cycle
description: "執行完整的內容更新循環（採集→洞見→更新→建置→提交→紀錄）。當需要「完整更新」「跑一輪更新」「update cycle」「更新流程」時使用。這是 orchestrator，會依序呼叫 collect → insight → update-content → build。"
---

# 完整更新循環（Orchestrator）

## 目的

協調四層管線的完整更新流程，確保每一步都正確執行並留下紀錄。

## 完整流程

```
⓪ 對照提問列表 → 確認本次方向
① /collect      → raw-sources/{日期}/
② /insight      → insights/{日期}/
③ /update-content → content/*.md 更新
④ /build        → site/ 重新生成
⑤ git commit    → 結構化訊息
⑥ 更新紀錄      → updates/{日期}.md
⑦ 驗證          → 確認品質
```

## 執行步驟

### Step ⓪：對照提問列表

1. 讀取 `content/_user-questions.md`
2. 統計目前覆蓋率
3. 列出 `❌ 未覆蓋` 和 `⚠️ 部分` 的提問
4. 詢問使用者：本次重點要覆蓋哪些？有新的來源嗎？

### Step ①：採集

執行 `/collect` skill 的流程。

如果使用者提供了特定來源（如檔案、網址、會議記錄），直接使用。
如果沒有，主動採集 git log + 官網 + Medium。

### Step ②：洞見

執行 `/insight` skill 的流程。

產出後，**暫停讓使用者確認變更建議**：
- 列出所有 `[ADD]`、`[UPDATE]`、`[REMOVE]`
- 問使用者：「這些變更建議可以嗎？需要調整嗎？」

### Step ③：更新內容

使用者確認後，執行 `/update-content` skill 的流程。

### Step ④：建置與部署

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

**注意：commit 訊息中不可包含 raw-sources/ 或 insights/ 的檔案路徑（已 gitignore，且可能含敏感資訊）。只描述來源類型（如「前台 git log」「官網擷取」），不寫內部路徑。**

**詢問使用者確認後再 commit。**

### Step ⑥：更新紀錄

建立 `updates/{日期}.md`。

**重要：raw-sources/ 和 insights/ 不進 git，所以 updates/ 是唯一的永久紀錄。必須包含足夠的上下文，讓未來的人不需要原始檔案也能理解本次更新。**

內容：

```markdown
# 更新紀錄：{日期}

## 本次摘要
{一段話描述這次更新了什麼}

## 提問覆蓋率變化
{前}% → {後}%
新覆蓋的提問：
- Q{N}：{提問內容}
- ...

## 採集來源
{列出來源類型和範圍，不含敏感路徑}
- 前台 git log（{起迄日期}，{N} 筆 commit）
- 官網擷取（intro.botrun.ai）
- ...

## 關鍵決策
{跨來源比對中的矛盾如何解決、為什麼選擇這個方案}
- 決策 1：{描述} → 以 {來源} 為準，因為 {理由}
- ...

## Final MD 變更
- [ADD] {頁面}: {說明}
- [UPDATE] {頁面}: {說明}
- [REMOVE] {頁面}: {說明}

## 待下次更新
{未完成項目}
```

### Step ⑦：驗證

1. 從提問列表挑 3-5 個已更新的提問
2. 模擬 AI 用 llms.txt + 頁面內容回答
3. 確認回答品質

## 快速模式

如果使用者說「快速更新」或只提供一個來源：

1. 跳過 Step ⓪（不需要完整對照）
2. Step ① 只採集指定來源
3. Step ② 直接產出變更建議（不需完整比對）
4. Step ③④⑤⑥⑦ 正常執行

## 中斷恢復

如果流程中斷：

1. 讀取 `content/_update-tracker.md` 確認上次進度
2. 檢查 `raw-sources/` 和 `insights/` 最新日期目錄
3. 從中斷點繼續，不需要重頭來

## 規則

- **每步之間都要向使用者確認**（特別是 Step ② 的變更建議）
- **不要一口氣跑完不停**，PM 需要有機會審查
- **紀錄完整**：每次更新必須有 updates/{日期}.md

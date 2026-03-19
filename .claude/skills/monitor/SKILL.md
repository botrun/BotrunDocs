---
name: monitor
description: 監控 BotrunDocs 是否能被 AI Agent 搜尋到。執行基礎設施檢查 + AI 搜尋引擎實測。當需要「監控」「檢查可見性」「能不能搜尋到」「monitor」時使用。
user_invocable: true
---

# AI 可見性監控

## 目的

檢查 BotrunDocs 網站是否能被 AI Agent 發現與搜尋到。分兩階段：
1. **基礎設施檢查**（shell 腳本）：HTTP 可存取性、檔案內容、結構化資料、Google 收錄
2. **AI 搜尋實測**（Claude WebSearch）：模擬 AI Agent 搜尋，驗證是否出現在結果中

## 執行步驟

### 階段一：執行基礎設施監控腳本

```bash
bash /Users/chenwei/Documents/GitHub/BotrunDocs/scripts/monitor-ai-visibility.sh
```

讀取並顯示腳本輸出結果。

### 階段二：AI 搜尋引擎實測

用 WebSearch 工具對以下 4 個關鍵字逐一搜尋，**平行執行**：

1. 「Botrun 是什麼」
2. 「波特人 AI 平台」
3. 「台灣 AI Bot 建立平台」
4. 「botrun.ai 功能」

對每個搜尋結果，判斷：
- **是否出現 Botrun 品牌**（botrun.ai、intro.botrun.ai、Medium 文章等）
- **是否出現 BotrunDocs**（`storage.googleapis.com/botrun-docs-site` 或 `docs.botrun.ai`）

### 階段三：產出報告

用以下格式輸出報告：

```
## AI 搜尋實測報告（{日期}）

| 查詢 | Botrun 品牌 | BotrunDocs 文件站 | 來源 |
|------|:-----------:|:----------------:|------|
| ... | ✅/❌ | ✅/❌ | 來源列表 |

### 結論
- Botrun 品牌可見度：X/4
- BotrunDocs 文件站收錄：X/4
- 與上次比較：改善/持平/退步

### 建議行動
（根據結果列出具體下一步）
```

將報告追加寫入 `scripts/monitor-logs/search-test-{YYYY-MM-DD}.md`。

## 規則

- 每個搜尋結果都要列出實際來源 URL
- 不要猜測，只根據搜尋結果判斷
- 如果 BotrunDocs 未被收錄，在建議行動中提醒提交 sitemap

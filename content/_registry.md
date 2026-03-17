# 內容登錄表

> 此檔案記錄所有 content/*.md 的後設資料，作為管線的「目錄索引」。

---

## 頁面清單

| MD 檔案 | 對應 HTML | 主要資料來源 | 最後更新 | 狀態 |
|---------|----------|-------------|---------|------|
| content/index.md | site/index.html | intro.botrun.ai + git + Medium | 2026-03-11 | 已加入效能數據、TAIDE、政府案例 |
| content/features/index.md | site/features/index.html | git + Medium | 2026-03-11 | 已加入知識圖譜、.botrun 編譯、效能、Data as Agents |
| content/faq/index.md | site/faq/index.html | git + intro.botrun.ai + Medium | 2026-03-11 | 16 題 FAQ（+知識圖譜/TAIDE/.botrun） |
| content/getting-started/index.md | site/getting-started/index.html | Google Chat MCP（團隊內部討論、客戶導入實戰） | 2026-03-11 | 波特人導入之旅：高品味題庫、黑客松、教育訓練、真實案例 |

## 待建立頁面

| MD 檔案 | 對應 HTML | 預計來源 | 預計階段 |
|---------|----------|---------|---------|
| content/features/chat.md | site/features/chat.html | botrun_front git | Phase 3 |
| content/features/hatcher.md | site/features/hatcher.html | botrun_front git | Phase 3 |
| content/technical/index.md | site/technical/index.html | Medium + git | Phase 3 |

## 資料來源 → 頁面對應

| 資料來源 | 影響的頁面 |
|---------|----------|
| intro.botrun.ai（公司、獲獎、聯絡） | index.md |
| intro.botrun.ai /solution-list.html（案例） | index.md |
| intro.botrun.ai /faqs.html（基礎 Q&A） | faq/index.md |
| botrun_front git — 路由/元件/API | features/index.md, index.md |
| botrun_front git — Hatcher 型別定義 | features/index.md |
| botrun_front git — 認證/安全 | features/index.md, faq/index.md |
| botrun_front git — MCP/多代理 | features/index.md, faq/index.md |
| botrun_front git — 語音模型 | features/index.md, faq/index.md |
| 技術長 Medium（效能/知識圖譜/TAIDE/.botrun/政府案例） | index.md, features/index.md, faq/index.md |
| Google Chat MCP（團隊內部討論） | getting-started/index.md, faq/index.md |
| 共學會議（波雀雀頻道） | 待採集 → features/index.md |

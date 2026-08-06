## AI 搜尋實測報告（2026-03-24）

### 基礎設施檢查

通過 16 項 / 失敗 0 項 / 警告 1 項

- HTTP 端點全部正常（首頁、llms.txt、llms-full.txt、robots.txt、sitemap.xml 皆 200）
- Schema.org JSON-LD、Open Graph、meta description 皆存在
- Google 已收錄 docs.botrun.ai 及 botrun.ai 主站
- 警告：llms.txt 本地與線上版本不一致，需重新部署

### AI 搜尋引擎實測

| 查詢 | Botrun 品牌 | BotrunDocs 文件站 | 來源 |
|------|:-----------:|:----------------:|------|
| Botrun 是什麼 | V | X | botrun.ai、intro.botrun.ai、Medium CTO 文章 |
| 波特人 AI 平台 | V | X | intro.botrun.ai、intro.botrun.ai/about、痞客邦文章 |
| 台灣 AI Bot 建立平台 | X | X | 無任何 Botrun 相關結果 |
| botrun.ai 功能 | V | X | intro.botrun.ai、dev.botrun.ai、epb.botrun.ai、hd.botrun.ai、Medium CTO 文章 |

### 結論

- Botrun 品牌可見度：3/4
- BotrunDocs 文件站收錄：0/4
- docs.botrun.ai 在所有搜尋中完全未出現

### 建議行動

1. 立即重新部署（llms.txt 本地與線上不一致）
2. 提交 Sitemap 到 Google Search Console，確認 https://docs.botrun.ai/sitemap.xml 已提交
3. 從 intro.botrun.ai、botrun.github.io 加上指向 docs.botrun.ai 的反向連結
4. 在 CTO Medium 文章中引用 docs.botrun.ai
5. 強化通用關鍵字覆蓋（台灣 AI Bot 建立平台等）

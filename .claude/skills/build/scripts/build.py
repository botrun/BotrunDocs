#!/usr/bin/env python3
"""
BotrunDocs AI 檔案產生腳本
從 site/*.html 讀取內容，產生 llms.txt、llms-full.txt、sitemap.xml、robots.txt
（HTML 是唯一真相，不再從 Markdown 生成）
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path
from html.parser import HTMLParser

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
SITE_DIR = BASE_DIR / "site"
DOMAIN = "https://docs.botrun.ai"

# 頁面定義：(site 路徑, 導航標題)
NAV_PAGES = [
    ("index.html", "首頁"),
    ("features/index.html", "功能"),
    ("getting-started/index.html", "導入指南"),
    ("faq/index.html", "FAQ"),
]

SUB_PAGES = [
    ("features/native.html", "原生波特人"),
    ("features/hatcher.html", "孵化器"),
    ("features/platform.html", "平台能力"),
    ("getting-started/knowledge-base.html", "高品味題庫"),
    ("getting-started/hackathon.html", "黑客松實作"),
    ("getting-started/training.html", "教育訓練與優化"),
    ("faq/advanced.html", "功能與技術"),
]

PAGES = NAV_PAGES + SUB_PAGES

# 英文頁面定義
EN_NAV_PAGES = [
    ("en/index.html", "Home"),
    ("en/features/index.html", "Features"),
    ("en/getting-started/index.html", "Getting Started"),
    ("en/faq/index.html", "FAQ"),
]

EN_SUB_PAGES = [
    ("en/features/native.html", "Native Botrun"),
    ("en/features/hatcher.html", "Hatcher (Bot Builder)"),
    ("en/features/platform.html", "Platform Capabilities"),
    ("en/getting-started/knowledge-base.html", "Quality Question Bank"),
    ("en/getting-started/hackathon.html", "Hackathon"),
    ("en/getting-started/training.html", "Training & Optimization"),
    ("en/faq/advanced.html", "Features & Technical"),
]

EN_PAGES = EN_NAV_PAGES + EN_SUB_PAGES

ALL_PAGES = PAGES + EN_PAGES

# 中英文頁面對應（用於 sitemap hreflang）
def get_lang_pair(site_path):
    """回傳 (zh_path, en_path) 對應"""
    if site_path.startswith("en/"):
        zh_path = site_path[3:]  # 去掉 en/ 前綴
        return zh_path, site_path
    else:
        en_path = f"en/{site_path}"
        return site_path, en_path


class HTMLTextExtractor(HTMLParser):
    """從 HTML 中擷取純文字內容（含表格 Markdown 化）"""

    def __init__(self):
        super().__init__()
        self.in_main = False
        self.in_title = False
        self.skip_tags = {"script", "style", "nav"}
        self.skip_depth = 0
        self.main_text = []
        self.title = ""
        self.description = ""
        # 表格狀態
        self.in_table = False
        self.table_rows = []
        self.current_row = []
        self.current_cell = []
        self.in_thead = False
        self.header_row_count = 0
        # 連結狀態
        self.current_href = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "main":
            self.in_main = True
        elif tag == "title":
            self.in_title = True
        elif tag == "meta" and attrs_dict.get("name") == "description":
            self.description = attrs_dict.get("content", "")
        elif tag in self.skip_tags:
            self.skip_depth += 1

        if not self.in_main or self.skip_depth > 0:
            return

        # 表格處理
        if tag == "table":
            self.in_table = True
            self.table_rows = []
            self.header_row_count = 0
            return
        if self.in_table:
            if tag == "thead":
                self.in_thead = True
            elif tag == "tr":
                self.current_row = []
            elif tag in ("th", "td"):
                self.current_cell = []
            return

        # 一般內容
        if tag in ("h1", "h2", "h3", "h4", "p", "li", "br", "hr"):
            self.main_text.append("\n")
        if tag in ("h1", "h2", "h3"):
            self.main_text.append(f"{'#' * int(tag[1])} ")
        if tag == "a":
            self.current_href = attrs_dict.get("href", "")

    def handle_endtag(self, tag):
        if tag == "main":
            self.in_main = False
        elif tag == "title":
            self.in_title = False
        elif tag in self.skip_tags:
            self.skip_depth -= 1

        if not self.in_main or self.skip_depth > 0:
            return

        # 表格結束處理
        if self.in_table:
            if tag in ("th", "td"):
                self.current_row.append("".join(self.current_cell).strip())
            elif tag == "tr":
                if self.current_row:
                    self.table_rows.append(self.current_row)
                    if self.in_thead:
                        self.header_row_count += 1
            elif tag == "thead":
                self.in_thead = False
            elif tag == "table":
                self.in_table = False
                self._flush_table()
            return

        # 連結結束
        if tag == "a" and self.current_href:
            # 只保留外部連結，過濾掉站內導航
            href = self.current_href
            if href.startswith("http") and "docs.botrun.ai" not in href:
                self.main_text.append(f" ({href})")
            self.current_href = ""

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if not self.in_main or self.skip_depth > 0:
            return
        if self.in_table:
            self.current_cell.append(data)
        else:
            # 過濾導航文字（中文「← 返回XXX」或英文「← Back to」）
            stripped = data.strip()
            if stripped.startswith("← 返回") or stripped == "←":
                return
            if stripped.startswith("返回") and stripped.endswith("總覽"):
                return
            if stripped.startswith("返回") and stripped.endswith("問答"):
                return
            if stripped.startswith("← Back") or stripped.startswith("Back to"):
                return
            self.main_text.append(data)

    def _flush_table(self):
        """將表格轉為 Markdown 表格格式"""
        if not self.table_rows:
            return
        # 計算欄寬
        col_count = max(len(row) for row in self.table_rows)
        # 補齊不足欄數
        for row in self.table_rows:
            while len(row) < col_count:
                row.append("")

        self.main_text.append("\n")
        # 輸出表頭
        header = self.table_rows[0]
        self.main_text.append("| " + " | ".join(header) + " |\n")
        self.main_text.append("| " + " | ".join("---" for _ in header) + " |\n")
        # 輸出資料行（跳過已當表頭的行）
        start = self.header_row_count if self.header_row_count > 0 else 1
        for row in self.table_rows[start:]:
            self.main_text.append("| " + " | ".join(row) + " |\n")
        self.main_text.append("\n")

    def get_text(self):
        text = "".join(self.main_text)
        # 清理多餘空白和換行
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()


def extract_page_info(html_path: Path) -> dict:
    """從 HTML 檔案中擷取標題、描述、純文字內容"""
    html = html_path.read_text(encoding="utf-8")
    parser = HTMLTextExtractor()
    parser.feed(html)
    return {
        "title": parser.title.strip(),
        "description": parser.description.strip(),
        "text": parser.get_text(),
    }


def build_llms_txt() -> str:
    """產生 llms.txt（AI Agent 索引）"""
    lines = [
        "# Botrun 波特人",
        "",
        "> Botrun 波特人是台灣卡米爾公司開發的 AI 平台。",
        "> 上傳 PDF 建立知識庫問答、不寫程式建立自訂 Bot、支援地端部署。",
        "> 政府部會（內政部、數位部、法務部）與企業已導入使用。",
        "",
        "## 頁面索引",
        "",
    ]
    for site_path, label in PAGES:
        url = DOMAIN if site_path == "index.html" else f"{DOMAIN}/{site_path}"
        html_file = SITE_DIR / site_path
        if html_file.exists():
            info = extract_page_info(html_file)
            desc = info["description"]
            lines.append(f"- [{label}]({url}): {desc}")

    # 英文頁面索引
    lines.extend(["", "## English Pages", ""])
    for site_path, label in EN_PAGES:
        url = f"{DOMAIN}/en/" if site_path == "en/index.html" else f"{DOMAIN}/{site_path}"
        html_file = SITE_DIR / site_path
        if html_file.exists():
            info = extract_page_info(html_file)
            desc = info["description"]
            lines.append(f"- [{label}]({url}): {desc}")

    lines.extend([
        "",
        "## 聯絡",
        "",
        "- 服務平台：https://botrun.ai",
        "- 公司官網：https://intro.botrun.ai",
        "- Email：service@cameo.tw",
        "- 電話：02-2912-5028",
    ])

    return "\n".join(lines)


def build_llms_full_txt() -> str:
    """產生 llms-full.txt（完整內容，AI Agent 一次讀完整站）"""
    lines = [
        "# Botrun 波特人 — 完整文件",
        "",
        "> Botrun 波特人是台灣卡米爾公司開發的 AI 平台。",
        "> 上傳 PDF 建立知識庫問答、不寫程式建立自訂 Bot、支援地端部署。",
        "> 政府部會（內政部、數位部、法務部）與企業已導入使用。",
        "",
    ]

    for site_path, label in PAGES:
        html_file = SITE_DIR / site_path
        if not html_file.exists():
            continue
        info = extract_page_info(html_file)
        url = DOMAIN if site_path == "index.html" else f"{DOMAIN}/{site_path}"
        lines.append("---")
        lines.append("")
        lines.append(f"## {label}")
        lines.append(f"URL: {url}")
        lines.append("")
        lines.append(info["text"])
        lines.append("")

    # 英文頁面
    lines.append("---")
    lines.append("")
    lines.append("# English Version")
    lines.append("")

    for site_path, label in EN_PAGES:
        html_file = SITE_DIR / site_path
        if not html_file.exists():
            continue
        info = extract_page_info(html_file)
        url = f"{DOMAIN}/en/" if site_path == "en/index.html" else f"{DOMAIN}/{site_path}"
        lines.append("---")
        lines.append("")
        lines.append(f"## {label}")
        lines.append(f"URL: {url}")
        lines.append("")
        lines.append(info["text"])
        lines.append("")

    lines.extend([
        "---",
        "",
        "## 聯絡 / Contact",
        "",
        "- 服務平台 / Platform：https://botrun.ai",
        "- 公司官網 / Official Site：https://intro.botrun.ai",
        "- Email：service@cameo.tw",
        "- 電話 / Phone：02-2912-5028",
    ])

    return "\n".join(lines)


def build_sitemap() -> str:
    """產生 sitemap.xml（含雙語 hreflang）"""
    today = datetime.now().strftime('%Y-%m-%d')
    urls = []

    for site_path, _ in ALL_PAGES:
        is_en = site_path.startswith("en/")
        if site_path == "index.html":
            url = DOMAIN
        elif site_path == "en/index.html":
            url = f"{DOMAIN}/en/"
        else:
            url = f"{DOMAIN}/{site_path}"

        # 決定 priority
        if site_path in ("index.html",):
            priority = "1.0"
        elif site_path in ("en/index.html",):
            priority = "0.9"
        elif is_en:
            priority = "0.7"
        else:
            priority = "0.8"

        # 取得對應的中英文 URL
        zh_path, en_path = get_lang_pair(site_path)
        zh_url = DOMAIN if zh_path == "index.html" else f"{DOMAIN}/{zh_path}"
        en_url = f"{DOMAIN}/en/" if en_path == "en/index.html" else f"{DOMAIN}/{en_path}"

        urls.append(
            f"  <url>\n"
            f"    <loc>{url}</loc>\n"
            f'    <xhtml:link rel="alternate" hreflang="zh-TW" href="{zh_url}"/>\n'
            f'    <xhtml:link rel="alternate" hreflang="en" href="{en_url}"/>\n'
            f"    <lastmod>{today}</lastmod>\n"
            f"    <changefreq>weekly</changefreq>\n"
            f"    <priority>{priority}</priority>\n"
            f"  </url>"
        )

    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(urls) + "\n"
        "</urlset>"
    )


def build_robots() -> str:
    """產生 robots.txt"""
    return (
        "User-agent: *\n"
        "Allow: /\n"
        f"Sitemap: {DOMAIN}/sitemap.xml\n"
        f"Llms-Txt: {DOMAIN}/llms.txt\n"
    )


def main():
    print("=== BotrunDocs AI 檔案產生 ===\n")

    # 確認 site/ 存在
    if not SITE_DIR.exists():
        print("❌ site/ 目錄不存在")
        return

    # 檢查頁面
    missing = []
    for site_path, label in ALL_PAGES:
        if not (SITE_DIR / site_path).exists():
            missing.append(site_path)
    if missing:
        print(f"  ⚠️ 缺少頁面：{', '.join(missing)}")

    # 產生 AI 友善檔案
    llms_txt = build_llms_txt()
    (SITE_DIR / "llms.txt").write_text(llms_txt, encoding="utf-8")
    print(f"  ✅ llms.txt")

    llms_full_txt = build_llms_full_txt()
    (SITE_DIR / "llms-full.txt").write_text(llms_full_txt, encoding="utf-8")
    size_kb = len(llms_full_txt.encode("utf-8")) / 1024
    print(f"  ✅ llms-full.txt ({size_kb:.1f} KB)")

    sitemap = build_sitemap()
    (SITE_DIR / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print(f"  ✅ sitemap.xml")

    robots = build_robots()
    (SITE_DIR / "robots.txt").write_text(robots, encoding="utf-8")
    print(f"  ✅ robots.txt")

    print(f"\n=== 完成：{len(ALL_PAGES) - len(missing)} 頁讀取（中文 {len(PAGES)} + 英文 {len(EN_PAGES)}）+ 4 個 AI 檔案產生 ===")


if __name__ == "__main__":
    main()

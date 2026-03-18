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


class HTMLTextExtractor(HTMLParser):
    """從 HTML 中擷取純文字內容"""

    def __init__(self):
        super().__init__()
        self.in_main = False
        self.in_title = False
        self.in_meta_desc = False
        self.skip_tags = {"script", "style", "nav"}
        self.skip_depth = 0
        self.main_text = []
        self.title = ""
        self.description = ""

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
        # 加入換行標記
        if self.in_main and self.skip_depth == 0:
            if tag in ("h1", "h2", "h3", "h4", "p", "li", "tr", "br", "hr"):
                self.main_text.append("\n")
            if tag in ("h1", "h2", "h3"):
                self.main_text.append(f"{'#' * int(tag[1])} ")

    def handle_endtag(self, tag):
        if tag == "main":
            self.in_main = False
        elif tag == "title":
            self.in_title = False
        elif tag in self.skip_tags:
            self.skip_depth -= 1

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_main and self.skip_depth == 0:
            self.main_text.append(data)

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
        "> Botrun 波特人是台灣卡米爾公司開發的企業 AI 平台。",
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
        "> Botrun 波特人是台灣卡米爾公司開發的企業 AI 平台。",
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

    lines.extend([
        "---",
        "",
        "## 聯絡",
        "",
        "- 服務平台：https://botrun.ai",
        "- 公司官網：https://intro.botrun.ai",
        "- Email：service@cameo.tw",
        "- 電話：02-2912-5028",
    ])

    return "\n".join(lines)


def build_sitemap() -> str:
    """產生 sitemap.xml"""
    urls = []
    for site_path, _ in PAGES:
        url = DOMAIN if site_path == "index.html" else f"{DOMAIN}/{site_path}"
        priority = "1.0" if site_path == "index.html" else "0.8"
        urls.append(
            f"  <url>\n"
            f"    <loc>{url}</loc>\n"
            f"    <lastmod>{datetime.now().strftime('%Y-%m-%d')}</lastmod>\n"
            f"    <priority>{priority}</priority>\n"
            f"  </url>"
        )

    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
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
    for site_path, label in PAGES:
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

    print(f"\n=== 完成：{len(PAGES) - len(missing)} 頁讀取 + 4 個 AI 檔案產生 ===")


if __name__ == "__main__":
    main()

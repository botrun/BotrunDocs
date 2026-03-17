#!/usr/bin/env python3
"""
BotrunDocs 建置腳本
將 content/*.md 轉換為 site/*.html（純靜態，AI 爬蟲 100% 可讀）
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path

import markdown

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent.parent
CONTENT_DIR = BASE_DIR / "content"
SITE_DIR = BASE_DIR / "site"
DOMAIN = "https://docs.botrun.ai"

# 頁面定義：(content 路徑, site 路徑, 導航標題)
# 主導航頁面
NAV_PAGES = [
    ("index.md", "index.html", "首頁"),
    ("features/index.md", "features/index.html", "功能"),
    ("getting-started/index.md", "getting-started/index.html", "導入指南"),
    ("faq/index.md", "faq/index.html", "FAQ"),
]

# 子頁面（不出現在主導航列，但會生成 HTML）
SUB_PAGES = [
    ("features/native.md", "features/native.html", "原生波特人"),
    ("features/hatcher.md", "features/hatcher.html", "孵化器"),
    ("features/platform.md", "features/platform.html", "平台能力"),
    ("getting-started/knowledge-base.md", "getting-started/knowledge-base.html", "高品味題庫"),
    ("getting-started/hackathon.md", "getting-started/hackathon.html", "黑客松實作"),
    ("getting-started/training.md", "getting-started/training.html", "教育訓練與優化"),
    ("faq/advanced.md", "faq/advanced.html", "功能與技術"),
]

PAGES = NAV_PAGES + SUB_PAGES

# 功能側邊欄定義：(site 路徑, 標題, 分組標籤)
FEATURE_SIDEBAR = [
    ("features/index.html", "功能總覽", None),
    ("features/native.html", "原生波特人", None),
    ("features/hatcher.html", "孵化器（Hatcher）", None),
    ("features/platform.html", "平台能力", None),
]

# 導入指南側邊欄定義
GUIDE_SIDEBAR = [
    ("getting-started/index.html", "導入總覽", None),
    ("getting-started/knowledge-base.html", "高品味題庫", None),
    ("getting-started/hackathon.html", "黑客松實作", None),
    ("getting-started/training.html", "教育訓練與優化", None),
]

# FAQ 側邊欄定義
FAQ_SIDEBAR = [
    ("faq/index.html", "常見問答", None),
    ("faq/advanced.html", "功能與技術", None),
]


def parse_frontmatter(text: str) -> tuple:
    """拆分 YAML frontmatter 和 markdown 內容"""
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            meta = {}
            for line in parts[1].strip().split("\n"):
                if ":" in line and not line.startswith(" ") and not line.startswith("-"):
                    key, val = line.split(":", 1)
                    meta[key.strip()] = val.strip().strip('"')
            return meta, parts[2].strip()
    return {}, text


def md_to_html(md_text: str) -> str:
    """將 markdown 轉為 HTML"""
    return markdown.markdown(
        md_text,
        extensions=["tables", "fenced_code", "toc"],
        extension_configs={"toc": {"permalink": False}},
    )


def get_nav_html(current_path: str) -> str:
    """產生導航列 HTML"""
    items = []
    for _, site_path, label in NAV_PAGES:
        # 計算相對路徑
        current_depth = current_path.count("/")
        prefix = "../" * current_depth if current_depth > 0 else ""
        href = f"{prefix}{site_path}" if site_path != "index.html" else f"{prefix}index.html"

        active = " class=\"active\"" if site_path == current_path else ""
        items.append(f'<a href="{href}"{active}>{label}</a>')

    return "\n        ".join(items)


def get_sidebar_html(current_path: str) -> str:
    """產生側邊欄 HTML（功能頁、導入指南頁或 FAQ 頁）"""
    if current_path.startswith("getting-started/"):
        sidebar_items = GUIDE_SIDEBAR
    elif current_path.startswith("faq/"):
        sidebar_items = FAQ_SIDEBAR
    else:
        sidebar_items = FEATURE_SIDEBAR
    items = []
    last_group = None
    for site_path, label, group in sidebar_items:
        # 分組標題
        if group and group != last_group:
            items.append(f'<div class="sidebar-group">{group}</div>')
            last_group = group
        active = ' class="active"' if site_path == current_path else ""
        # 同層級相對路徑
        filename = site_path.split("/")[-1]
        items.append(f'<a href="{filename}"{active}>{label}</a>')
    return "\n      ".join(items)


def has_sidebar_page(site_path: str) -> bool:
    """判斷是否需要側邊欄"""
    return site_path.startswith("features/") or site_path.startswith("getting-started/") or site_path.startswith("faq/")


def build_schema(meta: dict, page_path: str) -> str:
    """產生 Schema.org JSON-LD"""
    schema_type = meta.get("schema_type", "WebPage")
    first_type = schema_type.split(",")[0].strip()

    schema = {
        "@context": "https://schema.org",
        "@type": first_type,
        "name": meta.get("title", "Botrun 波特人"),
        "description": meta.get("description", ""),
        "url": f"{DOMAIN}/{page_path}" if page_path != "index.html" else DOMAIN,
        "inLanguage": "zh-TW",
        "dateModified": meta.get("last_updated", datetime.now().strftime("%Y-%m-%d")),
    }

    if first_type == "SoftwareApplication":
        schema["applicationCategory"] = "BusinessApplication"
        schema["operatingSystem"] = "Web"
        schema["offers"] = {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "TWD",
            "description": "免費試用 1 個月",
        }

    if first_type == "Organization":
        schema["legalName"] = "卡米爾股份有限公司"
        schema["alternateName"] = "CAMEO INC."

    return json.dumps(schema, ensure_ascii=False, indent=2)


def render_page(meta: dict, body_html: str, site_path: str) -> str:
    """渲染完整 HTML 頁面"""
    title = meta.get("title", "Botrun 波特人")
    description = meta.get("description", "")
    keywords = meta.get("keywords", "Botrun, 波特人")
    schema_json = build_schema(meta, site_path)
    nav_html = get_nav_html(site_path)
    has_sidebar = has_sidebar_page(site_path)

    # canonical URL
    canonical = DOMAIN if site_path == "index.html" else f"{DOMAIN}/{site_path}"

    # 側邊欄 CSS（僅功能頁面）
    sidebar_css = ""
    if has_sidebar:
        sidebar_css = """
    /* 文件佈局：側邊欄 + 內容 */
    .docs-layout {
      display: flex;
      max-width: 1100px;
      margin: 0 auto;
      gap: 0;
    }
    .sidebar {
      width: 220px;
      min-width: 220px;
      position: sticky;
      top: 52px;
      height: calc(100vh - 52px);
      overflow-y: auto;
      border-right: 1px solid var(--border);
      padding: 1.5rem 0;
      background: var(--bg);
    }
    .sidebar a {
      display: block;
      padding: 0.4rem 1.25rem;
      color: var(--text-muted);
      text-decoration: none;
      font-size: 0.88rem;
      border-left: 3px solid transparent;
      transition: all 0.15s;
    }
    .sidebar a:hover {
      color: var(--text);
      background: var(--bg-card);
      text-decoration: none;
    }
    .sidebar a.active {
      color: var(--accent);
      border-left-color: var(--accent);
      background: rgba(56, 189, 248, 0.08);
      font-weight: 500;
    }
    .docs-layout main {
      flex: 1;
      min-width: 0;
      max-width: none;
      padding: 2rem 2.5rem 4rem;
    }
    .docs-layout + footer {
      max-width: 1100px;
    }

    /* 手機版側邊欄 */
    .sidebar-toggle {
      display: none;
      position: fixed;
      bottom: 1.5rem;
      right: 1.5rem;
      z-index: 200;
      width: 48px;
      height: 48px;
      border-radius: 50%;
      background: var(--accent);
      color: var(--bg);
      border: none;
      font-size: 1.3rem;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }
    @media (max-width: 768px) {
      .docs-layout { flex-direction: column; }
      .sidebar {
        position: fixed;
        top: 52px;
        left: 0;
        width: 260px;
        height: calc(100vh - 52px);
        z-index: 150;
        transform: translateX(-100%);
        transition: transform 0.25s ease;
        box-shadow: 4px 0 20px rgba(0,0,0,0.5);
      }
      .sidebar.open { transform: translateX(0); }
      .sidebar-overlay {
        display: none;
        position: fixed;
        top: 52px;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.5);
        z-index: 140;
      }
      .sidebar-overlay.open { display: block; }
      .sidebar-toggle { display: flex; align-items: center; justify-content: center; }
      .docs-layout main { padding: 1.5rem 1rem 4rem; }
    }"""

    # 側邊欄 HTML
    sidebar_block = ""
    if has_sidebar:
        sidebar_html = get_sidebar_html(site_path)
        sidebar_block = f"""
  <div class="docs-layout">
    <aside class="sidebar" id="sidebar">
      {sidebar_html}
    </aside>
    <main>
{body_html}
    </main>
  </div>
  <div class="sidebar-overlay" id="sidebarOverlay"></div>
  <button class="sidebar-toggle" id="sidebarToggle" aria-label="切換功能選單">☰</button>"""

    # 一般頁面內容
    main_block = ""
    if not has_sidebar:
        main_block = f"""
  <main>
{body_html}
  </main>"""

    # 側邊欄 JS（手機版切換）
    sidebar_js = ""
    if has_sidebar:
        sidebar_js = """
  <script>
  (function() {
    var btn = document.getElementById('sidebarToggle');
    var sidebar = document.getElementById('sidebar');
    var overlay = document.getElementById('sidebarOverlay');
    if (!btn) return;
    function toggle() {
      sidebar.classList.toggle('open');
      overlay.classList.toggle('open');
    }
    btn.addEventListener('click', toggle);
    overlay.addEventListener('click', toggle);
    sidebar.querySelectorAll('a').forEach(function(a) {
      a.addEventListener('click', function() {
        if (window.innerWidth <= 768) toggle();
      });
    });
  })();
  </script>"""

    return f"""<!DOCTYPE html>
<html lang="zh-TW">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <meta name="keywords" content="{keywords}">
  <link rel="canonical" href="{canonical}">

  <!-- Open Graph -->
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{canonical}">
  <meta property="og:locale" content="zh_TW">

  <!-- Schema.org JSON-LD -->
  <script type="application/ld+json">
{schema_json}
  </script>

  <style>
    :root {{
      --bg: #0f172a;
      --bg-card: #1e293b;
      --bg-code: #334155;
      --text: #e2e8f0;
      --text-muted: #94a3b8;
      --accent: #38bdf8;
      --accent2: #818cf8;
      --border: #334155;
      --max-width: 860px;
    }}
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
                   "Noto Sans TC", "Microsoft JhengHei", sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.8;
      font-size: 16px;
    }}

    /* 導航列 */
    nav {{
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(15, 23, 42, 0.95);
      backdrop-filter: blur(8px);
      border-bottom: 1px solid var(--border);
      padding: 0.75rem 1.5rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      overflow-x: auto;
    }}
    nav .logo {{
      font-weight: 700;
      font-size: 1.1rem;
      color: var(--accent);
      margin-right: 1rem;
      white-space: nowrap;
      text-decoration: none;
    }}
    nav a {{
      color: var(--text-muted);
      text-decoration: none;
      padding: 0.4rem 0.8rem;
      border-radius: 6px;
      font-size: 0.9rem;
      white-space: nowrap;
      transition: all 0.2s;
    }}
    nav a:hover {{ color: var(--text); background: var(--bg-card); }}
    nav a.active {{ color: var(--accent); background: var(--bg-card); }}

    /* 主內容 */
    main {{
      max-width: var(--max-width);
      margin: 0 auto;
      padding: 2rem 1.5rem 4rem;
    }}

    /* 標題 */
    h1 {{
      font-size: 2rem;
      font-weight: 700;
      margin: 2rem 0 1rem;
      background: linear-gradient(90deg, var(--accent), var(--accent2));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      line-height: 1.3;
    }}
    h2 {{
      font-size: 1.5rem;
      font-weight: 600;
      margin: 2.5rem 0 0.75rem;
      color: var(--text);
      padding-bottom: 0.5rem;
      border-bottom: 1px solid var(--border);
    }}
    h3 {{
      font-size: 1.2rem;
      font-weight: 600;
      margin: 1.5rem 0 0.5rem;
      color: var(--accent);
    }}
    h4 {{
      font-size: 1rem;
      font-weight: 600;
      margin: 1.2rem 0 0.4rem;
      color: var(--text-muted);
    }}

    /* 段落與列表 */
    p {{ margin: 0.75rem 0; }}
    ul, ol {{ margin: 0.75rem 0; padding-left: 1.5rem; }}
    li {{ margin: 0.3rem 0; }}

    /* 連結 */
    a {{ color: var(--accent); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}

    /* 表格 */
    table {{
      width: 100%;
      border-collapse: collapse;
      margin: 1rem 0;
      font-size: 0.9rem;
      overflow-x: auto;
      display: block;
    }}
    th, td {{
      padding: 0.6rem 0.8rem;
      text-align: left;
      border: 1px solid var(--border);
    }}
    th:first-child, td:first-child {{
      white-space: nowrap;
    }}
    th {{
      background: var(--bg-card);
      font-weight: 600;
      color: var(--accent);
      white-space: nowrap;
    }}
    td {{ background: rgba(30, 41, 59, 0.5); }}
    tr:hover td {{ background: var(--bg-card); }}

    /* 引用 */
    blockquote {{
      border-left: 3px solid var(--accent);
      padding: 0.75rem 1rem;
      margin: 1rem 0;
      background: var(--bg-card);
      border-radius: 0 8px 8px 0;
      color: var(--text-muted);
    }}
    blockquote strong {{ color: var(--text); }}

    /* 程式碼 */
    code {{
      background: var(--bg-code);
      padding: 0.15rem 0.4rem;
      border-radius: 4px;
      font-size: 0.85em;
      font-family: "SF Mono", Menlo, monospace;
    }}
    pre {{
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 1rem;
      overflow-x: auto;
      margin: 1rem 0;
    }}
    pre code {{
      background: none;
      padding: 0;
      font-size: 0.85rem;
      line-height: 1.6;
    }}

    /* 水平線 */
    hr {{
      border: none;
      border-top: 1px solid var(--border);
      margin: 2rem 0;
    }}

    /* 強調 */
    strong {{ color: #f1f5f9; }}
    em {{ color: var(--text-muted); }}

    /* 頁尾 */
    footer {{
      max-width: var(--max-width);
      margin: 0 auto;
      padding: 2rem 1.5rem;
      border-top: 1px solid var(--border);
      color: var(--text-muted);
      font-size: 0.85rem;
      text-align: center;
    }}

    /* RWD */
    @media (max-width: 640px) {{
      h1 {{ font-size: 1.5rem; }}
      h2 {{ font-size: 1.25rem; }}
      table {{ font-size: 0.8rem; }}
      th, td {{ padding: 0.4rem 0.5rem; }}
      nav {{ padding: 0.5rem 1rem; }}
    }}
{sidebar_css}
  </style>
</head>
<body>
  <nav>
    <a href="{('../' * site_path.count('/')) or ''}index.html" class="logo">Botrun Docs</a>
    {nav_html}
  </nav>
{sidebar_block}{main_block}
  <footer>
    <p>Botrun 波特人 — 卡米爾股份有限公司（CAMEO INC.）</p>
    <p>service@cameo.tw &middot; 02-2912-5028</p>
    <p>最後更新：{meta.get('last_updated', datetime.now().strftime('%Y-%m-%d'))}</p>
  </footer>
{sidebar_js}
</body>
</html>"""


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
    for content_path, site_path, label in PAGES:
        url = DOMAIN if site_path == "index.html" else f"{DOMAIN}/{site_path}"
        md_file = CONTENT_DIR / content_path
        if md_file.exists():
            meta, _ = parse_frontmatter(md_file.read_text(encoding="utf-8"))
            desc = meta.get("description", "")
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


def build_sitemap() -> str:
    """產生 sitemap.xml"""
    urls = []
    for _, site_path, _ in PAGES:
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
    )


def main():
    print("=== BotrunDocs 建置開始 ===\n")

    # 建立目錄
    for _, site_path, _ in PAGES:
        out_dir = SITE_DIR / Path(site_path).parent
        out_dir.mkdir(parents=True, exist_ok=True)

    # 轉換每個頁面
    for content_path, site_path, label in PAGES:
        md_file = CONTENT_DIR / content_path
        if not md_file.exists():
            print(f"  ⚠️ 跳過 {content_path}（檔案不存在）")
            continue

        raw = md_file.read_text(encoding="utf-8")
        meta, md_body = parse_frontmatter(raw)
        body_html = md_to_html(md_body)
        page_html = render_page(meta, body_html, site_path)

        out_file = SITE_DIR / site_path
        out_file.write_text(page_html, encoding="utf-8")
        size_kb = len(page_html.encode("utf-8")) / 1024
        print(f"  ✅ {site_path} ({size_kb:.1f} KB)")

    # 產生 AI 友善檔案
    llms_txt = build_llms_txt()
    (SITE_DIR / "llms.txt").write_text(llms_txt, encoding="utf-8")
    print(f"  ✅ llms.txt")

    sitemap = build_sitemap()
    (SITE_DIR / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print(f"  ✅ sitemap.xml")

    robots = build_robots()
    (SITE_DIR / "robots.txt").write_text(robots, encoding="utf-8")
    print(f"  ✅ robots.txt")

    print(f"\n=== 建置完成：{len(PAGES)} 頁 + 3 個 AI 檔案 ===")


if __name__ == "__main__":
    main()

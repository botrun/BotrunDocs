#!/usr/bin/env python3
"""
BDD/TDD 測試：驗證波特人小隊相關內容已完全從網站移除。

Feature: 移除波特人小隊
  Scenario: 所有頁面不應包含波特人小隊相關內容
    Given 網站已建置完成
    When 檢查所有 site/*.html
    Then 不應出現任何波特人小隊相關字詞
    And 導覽列不應包含波特小隊連結
    And bots 目錄不應存在
    And build.py 不應定義 bots 頁面
"""

import os
import re
import glob
import unittest
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

# DRY: 統一定義所有需要排除的關鍵字（單一來源）
# 注意：「波程」「波分」「波文」已被新 Bot 名稱（波程、波分段、波文件問答）重新使用，
# 因此改用正規表達式精確比對，避免誤判新 Bot 名稱。
BOT_SQUAD_KEYWORDS = [
    "波特小隊", "波特人小隊", "波小隊", "Bot Squad",
    "波庫", "波秒答", "波媽",
    "波露露", "波駿馬", "波火眼", "波大神",
    "波林 007", "波林007",
    "波金法", "永恆知己",
    "bots-detail", "bots/index",
]

# DRY: 需要精確比對的舊關鍵字（不能 substring match，因為是新 Bot 的子字串）
import re
OLD_BOT_EXACT_PATTERNS = [
    # 「波分」但不是「波分段」
    re.compile(r"波分(?!段)"),
    # 「波文」但不是「波文件問答」
    re.compile(r"波文(?!件問答)"),
    # 「波程」但不是「波程式」等新用途（波程 本身是新 Bot 名稱，所以不再禁止）
]

# DRY: 需要檢查的目錄（排除 updates/ 歷史紀錄）
SCAN_DIRS = {
    "site": BASE_DIR / "site",
}

# DRY: 需要單獨檢查的檔案
SCAN_FILES = [
    BASE_DIR / ".claude" / "skills" / "build" / "scripts" / "build.py",
    BASE_DIR / "README.md",
    BASE_DIR / "CLAUDE.md",
]


def find_keyword_in_file(filepath: str, keywords: list, patterns: list = None) -> list:
    """DRY: 單一函式搜尋檔案中的關鍵字+正規式，回傳 (行號, 關鍵字, 行內容)"""
    results = []
    if patterns is None:
        patterns = []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                for kw in keywords:
                    if kw.lower() in line.lower():
                        results.append((line_num, kw, line.strip()))
                for pat in patterns:
                    if pat.search(line):
                        results.append((line_num, pat.pattern, line.strip()))
    except (UnicodeDecodeError, FileNotFoundError):
        pass
    return results


def scan_directory(directory: Path, extensions: list, keywords: list, patterns: list = None) -> dict:
    """DRY: 掃描目錄下所有指定副檔名的檔案"""
    violations = {}
    for ext in extensions:
        for filepath in directory.rglob(f"*{ext}"):
            hits = find_keyword_in_file(str(filepath), keywords, patterns)
            if hits:
                rel = str(filepath.relative_to(BASE_DIR))
                violations[rel] = hits
    return violations


class TestBotSquadRemoved(unittest.TestCase):
    """BDD Scenario: 所有頁面不應包含波特人小隊相關內容"""

    def test_site_html_no_bot_squad_keywords(self):
        """Given site/*.html, Then 不應出現任何波特人小隊相關字詞"""
        violations = scan_directory(
            SCAN_DIRS["site"], [".html", ".txt", ".xml"], BOT_SQUAD_KEYWORDS, OLD_BOT_EXACT_PATTERNS
        )
        self.assertEqual(
            violations, {},
            f"\n\nsite/ 中仍有波特人小隊關鍵字:\n"
            + "\n".join(
                f"  {f}:{ln} [{kw}] {text}"
                for f, hits in violations.items()
                for ln, kw, text in hits
            ),
        )

    def test_build_py_no_bots_page(self):
        """Given build.py, Then NAV_PAGES 和 SUB_PAGES 不應包含 bots"""
        build_py = SCAN_FILES[0]
        hits = find_keyword_in_file(str(build_py), ["bots/", "bots-detail", "波特小隊"])
        self.assertEqual(
            hits, [],
            f"\n\nbuild.py 中仍有 bots 定義:\n"
            + "\n".join(f"  L{ln} [{kw}] {text}" for ln, kw, text in hits),
        )

    def test_site_bots_html_not_exist(self):
        """Then site/bots/ 目錄不應存在"""
        self.assertFalse(
            (BASE_DIR / "site" / "bots").exists(),
            "site/bots/ 目錄仍然存在",
        )

    def test_nav_no_bot_squad_link(self):
        """Then 所有 HTML 的導覽列不應包含波特小隊連結"""
        for html_file in (BASE_DIR / "site").rglob("*.html"):
            content = html_file.read_text(encoding="utf-8")
            # 檢查 <nav> 區塊
            nav_match = re.search(r"<nav>.*?</nav>", content, re.DOTALL)
            if nav_match:
                nav_html = nav_match.group()
                self.assertNotIn(
                    "波特小隊", nav_html,
                    f"{html_file.name} 的導覽列仍有「波特小隊」",
                )
                self.assertNotIn(
                    "bots/", nav_html,
                    f"{html_file.name} 的導覽列仍有 bots/ 連結",
                )

    def test_standalone_files_no_keywords(self):
        """Then README.md, CLAUDE.md 等不應有殘留"""
        for filepath in SCAN_FILES:
            if filepath.exists():
                hits = find_keyword_in_file(str(filepath), BOT_SQUAD_KEYWORDS)
                rel = str(filepath.relative_to(BASE_DIR))
                self.assertEqual(
                    hits, [],
                    f"\n\n{rel} 中仍有波特人小隊關鍵字:\n"
                    + "\n".join(f"  L{ln} [{kw}] {text}" for ln, kw, text in hits),
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)

#!/usr/bin/env python3
"""
BDD/TDD 測試：驗證「波夫」錯字已全部改為「波孵」。

Feature: 修正錯字
  Scenario: site/ 不應出現「波夫」
  Scenario: 應改為「波孵」
"""

import unittest
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
SITE_DIR = BASE_DIR / "site"

# DRY: 排除 updates/ 歷史紀錄
EXCLUDE_DIRS = {"updates"}


def scan_for_text(directory, extensions, text, exclude_dirs=None):
    """DRY: 掃描目錄中的指定文字，回傳 {檔案: [(行號, 行內容)]}"""
    if exclude_dirs is None:
        exclude_dirs = set()
    results = {}
    for ext in extensions:
        for f in directory.rglob(f"*{ext}"):
            if any(d in f.parts for d in exclude_dirs):
                continue
            try:
                for ln, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
                    if text in line:
                        rel = str(f.relative_to(BASE_DIR))
                        results.setdefault(rel, []).append((ln, line.strip()))
            except UnicodeDecodeError:
                pass
    return results


class TestTypoBofu(unittest.TestCase):

    def test_no_bofu_in_site(self):
        """Then site/ 不應出現「波夫」"""
        hits = scan_for_text(SITE_DIR, [".html", ".txt", ".xml"], "波夫")
        self.assertEqual(hits, {}, f"site/ 仍有「波夫」:\n" +
            "\n".join(f"  {f}:{ln} {t}" for f, lines in hits.items() for ln, t in lines))

    def test_bofu_replaced_in_site(self):
        """Then site/ 應出現「波孵」"""
        all_text = ""
        for f in SITE_DIR.rglob("*.html"):
            all_text += f.read_text(encoding="utf-8")
        self.assertIn("波孵", all_text, "site/ 缺少「波孵」")


if __name__ == "__main__":
    unittest.main(verbosity=2)

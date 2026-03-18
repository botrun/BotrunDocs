#!/usr/bin/env python3
"""
BDD/TDD 測試：原生波特人頁面應移除「網頁擷取」段落。

Feature: 移除網頁擷取段落
  Scenario: native.html 不應有「網頁擷取」章節
  Scenario: 其他功能章節應保留
"""

import unittest
from pathlib import Path

NATIVE_HTML = Path(__file__).parent.parent / "site" / "features" / "native.html"


class TestRemoveWebScrape(unittest.TestCase):

    def setUp(self):
        self.html = NATIVE_HTML.read_text(encoding="utf-8")

    def test_no_web_scrape_section(self):
        """Then native.html 不應有「網頁擷取」章節"""
        self.assertNotIn("網頁擷取", self.html)

    def test_other_sections_remain(self):
        """Then 其他功能章節應保留"""
        for section in ["即時搜尋", "PDF 深度分析", "多圖辨識", "AI 圖片生成"]:
            self.assertIn(section, self.html, f"缺少：{section}")


if __name__ == "__main__":
    unittest.main(verbosity=2)

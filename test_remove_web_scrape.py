#!/usr/bin/env python3
"""
BDD/TDD 測試：原生波特人頁面應移除「網頁擷取」段落。

Feature: 移除網頁擷取段落
  Scenario: native.md 不應有「網頁擷取」章節
  Scenario: 其他功能章節應保留
"""

import unittest
from pathlib import Path

NATIVE_MD = Path(__file__).parent / "content" / "features" / "native.md"


class TestRemoveWebScrape(unittest.TestCase):

    def setUp(self):
        self.md = NATIVE_MD.read_text(encoding="utf-8")

    def test_no_web_scrape_section(self):
        """Then native.md 不應有「## 網頁擷取」章節"""
        self.assertNotIn("## 網頁擷取", self.md)

    def test_other_sections_remain(self):
        """Then 其他功能章節應保留"""
        for section in ["即時搜尋", "PDF 深度分析", "多圖辨識", "AI 圖片生成"]:
            self.assertIn(section, self.md, f"缺少：{section}")


if __name__ == "__main__":
    unittest.main(verbosity=2)

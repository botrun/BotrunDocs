#!/usr/bin/env python3
"""
BDD/TDD 測試：功能頁側邊欄應乾淨無分組標籤。

Feature: 側邊欄精簡
  Scenario: 側邊欄不應有分組標籤文字
  Scenario: 側邊欄四個連結應保留
"""

import unittest
from pathlib import Path

BASE_DIR = Path(__file__).parent
SITE_DIR = BASE_DIR / "site"

FEATURE_HTML = SITE_DIR / "features" / "index.html"


class TestSidebarClean(unittest.TestCase):

    def setUp(self):
        self.html = FEATURE_HTML.read_text(encoding="utf-8")

    def test_no_group_labels(self):
        """Then 側邊欄不應有 sidebar-group 分組標籤"""
        self.assertNotIn("sidebar-group", self.html)

    def test_has_all_links(self):
        """Then 側邊欄應有四個頁面連結"""
        for text in ["功能總覽", "原生波特人", "孵化器", "平台能力"]:
            self.assertIn(text, self.html, f"側邊欄缺少：{text}")


if __name__ == "__main__":
    unittest.main(verbosity=2)

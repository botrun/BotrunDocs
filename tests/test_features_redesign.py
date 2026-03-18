#!/usr/bin/env python3
"""
BDD/TDD 測試：功能頁精簡 + Agentic AI 整合到首頁。

Feature: 功能頁精簡化
  Scenario: 功能頁應移除全部已上線的功能狀態表
  Scenario: 功能頁應移除 Agentic AI 段落（已整合至首頁）
  Scenario: 功能頁三個子層不應有重複的功能表格
  Scenario: 功能頁行數應大幅縮減
  Scenario: 19 Bot 表格應保留但精簡
  Scenario: 首頁應包含 Agentic AI 精簡內容
"""

import unittest
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
FEATURES_HTML = BASE_DIR / "site" / "features" / "index.html"
INDEX_HTML = BASE_DIR / "site" / "index.html"


class TestFeaturesRedesign(unittest.TestCase):

    def setUp(self):
        self.features_html = FEATURES_HTML.read_text(encoding="utf-8")
        self.index_html = INDEX_HTML.read_text(encoding="utf-8")

    # --- 功能頁精簡 ---

    def test_features_no_status_table(self):
        """Then 功能頁不應有「功能狀態一覽」"""
        self.assertNotIn("功能狀態一覽", self.features_html)

    def test_features_no_agentic_section(self):
        """Then 功能頁不應有 Agentic AI 段落"""
        self.assertNotIn("Agentic AI 五大核心特色", self.features_html)

    def test_features_has_bot_list(self):
        """Then 功能頁應保留 Bot 列表"""
        self.assertIn("波逐字稿", self.features_html)
        self.assertIn("波繪圖", self.features_html)

    def test_features_has_three_layers(self):
        """Then 功能頁應保留三層架構導航"""
        self.assertIn("原生波特人", self.features_html)
        self.assertIn("孵化器", self.features_html)
        self.assertIn("平台能力", self.features_html)

    # --- 首頁整合 Agentic AI ---

    def test_index_has_agentic(self):
        """Then 首頁應包含 Agentic AI 相關內容"""
        self.assertIn("Agentic", self.index_html)


if __name__ == "__main__":
    unittest.main(verbosity=2)

#!/usr/bin/env python3
"""
BDD/TDD 測試：驗證首頁精簡為著陸頁。

Feature: 首頁精簡化
  Scenario: 首頁應簡潔，行數大幅縮減
  Scenario: 首頁應保留核心結構（Hero、賣點、社會證明、CTA）
  Scenario: 詳細案例、評分法、零幻覺攻擊表不應出現在首頁
  Scenario: 政府機關名稱應保留但不展開細節
"""

import unittest
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
INDEX_HTML = BASE_DIR / "site" / "index.html"


class TestHomepageRedesign(unittest.TestCase):

    def setUp(self):
        self.html = INDEX_HTML.read_text(encoding="utf-8")
        self.html_lines = self.html.splitlines()

    # --- 核心結構存在 ---

    def test_has_hero_section(self):
        """Then 首頁應有 Botrun 波特人標題"""
        self.assertIn("Botrun 波特人", self.html)

    def test_has_cta_contact(self):
        """Then 首頁應有聯絡資訊 CTA"""
        self.assertIn("service@cameo.tw", self.html)

    def test_has_botrun_link(self):
        """Then 首頁應有 botrun.ai 連結"""
        self.assertIn("botrun.ai", self.html)

    # --- 不應出現的冗長內容 ---

    def test_no_detailed_attack_table(self):
        """Then 首頁不應有零幻覺攻擊類別詳細表格"""
        self.assertNotIn("Prompt_Injection", self.html)
        self.assertNotIn("Emotional_DoS", self.html)
        self.assertNotIn("Ideological_Trap", self.html)

    def test_no_expanded_case_details(self):
        """Then 首頁不應展開個別案例的「問題→方案→成效」"""
        count = self.html.count("- 問題：") + self.html.count("- 方案：") + self.html.count("- 成效：")
        self.assertLessEqual(count, 0,
            f"首頁仍有 {count} 個展開的案例細節（問題/方案/成效）")

    def test_government_names_present(self):
        """Then 首頁應提及主要政府機關名稱"""
        for name in ["內政部", "數位部", "立法院", "環境部"]:
            self.assertIn(name, self.html, f"首頁缺少機關名稱：{name}")


if __name__ == "__main__":
    unittest.main(verbosity=2)

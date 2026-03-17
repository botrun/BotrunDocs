#!/usr/bin/env python3
"""
BDD/TDD 測試：驗證首頁有專屬 CSS 優化。

Feature: 首頁 CSS 優化
  Scenario: 首頁 body 應有 class="home" 標記
  Scenario: 首頁應有 Hero 區塊樣式
  Scenario: 首頁應有卡片式佈局樣式
  Scenario: 首頁應有 CTA 按鈕樣式
  Scenario: 其他頁面不應有 class="home"
"""

import unittest
from pathlib import Path

BASE_DIR = Path(__file__).parent
SITE_DIR = BASE_DIR / "site"

INDEX_HTML = SITE_DIR / "index.html"
FEATURES_HTML = SITE_DIR / "features" / "index.html"


class TestHomepageCss(unittest.TestCase):

    def setUp(self):
        self.home_html = INDEX_HTML.read_text(encoding="utf-8")
        self.features_html = FEATURES_HTML.read_text(encoding="utf-8")

    def test_home_body_class(self):
        """Then 首頁 body 應有 class="home" """
        self.assertIn('class="home"', self.home_html)

    def test_other_page_no_home_class(self):
        """Then 其他頁面 body 不應有 class="home" """
        self.assertNotIn('class="home"', self.features_html)

    def test_has_hero_css(self):
        """Then 首頁應有 .home .hero 樣式"""
        self.assertIn(".home .hero", self.home_html)

    def test_has_feature_cards_css(self):
        """Then 首頁應有 .feature-cards 卡片樣式"""
        self.assertIn(".feature-cards", self.home_html)

    def test_has_cta_button_css(self):
        """Then 首頁應有 .cta-btn 按鈕樣式"""
        self.assertIn(".cta-btn", self.home_html)

    def test_has_hero_markup(self):
        """Then 首頁 HTML 應有 hero 區塊標記"""
        self.assertIn('class="hero"', self.home_html)

    def test_has_feature_cards_markup(self):
        """Then 首頁 HTML 應有 feature-cards 區塊標記"""
        self.assertIn('class="feature-cards"', self.home_html)


if __name__ == "__main__":
    unittest.main(verbosity=2)

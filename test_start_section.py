#!/usr/bin/env python3
"""
BDD/TDD 測試：驗證「開始使用」與「聯絡資訊」段落修改正確。

Feature: 修改開始使用段落
  Scenario: 免費試用文字已移除
  Scenario: 聯絡資訊包含 service@cameo.tw
"""

import unittest
from pathlib import Path

BASE_DIR = Path(__file__).parent

# DRY: 需要檢查的檔案
INDEX_MD = BASE_DIR / "content" / "index.md"
INDEX_HTML = BASE_DIR / "site" / "index.html"

# DRY: 應移除的文字
REMOVED_TEXTS = [
    "新客戶通過審核後享",
    "1 個月免費體驗",
    "前往 https://botrun.ai 註冊",
]

# DRY: 應存在的文字
REQUIRED_TEXTS = [
    "service@cameo.tw",
]


class TestStartSection(unittest.TestCase):
    """Scenario: 開始使用段落修改正確"""

    def setUp(self):
        self.md = INDEX_MD.read_text(encoding="utf-8")
        self.html = INDEX_HTML.read_text(encoding="utf-8")

    def test_free_trial_removed_from_md(self):
        """Then content/index.md 不應包含免費試用相關文字"""
        for text in REMOVED_TEXTS:
            self.assertNotIn(text, self.md, f"index.md 仍有：{text}")

    def test_free_trial_removed_from_html(self):
        """Then site/index.html 不應包含免費試用相關文字"""
        for text in REMOVED_TEXTS:
            self.assertNotIn(text, self.html, f"index.html 仍有：{text}")

    def test_contact_email_in_md(self):
        """Then content/index.md 聯絡資訊應包含 service@cameo.tw"""
        for text in REQUIRED_TEXTS:
            self.assertIn(text, self.md, f"index.md 缺少：{text}")

    def test_contact_email_in_html(self):
        """Then site/index.html 聯絡資訊應包含 service@cameo.tw"""
        for text in REQUIRED_TEXTS:
            self.assertIn(text, self.html, f"index.html 缺少：{text}")


if __name__ == "__main__":
    unittest.main(verbosity=2)

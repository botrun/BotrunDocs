#!/usr/bin/env python3
"""
BDD/TDD 測試：驗證「系統訊息」、「後端已就緒、前端尚未開放」、「API 串接」段落已移除。

Feature: 移除平台能力頁面中的三個段落
  Scenario: content/features/platform.md 不應出現這三個段落
  Scenario: site/features/platform.html 不應出現這三個段落
"""

import unittest
from pathlib import Path

BASE_DIR = Path(__file__).parent

PLATFORM_MD = BASE_DIR / "content" / "features" / "platform.md"
PLATFORM_HTML = BASE_DIR / "site" / "features" / "platform.html"

# DRY: 應移除的段落標題/關鍵文字
REMOVED_TEXTS = [
    "系統訊息",
    "後端已就緒、前端尚未開放",
    "API 串接",
    "可用的 API 端點",
    "Bearer Token",
    "Bot API 端點",
    "Google Docs 同步",
]


class TestRemoveSections(unittest.TestCase):

    def setUp(self):
        self.md = PLATFORM_MD.read_text(encoding="utf-8")
        self.html = PLATFORM_HTML.read_text(encoding="utf-8")

    def test_removed_from_md(self):
        """Then platform.md 不應出現被刪段落"""
        for text in REMOVED_TEXTS:
            self.assertNotIn(text, self.md, f"platform.md 仍有：{text}")

    def test_removed_from_html(self):
        """Then platform.html 不應出現被刪段落"""
        for text in REMOVED_TEXTS:
            self.assertNotIn(text, self.html, f"platform.html 仍有：{text}")


if __name__ == "__main__":
    unittest.main(verbosity=2)

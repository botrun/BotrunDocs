#!/usr/bin/env python3
"""
BDD/TDD 測試：驗證簡報內容已正確更新到網站。

Feature: 簡報內容同步到網站
  Scenario: 19 個 Bot（智XX→波XX）完整列表已加入
  Scenario: MCP 說明已更新
  Scenario: 台灣三中心部署資訊已加入
  Scenario: Agentic AI 五大核心特色已加入
  Scenario: 波特人評分法已加入
  Scenario: COSTAR 提示詞架構已加入
  Scenario: 零幻覺證明標章已加入
  Scenario: 新政府應用案例已加入
  Scenario: 開放 vs 商用模型說明已加入
  Scenario: 不應出現「智XX」名稱（應為「波XX」）
"""

import unittest
from pathlib import Path

BASE_DIR = Path(__file__).parent
CONTENT_DIR = BASE_DIR / "content"
SITE_DIR = BASE_DIR / "site"

# DRY: 簡報中的 19 個 Bot（智XX→波XX 對應）
BOTS_FROM_PPTX = [
    ("波逐字稿", "聲音與語言精靈", "上傳音檔轉換成文字"),
    ("波分段", "文字魔法師", "將長段落的文字"),
    ("波翻譯", "聲音與語言精靈", "多國語言翻譯"),
    ("波新聞稿", "文字魔法師", "撰寫新聞稿"),
    ("波繪圖", "創意畫匠", "產生圖片"),
    ("波畫室", "創意畫匠", "精緻提示工程繪製"),
    ("波流程圖", "創意畫匠", "心智圖"),
    ("波文件問答", "文件助理", "上傳多份文件"),
    ("波程", "程式碼大師", "程式碼"),
    ("波公文", "文字魔法師", "公文撰寫"),
    ("波提示工程", "文字魔法師", "提示工程"),
    ("波臺德", "聲音與語言精靈", "臺德"),
    ("波簡報", "文字魔法師", "簡報"),
    ("波數據分析", "數據洞察家", "數據"),
    ("波會議記錄", "全能文件助理", "會議紀錄"),
    ("波Youtube", "聲音與語言精靈", "youtube"),
    ("波旅程地圖", "全能文件助理", "旅程地圖"),
    ("波網頁", "創意畫匠", "html"),
]

# DRY: 波特人評分法 9 項指標
SCORING_METRICS = ["真", "新", "穩", "安", "人", "準", "快", "全", "省"]

# DRY: Agentic AI 五大核心
AGENTIC_FEATURES = ["主動規劃", "多步工作流", "工具整合", "目標導向", "自主修正"]

# DRY: 台灣三中心
THREE_CENTERS = [
    ("臺北", "AWS", "Claude Sonnet"),
    ("新竹", "國網中心", "Llama"),
    ("彰化", "Google", "Claude Haiku"),
]

# DRY: 零幻覺標章
ZERO_HALLUCINATION_BADGES = ["帝國標章", "黑熊標章", "基礎標章"]

# DRY: 不應出現的「智XX」名稱
ZHI_KEYWORDS = [
    "智逐字稿", "智分段", "智翻譯", "智新聞稿", "智繪圖",
    "智畫室", "智流程圖", "智文件問答", "智程", "智公文",
    "智提示工程", "智臺德", "智簡報", "智數據分析",
    "智會議記錄", "智Youtube", "智旅程地圖", "智網頁",
]

# DRY: 新政府案例關鍵字
GOV_CASES = ["環境部", "公共工程委員會", "僑委會", "食藥署", "環管署", "教育部"]


def read_all_content(directory, extensions):
    """DRY: 讀取目錄下所有指定副檔名檔案的合併內容"""
    combined = ""
    for ext in extensions:
        for f in directory.rglob(f"*{ext}"):
            combined += f.read_text(encoding="utf-8") + "\n"
    return combined


class TestPptxBotList(unittest.TestCase):
    """Scenario: 19 個 Bot 完整列表已加入網站"""

    def setUp(self):
        self.content = read_all_content(CONTENT_DIR, [".md"])

    def test_all_bot_names_present(self):
        """Then 所有 19 個波XX Bot 名稱都應出現在 content/ 中"""
        missing = [name for name, _, _ in BOTS_FROM_PPTX if name not in self.content]
        self.assertEqual(missing, [], f"缺少以下 Bot: {missing}")

    def test_bot_categories_present(self):
        """Then Bot 分類名稱都應出現"""
        categories = set(cat for _, cat, _ in BOTS_FROM_PPTX)
        missing = [cat for cat in categories if cat not in self.content]
        self.assertEqual(missing, [], f"缺少以下分類: {missing}")

    def test_no_zhi_keywords_in_content(self):
        """Then content/ 不應出現「智XX」名稱"""
        found = [kw for kw in ZHI_KEYWORDS if kw in self.content]
        self.assertEqual(found, [], f"content/ 仍有「智XX」: {found}")

    def test_no_zhi_keywords_in_site(self):
        """Then site/ 不應出現「智XX」名稱"""
        site_content = read_all_content(SITE_DIR, [".html", ".txt"])
        found = [kw for kw in ZHI_KEYWORDS if kw in site_content]
        self.assertEqual(found, [], f"site/ 仍有「智XX」: {found}")


class TestPptxPlatformInfo(unittest.TestCase):
    """Scenario: 平台資訊已更新"""

    def setUp(self):
        self.content = read_all_content(CONTENT_DIR, [".md"])

    def test_three_centers_present(self):
        """Then 台灣三中心資訊應出現"""
        for city, provider, _ in THREE_CENTERS:
            self.assertIn(city, self.content, f"缺少三中心: {city}")
            self.assertIn(provider, self.content, f"缺少提供商: {provider}")

    def test_mcp_type_c_analogy(self):
        """Then MCP Type-C 比喻應出現"""
        self.assertIn("Type-C", self.content, "缺少 MCP Type-C 比喻")

    def test_open_vs_commercial_model(self):
        """Then 開放 vs 商用模型說明應出現"""
        self.assertIn("開放模型", self.content, "缺少「開放模型」說明")
        self.assertIn("商用模型", self.content, "缺少「商用模型」說明")


class TestPptxAgenticAI(unittest.TestCase):
    """Scenario: Agentic AI 五大核心特色已加入"""

    def setUp(self):
        self.content = read_all_content(CONTENT_DIR, [".md"])

    def test_agentic_features_present(self):
        """Then 五大核心特色都應出現"""
        missing = [f for f in AGENTIC_FEATURES if f not in self.content]
        self.assertEqual(missing, [], f"缺少 Agentic AI 特色: {missing}")


class TestPptxScoringMethod(unittest.TestCase):
    """Scenario: 波特人評分法已加入"""

    def setUp(self):
        self.content = read_all_content(CONTENT_DIR, [".md"])

    def test_scoring_title_present(self):
        """Then 波特人評分法標題應出現"""
        self.assertIn("波特人評分法", self.content)

    def test_scoring_metrics_present(self):
        """Then 9 項指標的英文名稱應出現"""
        english_names = ["Real", "New", "Stable", "Safe", "Human", "Accurate", "Fast", "Complete", "Economic"]
        missing = [n for n in english_names if n not in self.content]
        self.assertEqual(missing, [], f"缺少評分指標: {missing}")


class TestPptxCOSTAR(unittest.TestCase):
    """Scenario: COSTAR 提示詞架構已加入"""

    def setUp(self):
        self.content = read_all_content(CONTENT_DIR, [".md"])

    def test_costar_present(self):
        """Then COSTAR 應出現"""
        self.assertIn("COSTAR", self.content)


class TestPptxZeroHallucination(unittest.TestCase):
    """Scenario: 零幻覺證明標章已加入"""

    def setUp(self):
        self.content = read_all_content(CONTENT_DIR, [".md"])

    def test_zero_hallucination_title(self):
        """Then 零幻覺證明標章標題應出現"""
        self.assertIn("零幻覺", self.content)

    def test_badges_present(self):
        """Then 三種標章應出現"""
        missing = [b for b in ZERO_HALLUCINATION_BADGES if b not in self.content]
        self.assertEqual(missing, [], f"缺少標章: {missing}")


class TestPptxGovCases(unittest.TestCase):
    """Scenario: 新政府應用案例已加入"""

    def setUp(self):
        self.content = read_all_content(CONTENT_DIR, [".md"])

    def test_new_gov_agencies_present(self):
        """Then 新政府機關案例應出現"""
        missing = [g for g in GOV_CASES if g not in self.content]
        self.assertEqual(missing, [], f"缺少政府案例: {missing}")


if __name__ == "__main__":
    unittest.main(verbosity=2)

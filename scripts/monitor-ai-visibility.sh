#!/bin/bash
# ==============================================================================
# AI Agent 可搜尋性監控腳本
# 用途：檢查 Botrun 文件網站是否能被 AI Agent 發現與存取
#
# 使用方式：
#   手動執行：bash scripts/monitor-ai-visibility.sh
#   cron 模式：bash scripts/monitor-ai-visibility.sh --cron
# ==============================================================================

set -uo pipefail

# --- 設定 ---
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
SITE_BASE="https://botrun-docs.web.app"
LOG_DIR="${SCRIPT_DIR}/monitor-logs"
TIMESTAMP=$(date '+%Y-%m-%d_%H%M%S')
LOG_FILE="${LOG_DIR}/monitor-${TIMESTAMP}.log"
SUMMARY_FILE="${LOG_DIR}/summary.csv"

SEARCH_QUERIES=(
  "Botrun 是什麼"
  "波特人 AI 平台"
  "台灣 AI Bot 建立平台"
  "botrun.ai 功能"
)

DOCS_URL_PATTERN="botrun-docs.web.app"

# --- 模式判斷 ---
CRON_MODE=false
if [ "${1:-}" = "--cron" ]; then
  CRON_MODE=true
fi

# --- 顏色（cron 模式關閉） ---
if [ "$CRON_MODE" = true ]; then
  RED='' GREEN='' YELLOW='' CYAN='' NC=''
else
  RED='\033[0;31m' GREEN='\033[0;32m' YELLOW='\033[0;33m' CYAN='\033[0;36m' NC='\033[0m'
fi

pass=0
fail=0
warn=0
site_ok=0
site_total=5
link_count=0
page_count=0
schema_ok="N"
search_found=0
search_total=${#SEARCH_QUERIES[@]}

log_pass() { echo -e "${GREEN}PASS${NC} $1"; ((pass++)); }
log_fail() { echo -e "${RED}FAIL${NC} $1"; ((fail++)); }
log_warn() { echo -e "${YELLOW}WARN${NC} $1"; ((warn++)); }
log_info() { echo -e "${CYAN}INFO${NC} $1"; }

mkdir -p "$LOG_DIR"

if [ ! -f "$SUMMARY_FILE" ]; then
  echo "日期,時間,通過,失敗,警告,網站可存取,llms.txt連結數,sitemap頁面數,Schema.org,搜尋收錄,備註" > "$SUMMARY_FILE"
fi

# ==============================================================================
echo "=============================================="
echo " Botrun AI 可見性監控報告"
echo " 檢查時間：$(date '+%Y-%m-%d %H:%M:%S %Z')"
echo " 部署 URL：${SITE_BASE}"
echo "=============================================="
echo ""

# --- 第一層：HTTP 可存取性 ---
echo "── 第一層：HTTP 可存取性 ──"

check_url() {
  local url="$1"
  local desc="$2"
  local status
  status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 15 "$url" 2>/dev/null || echo "000")
  if [ "$status" = "200" ]; then
    log_pass "$desc → HTTP $status"
    ((site_ok++))
  elif [ "$status" = "000" ]; then
    log_fail "$desc → 連線失敗"
  else
    log_fail "$desc → HTTP $status"
  fi
}

check_url "${SITE_BASE}/" "首頁"
check_url "${SITE_BASE}/llms.txt" "llms.txt（AI Agent 索引）"
check_url "${SITE_BASE}/llms-full.txt" "llms-full.txt（完整內容）"
check_url "${SITE_BASE}/robots.txt" "robots.txt（爬蟲規則）"
check_url "${SITE_BASE}/sitemap.xml" "sitemap.xml（搜尋引擎索引）"

echo ""

# --- 第二層：AI 關鍵檔案內容驗證 ---
echo "── 第二層：AI 關鍵檔案內容驗證 ──"

LLMS_CONTENT=$(curl -s --max-time 15 "${SITE_BASE}/llms.txt" 2>/dev/null || echo "")
if [ -n "$LLMS_CONTENT" ]; then
  link_count=$(echo "$LLMS_CONTENT" | grep -c "https://" || true)
  if [ "$link_count" -ge 5 ]; then
    log_pass "llms.txt 包含 $link_count 個頁面連結"
  else
    log_warn "llms.txt 僅有 $link_count 個連結（預期 >=5）"
  fi

  SAMPLE_LINK=$(echo "$LLMS_CONTENT" | grep -oE "https://[^ ]+\.html" | sort -R 2>/dev/null | head -1 || echo "$LLMS_CONTENT" | grep -oE "https://[^ ]+\.html" | tail -1 || true)
  if [ -n "$SAMPLE_LINK" ]; then
    LINK_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 15 "$SAMPLE_LINK" 2>/dev/null || echo "000")
    if [ "$LINK_STATUS" = "200" ]; then
      log_pass "llms.txt 抽樣連結可存取 ($SAMPLE_LINK)"
    else
      log_fail "llms.txt 抽樣連結不可存取 ($SAMPLE_LINK → $LINK_STATUS)"
    fi
  fi

  BAD_LINKS=$(echo "$LLMS_CONTENT" | grep -c "docs\.botrun\.ai" || true)
  if [ "$BAD_LINKS" -gt 0 ]; then
    log_fail "llms.txt 仍有 $BAD_LINKS 個指向 docs.botrun.ai 的未生效連結"
  else
    log_pass "llms.txt 無死連結"
  fi
else
  log_fail "無法取得 llms.txt 內容"
fi

ROBOTS_CONTENT=$(curl -s --max-time 15 "${SITE_BASE}/robots.txt" 2>/dev/null || echo "")
if echo "$ROBOTS_CONTENT" | grep -qi "sitemap"; then
  SITEMAP_URL=$(echo "$ROBOTS_CONTENT" | grep -i "sitemap" | awk '{print $2}')
  SITEMAP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" --max-time 15 "$SITEMAP_URL" 2>/dev/null || echo "000")
  if [ "$SITEMAP_STATUS" = "200" ]; then
    log_pass "robots.txt Sitemap 連結可存取"
  else
    log_fail "robots.txt Sitemap 連結不可存取 ($SITEMAP_URL → $SITEMAP_STATUS)"
  fi
else
  log_warn "robots.txt 缺少 Sitemap 宣告"
fi

SITEMAP_CONTENT=$(curl -s --max-time 15 "${SITE_BASE}/sitemap.xml" 2>/dev/null || echo "")
if [ -n "$SITEMAP_CONTENT" ]; then
  page_count=$(echo "$SITEMAP_CONTENT" | grep -c "<loc>" || true)
  if [ "$page_count" -ge 5 ]; then
    log_pass "sitemap.xml 包含 $page_count 個頁面"
  else
    log_warn "sitemap.xml 僅有 $page_count 個頁面（預期 >=5）"
  fi

  BAD_SITEMAP=$(echo "$SITEMAP_CONTENT" | grep -c "docs\.botrun\.ai" || true)
  if [ "$BAD_SITEMAP" -gt 0 ]; then
    log_fail "sitemap.xml 仍有 $BAD_SITEMAP 個指向 docs.botrun.ai 的未生效連結"
  else
    log_pass "sitemap.xml 無死連結"
  fi
fi

echo ""

# --- 第三層：Schema.org 結構化資料 ---
echo "── 第三層：Schema.org 結構化資料 ──"

INDEX_HTML=$(curl -s --max-time 15 "${SITE_BASE}/" 2>/dev/null || echo "")

if echo "$INDEX_HTML" | grep -q "application/ld+json"; then
  log_pass "首頁包含 Schema.org JSON-LD"
  schema_ok="Y"
else
  log_warn "首頁缺少 Schema.org JSON-LD"
fi

if echo "$INDEX_HTML" | grep -q 'og:title'; then
  log_pass "首頁包含 Open Graph meta"
else
  log_warn "首頁缺少 Open Graph meta"
fi

if echo "$INDEX_HTML" | grep -q 'meta name="description"'; then
  log_pass "首頁包含 meta description"
else
  log_warn "首頁缺少 meta description"
fi

echo ""

# --- 第四層：內容一致性（本地 vs 線上） ---
echo "── 第四層：內容一致性 ──"

if [ -f "${PROJECT_DIR}/site/llms.txt" ]; then
  LOCAL_HASH=$(md5 -q "${PROJECT_DIR}/site/llms.txt" 2>/dev/null || md5sum "${PROJECT_DIR}/site/llms.txt" | awk '{print $1}')
  REMOTE_CONTENT=$(curl -s --max-time 15 "${SITE_BASE}/llms.txt" 2>/dev/null || echo "")
  REMOTE_HASH=$(echo "$REMOTE_CONTENT" | md5 2>/dev/null || echo "$REMOTE_CONTENT" | md5sum | awk '{print $1}')
  if [ "$LOCAL_HASH" = "$REMOTE_HASH" ]; then
    log_pass "llms.txt 本地與線上一致"
  else
    log_warn "llms.txt 本地與線上不一致（可能需要重新部署）"
  fi
else
  log_info "略過一致性檢查（非專案目錄執行）"
fi

echo ""

# --- 第五層：Google 搜尋引擎收錄檢查 ---
echo "── 第五層：Google 搜尋收錄 ──"

SITE_INDEXED=$(curl -s --max-time 15 -A "Mozilla/5.0" "https://www.google.com/search?q=site:botrun-docs.web.app" 2>/dev/null || echo "")
if echo "$SITE_INDEXED" | grep -qi "botrun-docs"; then
  log_pass "Google 已收錄 botrun-docs.web.app"
else
  log_fail "Google 尚未收錄 botrun-docs.web.app"
fi

MAIN_INDEXED=$(curl -s --max-time 15 -A "Mozilla/5.0" "https://www.google.com/search?q=site:botrun.ai" 2>/dev/null || echo "")
if echo "$MAIN_INDEXED" | grep -qi "botrun"; then
  log_pass "Google 已收錄 botrun.ai 主站"
else
  log_warn "Google 未收錄 botrun.ai 主站"
fi

echo ""
echo "── 第六層：AI 搜尋引擎實測 ──"
echo ""
log_info "此層需在 Claude Code 中由 AI 執行 WebSearch 測試"
log_info "測試關鍵字："
for q in "${SEARCH_QUERIES[@]}"; do
  echo "    - $q"
done
echo ""
log_info "判斷標準：搜尋結果是否包含 ${DOCS_URL_PATTERN}"
log_info "請在 Claude Code 中執行 /monitor，Claude 會自動進行搜尋測試"
echo ""

# --- 總結 ---
echo "=============================================="
echo " 監控總結"
echo "=============================================="
echo -e " ${GREEN}通過：${pass}${NC}  ${RED}失敗：${fail}${NC}  ${YELLOW}警告：${warn}${NC}"
echo ""

if [ "$fail" -gt 0 ]; then
  echo -e "${RED}有 ${fail} 項檢查失敗，AI Agent 可能無法正常搜尋到網站。${NC}"
elif [ "$warn" -gt 0 ]; then
  echo -e "${YELLOW}有 ${warn} 項警告，建議改善以提升 AI 可見性。${NC}"
else
  echo -e "${GREEN}所有檢查通過！網站對 AI Agent 完全可見。${NC}"
fi

echo ""

# --- 寫入 summary.csv ---
DATE_STR=$(date '+%Y-%m-%d')
TIME_STR=$(date '+%H:%M')
NOTES=""
if [ "$fail" -gt 0 ]; then NOTES="有失敗項目"; fi
echo "${DATE_STR},${TIME_STR},${pass},${fail},${warn},${site_ok}/${site_total},${link_count},${page_count},${schema_ok},${search_found}/${search_total},${NOTES}" >> "$SUMMARY_FILE"

# --- cron 模式：失敗時發送通知 ---
if [ "$CRON_MODE" = true ] && [ "$fail" -gt 0 ]; then
  osascript -e "display notification \"${fail} 項檢查失敗，請檢查 AI 可見性\" with title \"Botrun 監控警報\" sound name \"Basso\"" 2>/dev/null || true
fi

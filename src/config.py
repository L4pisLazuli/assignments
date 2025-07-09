"""
WebClassクライアント設定ファイル
"""
import os
from pathlib import Path

# ディレクトリ設定
PROJECT_ROOT = Path(__file__).parent
OUTPUT_DIR = PROJECT_ROOT / "../output"
LOG_DIR = OUTPUT_DIR

# ログ設定
LOG_FILE = LOG_DIR / "webclass.log"
DEBUG_LOG_FILE = PROJECT_ROOT / ".webclass_debug.log"  # 隠しファイル化
EXECUTION_HISTORY_FILE = OUTPUT_DIR / ".execution_history.json"  # 隠しファイル化

# WebClass設定
WEBCLASS_URL = "https://els.sa.dendai.ac.jp"
DEFAULT_DATE = "2000-01-01"

# セキュリティ設定
DAILY_EXECUTION_LIMIT = True

# HTML出力設定
HTML_OUTPUT_FILE = OUTPUT_DIR / "webclass_info.html" 

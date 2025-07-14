"""
共通ユーティリティ関数
"""
import json
import sys
from datetime import datetime
from pathlib import Path

from config import EXECUTION_HISTORY_FILE, DAILY_EXECUTION_LIMIT


def check_execution_limit(logger):
    """1日1回の実行制限をチェックする関数"""
    if not DAILY_EXECUTION_LIMIT:
        return
        
    try:
        # 現在の日付
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 実行履歴の読み込み
        if EXECUTION_HISTORY_FILE.exists():
            try:
                with open(EXECUTION_HISTORY_FILE, "r", encoding="utf-8") as f:
                    history = json.load(f)
            except json.JSONDecodeError:
                logger.error("実行履歴ファイルの読み込みに失敗しました")
                history = {}
        else:
            history = {}
        
        # 最後の実行日をチェック
        last_execution = history.get("last_execution")
        if last_execution == today:
            logger.warning("本日は既に実行済みです")
            print("エラー: 本日は既に実行済みです。")
            print("次回の実行は明日以降にしてください。")
            sys.exit(1)
        
        # 実行履歴を更新
        history["last_execution"] = today
        EXECUTION_HISTORY_FILE.parent.mkdir(exist_ok=True)
        with open(EXECUTION_HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
        
        logger.info(f"実行履歴を更新しました: {today}")
    except Exception as e:
        logger.error(f"実行制限チェック中にエラーが発生しました: {e}")
        raise


def load_env_credentials():
    """環境変数から認証情報を読み込む"""
    import dotenv
    
    dotenv.load_dotenv()
    username = dotenv.get_key("../.env", "USERNAME")
    password = dotenv.get_key("../.env", "PASSWORD")
    
    if not username or not password:
        raise ValueError("環境変数 USERNAME または PASSWORD が設定されていません")
    
    return username, password


def create_output_directory():
    """出力ディレクトリを作成"""
    from config import OUTPUT_DIR
    OUTPUT_DIR.mkdir(exist_ok=True)
    return OUTPUT_DIR


def deduplicate_assignments(assignments):
    """課題の重複を除去し、期限順にソートする"""
    unique_assignments = []
    seen = set()
    for assignment in assignments:
        key = f"{assignment.get('subject')}_{assignment.get('name')}"
        if key not in seen:
            seen.add(key)
            unique_assignments.append(assignment)
    
    # 期限順にソート
    unique_assignments.sort(key=lambda x: x.get('availability_period_to', '9999/99/99 99:99'))
    
    return unique_assignments


def calculate_urgency(due_date_str):
    """期限から緊急度を計算する"""
    try:
        due_dt = datetime.strptime(due_date_str, "%Y/%m/%d %H:%M")
        now = datetime.now()
        days_left = (due_dt - now).days
        
        if days_left <= 3:
            return "urgent"
        elif days_left <= 7:
            return "warning"
        else:
            return "normal"
    except:
        return "normal" 

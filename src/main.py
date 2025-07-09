"""
WebClassクライアント メインスクリプト
"""
import sys
from datetime import datetime
from pathlib import Path

# ローカルモジュールのインポート
from webclass_client import WebClassClient
from webclass_client.logger_setup import setup_logger
from config import (
    WEBCLASS_URL, OUTPUT_DIR, LOG_FILE, HTML_OUTPUT_FILE, 
    DEBUG_LOG_FILE, DEFAULT_DATE
)
from utils import (
    check_execution_limit, load_env_credentials, 
    create_output_directory
)
from html_generator import generate_html


def main():
    """メイン処理"""
    # ロガーの設定
    logger = setup_logger(__name__, log_file=LOG_FILE)
    
    try:
        # 出力ディレクトリの作成
        create_output_directory()
        
        # 実行制限のチェック
        check_execution_limit(logger)
        
        # 認証情報の読み込み
        try:
            username, password = load_env_credentials()
        except ValueError as e:
            logger.error(str(e))
            print("エラー: 環境変数が設定されていません。")
            print(".envファイルを確認してください。")
            sys.exit(1)

        # WebClassクライアントの初期化とログイン
        with WebClassClient(WEBCLASS_URL, debug_mode=False) as client:
            client.set_login_info(username, password)
        
            if not client.login():
                logger.error("ログインに失敗しました")
                print("ログインに失敗しました。")
                sys.exit(1)
            
            logger.info("WebClassへのログインが完了しました")
            
            # データの取得
            logger.info("課題情報を取得中...")
            assignment_info = client.get_assignment_info(datetime.now())
            logger.info(f"課題情報を取得しました: {len(assignment_info)}件")

            logger.info("お知らせ情報を取得中...")
            messages_with_subject = get_all_messages(client)
            logger.info(f"お知らせを取得しました: {len(messages_with_subject)}件")
            
            # HTML生成と保存
            logger.info("HTMLファイルを生成中...")
            html_content = generate_html(assignment_info, messages_with_subject, logger)
            
            with open(HTML_OUTPUT_FILE, "w", encoding="utf-8") as f:
                f.write(html_content)

            logger.info(f"HTMLファイルを生成しました: {HTML_OUTPUT_FILE}")
            print("HTMLファイルの生成が完了しました。")
            print(f"出力先: {HTML_OUTPUT_FILE}")

    except KeyboardInterrupt:
        logger.info("ユーザーによって処理が中断されました")
        print("\n処理が中断されました。")
        sys.exit(0)
    except Exception as e:
        logger.error(f"予期せぬエラーが発生しました: {e}")
        print("エラーが発生しました。")
        print("詳細はログファイルを確認してください。")
        sys.exit(1)


def get_all_messages(client):
    """全講義のメッセージを取得する"""
    messages_with_subject = []
    
    try:
        lecture_ids = client.get_lecture_id_list()
        
        for lecture_id in lecture_ids:
            try:
                subject = client.get_lecture_name(lecture_id)
                messages = client.get_lecture_message(lecture_id, DEFAULT_DATE)
                for message in messages:
                    messages_with_subject.append((subject, message))
            except Exception as e:
                # 個別の講義で失敗しても続行
                client.logger.warning(f"講義ID {lecture_id} のメッセージ取得に失敗: {e}")
                continue
                
    except Exception as e:
        client.logger.error(f"講義メッセージの取得中にエラーが発生しました: {e}")
        raise
    
    return messages_with_subject


if __name__ == "__main__":
    main()

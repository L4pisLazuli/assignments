"""
WebClassクライアントのメインクラス
"""
from .logger_setup import setup_logger
from .session_manager import SessionManager
from .lectures import get_lecture_id_list, get_lecture_info, get_lecture_name
from .assignments import get_assignment_info
from .messages import get_lecture_message


class WebClassClient:
    """WebClassとの通信を行うクライアントクラス"""
    
    def __init__(self, url, debug_mode=False):
        """
        初期化
        
        Args:
            url: WebClassのURL
            debug_mode: デバッグモード
        """
        self.url = url
        self.login_info = {"username": "", "val": ""}
        self.session_manager = SessionManager()
        self.acs = {"acs_": "12345678"}
        self.cookie = None
        self.debug_mode = debug_mode
        self.logger = setup_logger(__name__, debug_mode=debug_mode)
        self._is_logged_in = False

    def set_login_info(self, username, password):
        """ログイン情報を設定"""
        if not username or not password:
            raise ValueError("ユーザー名とパスワードは必須です")
        
        self.login_info["username"] = username
        self.login_info["val"] = password

    def set_wbt_session(self, wbt_session):
        """WBTセッションを設定"""
        self.cookie = self.session_manager.set_wbt_session(wbt_session, self.logger)

    def login(self):
        """ログイン処理"""
        try:
            session, acs, cookie = self.session_manager.login(
                self.url, self.login_info, self.logger
            )
            if session is not None:
                self.acs = acs
                self.cookie = cookie
                self._is_logged_in = True
                self.logger.info("ログインに成功しました")
                return True
            else:
                self.logger.error("ログインに失敗しました")
                return False
        except Exception as e:
            self.logger.error(f"ログイン処理中にエラーが発生しました: {e}")
            return False

    def logout(self):
        """ログアウト処理"""
        try:
            result = self.session_manager.logout(self.url, self.logger)
            if result:
                self._is_logged_in = False
                self.logger.info("ログアウトしました")
            return result
        except Exception as e:
            self.logger.error(f"ログアウト処理中にエラーが発生しました: {e}")
            return False

    def _check_login_status(self):
        """ログイン状態をチェック"""
        if not self._is_logged_in:
            raise RuntimeError("ログインしていません。先にlogin()を呼び出してください。")

    def get_lecture_id_list(self):
        """講義IDリストを取得"""
        self._check_login_status()
        return get_lecture_id_list(
            self.url, self.acs, self.cookie, 
            self.session_manager.session, self.logger
        )

    def get_lecture_info(self, lecture_id):
        """講義情報を取得"""
        self._check_login_status()
        return get_lecture_info(
            self.url, lecture_id, self.acs, self.cookie, 
            self.session_manager.session, self.logger
        )

    def get_lecture_name(self, lecture_id):
        """講義名を取得"""
        self._check_login_status()
        return get_lecture_name(
            self.url, lecture_id, self.acs, self.cookie, 
            self.session_manager.session, self.logger
        )

    def get_assignment_info(self, date="2000-01-01"):
        """課題情報を取得"""
        self._check_login_status()
        return get_assignment_info(
            self.url, self.acs, self.cookie, 
            self.session_manager.session, date, self.logger
        )

    def get_lecture_message(self, lecture_id, date="2000-01-01"):
        """講義メッセージを取得"""
        self._check_login_status()
        return get_lecture_message(
            self.url, lecture_id, self.acs, self.cookie, 
            self.session_manager.session, date, self.logger
        )

    def __enter__(self):
        """コンテキストマネージャーのエントリー"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """コンテキストマネージャーの終了処理"""
        if self._is_logged_in:
            self.logout()

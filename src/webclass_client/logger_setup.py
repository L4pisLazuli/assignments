"""
ロギング設定モジュール
"""
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logger(name, log_file=None, debug_mode=False):
    """
    統一されたロガー設定
    
    Args:
        name: ロガー名
        log_file: ログファイルパス（Noneの場合はデフォルト）
        debug_mode: デバッグモード
    """
    logger = logging.getLogger(name)
    
    # 既にハンドラーが設定されている場合はスキップ
    if logger.handlers:
        return logger
    
    # ログレベル設定
    log_level = logging.DEBUG if debug_mode else logging.INFO
    logger.setLevel(log_level)
    
    # ファイルハンドラー
    if log_file:
        log_file = Path(log_file)
        log_file.parent.mkdir(exist_ok=True)
        
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=1024*1024,  # 1MB
            backupCount=3,
            encoding='utf-8'
        )
        file_handler.setLevel(log_level)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    # コンソールハンドラー
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter('%(levelname)s: %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # 親ロガーへの伝播を無効化
    logger.propagate = False
    
    return logger
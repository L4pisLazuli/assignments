# WebClass クライアント

## 概要

WebClass（大学のLMS）から課題・お知らせ情報を自動取得し、HTML形式で出力するPythonクライアントです。

- ログイン情報は.envファイルで管理
- 1日1回の実行制限機能あり
- 出力は `output/` ディレクトリにHTML・ログ等を生成
- コードは `src/` 配下に整理

---

## ディレクトリ構成

```
assignments/
├── src/
│   ├── main.py                # メインスクリプト
│   ├── config.py              # 設定管理
│   ├── utils.py               # 共通ユーティリティ
│   ├── html_generator.py      # HTML生成
│   └── webclass_client/       # パッケージ本体
│       ├── __init__.py
│       ├── client.py
│       ├── logger_setup.py
│       ├── messages.py
│       ├── assignments.py
│       ├── lectures.py
│       └── session_manager.py
├── output/                    # 生成物・ログ・履歴
├── tests/                     # テストコード用（空）
├── requirements.txt           # 依存パッケージ
├── README.md                  # このファイル
├── get_webclass_info.bat      # バッチ起動用
└── .gitignore
```

---

## セットアップ手順

1. **依存パッケージのインストール**

```bash
pip install -r requirements.txt
```

2. **.envファイルの作成**

srcフォルダ内に `.env` ファイルを作成し、以下の内容を記載してください：

```
USERNAME=あなたのWebClassユーザー名
PASSWORD=あなたのWebClassパスワード
```

3. **実行方法**

```bash
cd src
python main.py
```

または、ルートのバッチファイルからも起動可能です：
get_webclass_info.bat内の以下の部分を編集してください
```bash
cd PATH_TO_THIS_DIRECTORY
```
以下のコマンドで実行します
```bash
./get_webclass_info.bat
```

---

## 主な機能

- WebClassへの自動ログイン・課題/お知らせの取得
- 取得データのHTML出力（output/webclass_info.html）
- ログファイル出力（output/webclass.log）
- 実行履歴・一時ファイルは隠しファイル化
- モジュール分割による高い保守性

---

## 注意事項

- Python 3.8以上推奨
- .envファイルの管理に注意してください（Git管理対象外推奨）
- output/配下のファイルは都度上書きされます
- セットアップ時に失敗し、実行制限に引っかかる場合はoutputフォルダを削除し、再度お試しください

---

## ライセンス

MIT License

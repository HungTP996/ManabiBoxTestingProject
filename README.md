.env：URL や API キーなどの機密な環境変数を保存するファイル。必ず .gitignore に追加すること。
pytest.ini：pytest の設定ファイル。テストの検出方法や実行方法をここでカスタマイズできる。
config/：プロジェクトの各種設定をまとめるディレクトリ。
    + init.py：settings.py など必要なモジュールを読み込む。
    + settings.py：.env から変数を読み取り、アプリケーションに提供するファイル。
    + tests/：すべてのテストを配置するディレクトリ。
    + conftest.py：全テストで共有するフィクスチャを定義するファイル。app_settings フィクスチャをここに置き、必要に応じて他のフィクスチャも追加する。

# 実施前に

# 仮想環境を作成
python3 -m venv venv

# 仮想環境を有効化
source venv/Scripts/activate

# テストライブラリをインストール
pip install -r requirements.txt

# Allure の設定
1. PowerShell を開きます。
2. 以下のコマンドを実行して、PowerShell がインストールスクリプトを実行できるようにします。
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
3. 次に、以下のコマンドを実行して Scoop をインストールします。
irm get.scoop.sh | iex
4. Allure をインストールします。
scoop install allure
5. Allure のインストールを確認します。
allure --version

# 全てのテストを実行
pytest

# 特定のテストファイルを実行
pytest tests/frontend/test_*.py

# 特定のテスト関数を実行
pytest tests/frontend/test_*.py -k "test_*"

# 仮想環境を停止
deactivate
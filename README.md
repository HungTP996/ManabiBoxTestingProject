# ディレクトリ構造 :
```
my_project/
├── .env
├── .gitignore
├── pytest.ini
├── config/
│   ├── __init__.py
│   └── settings.py
├── src/
│   ├── __init__.py
│   └── my_app.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── frontend/
    │   ├── __init__.py
    │   └── test_manabibox_page.py
    └── backend/
        ├── __init__.py
        └── test_api.py
```

my_project/: Thư mục gốc của dự án./プロジェクトルート
.env: File chứa các biến môi trường nhạy cảm như URL, API keys. File này phải được thêm vào .gitignore.
.env：URL や API キーなどの機密な環境変数を保存するファイル。必ず .gitignore に追加すること。
pytest.ini: File cấu hình cho pytest. Bạn có thể tùy chỉnh cách pytest tìm kiếm và chạy các bài kiểm thử tại đây.
pytest.ini：pytest の設定ファイル。テストの検出方法や実行方法をここでカスタマイズできる。
config/: Thư mục chứa các thiết lập cấu hình của dự án.
config/：プロジェクトの各種設定をまとめるディレクトリ。
    + __init__.py: Load những module cần thiết bên trong như settings.py
    + init.py：settings.py など必要なモジュールを読み込む。
    + settings.py: File đọc các biến từ .env và cung cấp chúng cho ứng dụng.
    + settings.py：.env から変数を読み取り、アプリケーションに提供するファイル。
    + tests/: Thư mục chứa tất cả các bài kiểm thử.
    + tests/：すべてのテストを配置するディレクトリ。
    + conftest.py: File chứa các fixtures được chia sẻ cho toàn bộ các bài kiểm thử. Đây là nơi bạn sẽ đặt fixture app_settings và có thể là các fixture khác nếu cần.
    + conftest.py：全テストで共有するフィクスチャを定義するファイル。app_settings フィクスチャをここに置き、必要に応じて他のフィクスチャも追加する。
    + frontend/: Thư mục dành riêng cho các bài kiểm thử frontend, sử dụng Playwright.
    + frontend/：Playwright を用いたフロントエンド向けテスト用ディレクトリ。
    + backend/: Thư mục dành riêng cho các bài kiểm thử backend, ví dụ như kiểm thử API
    + backend/：バックエンド向けテスト（例：API テスト）用ディレクトリ。**必要だがない**

# 実施前に
```
# tạo môi trường ảo/仮想環境を作成（例: フォルダ名を .venv に）
python3 -m venv venv

# connect vào môi trường ảo/有効化
source venv/Scripts/activate

# install thư viện test
pip install -r requirements.txt


# chạy test toàn bộ
pytest

# chạy test FE
pytest tests/frontend/

# Chạy test file riêng
pytest tests/frontend/test_google_page.py

# chạy cụ thể 1 function
pytest tests/frontend/test_google_page.py -k "test_google_search_page_title"

# để stop môi trường
deactivate

# --alluredir=./allure-results
```

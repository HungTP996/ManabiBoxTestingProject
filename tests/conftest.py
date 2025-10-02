# conftest.py
import os
from typing import Any, Generator
import pytest
import json
import google.generativeai as genai
from PIL import Image
from playwright.sync_api import Page, expect, Browser, BrowserContext
from config import settings

# =============================================================================
# Pytest Hooks (pytestフック)
# =============================================================================

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    各テストの実行結果（成功、失敗、スキップ）を item オブジェクトに保存するフック。
    失敗時のスクリーンショット取得などで利用します。
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

def pytest_make_parametrize_id(config, val, argname):
    """
    パラメータ化テストのテストIDをカスタマイズするフック。
    レポートに見やすい名前を表示します。
    """
    if argname == "test_case" and isinstance(val, dict):
        return val.get("test_id") or val.get("description")
    return None

# =============================================================================
# Browser Fixtures (ブラウザ関連のフィクスチャ)
# =============================================================================

@pytest.fixture(scope="class")
def browser_context(browser: Browser) -> Generator[BrowserContext, Any, None]:
    context = browser.new_context()
    yield context
    context.close()


@pytest.fixture(scope="class")
def page(browser_context: BrowserContext) -> Generator[Page, Any, None]:
    page = browser_context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="class")
def page_on_failure(page: Page, request):
    """
    テスト失敗時に自動でスクリーンショットを保存する機能を追加したページフィクスチャ。
    """
    yield page

    # `rep_call` 属性の存在を確認してからアクセスする
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        screenshots_dir = "screenshots"
        # screenshotsディレクトリがなければ作成
        os.makedirs(screenshots_dir, exist_ok=True)

        screenshot_path = os.path.join(
            screenshots_dir, f"{request.node.name}_FAILURE.png"
        )
        try:
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"\n📸 スクリーンショットを保存しました: {screenshot_path}")
        except Exception as e:
            print(f"\n🚨 スクリーンショットの保存に失敗しました: {e}")


@pytest.fixture(scope="class")
def logged_in_page(page_on_failure: Page) -> Page:
    """
    アプリケーションにログイン済みの状態のページを提供するフィクスチャ。
    クラスごとに一度だけログイン処理を実行します。
    """
    page = page_on_failure
    print(f"\n--- [CLASS SCOPE] ログイン処理を開始します ---")

    page.goto(settings.BASE_URL, timeout=60000)
    pw_input = page.get_by_role("textbox", name="パスワード")
    pw_input.fill(settings.PASSWORD)
    pw_input.press("Enter")

    # ログイン成功の検証
    expect(page.get_by_alt_text("まなびボックス")).to_be_visible(timeout=15000)
    print("--- [CLASS SCOPE] ログインに成功しました ---")

    yield page

    print("\n--- [CLASS SCOPE] ログインフィクスチャを終了します ---")


# =============================================================================
# AI Verification Fixture (AI検証フィクスチャ)
# =============================================================================

@pytest.fixture(scope="session")
def ai_vision_verifier():
    """
    AIによる画像検証機能を提供します。
    テストセッション全体でモデルのセットアップを一度だけ行います。
    """
    print("\n--- [SESSION SCOPE] AI Vision Verifierを初期化中 ---")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        pytest.fail("GEMINI_API_KEYが見つかりません。.envファイルを確認してください。")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 検証用の内部関数を定義して返す
    def _verify(screenshot_path: str, expected_char: str) -> bool:
        """指定された画像の文字が期待値と一致するかをAIで検証します。"""
        print(f"\n--- 画像 '{screenshot_path}' をAIに送信して分析中... ---")
        try:
            image = Image.open(screenshot_path)
            prompt = f"Is the character in this image the Japanese for '{expected_char}'? Answer only YES or NO."
            # 日本語でプロンプトを記述する場合：
            # prompt = f"この画像に写っている文字は日本語の「{expected_char}」ですか？「はい」か「いいえ」だけで答えてください。"

            response = model.generate_content([prompt, image])
            ai_answer = response.text.strip().upper()

            print(f"-> AIからの応答: '{ai_answer}'")
            return ai_answer == "YES"

        except Exception as e:
            pytest.fail(f"AI APIの呼び出し中にエラーが発生しました: {e}")
            return False

    # テストが呼び出せるように_verify関数自体を返す
    yield _verify

# =============================================================================
# Json fixture
# =============================================================================

@pytest.fixture(scope="session")
def kokugo_test_data():
    """Fixture này tải toàn bộ dữ liệu từ file data.json."""
    file_path = "tests/kokugo/data.json" # Đảm bảo đường dẫn chính xác
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data
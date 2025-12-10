# conftest.py
import os
from typing import Any, Generator
import pytest
import json
import google.generativeai as genai
from PIL import Image
from pathlib import Path
from playwright.sync_api import Page, expect, Browser, BrowserContext
from config import settings


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


# パラメータ化されたテストのIDを生成
def pytest_make_parametrize_id(config, val, argname):
    if argname == "test_case" and isinstance(val, dict):
        return val.get("test_id") or val.get("description")
    return None


# ブラウザコンテキストをクラススコープで作成・破棄
@pytest.fixture(scope="class")
def browser_context(browser: Browser) -> Generator[BrowserContext, Any, None]:
    context = browser.new_context()
    yield context
    context.close()


# ページオブジェクトをクラススコープで作成・破棄
@pytest.fixture(scope="class")
def page(browser_context: BrowserContext) -> Generator[Page, Any, None]:
    page = browser_context.new_page()
    yield page
    page.close()


# テスト失敗時にスクリーンショットを撮るフィクスチャ
@pytest.fixture(scope="class")
def page_on_failure(page: Page, request):
    yield page

    # テストが失敗した場合
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        screenshots_dir = "screenshots"
        os.makedirs(screenshots_dir, exist_ok=True)

        screenshot_path = os.path.join(
            screenshots_dir, f"{request.node.name}_FAILURE.png"
        )
        try:
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"\n📸 スクリーンショットを保存しました: {screenshot_path}")
        except Exception as e:
            print(f"\n🚨 スクリーンショットの保存に失敗しました: {e}")


# ログイン済みのページを提供するフィクスチャ (クラススコープ)
@pytest.fixture(scope="class")
def logged_in_page(page_on_failure: Page) -> Page:

    page = page_on_failure
    print(f"\n--- [CLASS SCOPE] ログイン処理を開始します ---")

    page.goto(settings.BASE_URL, timeout=60000)
    pw_input = page.get_by_role("textbox", name="パスワード") # パスワード入力フィールド
    pw_input.fill(settings.PASSWORD)
    pw_input.press("Enter") # Enterキーを押してログイン

    # ログイン成功の確認 (例: 特定の要素の表示を待つ)
    expect(page.get_by_alt_text("まなびボックス")).to_be_visible(timeout=15000)
    print("--- [CLASS SCOPE] ログインに成功しました ---")

    yield page

    print("\n--- [CLASS SCOPE] ログインフィクスチャを終了します ---")


# AI (Gemini) を使用した画像検証機能を提供するフィクスチャ (セッションスコープ)
@pytest.fixture(scope="session")
def ai_vision_verifier():
    print("\n--- [SESSION SCOPE] AI Vision Verifierを初期化中 ---")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        pytest.fail("GEMINI_API_KEYが見つかりません。.envファイルを確認してください。")

    genai.configure(api_key=api_key)
    # 画像解析に適したモデルを使用
    model = genai.GenerativeModel('gemini-1.5-flash')

    # 検証用の内部関数を定義して返す
    def _verify(screenshot_path: str, expected_char: str) -> bool:
        print(f"\n--- 画像 '{screenshot_path}' をAIに送信して分析中... ---")
        try:
            image = Image.open(screenshot_path)
            # AIへのプロンプト
            prompt = f"Is the character in this image the Japanese for '{expected_char}'? Answer only YES or NO."

            response = model.generate_content([prompt, image])
            ai_answer = response.text.strip().upper()

            print(f"-> AIからの応答: '{ai_answer}'")
            return ai_answer == "YES"

        except Exception as e:
            pytest.fail(f"AI APIの呼び出し中にエラーが発生しました: {e}")
            return False

    yield _verify


@pytest.fixture(scope="session")
def kokugo_test_data():
    current_dir = Path(__file__).parent
    file_path = current_dir / "kokugo" / "data.json"
    print(f"--> Đang đọc file data tại: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data
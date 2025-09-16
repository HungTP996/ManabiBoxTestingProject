# conftest.py
import pytest
import os
import google.generativeai as genai
from playwright.sync_api import Page, expect, Browser, BrowserContext
from PIL import Image
from config import settings

# Hook để lấy kết quả test (giữ nguyên)
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

# ===================================================================
# ============================== AMEDESUYO ==========================
# ===================================================================

# Bước 1: Tạo browser context với phạm vi "class"
@pytest.fixture(scope="class")
def browser_context(browser: Browser):
    context = browser.new_context()
    yield context
    context.close()

# Bước 2: Tạo page từ browser context, cũng với phạm vi "class"
@pytest.fixture(scope="class")
def page(browser_context: BrowserContext):
    # Tạo một trang mới cho lớp test
    page = browser_context.new_page()
    yield page
    page.close()

# Bước 3: Fixture chụp ảnh màn hình, giờ đây sẽ dùng page có scope="class"
@pytest.fixture(scope="class")
def page_on_failure(page: Page, request):
    yield page

    # THAY ĐỔI CHÍNH NẰM Ở ĐÂY
    # Kiểm tra xem 'rep_call' có tồn tại không trước khi truy cập
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        # Tạo thư mục screenshots nếu chưa có
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")
        screenshot_path = os.path.join("screenshots", f"{request.node.name}_FAILURE.png")
        try:
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"\n📸 スクリーンショットを保存しました: {screenshot_path}")
        except Exception as e:
            print(f"\n🚨 スクリーンショットの保存に失敗しました: {e}")

# Bước 4: Fixture đăng nhập, dùng page_on_failure (đã có scope="class")
@pytest.fixture(scope="class")
def logged_in_page(page_on_failure: Page) -> Page:
    page = page_on_failure
    print(f"\n--- [CLASS SCOPE] ログイン処理を開始します ---")
    page.goto(settings.BASE_URL, timeout=60000)
    pw_input = page.get_by_role("textbox", name="パスワード")
    pw_input.fill(settings.PASSWORD)
    pw_input.press("Enter")
    expect(page.get_by_alt_text("まなびボックス")).to_be_visible(timeout=15000)
    yield page
    print("\n--- [CLASS SCOPE] ログインフィクスチャを終了します ---")

# Hook để đặt tên cho report (giữ nguyên)
def pytest_make_parametrize_id(config, val, argname):
    if argname == "test_case" and isinstance(val, dict):
        return val.get("test_id") or val.get("description")
    return None


@pytest.fixture(scope="session")
def ai_vision_verifier():
    """
    Fixture này cung cấp một hàm có khả năng xác minh hình ảnh bằng AI.
    Nó chỉ thiết lập model một lần duy nhất cho toàn bộ phiên test.
    """
    print("\n--- [SESSION SCOPE] Khởi tạo AI Vision Verifier ---")
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        pytest.fail("GEMINI_API_KEY không được tìm thấy. Vui lòng kiểm tra file .env.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Định nghĩa một hàm nội bộ và trả về nó
    def _verify(screenshot_path: str, expected_char: str) -> bool:
        print(f"\n--- Gửi ảnh '{screenshot_path}' cho AI để phân tích... ---")
        try:
            image = Image.open(screenshot_path)
            prompt = f"Is the character in this image the Japanese hiragana for '{expected_char}'? Answer only YES or NO."

            response = model.generate_content([prompt, image])
            ai_answer = response.text.strip().upper()

            print(f"-> Phản hồi từ AI: '{ai_answer}'")
            return ai_answer == "YES"
        except Exception as e:
            pytest.fail(f"Lỗi khi gọi API của AI: {e}")
            return False

    # Trả về chính hàm _verify để các bài test có thể gọi nó
    yield _verify
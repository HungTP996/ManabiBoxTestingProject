import pytest
from playwright.sync_api import Page, expect
import os

@pytest.fixture(scope="function")
def kanji_go_quiz_page(logged_in_page: Page):
    """
    Fixture này thực hiện toàn bộ quá trình để vào bài làm của chữ "五".
    """
    page = logged_in_page
    print("\n--- [SETUP] Bắt đầu điều hướng đến bài làm chữ '五' ---")
    page.get_by_alt_text("漢字").click()
    go_button_in_list = page.get_by_text("五 ", exact=True)
    expect(go_button_in_list).to_be_visible(timeout=10000)
    go_button_in_list.click()
    page.get_by_text("つぎにすすむ").click()
    expect(page.locator(".kanji-canvas.upper-canvas")).to_be_visible()
    print("--- [SETUP] Đã vào màn hình vẽ, sẵn sàng cho test ---")
    yield page
class TestGo:
    def test_kanji_go_drawing_and_ai_verification(self, kanji_go_quiz_page: Page, ai_vision_verifier):
        """
        Test kịch bản: Vẽ chữ "五", sau đó xác minh bằng AI.
        """
        page = kanji_go_quiz_page
        for i in range(3):
            print(f"\n--> Bắt đầu lần vẽ và xác minh thứ {i + 1}")
            drawing_canvas = page.locator(".kanji-canvas.upper-canvas")
            expect(drawing_canvas).to_be_visible()
            expect(drawing_canvas).to_be_enabled()
            page.wait_for_timeout(10000) 

            canvas_box = drawing_canvas.bounding_box()
            origin_x, origin_y = canvas_box['x'], canvas_box['y']
            page.mouse.move(origin_x + 102, origin_y + 88)
            page.mouse.down()
            page.mouse.move(origin_x + 170, origin_y + 89)
            page.mouse.move(origin_x + 223, origin_y + 76)
            page.mouse.up()
            page.mouse.move(origin_x + 163, origin_y + 85)
            page.mouse.down()
            page.mouse.move(origin_x + 117, origin_y + 238)
            page.mouse.up()
            page.mouse.move(origin_x + 95, origin_y + 163)
            page.mouse.down()
            page.mouse.move(origin_x + 150, origin_y + 150)
            page.mouse.move(origin_x + 208, origin_y + 152)
            page.mouse.move(origin_x + 210, origin_y + 155)
            page.mouse.move(origin_x + 205, origin_y + 155)
            page.mouse.move(origin_x + 205, origin_y + 235)
            page.mouse.up()
            page.mouse.move(origin_x + 45, origin_y + 245)
            page.mouse.down()
            page.mouse.move(origin_x + 280, origin_y + 235)
            page.mouse.up()
            print("--- Vẽ xong! ---")
            canvas_to_verify = page.locator("canvas").nth(2)
            folder_name = "ai_screenshots"
            os.makedirs(folder_name, exist_ok=True)
            screenshot_path = os.path.join(folder_name, f"go_drawing_to_verify_{i + 1}.png")
            canvas_to_verify.screenshot(path=screenshot_path)
            print(f"-> Đã chụp ảnh bảng vẽ và lưu tại: {screenshot_path}")

            is_correct = ai_vision_verifier(screenshot_path=screenshot_path, expected_char="五")
            assert is_correct, f"AI không nhận diện đúng ký tự '五' ở lần lặp thứ {i + 1}."
            print("-> AI đã xác nhận hình vẽ chính xác!")

            # --- Chuyển tiếp ---
            page.get_by_text("つけ", exact=True).click()
            expect(page.get_by_alt_text("level return")).to_be_visible()
            page.get_by_text("つぎにすすむ").click()

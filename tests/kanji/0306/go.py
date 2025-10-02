import pytest
from playwright.sync_api import Page, expect
import os

# ===================================================================
# == FIXTURE SETUP: Chuẩn bị môi trường cho bài test ==
# ===================================================================
@pytest.fixture(scope="function")
def kanji_go_quiz_page(logged_in_page: Page):
    """
    Fixture này thực hiện toàn bộ quá trình để vào bài làm của chữ "五".
    """
    page = logged_in_page
    print("\n--- [SETUP] Bắt đầu điều hướng đến bài làm chữ '五' ---")
    # Bước 1: Click vào môn "漢字"
    page.get_by_alt_text("漢字").click()
    # Chờ cho trang Kanji tải xong (kiểm tra sự hiện diện của nút "五")
    go_button_in_list = page.get_by_text("五 ", exact=True)
    expect(go_button_in_list).to_be_visible(timeout=10000)
    # Bước 2: Click vào chữ "五" để vào xem chi tiết
    go_button_in_list.click()
    # Bước 3: Click "つぎにすすむ" để vào màn hình vẽ
    page.get_by_text("つぎにすすむ").click()
    # Chờ màn hình vẽ xuất hiện
    expect(page.locator(".kanji-canvas.upper-canvas")).to_be_visible()
    print("--- [SETUP] Đã vào màn hình vẽ, sẵn sàng cho test ---")
    yield page

# ===================================================================
# == LỚP TEST: Chứa các kịch bản test cho chữ "五" ==
# ===================================================================
class TestGo:

    # THÊM `ai_vision_verifier` VÀO DANH SÁCH THAM SỐ
    def test_kanji_go_drawing_and_ai_verification(self, kanji_go_quiz_page: Page, ai_vision_verifier):
        """
        Test kịch bản: Vẽ chữ "五", sau đó xác minh bằng AI.
        """
        page = kanji_go_quiz_page
        for i in range(3):
            print(f"\n--> Bắt đầu lần vẽ và xác minh thứ {i + 1}")

            # Lấy locator của bảng vẽ và tọa độ
            drawing_canvas = page.locator(".kanji-canvas.upper-canvas")
            expect(drawing_canvas).to_be_visible()
            expect(drawing_canvas).to_be_enabled()
            page.wait_for_timeout(10000)  # Chờ 1 giây là đủ

            canvas_box = drawing_canvas.bounding_box()
            origin_x, origin_y = canvas_box['x'], canvas_box['y']

            # --- Nét ①: Nét ngang trên cùng ---
            page.mouse.move(origin_x + 102, origin_y + 88)
            page.mouse.down()
            page.mouse.move(origin_x + 170, origin_y + 89)
            page.mouse.move(origin_x + 223, origin_y + 76)
            page.mouse.up()
            # --- Nét ②: Nét sổ dọc ---
            page.mouse.move(origin_x + 163, origin_y + 85)
            page.mouse.down()
            page.mouse.move(origin_x + 117, origin_y + 238)
            page.mouse.up()
            # --- Nét ③: Nét ngang gập ---
            page.mouse.move(origin_x + 95, origin_y + 163)
            page.mouse.down()
            page.mouse.move(origin_x + 150, origin_y + 150)
            page.mouse.move(origin_x + 208, origin_y + 152)
            page.mouse.move(origin_x + 210, origin_y + 155)
            page.mouse.move(origin_x + 205, origin_y + 155)
            page.mouse.move(origin_x + 205, origin_y + 235)
            page.mouse.up()
            # --- Nét ④: Nét ngang dưới cùng (Nét "đóng") ---
            page.mouse.move(origin_x + 45, origin_y + 245)
            page.mouse.down()
            page.mouse.move(origin_x + 280, origin_y + 235)
            page.mouse.up()
            print("--- Vẽ xong! ---")
            canvas_to_verify = page.locator("canvas").nth(2)
            folder_name = "ai_screenshots"
            os.makedirs(folder_name, exist_ok=True)
            # Thay đổi tên file cho mỗi lần lặp để không bị ghi đè
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

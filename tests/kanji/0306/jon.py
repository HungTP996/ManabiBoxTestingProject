import pytest
from playwright.sync_api import Page, expect
import os

# ===================================================================
# == FIXTURE SETUP: Chuẩn bị môi trường cho bài test ==
# ===================================================================
@pytest.fixture(scope="function")
def kanji_go_quiz_page(logged_in_page: Page):
    """
    Fixture này thực hiện toàn bộ quá trình để vào bài làm của chữ "四 ".
    """
    page = logged_in_page
    print("\n--- [SETUP] Bắt đầu điều hướng đến bài làm chữ '四 ' ---")
    # Bước 1: Click vào môn "漢字"
    page.get_by_alt_text("漢字").click()
    # Chờ cho trang Kanji tải xong (kiểm tra sự hiện diện của nút "四 ")
    go_button_in_list = page.get_by_text("四  ", exact=True)
    expect(go_button_in_list).to_be_visible(timeout=10000)
    # Bước 2: Click vào chữ "四 " để vào xem chi tiết
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
    def test_kanji_jon_drawing_and_ai_verification(self, kanji_go_quiz_page: Page, ai_vision_verifier):
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

            # --- Nét ①: Nét dọc ---
            page.mouse.move(origin_x + 63, origin_y + 106)
            page.mouse.down()
            page.mouse.move(origin_x + 73, origin_y + 240)
            page.mouse.up()
            # --- Nét ②: Nét ngang gập ---
            page.mouse.move(origin_x + 60, origin_y + 110)
            page.mouse.down()
            page.mouse.move(origin_x + 222, origin_y + 92)
            page.mouse.move(origin_x + 264, origin_y + 92)
            # page.mouse.move(origin_x + 265, origin_y + 93)
            page.mouse.move(origin_x + 264, origin_y + 94)
            page.mouse.move(origin_x + 264, origin_y + 95)
            page.mouse.move(origin_x + 250, origin_y + 230)
            page.mouse.up()
            # --- Nét ③: nét sổ trái
            page.mouse.move(origin_x + 135, origin_y + 100)
            page.mouse.down()
            page.mouse.move(origin_x + 130, origin_y + 125)
            page.mouse.move(origin_x + 125, origin_y + 150)
            page.mouse.move(origin_x + 105, origin_y + 185)
            page.mouse.move(origin_x + 75, origin_y + 200)
            page.mouse.up()
            # --- Nét ④: nét sổ vòng cung sang phải ---
            page.mouse.move(origin_x + 175, origin_y + 100)
            page.mouse.down()
            page.mouse.move(origin_x + 175, origin_y + 125)
            page.mouse.move(origin_x + 185, origin_y + 170)
            page.mouse.move(origin_x + 195, origin_y + 170)
            page.mouse.move(origin_x + 255, origin_y + 170)
            page.mouse.up()
            # --- Nét ⑤: Nét ngang dưới cùng (Nét "đóng") ---
            page.mouse.move(origin_x + 74, origin_y + 238)
            page.mouse.down()
            page.mouse.move(origin_x + 250, origin_y + 230)
            page.mouse.up()
            print("--- Vẽ xong! ---")
            canvas_to_verify = page.locator("canvas").nth(2)
            folder_name = "ai_screenshots"
            os.makedirs(folder_name, exist_ok=True)
            # Thay đổi tên file cho mỗi lần lặp để không bị ghi đè
            screenshot_path = os.path.join(folder_name, f"jon_drawing_to_verify_{i + 1}.png")
            canvas_to_verify.screenshot(path=screenshot_path)
            print(f"-> Đã chụp ảnh bảng vẽ và lưu tại: {screenshot_path}")

            is_correct = ai_vision_verifier(screenshot_path=screenshot_path, expected_char="四")
            assert is_correct, f"AI không nhận diện đúng ký tự '四' ở lần lặp thứ {i + 1}."
            print("-> AI đã xác nhận hình vẽ chính xác!")

            # --- Chuyển tiếp ---
            page.get_by_text("つけ", exact=True).click()
            expect(page.get_by_alt_text("level return")).to_be_visible()
            page.get_by_text("つぎにすすむ").click()

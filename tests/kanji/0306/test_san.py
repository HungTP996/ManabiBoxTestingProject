import pytest
from playwright.sync_api import Page, expect
import os

# ===================================================================
# == FIXTURE SETUP: Chuẩn bị môi trường cho bài test ==
# ===================================================================
@pytest.fixture(scope="function")
def kanji_go_quiz_page(logged_in_page: Page):
    """
    Fixture này thực hiện toàn bộ quá trình để vào bài làm của chữ "三 ".
    """
    page = logged_in_page
    print("\n--- [SETUP] Bắt đầu điều hướng đến bài làm chữ '三 ' ---")
    # Bước 1: Click vào môn "漢字"
    page.get_by_alt_text("漢字").click()
    # Chờ cho trang Kanji tải xong (kiểm tra sự hiện diện của nút "三  ")
    go_button_in_list = page.get_by_text("三  ", exact=True)
    expect(go_button_in_list).to_be_visible(timeout=10000)
    # Bước 2: Click vào chữ "三 " để vào xem chi tiết
    go_button_in_list.click()
    # Bước 3: Click "つぎにすすむ" để vào màn hình vẽ
    page.get_by_text("つぎにすすむ").click()
    # Chờ màn hình vẽ xuất hiện
    expect(page.locator(".kanji-canvas.upper-canvas")).to_be_visible()
    print("--- [SETUP] Đã vào màn hình vẽ, sẵn sàng cho test ---")
    yield page

# ===================================================================
# == LỚP TEST: Chứa các kịch bản test cho chữ "三 " ==
# ===================================================================

class TestGo:
    def test_kanji_go_drawing_only(self, kanji_go_quiz_page: Page):
        """
        Test kịch bản: Vẽ chữ "三 " và điều hướng qua các bước (bỏ qua xác minh AI).
        """
        page = kanji_go_quiz_page
        for i in range(3):
            print(f"\n--> Bắt đầu lần vẽ và xác minh thứ {i + 1}")

            # Lấy locator của bảng vẽ và tọa độ
            drawing_canvas = page.locator(".kanji-canvas.upper-canvas")
            expect(drawing_canvas).to_be_visible()
            expect(drawing_canvas).to_be_enabled()
            page.wait_for_timeout(5000)

            canvas_box = None
            for _ in range(5):
                canvas_box = drawing_canvas.bounding_box()
                if canvas_box:
                    break
                page.wait_for_timeout(200)
            assert canvas_box, "Không lấy được bounding_box của canvas"
            origin_x, origin_y = canvas_box["x"], canvas_box["y"]

            # --- Nét ①: Nét ngang trên cùng ---
            page.mouse.move(origin_x + 88, origin_y + 88)
            page.mouse.down()
            page.mouse.move(origin_x + 224, origin_y + 78)
            page.mouse.up()
            # --- Nét ②: Nét sổ dọc ---
            page.mouse.move(origin_x + 88, origin_y + 165)
            page.mouse.down()
            page.mouse.move(origin_x + 220, origin_y + 155)
            page.mouse.up()
            # --- Nét ③: Nét ngang gập ---
            page.mouse.move(origin_x + 42, origin_y + 248)
            page.mouse.down()
            page.mouse.move(origin_x + 100, origin_y + 240)
            page.mouse.move(origin_x + 220, origin_y + 230)
            page.mouse.move(origin_x + 280, origin_y + 240)
            page.mouse.up()

            print("--- Vẽ xong! ---")
            canvas_to_verify = page.locator(".kanji-canvas.upper-canvas").first
            folder_name = "ai_screenshots"
            os.makedirs(folder_name, exist_ok=True)
            # Thay đổi tên file cho mỗi lần lặp để không bị ghi đè
            screenshot_path = os.path.join(folder_name, f"go_drawing_to_verify_{i + 1}.png")
            expect(canvas_to_verify).to_be_visible(timeout=10000)
            canvas_to_verify.scroll_into_view_if_needed()
            canvas_to_verify.screenshot(path=screenshot_path)
            print(f"-> Đã chụp ảnh bảng vẽ và lưu tại: {screenshot_path}")

            # --- Chuyển tiếp ---
            submit_btn = page.get_by_text("つけ").first
            expect(submit_btn).to_be_visible(timeout=10000)
            expect(submit_btn).to_be_enabled(timeout=10000)
            submit_btn.click()
            expect(page.get_by_alt_text("level return")).to_be_visible()
            page.get_by_text("つぎにすすむ").click()

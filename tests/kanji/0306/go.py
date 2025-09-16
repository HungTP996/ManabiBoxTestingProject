import pytest
from playwright.sync_api import Page, expect
import time

# ===================================================================
# == FIXTURE SETUP ==
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
    go_button_in_list = page.get_by_text("五", exact=True)
    expect(go_button_in_list).to_be_visible()

    # Bước 2: Click vào chữ "五" để vào xem chi tiết
    go_button_in_list.click()

    # Bước 3: Click "つぎにすすむ" để vào màn hình vẽ
    page.get_by_text("つぎにすすむ").click()

    # Chờ màn hình vẽ xuất hiện
    expect(page.locator(".kanji-canvas.upper-canvas")).to_be_visible()

    print("--- [SETUP] Đã vào màn hình vẽ, sẵn sàng cho test ---")
    yield page

# ===================================================================
# == LỚP TEST ==
# ===================================================================

class TestGo:
    def test_kanji_go(self, kanji_go_quiz_page: Page):
        """
        Test kịch bản: Vẽ lại chữ "五" lên canvas.
        """
        # 'page' bây giờ đã ở sẵn màn hình vẽ nhờ fixture
        page = kanji_go_quiz_page

        # Lấy locator của bảng vẽ và tọa độ của nó
        drawing_canvas = page.locator(".kanji-canvas.upper-canvas")
        expect(drawing_canvas).to_be_visible()
        expect(drawing_canvas).to_be_enabled()
        page.wait_for_timeout(5000) # Chờ một chút để canvas sẵn sàng
        canvas_box = drawing_canvas.bounding_box()
        origin_x, origin_y = canvas_box['x'], canvas_box['y']

        print("\n--- Bắt đầu vẽ chữ「五」---")

        # --- Nét ①: Nét ngang trên cùng ---
        print("--> Đang vẽ nét ngang trên...")
        page.mouse.move(origin_x + 102, origin_y + 88)
        page.mouse.down()
        page.mouse.move(origin_x + 170, origin_y + 89)
        page.mouse.move(origin_x + 223, origin_y + 76)
        page.mouse.up()

        # --- Nét ②: Nét sổ dọc ---
        print("--> Đang vẽ nét sổ dọc...")
        page.mouse.move(origin_x + 163, origin_y + 85)
        page.mouse.down()
        page.mouse.move(origin_x + 117, origin_y + 238)
        page.mouse.up()

        # --- Nét ③: Nét ngang gập ---
        print("--> Đang vẽ nét ngang gập...")
        page.mouse.move(origin_x + 95, origin_y + 163)
        page.mouse.down()
        page.mouse.move(origin_x + 223, origin_y + 150)
        page.mouse.move(origin_x + 223, origin_y + 150)
        page.mouse.move(origin_x + 210, origin_y + 155)
        page.mouse.move(origin_x + 223, origin_y + 238) # Gập góc và kéo thẳng xuống
        page.mouse.up()

        # --- Nét ④: Nét ngang dưới cùng (Nét "đóng") ---
        print("--> Đang vẽ nét đóng...")
        page.mouse.move(origin_x + 40, origin_y + 240)
        page.mouse.down()
        page.mouse.move(origin_x + 200, origin_y + 250)
        page.mouse.up()

        print("--- Vẽ xong! ---")

        # Tạm dừng 3 giây để bạn có thể xem kết quả
        time.sleep(50)
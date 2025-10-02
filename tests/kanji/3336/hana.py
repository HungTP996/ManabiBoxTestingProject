import pytest
from playwright.sync_api import Page, expect
import time

@pytest.fixture(scope="function")
def kanji_hana_quiz_page(logged_in_page: Page):
    """
    Fixture này thực hiện toàn bộ quá trình để vào bài làm của chữ "花".
    """
    page = logged_in_page
    print("\n--- [SETUP] Bắt đầu điều hướng đến bài làm chữ '花' ---")

    # Bước 1: Click vào môn "漢字"
    page.get_by_alt_text("漢字").click()

    # Chờ cho trang Kanji tải xong (kiểm tra sự hiện diện của nút "花")
    hana_button_in_list = page.get_by_text("花", exact=True)
    expect(hana_button_in_list).to_be_visible()

    # Bước 2: Click vào chữ "花" để vào xem chi tiết
    hana_button_in_list.click()

    # Bước 3: Click "つぎにすすむ" để vào màn hình vẽ
    page.get_by_text("つぎにすすむ").click()

    # Chờ màn hình vẽ xuất hiện
    expect(page.locator(".kanji-canvas.upper-canvas")).to_be_visible()

    print("--- [SETUP] Đã vào màn hình vẽ, sẵn sàng cho test ---")
    yield page

# ===================================================================
# == LỚP TEST ==
# ===================================================================

class TestKanjiNoHanashiTopic:

    def test_kanji_hana_full_workflow(self, kanji_hana_quiz_page: Page):
        """
        Test kịch bản: Vẽ lại chữ "花" lên canvas.
        """
        # 'page' bây giờ đã ở sẵn màn hình vẽ nhờ fixture
        page = kanji_hana_quiz_page
        print("\n--- Bắt đầu kịch bản vẽ chữ '花' ---")

        # Lấy locator của bảng vẽ và tọa độ của nó
        drawing_canvas = page.locator(".kanji-canvas.upper-canvas")
        expect(drawing_canvas).to_be_visible()
        expect(drawing_canvas).to_be_enabled()
        page.wait_for_timeout(5000)
        canvas_box = drawing_canvas.bounding_box()
        origin_x, origin_y = canvas_box['x'], canvas_box['y']

        print("--> Bắt đầu vẽ chữ Hán '花'...")
        # Phần trên: Bộ Thảo (艹)
        page.mouse.move(origin_x + 62, origin_y + 88)
        page.mouse.down()
        page.mouse.move(origin_x + 243, origin_y + 77)
        page.mouse.up()
        page.wait_for_timeout(500)
        page.mouse.move(origin_x + 112, origin_y + 35)
        page.mouse.down()
        page.mouse.move(origin_x + 115, origin_y + 117)
        page.mouse.up()
        page.wait_for_timeout(500)
        page.mouse.move(origin_x + 200, origin_y + 32)
        page.mouse.down()
        page.mouse.move(origin_x + 170, origin_y + 110)
        page.mouse.up()
        page.wait_for_timeout(500)
        # Phần dưới: Chữ Hóa (化)
        page.mouse.move(origin_x + 112, origin_y + 135)
        page.mouse.down()
        page.mouse.move(origin_x + 110, origin_y + 150)
        page.mouse.move(origin_x + 95, origin_y + 183)
        page.mouse.move(origin_x + 90, origin_y + 190)
        page.mouse.move(origin_x + 51, origin_y + 234)
        page.mouse.up()

        page.wait_for_timeout(500)
        page.mouse.move(origin_x + 92, origin_y + 185)
        page.mouse.down()
        page.mouse.move(origin_x + 100, origin_y + 210)
        page.mouse.move(origin_x + 105, origin_y + 220)
        page.mouse.move(origin_x + 98, origin_y + 285)
        page.mouse.up()

        page.wait_for_timeout(7000)
        page.mouse.move(origin_x + 238, origin_y + 135)
        page.mouse.down()
        page.mouse.move(origin_x + 220, origin_y + 150)
        page.mouse.move(origin_x + 205, origin_y + 165)
        page.mouse.move(origin_x + 185, origin_y + 175)
        page.mouse.move(origin_x + 178, origin_y + 180)
        page.mouse.up()

        page.wait_for_timeout(500)
        page.mouse.move(origin_x + 178, origin_y + 120)
        page.mouse.down()
        page.mouse.move(origin_x + 170, origin_y + 275)
        page.mouse.move(origin_x + 277, origin_y + 275)
        page.mouse.move(origin_x + 277, origin_y + 275)
        page.mouse.move(origin_x + 287, origin_y + 275)
        page.mouse.move(origin_x + 283, origin_y + 240)
        page.mouse.up()
        page.wait_for_timeout(500)
        print("--- Vẽ xong! ---")
        time.sleep(300)


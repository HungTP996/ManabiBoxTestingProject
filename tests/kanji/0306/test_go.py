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
    def _draw_kanji(self, page: Page, origin_x: float, origin_y: float):
        """Hàm hỗ trợ vẽ các nét chữ '五'"""
        # Nét 1
        page.mouse.move(origin_x + 102, origin_y + 88)
        page.mouse.down()
        page.mouse.move(origin_x + 170, origin_y + 89)
        page.mouse.move(origin_x + 223, origin_y + 76)
        page.mouse.up()
        
        # Nét 2
        page.mouse.move(origin_x + 163, origin_y + 85)
        page.mouse.down()
        page.mouse.move(origin_x + 117, origin_y + 238)
        page.mouse.up()
        
        # Nét 3
        page.mouse.move(origin_x + 95, origin_y + 163)
        page.mouse.down()
        page.mouse.move(origin_x + 150, origin_y + 150)
        page.mouse.move(origin_x + 208, origin_y + 152)
        page.mouse.move(origin_x + 210, origin_y + 155)
        page.mouse.move(origin_x + 205, origin_y + 155)
        page.mouse.move(origin_x + 205, origin_y + 235)
        page.mouse.up()
        
        # Nét 4
        page.mouse.move(origin_x + 45, origin_y + 245)
        page.mouse.down()
        page.mouse.move(origin_x + 280, origin_y + 235)
        page.mouse.up()

    def test_kanji_go_drawing_flow_only(self, kanji_go_quiz_page: Page):
        """
        Test kịch bản: Vẽ chữ "五" và điều hướng qua các bước (Bỏ qua xác minh AI).
        """
        page = kanji_go_quiz_page
        
        for i in range(3):
            print(f"\n--> Bắt đầu lần vẽ thứ {i + 1}")
            drawing_canvas = page.locator(".kanji-canvas.upper-canvas")
            expect(drawing_canvas).to_be_visible()
            expect(drawing_canvas).to_be_enabled()
            page.wait_for_timeout(5000)
            
            # Lấy tọa độ gốc (đợi bounding_box sẵn sàng)
            canvas_box = None
            for _ in range(5):
                canvas_box = drawing_canvas.bounding_box()
                if canvas_box:
                    break
                page.wait_for_timeout(200)
            assert canvas_box, "Không lấy được bounding_box của canvas"
            origin_x, origin_y = canvas_box["x"], canvas_box["y"]

            # Thực hiện vẽ
            self._draw_kanji(page, origin_x, origin_y)
            print("--- Vẽ xong! ---")

            # Chờ một chút để nét vẽ hiển thị rõ ràng trước khi chụp (optional)
            page.wait_for_timeout(500)

            # Chụp ảnh màn hình (chỉ để lưu lại làm bằng chứng/debug, không verify)
            # Nếu canvas không sẵn sàng thì bỏ qua, tránh chặn flow
            canvas_to_verify = page.locator(".kanji-canvas.upper-canvas").first
            if canvas_to_verify.count() > 0:
                folder_name = "debug_screenshots"
                os.makedirs(folder_name, exist_ok=True)
                screenshot_path = os.path.join(folder_name, f"go_drawing_step_{i + 1}.png")
                try:
                    canvas_to_verify.scroll_into_view_if_needed()
                    canvas_to_verify.screenshot(path=screenshot_path)
                    print(f"-> Đã lưu ảnh vẽ tại: {screenshot_path}")
                except Exception as e:
                    print(f"-> Bỏ qua chụp ảnh (canvas không sẵn sàng): {e}")
            else:
                print("-> Bỏ qua chụp ảnh (không tìm thấy canvas)")

            # --- Chuyển tiếp (Logic game) ---
            # Click nút xác nhận/nộp bài (tuỳ thuộc vào UI game hiển thị nút gì sau khi vẽ)
            # Nút xác nhận có thể thay đổi nhẹ text, nên không ép exact
            submit_btn = page.get_by_text("つけ").first
            expect(submit_btn).to_be_visible(timeout=10000)
            expect(submit_btn).to_be_enabled(timeout=10000)
            print("-> Nút 'つけ' đã sẵn sàng, tiến hành click")
            submit_btn.click()
            
            # Đảm bảo chuyển cảnh thành công
            expect(page.get_by_alt_text("level return")).to_be_visible()
            
            page.get_by_text("つぎにすすむ").click()
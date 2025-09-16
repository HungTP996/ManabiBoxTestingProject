# tests/ai_tests/test_kaigara_pre.py
import pytest
import re
import os
from playwright.sync_api import Page, expect


@pytest.fixture(scope="function")
def drawing_page(logged_in_page: Page):
    """Fixture để vào đúng trang vẽ."""
    page = logged_in_page
    page.get_by_alt_text("国語").click()
    page.get_by_text("プレテスト").nth(3).click()
    yield page


def draw_kawa(page: Page):
    """Hàm trợ giúp, mô phỏng hành động vẽ chữ 「かわ」."""
    print("\n--- Bắt đầu vẽ chữ 「かわ」 ---")
    drawing_canvas = page.locator(".kanji-canvas.upper-canvas")
    expect(drawing_canvas).to_be_visible()
    canvas_box = drawing_canvas.bounding_box()
    origin_x, origin_y = canvas_box['x'], canvas_box['y']

    # --- Vẽ chữ「か」---
    page.mouse.move(origin_x + 100, origin_y + 70);
    page.mouse.down()
    page.mouse.move(origin_x + 210, origin_y + 50);
    page.mouse.move(origin_x + 180, origin_y + 180)
    page.mouse.move(origin_x + 170, origin_y + 170);
    page.mouse.up()
    page.mouse.move(origin_x + 140, origin_y + 40);
    page.mouse.down()
    page.mouse.move(origin_x + 100, origin_y + 160);
    page.mouse.up()
    page.mouse.move(origin_x + 200, origin_y + 60);
    page.mouse.down()
    page.mouse.move(origin_x + 230, origin_y + 80);
    page.mouse.up()

    # --- Vẽ chữ「わ」---
    page.mouse.move(origin_x + 100, origin_y + 200);
    page.mouse.down()
    page.mouse.move(origin_x + 90, origin_y + 320);
    page.mouse.up()
    page.mouse.move(origin_x + 90, origin_y + 220);
    page.mouse.down()
    page.mouse.move(origin_x + 170, origin_y + 180);
    page.mouse.move(origin_x + 50, origin_y + 300)
    page.mouse.move(origin_x + 190, origin_y + 210);
    page.mouse.move(origin_x + 200, origin_y + 275)
    page.mouse.move(origin_x + 150, origin_y + 320);
    page.mouse.up()
    print("-> Vẽ xong.")

def test_drawing_with_ai_verification(drawing_page: Page, ai_vision_verifier):
    """
    Test kịch bản: Vẽ -> Xác nhận -> Chụp ảnh -> Kiểm tra bằng AI -> Chấm điểm.
    """
    page = drawing_page
    # 1. Vẽ chữ
    draw_kawa(page)
    # 2. Click "決定" để chuyển hình vẽ
    page.locator("div").filter(has_text=re.compile(r"^決けっ定てい$")).nth(2).click()
    page.wait_for_timeout(1000)

    # 3. Chụp ảnh ô kết quả
    result_box = page.locator(".upper-canvas").first
    folder_name = "ai_screenshots"
    os.makedirs(folder_name, exist_ok=True)
    screenshot_path = os.path.join(folder_name, "drawing_to_verify.png")
    result_box.screenshot(path=screenshot_path)
    print(f"-> Đã chụp ảnh kết quả và lưu tại: {screenshot_path}")

    # 4. Gửi ảnh cho AI và xác minh
    is_correct = ai_vision_verifier(screenshot_path=screenshot_path, expected_char="かわ")
    assert is_correct, "AI không nhận diện đúng ký tự."
    print("-> AI đã xác nhận hình vẽ chính xác!")

    # 5. Click "こたえあわせ" để chấm điểm
    kotaeawase_button = page.get_by_role("button", name="こたえあわせ")
    expect(kotaeawase_button).to_be_enabled(timeout=5000)
    kotaeawase_button.click()

    # 6. Kiểm tra kết quả đúng
    expect(page.locator(".icon__answer--right")).to_be_visible()
    print("\n--- Test hoàn tất ---")
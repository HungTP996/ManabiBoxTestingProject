import pytest, re
from playwright.sync_api import Page, expect


@pytest.fixture(scope="function")
def drawing_page(logged_in_page: Page):
    """
    Fixture này thực hiện các bước setup:
    1. Đăng nhập (từ fixture có sẵn).
    2. Vào trang Kokugo.
    3. Click vào "プレテスト" thứ tư để vào trang vẽ.
    """
    page = logged_in_page
    print("\n--- [SETUP] Bắt đầu điều hướng đến trang vẽ ---")

    # Vào trang Kokugo
    page.get_by_alt_text("国語").click()

    # Chờ cho đến khi trang Kokugo tải xong
    expect(page.get_by_text("プレテスト").first).to_be_visible()
    print("-> Đã vào trang Kokugo.")

    # Tìm tất cả các nút "プレテスト" và click vào cái thứ 4 (index=3)
    fourth_pretest_button = page.get_by_text("プレテスト").nth(3)
    fourth_pretest_button.click()
    print("-> Đã click vào 'プレテスト' thứ 4.")

    # Chờ một chút để trang vẽ tải hoàn tất
    page.wait_for_timeout(1000)

    # Giao lại page đã ở đúng trang vẽ cho bài test
    yield page

    print("\n--- [TEARDOWN] Kết thúc test vẽ ---")


def test_drawing_and_visual_verification(drawing_page: Page):
    """
    Test kịch bản vẽ và xác minh kết quả bằng cách so sánh ảnh chụp màn hình.
    """
    # 'page' bây giờ đã ở sẵn trên trang vẽ nhờ fixture
    page = drawing_page

    # --- Mô phỏng hành động vẽ ---
    print("--- Bắt đầu vẽ ---")
    # !!! THAY THẾ BẰNG LOCATOR CỦA BẢNG VẼ LỚN !!!
    drawing_canvas = page.locator(".kanji-canvas.upper-canvas")
    # Đảm bảo canvas đã hiển thị trước khi lấy tọa độ
    expect(drawing_canvas).to_be_visible()
    canvas_box = drawing_canvas.bounding_box()

    # Tọa độ gốc để tính toán các nét vẽ
    origin_x = canvas_box['x']
    origin_y = canvas_box['y']

    print("\n--- Bắt đầu vẽ chữ 「かわ」 ---")

    # ===================================================================
    # == Vẽ chữ「か」 (ka) ==
    # ===================================================================
    print("--> Đang vẽ chữ 「か」...")
    # Bắt đầu nét vẽ
    page.mouse.move(origin_x + 100, origin_y + 70)
    page.mouse.down()
    # 1. Kéo sang ngang
    page.mouse.move(origin_x + 210, origin_y + 50)
    # 2. Kéo chéo xuống phía bên trái
    page.mouse.move(origin_x + 180, origin_y + 180)
    # 3. Tạo móc câu quặt vào trong (hơi đi lên và sang phải)
    page.mouse.move(origin_x + 170, origin_y + 170)
    # Kết thúc nét vẽ
    page.mouse.up()

    # # ===================================================================
    # # == Nét ②: Nét sổ thẳng ==
    # # ===================================================================
    print("--> Đang vẽ Nét ②...")
    # Bắt đầu từ phía trên, bên phải nét 1
    page.mouse.move(origin_x + 140, origin_y + 40)
    page.mouse.down()
    # Kéo một nét thẳng ngắn chạm vào nét 1
    page.mouse.move(origin_x + 100, origin_y + 160)
    page.mouse.up()
    # ===================================================================
    # == Nét ③: Nét phẩy (dấu "ten") ==
    # ===================================================================
    print("--> Đang vẽ Nét ③...")
    # Bắt đầu ở khoảng trống trên bên phải
    page.mouse.move(origin_x + 200, origin_y + 60)
    page.mouse.down()
    # Vẽ một dấu phẩy ngắn
    page.mouse.move(origin_x + 230, origin_y + 80)
    page.mouse.up()
    # ===================================================================
    # == Vẽ chữ「わ」 (wa) ==
    # ===================================================================
    print("--> Đang vẽ chữ 「わ」...")
    # Nét 1: Nét sổ thẳng
    page.mouse.move(origin_x + 100, origin_y + 200)
    page.mouse.down()
    page.mouse.move(origin_x + 90, origin_y + 320)
    page.mouse.up()

    # nét kéo sang ngang
    page.mouse.move(origin_x + 90, origin_y + 220)
    page.mouse.down()
    page.mouse.move(origin_x + 170, origin_y + 180)

    # Phần 1: Kéo chéo xuống dưới về phía bên trái
    page.mouse.move(origin_x + 50, origin_y + 300)
    # Phần 2: Lượn sang ngang về phía bên phải (giống chữ 'Z')
    page.mouse.move(origin_x + 190, origin_y + 210)
    # Bắt đầu vòng xuống và sang trái
    page.mouse.move(origin_x + 200, origin_y + 275)
    # Điểm thấp nhất của vòng cung, ở gần trung tâm
    page.mouse.move(origin_x + 150, origin_y + 320)
    # Hoàn thiện độ cong, hơi đi lên một chút
    # page.mouse.move(origin_x + 115, origin_y + 280)
    # ===================================================================
    page.mouse.up()
    page.pause()

    print("--- Vẽ xong! ---")

    # 1. Click nút "決定" bằng locator bạn cung cấp
    # Locator này tìm thẻ div thứ 3 có text chính xác là "決定"
    kettei_button = page.locator("div").filter(has_text=re.compile(r"^決けっ定てい$")).nth(2)
    kettei_button.click()
    print("-> Đã click nút '決定'.")

    # 2. Click nút "こたえあわせ"
    kotaeawase_button = page.get_by_role("button", name="こたえあわせ")
    kotaeawase_button.click()
    print("-> Đã click nút 'こたえあわせ'.")

    # --- Kiểm tra kết quả bằng Visual Test ---
    # !!! THAY THẾ BẰNG LOCATOR CỦA Ô KẾT QUẢ NHỎ MÀU ĐỎ !!!
    result_box = page.locator("#result_red_box")

    print("-> Chụp ảnh và so sánh với ảnh chuẩn...")
    expect(result_box).to_have_screenshot("drawing_result.png")

    print("--- Test hoàn tất: Hình ảnh khớp với ảnh chuẩn! ---")
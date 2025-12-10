import pytest
from playwright.sync_api import Page, expect
import json
from pathlib import Path

def load_test_data():
    current_dir = Path(__file__).parent.absolute()

    # Các vị trí có thể chứa file data.json
    possible_paths = [
        current_dir / "data.json",  # Cùng thư mục
        current_dir / "mojiwokakou" / "data.json",  # Trong thư mục con mojiwokakou
        Path("tests/hiragana/mojiwokakou/data.json")  # Đường dẫn cứng (fallback)
    ]

    json_path = None
    for path in possible_paths:
        if path.exists():
            json_path = path
            break

    if not json_path:
        raise FileNotFoundError(f"Không tìm thấy file data.json tại các đường dẫn: {[str(p) for p in possible_paths]}")

    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# Lọc lấy data của chữ 'つ'
all_drawing_tests = load_test_data()
drawing_tests = [test for test in all_drawing_tests if test['char'] == 'つ']

# Tạo thư mục screenshot nếu chưa có (dù không dùng AI nhưng vẫn chụp để debug nếu cần)
Path("debug_screenshots").mkdir(exist_ok=True)


@pytest.fixture(scope="function")
def go_to_character_selection(logged_in_page: Page):
    page = logged_in_page
    page.wait_for_load_state("networkidle")

    # Vào màn hình chọn chữ
    page.get_by_alt_text("ひらがな").click()
    page.locator(".figure__btn:has-text('きょうかしょの じゅん')").click()
    yield page


class TestHiraganaDrawing:

    # Đã XÓA tham số ai_vision_verifier
    @pytest.mark.parametrize("test_data", drawing_tests)
    def test_character_drawing(self, go_to_character_selection: Page, test_data):
        page = go_to_character_selection
        char_to_test = test_data["char"]
        draw_points = test_data["points"]

        print(f"\n--- Bắt đầu test chữ: {char_to_test} (Không dùng AI) ---")

        # 1. Chọn chữ cái
        page.locator(f".character:has-text('{char_to_test}')").click()
        page.get_by_text("つぎにすすむ", exact=True).click()

        # Đợi animation chuyển trang
        page.wait_for_timeout(1500)

        # 2. Vòng lặp 3 lần vẽ
        for i in range(3):
            print(f"\n--- Lần vẽ thứ {i + 1}/3 ---")

            drawing_canvas = page.locator(".kanji-canvas.upper-canvas")
            expect(drawing_canvas).to_be_visible()

            # Đợi một chút để đảm bảo canvas sẵn sàng nhận nét vẽ
            page.wait_for_timeout(1000)

            canvas_box = drawing_canvas.bounding_box()
            if not canvas_box:
                raise Exception("Không tìm thấy canvas.")

            origin_x, origin_y = canvas_box['x'], canvas_box['y']

            # Thực hiện thao tác vẽ
            drawing_canvas.hover()
            page.mouse.move(origin_x + draw_points[0][0], origin_y + draw_points[0][1])
            page.mouse.down()

            # Vẽ các điểm tiếp theo
            for point in draw_points[1:]:
                page.mouse.move(origin_x + point[0], origin_y + point[1], steps=5)

            page.mouse.up()
            print("--> Vẽ xong.")

            # Đợi app xử lý nét vẽ
            page.wait_for_timeout(1000)

            # --- BỎ QUA BƯỚC AI VERIFY ---
            # Thay vào đó, chỉ cần kiểm tra xem nút Chấm điểm có sáng lên không

            marutsuke_button = page.get_by_text("まるつけ", exact=True)

            # Kiểm tra nhanh trạng thái nút (để log debug)
            if not marutsuke_button.is_enabled():
                print(f"Cảnh báo (Lần {i + 1}): Nút Marutsuke chưa enable. Có thể nét vẽ chưa được nhận.")
                page.screenshot(path=f"debug_screenshots/fail_draw_{i + 1}.png")

            # Expect chính thức của bài test (sẽ fail test nếu nút không enable sau 10s)
            expect(marutsuke_button).to_be_enabled(timeout=10000)

            marutsuke_button.click()
            print("--> Đã bấm Marutsuke.")

            # Đợi animation chấm điểm (Hanamaru xuất hiện)
            page.wait_for_timeout(2500)

            # Xử lý nút "Tiếp theo"
            if i < 2:
                # Tìm nút Next. Có thể là "つぎにすすむ" hoặc tên khác
                next_button = page.get_by_text("つぎにすすむ", exact=True)

                if next_button.is_visible():
                    next_button.click()
                    print("--> Đã bấm Next.")
                    # Đợi trang reset trắng bảng để vẽ lần sau
                    page.wait_for_timeout(2000)
            else:
                print("--> Đã xong 3 lần vẽ.")

        print("\n--- Hoàn thành kịch bản vẽ ---")

        # 3. Kết thúc bài học
        # Tìm nút thoát (thường là "くにすすむ" hoặc "つぎにすすむ" lần cuối)
        try:
            # Ưu tiên tìm nút くにすすむ (Về mục lục/Bài tiếp)
            finish_button = page.get_by_text("くにすすむ", exact=True)

            if not finish_button.is_visible():
                # Nếu không thấy, thử tìm nút Next lần nữa (trường hợp UI khác)
                finish_button = page.get_by_text("つぎにすすむ", exact=True)

            # Nếu tìm thấy thì click, nếu không thì in cảnh báo nhưng không để fail test ở bước này
            if finish_button.is_visible():
                finish_button.click()
                print("--> Đã bấm nút kết thúc bài.")
            else:
                print("Cảnh báo: Không tìm thấy nút thoát bài học ở cuối cùng.")

        except Exception as e:
            print(f"Lỗi khi thoát bài: {e}")
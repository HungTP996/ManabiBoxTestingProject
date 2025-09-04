# tests/kokugo/test_ha_wo_tsukaou.py

import pytest
from playwright.sync_api import Page, expect
from .kokugo_test_data import QUESTIONS_DATA_HA_WO_TSUKAOU


@pytest.fixture(scope="class")
def kokugo_main_page(logged_in_page: Page):
    """
    Fixture này chạy 1 lần duy nhất: Đăng nhập và vào trang môn học Kokugo.
    """
    page = logged_in_page
    print("\n--- [CLASS SETUP] Đăng nhập và vào trang Kokugo ---")
    page.get_by_alt_text("国語").click()
    expect(page.get_by_text("あめですよ").first).to_be_visible()
    yield page


@pytest.fixture(scope="function")
def quiz_session(kokugo_main_page: Page):
    """
    Fixture này chạy TRƯỚC và SAU mỗi hàm test.
    Setup: Từ trang Kokugo, click vào chủ đề để vào màn hình làm bài.
    Teardown (Tùy chọn): Có thể thêm các bước dọn dẹp ở đây.
    """
    page = kokugo_main_page
    # --- PHẦN SETUP (Chạy trước mỗi test) ---
    print(f"\n--- [FUNCTION SETUP] Vào màn hình làm bài của chủ đề 'はを つかおう' ---")
    topic_container = page.locator("p:has-text('はを　つかおう')").locator("..")
    topic_container.get_by_alt_text("basic").click()

    yield page  # Giao quyền cho hàm test

    # --- PHẦN TEARDOWN (Chạy sau mỗi test) ---
    # Sau khi mỗi kịch bản (đúng/sai) kết thúc, nó sẽ tự động ở trang Kokugo.
    # Không cần thêm teardown ở đây vì luồng test đã xử lý việc thoát ra.
    print(f"--- [FUNCTION TEARDOWN] Kết thúc một kịch bản ---")


# ===================================================================
# == LỚP TEST: Chứa các kịch bản test ==
# ===================================================================

class TestTopicHaWoTsukaou:

    def test_full_quiz_happy_path(self, quiz_session: Page):
        """
        Kịch bản 1: Trả lời đúng tuần tự từ câu 1 đến câu 5.
        """
        page = quiz_session
        print("\n--- Bắt đầu kịch bản trả lời đúng từ câu 1 đến 5 ---")

        for index, question in enumerate(QUESTIONS_DATA_HA_WO_TSUKAOU):
            question_type = question.get("type", "text")
            print(f"--> Đang thực hiện câu hỏi {question['id']} (Loại: {question_type})")

            # --- Xử lý câu hỏi chọn đáp án ---
            if question_type == "text":
                for answer in question["correct_answers"]:
                    page.get_by_text(answer, exact=True).click()

            # --- Xử lý câu hỏi điền vào chỗ trống ---
            elif question_type == "fill_blank":
                for action in question["correct_answers"]:
                    blank_box = page.locator(action["blank_locator"])
                    choice = page.get_by_text(action["choice_text"], exact=True)
                    blank_box.click()
                    choice.click()

            # --- Xử lý câu hỏi kéo thả ---
            elif question_type == "drag_drop":
                for drag_action in question["correct_drag_mapping"]:
                    item_text = question["items_to_drag"][drag_action["item"]]
                    zone_selector = question["drop_zones"][drag_action["zone"]]
                    drop_zone = page.locator(zone_selector).nth(0 if drag_action["zone"] == "zone1" else 1)
                    page.get_by_text(item_text).drag_to(drop_zone)

            # --- Các bước kiểm tra và chuyển tiếp ---
            page.get_by_role("button", name="こたえあわせ").click()
            # Thêm bước click vào overlay kết quả để đóng nó nếu cần
            # page.locator(".result-overlay").click()

            if index < len(QUESTIONS_DATA_HA_WO_TSUKAOU) - 1:
                page.get_by_role("button", name="つぎへ").click()
            else:
                # Luồng kết thúc bài làm
                review_button = page.get_by_role("button", name="ふりかえり")
                expect(review_button).to_be_visible()
                review_button.click()

                review_title = page.locator("p:has-text('ふりかえり')")
                expect(review_title).to_be_visible()

                finish_button = page.get_by_text("おわる", exact=True)
                expect(finish_button).to_be_visible()
                finish_button.click()

        print("--- Kịch bản ĐÚNG hoàn tất ---")
        expect(page.get_by_text("あめですよ").first).to_be_visible()

    def test_full_quiz_all_incorrect(self, quiz_session: Page):
        """
        Kịch bản 2: Trả lời sai tất cả các câu hỏi.
        """
        page = quiz_session
        print("\n--- Bắt đầu kịch bản trả lời sai ---")

        for index, question in enumerate(QUESTIONS_DATA_HA_WO_TSUKAOU):
            question_type = question.get("type", "text")
            print(f"--> Đang thực hiện câu hỏi {question['id']} (Trả lời SAI)")

            # --- Xử lý câu 1, 2, 3 (chọn đáp án SAI) ---
            if question_type == "text":
                incorrect_answer = question["incorrect_answers"][0]
                page.get_by_text(incorrect_answer, exact=True).click()

            # --- Xử lý câu 4 (điền vào chỗ trống SAI) ---
            elif question_type == "fill_blank":
                # Đọc từ kịch bản sai "incorrect_answers"
                for action in question["incorrect_answers"]:
                    blank_box = page.locator(action["blank_locator"])
                    choice = page.get_by_text(action["choice_text"], exact=True)
                    blank_box.click()
                    choice.click()

            # --- Xử lý câu 5 (kéo thả SAI) ---
            elif question_type == "drag_drop":
                # Đọc từ kịch bản sai "incorrect_drag_mapping"
                for drag_action in question["incorrect_drag_mapping"]:
                    item_text = question["items_to_drag"][drag_action["item"]]
                    zone_selector = question["drop_zones"][drag_action["zone"]]
                    drop_zone = page.locator(zone_selector).nth(0 if drag_action["zone"] == "zone1" else 1)
                    page.get_by_text(item_text).drag_to(drop_zone)

            # --- Các bước kiểm tra và chuyển tiếp ---
            page.get_by_role("button", name="こたえあわせ").click()

            # Kiểm tra kết quả là SAI
            expect(page.locator(".icon__answer--wrong")).to_be_visible()

            # Chuyển tiếp sau khi trả lời
            if index < len(QUESTIONS_DATA_HA_WO_TSUKAOU) - 1:
                page.get_by_role("button", name="つぎへ").click()
            else:
                # Luồng kết thúc (giống như trên)
                review_button = page.get_by_role("button", name="ふりかえり")
                expect(review_button).to_be_visible()
                review_button.click()
                review_title = page.locator("p:has-text('ふりかえり')")
                expect(review_title).to_be_visible()
                finish_button = page.get_by_text("おわる", exact=True)
                expect(finish_button).to_be_visible()
                finish_button.click()

        print("--- Kịch bản SAI hoàn tất ---")
        expect(page.get_by_text("あめですよ").first).to_be_visible()
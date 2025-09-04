import pytest
import random
from playwright.sync_api import Page, expect

@pytest.fixture(scope="class")
def kokugo_main_page(logged_in_page: Page):
    """
    Fixture này chạy 1 lần duy nhất cho cả lớp test:
    Đăng nhập -> Vào trang chủ đề Kokugo.
    """
    page = logged_in_page
    print("\n--- [CLASS SETUP] Đăng nhập và vào trang Kokugo ---")
    page.get_by_alt_text("国語").click()
    expect(page.get_by_text("とん　こと　とん")).to_be_visible()
    yield page

@pytest.fixture(scope="function")
def quiz_session(kokugo_main_page: Page):
    """
    Fixture này chạy TRƯỚC MỖI HÀM TEST.
    Nhiệm vụ: Từ trang Kokugo, click vào title để vào màn hình câu hỏi.
    """
    page = kokugo_main_page
    print("\n--- [METHOD SETUP] Vào màn hình làm bài ---")
    topic_title = page.locator("p:has-text('ぶんを　つくろう')")
    topic_container = topic_title.locator("..")
    topic_container.get_by_alt_text("basic").click()
    yield page
class TestTonkototon_Scenarios:

    QUESTIONS_DATA = [
        # --- Câu hỏi 1:
        {
            "id": 1, "type": "text",
            "correct_answers": ["およぐ"],
            "incorrect_answers": ["はねる", "たべる"]
        },
        # --- Câu hỏi 2:
        {
            "id": 2, "type": "text",
            "correct_answers": ["ねる"],
            "incorrect_answers": ["はしる", "たべる"]
        },
        # --- Câu hỏi 3:
        {
            "id": 3, "type": "text",
            "correct_answers": ["わらう"],
            "incorrect_answers": ["おこる", "あるく"]
        },
        # --- Câu hỏi 4 ---
        {
            "id": 4, "type": "text",
            "correct_answers": ["あめが　ふる。", "あじさいが　さく。"],
            "incorrect_answers": ["かさが　こわれる。", "かえるが　ねる。"]
        },
        # --- Câu hỏi 5 ---
        {
            "id": 5, "type": "text",
            "correct_answers": ["とりが　おどろく。", "とりが　わらう。"],
            "incorrect_answers": ["とりが　たべる。", "とりが　およぐ。"]
        },
    ]

    def test_scenario_all_correct(self, quiz_session: Page):
        """Kịch bản 1: Chọn TẤT CẢ các đáp án đúng cho mỗi câu hỏi."""
        page = quiz_session
        print("\n--- Bắt đầu kịch bản: Tất cả đều đúng ---")

        total_questions = len(self.QUESTIONS_DATA)
        for index, question in enumerate(self.QUESTIONS_DATA):
            print(f"--> Câu hỏi {question['id']}: Chọn các đáp án ĐÚNG")

            # Vòng lặp để click vào TẤT CẢ các đáp án đúng
            for answer in question["correct_answers"]:
                # Logic mới: Kiểm tra loại locator và dùng đúng phương thức
                if question["type"] == "text":
                    page.get_by_text(answer, exact=True).click()
                else:  # "css" hoặc "xpath"
                    page.locator(answer).click()

            page.get_by_role("button", name="こたえあわせ").click()
            expect(page.locator(".icon__answer--right")).to_be_visible()

            if index < total_questions - 1:
                page.get_by_role("button", name="つぎへ").click()
            else:
                print("--> Hoàn thành câu cuối, bắt đầu luồng kết thúc...")
                review_button = page.locator("button:has-text('ふりかえり')")
                review_button.wait_for(state="visible", timeout=10000)
                print("-> Nút 'ふりかえり' đã xuất hiện.")
                review_button.click()
                print("-> Đã click 'ふりかえり'")
                review_title = page.locator("p:has-text('ふりかえり')")
                expect(review_title).to_be_visible()
                print("-> Đã vào trang Review")
                finish_button = page.get_by_text("おわる", exact=True)
                expect(finish_button).to_be_visible()
                finish_button.click()
                print("-> Đã click 'おわる'")

        expect(page.get_by_text("とん　こと　とん")).to_be_visible()

    def test_scenario_all_incorrect(self, quiz_session: Page):
        """Kịch bản 2: Chọn MỘT đáp án sai cho mỗi câu hỏi."""
        page = quiz_session
        print("\n--- Bắt đầu kịch bản: Tất cả đều sai ---")

        total_questions = len(self.QUESTIONS_DATA)
        for index, question in enumerate(self.QUESTIONS_DATA):
            print(f"--> Câu hỏi {question['id']}: Chọn một đáp án SAI")
            random.seed(15)
            # Chỉ cần click vào đáp án sai ĐẦU TIÊN trong danh sách
            first_incorrect_answer = question["incorrect_answers"][0]
            # Logic mới: Kiểm tra loại locator và dùng đúng phương thức
            if question["type"] == "text":
                page.get_by_text(first_incorrect_answer, exact=True).click()
            else:  # "css" hoặc "xpath"
                page.locator(first_incorrect_answer).click()

            page.get_by_role("button", name="こたえあわせ").click()
            expect(page.locator(".icon__answer--wrong")).to_be_visible()

            if index < total_questions - 1:
                page.get_by_role("button", name="つぎへ").click()
            else:
                print("--> Hoàn thành câu cuối, bắt đầu luồng kết thúc...")
                review_button = page.locator("button:has-text('ふりかえり')")
                review_button.wait_for(state="visible", timeout=10000)
                review_button.click()
                review_title = page.locator("p:has-text('ふりかえり')")
                expect(review_title).to_be_visible()
                finish_button = page.get_by_text("おわる", exact=True)
                expect(finish_button).to_be_visible()
                finish_button.click()

        print("--- Kịch bản hoàn tất ---")
        expect(page.get_by_text("とん　こと　とん")).to_be_visible()
import pytest
from playwright.sync_api import Page, expect
from tests.kokugo.kokugo_data import QUESTIONS_DATA_WOHEWO


# ===================================================================
# == FIXTURE SETUP ==
# ===================================================================

@pytest.fixture(scope="class")
def quiz_session(logged_in_page: Page):
    """
    Fixture này chạy 1 lần: Đăng nhập -> Vào Kokugo -> Vào bài làm của chủ đề.
    """
    page = logged_in_page
    print("\n--- [CLASS SETUP] Bắt đầu phiên làm bài cho chủ đề 'をへを つかおう' ---")

    # Giả định đang ở menu chính, vào trang Kokugo
    page.get_by_alt_text("国語").click()

    # Bước 1 & 2: Xác nhận các tiêu đề và click vào chủ đề để bắt đầu
    expect(page.get_by_text("をへを　つかおう")).to_be_visible()
    topic_link = page.get_by_text("上P.54～55")
    expect(topic_link).to_be_visible()
    topic_link.click()

    yield page


# ===================================================================
# == LỚP TEST ==
# ===================================================================

class TestTopicWohewoTsukaou:
    """
    Lớp này chứa các kịch bản test cho chủ đề "をへを つかおう".
    """

    def test_both_scenarios_sequentially(self, quiz_session: Page):
        """
        Test này thực hiện một luồng liên tục:
        1. Chạy kịch bản trả lời đúng từ câu 1-5, sau đó thoát ra.
        2. Từ trang chủ đề, vào lại bài làm và chạy kịch bản trả lời sai.
        """
        page = quiz_session

        # -------------------------------------------------------------------
        # -- KỊCH BẢN 1: TRẢ LỜI ĐÚNG --
        # -------------------------------------------------------------------
        print("\n--- Bắt đầu Kịch bản 1: Trả lời đúng từ câu 1 đến 5 ---")

        total_questions = len(QUESTIONS_DATA_WOHEWO)
        for index, question in enumerate(QUESTIONS_DATA_WOHEWO):
            print(f"--> Đang thực hiện câu hỏi {question['id']}")

            page.get_by_text(question["correct_answer"], exact=True).click()
            print(f"    -> Đã chọn đáp án: {question['correct_answer']}")

            page.get_by_role("button", name="こたえあわせ").click()
            expect(page.locator(".icon__answer--right")).to_be_visible()
            expect(page.get_by_text(question["expected_message"])).to_be_visible()
            print("    -> Kết quả hiển thị chính xác.")

            if index < total_questions - 1:
                page.get_by_role("button", name="つぎへ").click()

        # --- Luồng kết thúc bài làm ---
        review_button = page.get_by_role("button", name="ふりかえり")
        expect(review_button).to_be_visible()
        review_button.click()
        print("-> Đã click 'ふりかえり'")

        review_title = page.locator("p:has-text('ふりかえり')")
        expect(review_title).to_be_visible()
        print("-> Đã vào trang Review")

        finish_button = page.get_by_text("おわる", exact=True)
        expect(finish_button).to_be_visible()
        finish_button.click()
        print("-> Đã click 'おわる'")

        print("--- Kịch bản ĐÚNG hoàn tất, đã quay về trang chủ đề ---")
        expect(page.get_by_text("さとうと　しお").first).to_be_visible()

        # -------------------------------------------------------------------
        # -- KỊCH BẢN 2: TRẢ LỜI SAI (TIẾP NỐI) --
        # -------------------------------------------------------------------
        print("\n--- Bắt đầu Kịch bản 2: Trả lời sai từ câu 1 đến 5 ---")

        topic_link = page.get_by_text("上P.54～55")
        expect(topic_link).to_be_visible()
        topic_link.click()
        print("-> Đã vào lại màn hình làm bài để bắt đầu kịch bản sai.")

        for index, question in enumerate(QUESTIONS_DATA_WOHEWO):
            print(f"--> Đang thực hiện câu hỏi {question['id']} (trả lời SAI)")

            page.get_by_text(question["incorrect_answer"], exact=True).click()
            print(f"    -> Đã chọn đáp án sai: {question['incorrect_answer']}")

            page.get_by_role("button", name="こたえあわせ").click()
            expect(page.locator(".icon__answer--wrong")).to_be_visible()
            print("    -> Kết quả 'Sai' hiển thị chính xác.")

            if index < total_questions - 1:
                page.get_by_role("button", name="つぎへ").click()

        # --- Luồng kết thúc bài làm ---
        review_button = page.get_by_role("button", name="ふりかえり")
        expect(review_button).to_be_visible()
        review_button.click()

        review_title = page.locator("p:has-text('ふりかえり')")
        expect(review_title).to_be_visible()

        finish_button = page.get_by_text("おわる", exact=True)
        expect(finish_button).to_be_visible()
        finish_button.click()

        print("--- Kịch bản SAI hoàn tất, đã quay về trang chủ đề ---")
        expect(page.get_by_text("さとうと　しお").first).to_be_visible()
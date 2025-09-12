import pytest
from playwright.sync_api import Page, expect
from tests.kokugo.kokugo_data import QUESTIONS_DATA_DOUYATTEPRE


# ===================================================================
# == FIXTURE SETUP ==
# ===================================================================

@pytest.fixture(scope="class")
def quiz_session(logged_in_page: Page):
    """
    Fixture này chạy 1 lần: Đăng nhập -> Vào Kokugo -> Vào bài làm của chủ đề.
    """
    page = logged_in_page
    print("\n--- [CLASS SETUP] Bắt đầu phiên làm bài cho chủ đề 'さとうと　しお' ---")
    # Vào trang Kokugo
    page.get_by_alt_text("国語").click()
    expect(page.get_by_text("プレテスト").first).to_be_visible()
    expect(page.get_by_text("どう　やって　みを　まもるのかな").first).to_be_visible()
    page.locator(".p-10px > p").nth(1).click()
    yield page

# ===================================================================
# == LỚP TEST ==
# ===================================================================

class TestDouyatte:
    QUESTIONS_DATA = QUESTIONS_DATA_DOUYATTEPRE

    def test_both_scenarios_sequentially(self, quiz_session: Page):
        """
        Test này thực hiện một luồng liên tục:
        1. Chạy kịch bản trả lời đúng.
        2. Vào lại bài làm và chạy kịch bản trả lời sai.
        """
        page = quiz_session
        total_questions = len(self.QUESTIONS_DATA)

        # -------------------------------------------------------------------
        # -- KỊCH BẢN 1: TRẢ LỜI ĐÚNG --
        # -------------------------------------------------------------------
        print("\n--- Bắt đầu Kịch bản 1: Trả lời đúng ---")

        for index, question in enumerate(self.QUESTIONS_DATA):
            print(f"--> 質問 {question['id']} を実行中（正解を選択）")
            question_type = question.get("type", "text")

            for answer in question["correct_answers"]:
                if question_type == "text":
                    page.get_by_text(answer, exact=True).click()
                else:
                    page.locator(answer).click()

            page.get_by_role("button", name="こたえあわせ").click()
            expect(page.locator(".icon__answer--right")).to_be_visible()

            if index < total_questions - 1:
                page.get_by_role("button", name="つぎへ").click()
            else:
                # Luồng kết thúc
                review_button = page.locator("button:has-text('ふりかえり')")
                review_button.wait_for(state="visible", timeout=10000)
                review_button.click()
                review_title = page.locator("p:has-text('ふりかえり')")
                expect(review_title).to_be_visible()
                finish_button = page.get_by_text("おわる", exact=True)
                expect(finish_button).to_be_visible()
                finish_button.click()

        print("--- 正解シナリオを完了しました ---")
        expect(page.get_by_text("あめですよ")).to_be_visible()

        # -------------------------------------------------------------------
        # -- KỊCH BẢN 2: TRẢ LỜI SAI (TIẾP NỐI) --
        # -------------------------------------------------------------------
        print("\n--- Bắt đầu Kịch bản 2: Trả lời sai ---")
        expect(page.get_by_text("プレテスト").first).to_be_visible()
        expect(page.get_by_text("どう　やって　みを　まもるのかな").first).to_be_visible()
        page.locator(".p-10px > p").nth(1).click()
        print("-> Đã vào lại màn hình làm bài để bắt đầu kịch bản sai.")

        for index, question in enumerate(self.QUESTIONS_DATA):
            print(f"--> 質問 {question['id']} を実行中（不正解を選択）")
            question_type = question.get("type", "text")

            incorrect_answer = question["incorrect_answers"][0]
            if question_type == "text":
                page.get_by_text(incorrect_answer, exact=True).click()
            else:
                page.locator(incorrect_answer).click()

            page.get_by_role("button", name="こたえあわせ").click()
            expect(page.locator(".icon__answer--wrong")).to_be_visible()

            if index < total_questions - 1:
                page.get_by_role("button", name="つぎへ").click()
            else:
                # Luồng kết thúc (giữ nguyên)
                review_button = page.locator("button:has-text('ふりかえり')")
                review_button.wait_for(state="visible", timeout=10000)
                review_button.click()
                review_title = page.locator("p:has-text('ふりかえり')")
                expect(review_title).to_be_visible()
                finish_button = page.get_by_text("おわる", exact=True)
                expect(finish_button).to_be_visible()
                finish_button.click()

        print("--- 不正解シナリオを完了しました ---")
        expect(page.get_by_text("あめですよ")).to_be_visible()
import pytest
from playwright.sync_api import Page, expect
from tests.kokugo.kokugo_data import QUESTIONS_DATA_SATOUTOSHIO


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
    expect(page.get_by_text("さとうと　しお").first).to_be_visible()
    page.locator(".p-10px > p").first.click()
    yield page

# ===================================================================
# == LỚP TEST ==
# ===================================================================

class TestTopicSatoutoShio:

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
        print("\n--- Bắt đầu Kịch bản 1: Trả lời đúng ---")

        # --- Câu hỏi 1 ---
        q1 = QUESTIONS_DATA_SATOUTOSHIO[0]
        page.get_by_text(q1["correct_answer"], exact=True).click()
        page.get_by_role("button", name="こたえあわせ").click()
        expect(page.locator(".icon__answer--right")).to_be_visible()
        page.get_by_role("button", name="つぎへ").click()

        # --- Câu hỏi 2 ---
        q2 = QUESTIONS_DATA_SATOUTOSHIO[1]
        page.get_by_text(q2["correct_answer"], exact=True).click()
        page.get_by_role("button", name="こたえあわせ").click()
        expect(page.locator(".icon__answer--right")).to_be_visible()
        page.get_by_role("button", name="つぎへ").click()

        # --- Câu hỏi 3 ---
        q3 = QUESTIONS_DATA_SATOUTOSHIO[2]
        for answer in q3["correct_answers"]:
            page.get_by_text(answer, exact=True).click()
        page.get_by_role("button", name="こたえあわせ").click()
        expect(page.locator(".icon__answer--right")).to_be_visible()
        page.get_by_role("button", name="つぎへ").click()

        # --- Câu hỏi 4 ---
        q4 = QUESTIONS_DATA_SATOUTOSHIO[3]
        for answer in q4["correct_answers"]:
            page.get_by_text(answer, exact=True).click()
        page.get_by_role("button", name="こたえあわせ").click()
        expect(page.locator(".icon__answer--right")).to_be_visible()
        page.get_by_role("button", name="つぎへ").click()

        # --- Câu hỏi 5 ---
        q5 = QUESTIONS_DATA_SATOUTOSHIO[4]
        page.get_by_text(q5["correct_answer"], exact=True).click()
        page.get_by_role("button", name="こたえあわせ").click()
        expect(page.locator(".icon__answer--right")).to_be_visible()

        # --- Luồng kết thúc ---
        review_button = page.get_by_role("button", name="ふりかえり")
        expect(review_button).to_be_visible()
        review_button.click()
        review_title = page.locator("p:has-text('ふりかえり')")
        expect(review_title).to_be_visible()
        finish_button = page.get_by_text("おわる", exact=True)
        expect(finish_button).to_be_visible()
        finish_button.click()

        print("--- Kịch bản ĐÚNG hoàn tất ---")
        expect(page.get_by_text("さとうと　しお").first).to_be_visible()

        # -------------------------------------------------------------------
        # -- KỊCH BẢN 2: TRẢ LỜI SAI--
        # -------------------------------------------------------------------
        print("\n--- Bắt đầu Kịch bản 2: Trả lời sai ---")

        # BƯỚC CHUẨN BỊ: Từ trang chủ đề, vào lại bài làm
        page.locator(".p-10px > p").first.click()
        print("-> Đã vào lại màn hình làm bài để bắt đầu kịch bản sai.")

        # --- Câu hỏi 1 (Trả lời sai) ---
        page.get_by_text(q1["incorrect_answer"], exact=True).click()
        page.get_by_role("button", name="こたえあわせ").click()
        expect(page.locator(".icon__answer--wrong")).to_be_visible()
        page.get_by_role("button", name="つぎへ").click()

        # --- Câu hỏi 2 (Trả lời sai) ---
        page.get_by_text(q2["incorrect_answer"], exact=True).click()
        page.get_by_role("button", name="こたえあわせ").click()
        expect(page.locator(".icon__answer--wrong")).to_be_visible()
        page.get_by_role("button", name="つぎへ").click()

        # --- Câu hỏi 3 (Trả lời thiếu) ---
        page.get_by_text(q3["correct_answers"][0], exact=True).click()
        page.get_by_role("button", name="こたえあわせ").click()
        expect(page.locator(".icon__answer--wrong")).to_be_visible()
        page.get_by_role("button", name="つぎへ").click()

        # --- Câu hỏi 4 (Trả lời thiếu) ---
        page.get_by_text(q4["correct_answers"][0], exact=True).click()
        page.get_by_role("button", name="こたえあわせ").click()
        expect(page.locator(".icon__answer--wrong")).to_be_visible()
        page.get_by_role("button", name="つぎへ").click()

        # --- Câu hỏi 5 (Trả lời sai) ---
        page.get_by_text(q5["incorrect_answer"], exact=True).click()
        page.get_by_role("button", name="こたえあわせ").click()
        expect(page.locator(".icon__answer--wrong")).to_be_visible()

        # --- Luồng kết thúc (giống như trên) ---
        review_button_2 = page.get_by_role("button", name="ふりかえり")
        expect(review_button_2).to_be_visible()
        review_button_2.click()
        review_title_2 = page.locator("p:has-text('ふりかえり')")
        expect(review_title_2).to_be_visible()
        finish_button_2 = page.get_by_text("おわる", exact=True)
        expect(finish_button_2).to_be_visible()
        finish_button_2.click()

        print("--- Kịch bản SAI hoàn tất ---")
        expect(page.get_by_text("さとうと　しお").first).to_be_visible()
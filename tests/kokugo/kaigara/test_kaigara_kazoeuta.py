import pytest
from playwright.sync_api import Page, expect
from tests.kokugo.kokugo_data import QUESTIONS_DATA_KAZOEUTA


@pytest.fixture(scope="class")
def kokugo_main_page(logged_in_page: Page):
    """
    このFixtureはクラスごとに一度だけ実行されます：ログインして国語の教科ページに移動します。
    (Fixture này chạy 1 lần duy nhất: Đăng nhập và vào trang môn học Kokugo.)
    """
    page = logged_in_page
    print("\n--- [CLASS SETUP] ログインし、国語ページへ遷移します ---")
    page.get_by_alt_text("国語").click()
    expect(page.get_by_text("あめですよ")).to_be_visible()
    yield page

@pytest.fixture(scope="function")
def quiz_session(kokugo_main_page: Page):
    """
    このFixtureは各テストケースの前に実行されます。
    セットアップ：国語ページからトピックをクリックし、問題画面に移動します。
    (Fixture này chạy TRƯỚC mỗi hàm test.
    Setup: Từ trang Kokugo, click vào chủ đề để vào màn hình làm bài.)
    """
    page = kokugo_main_page
    # --- セットアップ処理（各テストの前に実行） ---
    print(f"\n--- [FUNCTION SETUP] 問題画面へ遷移します ---")
    topic_title = page.locator("p:has-text('かぞえうた')")
    topic_container = topic_title.locator("..")
    topic_container.get_by_alt_text("basic").click()
    yield page  # テスト関数に制御を渡します (Giao quyền cho hàm test)
    # --- ティアダウン処理（各テストの後に実行） ---
    print(f"--- [FUNCTION TEARDOWN] シナリオを終了します ---")

class TestNekoToNekko:
    # Gán dữ liệu vào biến của lớp
    QUESTIONS_DATA = QUESTIONS_DATA_KAZOEUTA

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
        topic_title = page.locator("p:has-text('かぞえうた')")
        topic_container = topic_title.locator("..")
        topic_container.get_by_alt_text("basic").click()
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
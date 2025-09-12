import pytest
from playwright.sync_api import Page, expect
from tests.kokugo.kokugo_data import QUESTIONS_DATA_KANJINOHANASHI

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
    topic_title = page.locator("p:has-text('かんじの　はなし')")
    topic_container = topic_title.locator("..")
    topic_container.get_by_alt_text("basic").click()

    yield page  # テスト関数に制御を渡します (Giao quyền cho hàm test)

    # --- ティアダウン処理（各テストの後に実行） ---
    print(f"--- [FUNCTION TEARDOWN] シナリオを終了します ---")

class TestKanjiNoHanashiTopic:
    QUESTIONS_DATA = QUESTIONS_DATA_KANJINOHANASHI

    def test_both_scenarios_sequentially(self, quiz_session: Page):
        """
        Test này thực hiện một luồng liên tục:
        1. Chạy kịch bản trả lời đúng.
        2. Vào lại bài làm và chạy kịch bản trả lời sai.
        """
        page = quiz_session
        total_questions = len(self.QUESTIONS_DATA)

        total_questions = len(self.QUESTIONS_DATA)
        for index, question in enumerate(self.QUESTIONS_DATA):
            question_type = question.get("type", "text")
            print(f"--> Câu hỏi {question['id']} (Loại: {question_type}): Chọn đáp án ĐÚNG")
            # --- Xử lý câu hỏi chọn đáp án (text, image, css, xpath) ---
            if question_type in ["text", "image", "css", "xpath"]:
                # Dữ liệu `correct_answers` là một danh sách (list)
                for answer in question["correct_answers"]:
                    if question_type == "text":
                        page.get_by_text(answer, exact=True).click()
                    else:
                        page.locator(answer).click()

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
                    page.locator("span").filter(has_text=item_text).drag_to(drop_zone)
            # ===================================================================

            # --- Các bước kiểm tra và chuyển tiếp ---
            page.get_by_role("button", name="こたえあわせ").click()
            expect(page.locator(".icon__answer--right")).to_be_visible()

            if index < total_questions - 1:
                page.get_by_role("button", name="つぎへ").click()
            else:
                # Luồng kết thúc bài làm
                review_button = page.locator("button:has-text('ふりかえり')")
                review_button.wait_for(state="visible", timeout=10000)
                review_button.click()

                review_title = page.locator("p:has-text('ふりかえり')")
                expect(review_title).to_be_visible()

                finish_button = page.get_by_text("おわる", exact=True)
                expect(finish_button).to_be_visible()
                finish_button.click()

        print("--- Kịch bản ĐÚNG hoàn tất ---")
        expect(page.get_by_text("あめですよ").first).to_be_visible()

        # -------------------------------------------------------------------
        # -- KỊCH BẢN 2: TRẢ LỜI SAI (TIẾP NỐI) --
        # -------------------------------------------------------------------
        print("\n--- Bắt đầu Kịch bản 2: Trả lời sai ---")
        topic_container = page.locator("p:has-text('かんじの　はなし')").locator("..")
        topic_container.get_by_alt_text("basic").click()
        print("-> Đã vào lại màn hình làm bài để bắt đầu kịch bản sai.")

        total_questions = len(self.QUESTIONS_DATA)
        for index, question in enumerate(self.QUESTIONS_DATA):
            question_type = question.get("type", "text")
            print(f"--> 質問 {question['id']} を実行中（不正解を選択）")

            # --- LOGIC TRẢ LỜI SAI CHO CÁC LOẠI CÂU HỎI ---
            if question_type == "text":
                # Chọn đáp án sai đầu tiên trong danh sách
                incorrect_answer = question["incorrect_answers"][0]
                page.get_by_text(incorrect_answer, exact=True).click()

            elif question_type == "fill_blank":
                # Thực hiện chuỗi hành động sai
                for action in question["incorrect_answers"]:
                    blank_box = page.locator(action["blank_locator"])
                    choice = page.get_by_text(action["choice_text"], exact=True)
                    blank_box.click()
                    choice.click()

            elif question_type == "drag_drop":
                # Thực hiện chuỗi kéo thả sai
                for drag_action in question["incorrect_drag_mapping"]:
                    item_text = question["items_to_drag"][drag_action["item"]]
                    zone_selector = question["drop_zones"][drag_action["zone"]]
                    drop_zone = page.locator(zone_selector).nth(0 if drag_action["zone"] == "zone1" else 1)
                    page.locator("span").filter(has_text=item_text).drag_to(drop_zone)

            # --- Các bước kiểm tra và chuyển tiếp ---
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
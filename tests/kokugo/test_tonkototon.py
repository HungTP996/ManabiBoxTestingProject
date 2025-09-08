# tests/kokugo/test_tonkototon.py

import pytest
import random
from playwright.sync_api import Page, expect
from .kokugo_data import QUESTIONS_DATA_TONKOTOTON


@pytest.fixture(scope="class")
def kokugo_main_page(logged_in_page: Page):
    """
    このFixtureはクラスごとに一度だけ実行されます：ログインして国語の教科ページに移動します。
    (Fixture này chạy 1 lần duy nhất: Đăng nhập và vào trang môn học Kokugo.)
    """
    page = logged_in_page
    print("\n--- [CLASS SETUP] ログインし、国語ページへ遷移します ---")
    page.get_by_alt_text("国語").click()
    expect(page.get_by_text("とん　こと　とん")).to_be_visible()
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
    topic_title = page.locator("p:has-text('ぶんを　つくろう')")
    topic_container = topic_title.locator("..")
    topic_container.get_by_alt_text("basic").click()

    yield page  # テスト関数に制御を渡します (Giao quyền cho hàm test)


class TestTonkototon_Scenarios:
    QUESTIONS_DATA = QUESTIONS_DATA_TONKOTOTON
    def test_scenario_all_correct(self, quiz_session: Page):
        """
        シナリオ1：すべての質問に正解します。
        (Kịch bản 1: Chọn TẤT CẢ các đáp án đúng cho mỗi câu hỏi.)
        """
        page = quiz_session
        print("\n--- 正解シナリオを開始 ---")

        total_questions = len(self.QUESTIONS_DATA)
        for index, question in enumerate(self.QUESTIONS_DATA):
            print(f"--> 質問 {question['id']} を実行中（正解を選択）")

            # すべての正解をクリックするためのループ
            for answer in question["correct_answers"]:
                # 新しいロジック：ロケーターのタイプを確認し、適切なメソッドを使用
                if question["type"] == "text":
                    page.get_by_text(answer, exact=True).click()
                else:  # "css" または "xpath"
                    page.locator(answer).click()

            page.get_by_role("button", name="こたえあわせ").click()
            expect(page.locator(".icon__answer--right")).to_be_visible()

            if index < total_questions - 1:
                page.get_by_role("button", name="つぎへ").click()
            else:
                print("--> 最後の質問を完了し、終了フローを開始します...")
                review_button = page.locator("button:has-text('ふりかえり')")
                review_button.wait_for(state="visible", timeout=10000)
                print("-> 「ふりかえり」ボタンが表示されました。")
                review_button.click()
                print("-> 「ふりかえり」ボタンをクリックしました。")
                review_title = page.locator("p:has-text('ふりかえり')")
                expect(review_title).to_be_visible()
                print("-> 確認ページに移動しました。")
                finish_button = page.get_by_text("おわる", exact=True)
                expect(finish_button).to_be_visible()
                finish_button.click()
                print("-> 「おわる」ボタンをクリックしました。")

        print("--- 正解シナリオを完了しました ---")
        expect(page.get_by_text("とん　こと　とん")).to_be_visible()

    def test_scenario_all_incorrect(self, quiz_session: Page):
        """
        シナリオ2：各質問に対して不正解を1つ選択します。
        (Kịch bản 2: Chọn MỘT đáp án sai cho mỗi câu hỏi.)
        """
        page = quiz_session
        print("\n--- 不正解シナリオを開始 ---")

        random.seed(15)
        total_questions = len(self.QUESTIONS_DATA)
        for index, question in enumerate(self.QUESTIONS_DATA):
            print(f"--> 質問 {question['id']} を実行中（不正解を選択）")

            # リストの最初の不正解をクリックするだけ
            first_incorrect_answer = random.choice(question["incorrect_answers"])
            if question["type"] == "text":
                page.get_by_text(first_incorrect_answer, exact=True).click()
            else:
                page.locator(first_incorrect_answer).click()

            page.get_by_role("button", name="こたえあわせ").click()
            expect(page.locator(".icon__answer--wrong")).to_be_visible()

            if index < total_questions - 1:
                page.get_by_role("button", name="つぎへ").click()
            else:
                # 終了フロー（上記と同じ）
                print("--> 最後の質問を完了し、終了フローを開始します...")
                review_button = page.locator("button:has-text('ふりかえり')")
                review_button.wait_for(state="visible", timeout=10000)
                review_button.click()
                review_title = page.locator("p:has-text('ふりかえり')")
                expect(review_title).to_be_visible()
                finish_button = page.get_by_text("おわる", exact=True)
                expect(finish_button).to_be_visible()
                finish_button.click()

        print("--- 不正解シナリオを完了しました ---")
        expect(page.get_by_text("とん　こと　とん")).to_be_visible()
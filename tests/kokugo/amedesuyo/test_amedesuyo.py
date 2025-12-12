import pytest
import allure
from playwright.sync_api import Page, expect
from tests.utils.choice_helpers import answer_question
from tests.utils.complete_helpers import complete_question

@pytest.fixture(scope="class")
def kokugo_main_page(logged_in_page: Page):
    """クラス設定：ログイン後、国語のメインページに移動します。"""
    page = logged_in_page
    # 2. allure.step() に変更
    with allure.step("国語のメインページに移動"):
        page.get_by_alt_text("国語").click()
        # expect(page.get_by_text("あめですよ")).to_be_visible()
    yield page

@pytest.fixture(scope="function")
def quiz_session(kokugo_main_page: Page):
    """関数設定：各テストの前にクイズセッションを開始します。"""
    page = kokugo_main_page
    with allure.step("トピック「ふたと　ぶた」の問題画面に移動"):
        topic_title = page.locator("p:has-text('ふたと　ぶた')")
        topic_container = topic_title.locator("..")
        topic_container.get_by_alt_text("basic").click()
    yield page

class Test_AmeDesuYo:
    def test_all_questions(self, quiz_session: Page, kokugo_test_data: dict):
        """シナリオ1：すべての問題に正しく解答する。"""
        page = quiz_session

        with allure.step("テストデータを準備"):
            questions = kokugo_test_data["AMEDESUYO"]
            total_questions = len(questions)

        for index, question_data in enumerate(questions):
            with allure.step(f"問題 {index + 1} に正しく解答する"):
                answer_question(page, question_data, "correct_answers")
                kotaeawase_button = page.get_by_role("button", name="こたえあわせ")
                expect(kotaeawase_button).to_be_enabled(timeout=10000)
                kotaeawase_button.click()
                expect(page.locator(".icon__answer--right")).to_be_visible()
                if "expected_message" in question_data:
                    expect(page.get_by_text(question_data["expected_message"])).to_be_visible()
                if index < total_questions - 1:
                    page.get_by_role("button", name="つぎへ").click()
                else:
                    complete_question(page)

        with allure.step("テスト完了を確認"):
            expect(page.get_by_text("あめですよ")).to_be_visible()

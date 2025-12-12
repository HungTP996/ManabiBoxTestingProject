import pytest
import allure
from playwright.sync_api import Page, expect
from tests.utils.choice_helpers import answer_question
from tests.utils.complete_helpers import complete_question


@pytest.fixture(scope="class")
def kokugo_main_page(logged_in_page: Page):
    page = logged_in_page
    print("\n--- [CLASS SETUP] ログインし、国語ページへ遷移します ---")
    page.get_by_alt_text("国語").click()
    # expect(page.get_by_text("あめですよ")).to_be_visible()
    yield page

@pytest.fixture(scope="function")
def quiz_session(kokugo_main_page: Page):
    page = kokugo_main_page
    print(f"\n--- [FUNCTION SETUP] 問題画面へ遷移します ---")
    topic_title = page.locator("p:has-text('かたかなの　かたち')")
    topic_container = topic_title.locator("..")
    topic_container.get_by_alt_text("basic").click()
    yield page
    print(f"--- [FUNCTION TEARDOWN] シナリオを終了します ---")


class Test_Katakananokatachi:
    def test_all_questions(self, quiz_session: Page, kokugo_test_data: dict):
        """シナリオ1：すべての問題に正しく解答する。"""
        page = quiz_session
        with allure.step("テストデータを準備"):
            questions = kokugo_test_data["KATAKANANOKATACHI"]
            total_questions = len(questions)

        for index, question_data in enumerate(questions):
            with allure.step(f"問題 {index + 1} に正しく解答する "):
                answer_question(page, question_data, "correct_answers")
                page.get_by_role("button", name="こたえあわせ").click()
                expect(page.locator(".icon__answer--right")).to_be_visible()
                if index < total_questions - 1:
                    page.get_by_role("button", name="つぎへ").click()
                else:
                    complete_question(page)

        with allure.step("テスト完了を確認"):
            expect(page.get_by_text("あめですよ")).to_be_visible()
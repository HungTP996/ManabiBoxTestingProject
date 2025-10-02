import pytest, allure
from playwright.sync_api import Page, expect
from tests.utils.choice_helpers import answer_question
from tests.utils.complete_helpers import complete_question


@pytest.fixture(scope="class")
def quiz_session(logged_in_page: Page):
    page = logged_in_page
    page.get_by_alt_text("国語").click()
    page.locator(".p-10px > p").nth(1).click()
    yield page


class TestDouYattePre:

    def test_test_all_questions(self, quiz_session: Page, kokugo_test_data: dict):
        page = quiz_session
        questions = kokugo_test_data["DOUYATTEPRE"]
        total_questions = len(questions)

        with allure.step("シナリオ1：すべての問題に正しく解答する"):
            for index, question in enumerate(questions):
                with allure.step(f"問題 {question['id']} に正しく解答 (Trả lời đúng câu hỏi {question['id']})"):
                    answer_question(page, question, "correct_answers")

                    page.get_by_role("button", name="こたえあわせ").click()
                    expect(page.locator(".icon__answer--right")).to_be_visible()

                    if index < total_questions - 1:
                        page.get_by_role("button", name="つぎへ").click()
                    else:
                        complete_question(page)

            with allure.step("テスト完了を確認"):
                expect(page.get_by_text("あめですよ")).to_be_visible()

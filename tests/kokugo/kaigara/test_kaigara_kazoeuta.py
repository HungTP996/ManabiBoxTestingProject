import pytest
import allure
from playwright.sync_api import Page, expect
from tests.utils.choice_helpers import answer_question
from tests.utils.complete_helpers import complete_question

@pytest.fixture(scope="class")
def quiz_session(logged_in_page: Page):
    """Fixture này vào bài làm của chủ đề 'かぞえうた'."""
    page = logged_in_page
    with allure.step("セットアップ：テストセッションを開始 "):
        page.get_by_alt_text("国語").click()
        topic_container = page.locator("p:has-text('かぞえうた')").locator("..")
        topic_container.get_by_alt_text("basic").click()
    yield page

class TestKazoeuta:

    def test_both_scenarios_sequentially(self, quiz_session: Page, kokugo_test_data: dict):
        page = quiz_session
        questions = kokugo_test_data["KAZOEUTA"]
        total_questions = len(questions)

        # -------------------------------------------------------------------
        # -- KỊCH BẢN 1: TRẢ LỜI ĐÚNG --
        # -------------------------------------------------------------------
        with allure.step("シナリオ1：すべての問題に正しく解答する (Kịch bản 1: Trả lời đúng tất cả các câu hỏi)"):
            for index, question in enumerate(questions):
                with allure.step(f"問題 {question['id']} に正しく解答 (Trả lời đúng câu hỏi {question['id']})"):
                    answer_question(page, question, "correct_answers")
                    page.get_by_role("button", name="こたえあわせ").click()
                    expect(page.locator(".icon__answer--right")).to_be_visible()

                    if index < total_questions - 1:
                        page.get_by_role("button", name="つぎへ").click()
                    else:
                        complete_question(page)

            with allure.step("テスト完了を確認 (Xác nhận hoàn thành bài test)"):
                expect(page.get_by_text("あめですよ")).to_be_visible()

        # -------------------------------------------------------------------
        # -- KỊCH BẢN 2: TRẢ LỜI SAI  --
        # -------------------------------------------------------------------
        with allure.step("シナリオ2：すべての問題に不正解する (Kịch bản 2: Trả lời sai tất cả các câu hỏi)"):
            with allure.step("再度クイズ画面に移動 (Vào lại màn hình làm bài)"):
                topic_container = page.locator("p:has-text('かぞえうた')").locator("..")
                topic_container.get_by_alt_text("basic").click()

            for index, question in enumerate(questions):
                with allure.step(f"問題 {question['id']} に不正解を解答 (Trả lời sai câu hỏi {question['id']})"):
                    answer_question(page, question, "incorrect_answers")
                    page.get_by_role("button", name="こたえあわせ").click()
                    expect(page.locator(".icon__answer--wrong")).to_be_visible()

                    if index < total_questions - 1:
                        page.get_by_role("button", name="つぎへ").click()
                    else:
                        complete_question(page)

            with allure.step("テスト完了を確認 (Xác nhận hoàn thành bài test)"):
                expect(page.get_by_text("あめですよ")).to_be_visible()
import pytest
import allure
from playwright.sync_api import Page, expect
from tests.utils.choice_helpers import answer_question
from tests.utils.complete_helpers import complete_question


@pytest.fixture(scope="class")
def quiz_session(logged_in_page: Page):
    """Fixture này vào bài làm của chủ đề 'かんじの はなし'."""
    page = logged_in_page
    with allure.step("セットアップ：テストセッションを開始 (Setup: Bắt đầu phiên test)"):
        page.get_by_alt_text("国語").click()
        topic_container = page.locator("p:has-text('かんじの　はなし')").locator("..")
        topic_container.get_by_alt_text("basic").click()
    yield page

class TestKanjiNoHanashi:

    def test_both_scenarios_sequentially(self, quiz_session: Page, kokugo_test_data: dict):

        page = quiz_session
        questions = kokugo_test_data["KANJINOHANASHI"]
        total_questions = len(questions)

        with allure.step("シナリオ1：すべての問題に正しく解答する "):
            for index, question in enumerate(questions):
                with allure.step(f"問題 {question['id']} に正しく解答 (Trả lời đúng câu hỏi {question['id']})"):

                    question_type = question.get("type", "text")

                    if question_type == "drag_drop":
                        # Nếu là câu kéo thả, dùng key "correct_drag_mapping"
                        answer_question(page, question, "correct_drag_mapping")
                    else:
                        # Với các loại câu hỏi khác, dùng key "correct_answers"
                        answer_question(page, question, "correct_answers")
                    # ===================================================================

                    page.get_by_role("button", name="こたえあわせ").click()
                    expect(page.locator(".icon__answer--right")).to_be_visible()

                    if index < total_questions - 1:
                        page.get_by_role("button", name="つぎへ").click()
                    else:
                        complete_question(page)


            with allure.step("テスト完了を確認"):
                expect(page.get_by_text("あめですよ")).to_be_visible()
import pytest
import allure
from playwright.sync_api import Page, expect
from tests.utils.choice_helpers import answer_question
from tests.utils.complete_helpers import complete_question


@pytest.fixture(scope="class")
def quiz_session(logged_in_page: Page):
    """Fixture này vào bài làm của chủ đề 'スイミー'."""
    page = logged_in_page
    with allure.step("セットアップ：テストセッションを開始 (Setup: Bắt đầu phiên test)"):
        page.get_by_alt_text("国語").click()
        topic_container = page.locator("p:has-text('スイミー)").nth(0).locator("..")
        topic_container.get_by_alt_text("basic").click()
    yield page


class Test_Suimi:
    def test_all_questions(self, quiz_session: Page, kokugo_test_data: dict):
        """シナリオ1：すべての問題に正しく解答する。"""
        page = quiz_session

        with allure.step("テストデータを準備"):
            questions = kokugo_test_data["SUIMI"]
            total_questions = len(questions)

        for index, question_data in enumerate(questions):
            with allure.step(f"問題 {index + 1} に正しく解答する (Trả lời đúng câu hỏi số {index + 1})"):
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

        with allure.step("テスト完了を確認 (Xác nhận hoàn thành bài test)"):
            expect(page.get_by_text("あめですよ")).to_be_visible()
    #
    # def test_all_incorrect_answers(self, quiz_session: Page, kokugo_test_data: dict):
    #     """シナリオ2：すべての問題に誤って解答する。"""
    #     page = quiz_session
    #
    #     with allure.step("テストデータを準備"):
    #         questions = kokugo_test_data["MATOMETEYOBUKOTOBA"]
    #
    #     for index, question_data in enumerate(questions):
    #         with allure.step(
    #                 f"問題 {index + 1} の不正解パターンをテスト (Test các trường hợp sai của câu hỏi {index + 1})"):
    #             incorrect_answers = question_data.get("incorrect_answers", [])
    #
    #             if not incorrect_answers:
    #                 continue
    #
    #             for incorrect_answer in incorrect_answers:
    #                 with allure.step(
    #                         f"選択肢「{incorrect_answer}」が不正解であることを確認 (Xác nhận lựa chọn '{incorrect_answer}' là sai)"):
    #                     test_data_for_this_run = question_data.copy()
    #                     test_data_for_this_run['incorrect_answers'] = [incorrect_answer]
    #                     answer_question(page, test_data_for_this_run, "incorrect_answers")
    #
    #                     kotaeawase_button = page.get_by_role("button", name="こたえあわせ")
    #                     expect(kotaeawase_button).to_be_enabled(timeout=10000)
    #                     kotaeawase_button.click()
    #                     expect(page.locator(".icon__answer--wrong")).to_be_visible()
    #             answer_question(page, question_data, "correct_answers")
    #             page.get_by_role("button", name="こたえあわせ").click()
    #             expect(page.locator(".icon__answer--right")).to_be_visible()
    #
    #             if index < len(questions) - 1:
    #                 page.get_by_role("button", name="つぎへ").click()
    #             else:
    #                 complete_question(page)
    #
    #     with allure.step("テスト完了を確認 (Xác nhận hoàn thành bài test)"):
    #         expect(page.get_by_text("あめですよ")).to_be_visible()
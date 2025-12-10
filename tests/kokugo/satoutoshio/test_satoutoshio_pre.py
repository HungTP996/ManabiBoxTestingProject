import pytest
import allure
from playwright.sync_api import Page, expect
from tests.utils.choice_helpers import answer_question
from tests.utils.complete_helpers import complete_question


@pytest.fixture(scope="class")
def quiz_session(logged_in_page: Page):
    """「さとうと しお」のテーマのテストを開始するためのフィクスチャ。"""
    page = logged_in_page
    with allure.step("セットアップ：テストセッションを開始"):
        page.get_by_alt_text("国語").click()
        # 最初のトピック要素をクリック
        page.locator(".p-10px > p").first.click()
    yield page


class TestTopicSatoutoShio:

    def test_all_questions_correct(self, quiz_session: Page, kokugo_test_data: dict):
        """
        このテストは、正解と不正解のシナリオを含む連続したフローを実行します。
        """
        page = quiz_session
        questions = kokugo_test_data["SATOUTOSHIO"]
        total_questions = len(questions)

        with allure.step("シナリオ1：すべての問題に正しく解答する"):
            for index, question in enumerate(questions):
                with allure.step(f"問題 {question['id']} に正しく解答"):
                    answer_question(page, question, "correct_answers")
                    page.get_by_role("button", name="こたえあわせ").click()
                    expect(page.locator(".icon__answer--right")).to_be_visible()
                    if index < total_questions - 1:
                        with allure.step("次の問題へ"):
                            page.get_by_role("button", name="つぎへ").click()
                    else:
                        with allure.step("テストを完了"):
                            complete_question(page)

            with allure.step("テスト完了画面を確認"):
                expect(page.get_by_text("さとうと　しお").first).to_be_visible()
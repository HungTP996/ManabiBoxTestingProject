import pytest
import allure
from playwright.sync_api import Page, expect
from tests.utils.choice_helpers import answer_question
from tests.utils.complete_helpers import complete_question


@pytest.fixture(scope="class")
def quiz_session(logged_in_page: Page):
    """「サラダで げんき」のテーマのテストを開始するためのフィクスチャ。"""
    page = logged_in_page
    with allure.step("セットアップ：テストセッションを開始"):
        page.get_by_alt_text("国語").click()
        # トピックコンテナを特定し、クリック
        topic_container = page.locator("p:has-text('サラダで　げんき')").nth(0).locator("..")
        topic_container.get_by_alt_text("basic").click()
    yield page


class TestSarada:

    def test_all_questions_correct(self, quiz_session: Page, kokugo_test_data: dict):
        """
        このテストは、正解のシナリオを含む連続したフローを実行します。
        """
        page = quiz_session
        questions = kokugo_test_data["SADADADEGENKI"]
        total_questions = len(questions)

        # -------------------------------------------------------------------
        # -- シナリオ 1: すべて正解 --
        # -------------------------------------------------------------------
        with allure.step("シナリオ1：すべての問題に正しく解答する"):
            for index, question in enumerate(questions):
                with allure.step(f"問題 {question['id']} に正しく解答"):
                    # 1. 回答
                    answer_question(page, question, "correct_answers")

                    # 2. 答え合わせ
                    page.get_by_role("button", name="こたえあわせ").click()

                    # 3. 正解を確認
                    expect(page.locator(".icon__answer--right")).to_be_visible()

                    # 4. 次へ/終了処理
                    if index < total_questions - 1:
                        with allure.step("次の問題へ"):
                            page.get_by_role("button", name="つぎへ").click()
                    else:
                        with allure.step("テストを完了"):
                            complete_question(page)

            with allure.step("テスト完了画面を確認"):
                # 完了画面に表示されるトピック名などを確認
                # データキーとトピック名が一致していない可能性がありますが、元のコードに合わせてテキスト要素を維持します。
                expect(page.get_by_text("とん　こと　とん")).to_be_visible()
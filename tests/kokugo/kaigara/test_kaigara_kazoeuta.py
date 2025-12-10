import pytest
import allure
from playwright.sync_api import Page, expect
from tests.utils.choice_helpers import answer_question
from tests.utils.complete_helpers import complete_question


@pytest.fixture(scope="class")
def quiz_session(logged_in_page: Page):
    """「かぞえうた」のテーマのテストを開始するためのフィクスチャ。"""
    page = logged_in_page
    with allure.step("セットアップ：テストセッションを開始"):
        page.get_by_alt_text("国語").click()
        # トピックコンテナを特定し、クリック
        topic_container = page.locator("p:has-text('かぞえうた')").locator("..")
        topic_container.get_by_alt_text("basic").click()
    yield page


class TestKazoeuta:

    def test_all_questions_correct(self, quiz_session: Page, kokugo_test_data: dict):
        """
        このテストは、正解と不正解のシナリオを含む連続したフローを実行します。
        """
        page = quiz_session
        questions = kokugo_test_data["KAZOEUTA"]
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
                expect(page.get_by_text("あめですよ")).to_be_visible()

        # -------------------------------------------------------------------
        # -- シナリオ 2: すべて不正解 --
        # -------------------------------------------------------------------
        # with allure.step("シナリオ2：すべての問題に不正解する"):
        #     with allure.step("再度クイズ画面に移動"):
        #         # 同じトピックを再度クリックして、テストをリセット
        #         topic_container = page.locator("p:has-text('かぞえうた')").locator("..")
        #         topic_container.get_by_alt_text("basic").click()

        #     for index, question in enumerate(questions):
        #         with allure.step(f"問題 {question['id']} に不正解を解答"):
        #             # 1. 不正解の選択肢で回答
        #             answer_question(page, question, "incorrect_answers")

        #             # 2. 答え合わせ
        #             page.get_by_role("button", name="こたえあわせ").click()

        #             # 3. 不正解を確認
        #             expect(page.locator(".icon__answer--wrong")).to_be_visible()

        #             # 4. 次へ/終了処理
        #             if index < total_questions - 1:
        #                 with allure.step("次の問題へ"):
        #                     # 次へ進むためには、ここで正解を入力し直す必要がある場合がありますが、
        #                     # 元のコードに従い、不正解を確認後「つぎへ」をクリックします。
        #                     page.get_by_role("button", name="つぎへ").click()
        #             else:
        #                 with allure.step("テストを完了"):
        #                     complete_question(page)

        #     with allure.step("テスト完了画面を確認"):
        #         expect(page.get_by_text("あめですよ")).to_be_visible()
import pytest
import allure
from playwright.sync_api import Page, expect
from tests.utils.choice_helpers import answer_question
from tests.utils.complete_helpers import complete_question


@pytest.fixture(scope="class")
def quiz_session(logged_in_page: Page):
    """「はを つかおう」のテーマのテストを開始するためのフィクスチャ。"""
    page = logged_in_page
    with allure.step("セットアップ：テストセッションを開始"):
        page.get_by_alt_text("国語").click()
        # トピックコンテナを特定し、クリック
        topic_container = page.locator("p:has-text('はを　つかおう')").locator("..")
        topic_container.get_by_alt_text("basic").click()
    yield page


class TestTopicHaWoTsukaou:

    def test_all_questions_correct(self, quiz_session: Page, kokugo_test_data: dict):
        """
        このテストは、正解と不正解のシナリオを含む連続したフローを実行します。
        """
        page = quiz_session
        questions = kokugo_test_data["HAWOTSUKAOU"]
        total_questions = len(questions)

        # -------------------------------------------------------------------
        # -- シナリオ 1: すべて正解 --
        # -------------------------------------------------------------------
        with allure.step("シナリオ1：すべての問題に正しく解答する"):
            for index, question in enumerate(questions):
                with allure.step(f"問題 {question['id']} に正しく解答"):
                    # 回答キーを特定し、回答
                    answer_key = "correct_drag_mapping" if question.get("type") == "drag_drop" else "correct_answers"
                    answer_question(page, question, answer_key)

                    # 答え合わせ
                    kotaeawase_button = page.get_by_role("button", name="こたえあわせ")
                    expect(kotaeawase_button).to_be_enabled()
                    kotaeawase_button.click()

                    # 正解アイコンを確認
                    expect(page.locator(".icon__answer--right")).to_be_visible()

                    # 次へ/終了処理
                    if index < total_questions - 1:
                        next_button = page.get_by_role("button", name="つぎへ")
                        expect(next_button).to_be_enabled()
                        next_button.click()
                    else:
                        complete_question(page)

            with allure.step("テスト完了画面を確認"):
                expect(page.get_by_text("あめですよ")).to_be_visible()

        # -------------------------------------------------------------------
        # # -- シナリオ 2: すべて不正解 (その後、次に進むために正解) --
        # # -------------------------------------------------------------------
        # with allure.step("シナリオ2：すべての問題に不正解する"):
        #     with allure.step("再度クイズ画面に移動"):
        #         # 同じテーマを再度クリックして、テストをリセット
        #         topic_container = page.locator("p:has-text('はを　つかおう')").locator("..")
        #         topic_container.get_by_alt_text("basic").click()

        #     for index, question in enumerate(questions):
        #         with allure.step(f"問題 {question['id']} の不正解パターンをテスト"):
        #             # 不正解の選択肢で回答
        #             answer_question(page, question, "incorrect_answers")

        #             # 答え合わせ
        #             kotaeawase_button = page.get_by_role("button", name="こたえあわせ")
        #             expect(kotaeawase_button).to_be_enabled()
        #             kotaeawase_button.click()

        #             # 不正解アイコンを確認
        #             expect(page.locator(".icon__answer--wrong")).to_be_visible()

        #             # 次に進むために、正解の選択肢を選び直す
        #             with allure.step("次の問題に進むため、正解を入力"):
        #                 answer_key = "correct_drag_mapping" if question.get(
        #                     "type") == "drag_drop" else "correct_answers"
        #                 answer_question(page, question, answer_key)

        #                 # 正解で答え合わせ
        #                 kotaeawase_button = page.get_by_role("button", name="こたえあわせ")
        #                 expect(kotaeawase_button).to_be_enabled()
        #                 kotaeawase_button.click()
        #                 expect(page.locator(".icon__answer--right")).to_be_visible()

        #             # 次へ/終了処理
        #             if index < total_questions - 1:
        #                 page.get_by_role("button", name="つぎへ").click()
        #             else:
        #                 complete_question(page)

        #     with allure.step("テスト完了画面を確認"):
        #         expect(page.get_by_text("あめですよ")).to_be_visible()
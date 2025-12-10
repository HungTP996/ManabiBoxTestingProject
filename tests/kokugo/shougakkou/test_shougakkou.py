import pytest
import allure
from playwright.sync_api import Page, expect
from tests.utils.choice_helpers import answer_question
from tests.utils.complete_helpers import complete_question


@pytest.fixture(scope="class")
def quiz_session(logged_in_page: Page):
    """「小学校の　ことを　しょうかいしよう」のテーマのテストを開始するためのフィクスチャ。"""
    page = logged_in_page
    with allure.step("セットアップ：テストセッションを開始"):
        page.get_by_alt_text("国語").click()
        # ID '20-0' を持つトピックコンテナをクリック
        topic_container = page.locator('[id="20-0"]')
        topic_container.click()
    yield page


class Test_Shougakkou:
    # クラス名をテーマに合わせて 'Test_Shougakkou' に変更しました
    def test_all_questions(self, quiz_session: Page, kokugo_test_data: dict):
        """シナリオ1：すべての問題に正しく解答する。"""
        page = quiz_session

        with allure.step("テストデータを準備"):
            # データキーを 'SHOUGAKKOU' に合わせます
            questions = kokugo_test_data["SHOUGAKKOU"]
            total_questions = len(questions)

        for index, question_data in enumerate(questions):
            with allure.step(f"問題 {index + 1}/{total_questions} に正しく解答"):
                # 1. 回答
                answer_question(page, question_data, "correct_answers")

                # 2. 「こたえあわせ」ボタンをクリック
                kotaeawase_button = page.get_by_role("button", name="こたえあわせ")
                expect(kotaeawase_button).to_be_enabled(timeout=10000)
                kotaeawase_button.click()

                # 3. 正解を確認
                expect(page.locator(".icon__answer--right")).to_be_visible()
                if "expected_message" in question_data:
                    expect(page.get_by_text(question_data["expected_message"])).to_be_visible()

                # 4. 次へ/終了処理
                if index < total_questions - 1:
                    with allure.step("次の問題へ"):
                        page.get_by_role("button", name="つぎへ").click()
                else:
                    with allure.step("テストを完了"):
                        complete_question(page)

        with allure.step("テスト完了画面を確認"):
            expect(page.get_by_text("あめですよ")).to_be_visible()
import pytest
import allure
from playwright.sync_api import Page, expect
from tests.utils.choice_helpers import answer_question
from tests.utils.complete_helpers import complete_question


@pytest.fixture(scope="class")
def quiz_session(logged_in_page: Page):
    """「かんじの はなし」のテーマのテストを開始するためのフィクスチャ。"""
    page = logged_in_page
    with allure.step("セットアップ：テストセッションを開始"):
        page.get_by_alt_text("国語").click()
        # トピックコンテナを特定し、クリック
        topic_container = page.locator("p:has-text('かんじの　はなし')").locator("..")
        topic_container.get_by_alt_text("basic").click()
    yield page


class TestKanjiNoHanashi:

    def test_all_questions_correct(self, quiz_session: Page, kokugo_test_data: dict):

        page = quiz_session
        questions = kokugo_test_data["KANJINOHANASHI"]
        total_questions = len(questions)

        # -------------------------------------------------------------------
        # -- シナリオ 1: すべて正解 --
        # -------------------------------------------------------------------
        with allure.step("シナリオ1：すべての問題に正しく解答する"):
            for index, question in enumerate(questions):
                with allure.step(f"問題 {question['id']} に正しく解答"):

                    question_type = question.get("type", "text")

                    if question_type == "drag_drop":
                        # ドラッグアンドドロップの場合は "correct_drag_mapping" を使用
                        answer_question(page, question, "correct_drag_mapping")
                    else:
                        # その他のタイプの問題には "correct_answers" を使用
                        answer_question(page, question, "correct_answers")
                    # ===================================================================

                    # 答え合わせ
                    page.get_by_role("button", name="こたえあわせ").click()

                    # 正解を確認
                    expect(page.locator(".icon__answer--right")).to_be_visible()

                    # 次へ/終了処理
                    if index < total_questions - 1:
                        with allure.step("次の問題へ"):
                            page.get_by_role("button", name="つぎへ").click()
                    else:
                        with allure.step("テストを完了"):
                            complete_question(page)

            with allure.step("テスト完了画面を確認"):
                # 完了画面に表示されるトピック名などを確認
                expect(page.get_by_text("あめですよ")).to_be_visible()
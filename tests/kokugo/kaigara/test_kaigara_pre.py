import pytest
import allure
import json
from pathlib import Path
from playwright.sync_api import Page, expect
from tests.utils.choice_helpers import answer_question
from tests.utils.drawing_helpers import draw_character
from tests.utils.complete_helpers import confirm_score_and_proceed, complete_question


@pytest.fixture(scope="class")
def quiz_session(logged_in_page: Page):
    page = logged_in_page
    with allure.step("セットアップ：テストセッションを開始"):
        page.get_by_alt_text("国語").click()
        page.locator(".p-10px > p").nth(3).click()
    yield page

@pytest.fixture(scope="module")
def quiz_data():
    """ファイル 'kaigara_data.json' からすべてのデータをロードする。"""
    current_file_path = Path(__file__)
    kaigara_dir = current_file_path.parent
    json_path = kaigara_dir / "kaigara_data.json"

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        pytest.fail(f"エラー: データファイルが見つかりません: {json_path}")
    return data


class TestKaigaraPre:
    def test_all_drawings(self, quiz_session: Page, quiz_data: dict):
        """
        テストシナリオ: すべての描画タスクをテストする。
        """
        page = quiz_session
        drawing_data_list = quiz_data.get("DRAWING_QUESTIONS", [])
        if not drawing_data_list:
            pytest.fail("データファイルに 'DRAWING_QUESTIONS' が見つかりません。")

        total_drawing_questions = len(drawing_data_list)

        with allure.step(f"パート 1: 描画問題 {total_drawing_questions} 問を実行"):
            for i, question_data in enumerate(drawing_data_list):
                word = question_data.get("word")
                with allure.step(f"描画問題 {i + 1}/{total_drawing_questions}: 「{word}」"):
                    draw_character(page, question_data)
                    confirm_score_and_proceed(page)

        print(f"描画問題 {total_drawing_questions} 問を完了しました。パート 2 へ進みます...")

        choice_questions = quiz_data.get("CHOICE_QUESTIONS", [])
        if not choice_questions:
            pytest.fail("データファイルに 'CHOICE_QUESTIONS' が見つかりません。")

        total_choice_questions = len(choice_questions)

        with allure.step(f"パート 2: 選択式問題 {total_choice_questions} 問を実行"):
            for index, question in enumerate(choice_questions):
                # 質問IDとタイプを表示
                with allure.step(f"選択式問題 {question['id']} (タイプ: {question.get('type')})"):

                    # 1. 質問に回答 (Helperを使用)
                    # ドラッグアンドドロップの場合は 'correct_drag_mapping' を使用、それ以外は 'correct_answers' を使用
                    answer_key = "correct_drag_mapping" if question.get("type") == "drag_drop" else "correct_answers"
                    answer_question(page, question, answer_key)

                    # 2. 'こたえあわせ' ボタンをクリック
                    kotaeawase_button = page.get_by_role("button", name="こたえあわせ")
                    expect(kotaeawase_button).to_be_enabled(timeout=10000)
                    kotaeawase_button.click()

                    # 3. 結果の確認 (正解アイコンが表示されることを確認)
                    expect(page.locator(".icon__answer--right")).to_be_visible(timeout=10000)

                    # 4. 最終問題/中間問題の処理
                    is_last_question = (index == total_choice_questions - 1)
                    if is_last_question:
                        # これがテスト全体の最終問題の場合
                        with allure.step("テスト全体の最終問題の処理"):
                            complete_question(page)  # 終了処理関数を呼び出す
                    else:
                        # まだ問題が残っている場合、'つぎへ' をクリック
                        with allure.step("'つぎへ' をクリックして次の問題へ"):
                            next_button = page.get_by_role("button", name="つぎへ")
                            expect(next_button).to_be_enabled(timeout=10000)
                            next_button.click()
                            # 新しいページの読み込みを待機 (重要)
                            page.wait_for_load_state("networkidle", timeout=10000)

        with allure.step("すべての質問を完了"):
            print("テスト全体を完了しました。")

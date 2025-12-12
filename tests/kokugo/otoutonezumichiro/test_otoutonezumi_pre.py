import pytest
import allure
import json
from pathlib import Path
from playwright.sync_api import Page, expect

# ヘルパー関数をインポート
from tests.utils.complete_helpers import confirm_score_and_proceed, complete_question
from tests.utils.drawing_helpers import draw_character
from tests.utils.choice_helpers import answer_question


@pytest.fixture(scope="module")
def quiz_data():
    """ファイル 'otoutonezumichiro_data.json' からデータをロードする。"""
    current_file_path = Path(__file__)
    otoutonezumichiro_dir = current_file_path.parent
    json_path = otoutonezumichiro_dir / "otoutonezumichiro_data.json"

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        pytest.fail(f"エラー: データファイルが見つかりません: {json_path}")
    return data


@pytest.fixture(scope="function")
def drawing_page(logged_in_page: Page):
    """描画ページへ遷移するためのフィクスチャ。"""
    page = logged_in_page
    with allure.step("国語プレテスト (おとうとねずみ) の描画ページへ移動"):
        page.get_by_alt_text("国語").click()
        # プレテストのトピック番号7をクリック
        page.get_by_text("プレテスト").nth(7).click()
    yield page


def test_full_quiz_flow(drawing_page: Page, quiz_data: dict):
    page = drawing_page
    drawing_data_list = quiz_data.get("DRAWING_QUESTIONS", [])
    if not drawing_data_list:
        pytest.fail("データファイルに 'DRAWING_QUESTIONS' が見つかりません。")

    total_drawing_questions = len(drawing_data_list)

    # -------------------------------------------------------------------
    # ## パート 1: 描画問題の実行
    # -------------------------------------------------------------------
    with allure.step(f"パート 1: 描画問題 {total_drawing_questions} 問を実行"):
        for i, question_data in enumerate(drawing_data_list):
            word = question_data.get("word")
            with allure.step(f"描画問題 {i + 1}/{total_drawing_questions}: 「{word}」"):
                # 1. 文字を描画
                draw_character(page, question_data)
                # 2. 採点 および '次へ' ボタンをクリック
                confirm_score_and_proceed(page)

        print(f"描画問題 {total_drawing_questions} 問を完了しました。パート 2 へ進みます...")

    choice_questions = quiz_data.get("CHOICE_QUESTIONS", [])
    if not choice_questions:
        pytest.fail("データファイルに 'CHOICE_QUESTIONS' が見つかりません。")

    total_choice_questions = len(choice_questions)

    # -------------------------------------------------------------------
    # ## パート 2: 選択式問題の実行
    # -------------------------------------------------------------------
    with allure.step(f"パート 2: 選択式問題 {total_choice_questions} 問を実行"):
        for index, question in enumerate(choice_questions):
            with allure.step(f"選択式問題 {question['id']} (タイプ: {question.get('type')})"):

                # 1. 質問に回答
                answer_key = "correct_drag_mapping" if question.get("type") == "drag_drop" else "correct_answers"
                answer_question(page, question, answer_key)

                # 2. 'こたえあわせ' ボタンをクリック
                kotaeawase_button = page.get_by_role("button", name="こたえあわせ")
                expect(kotaeawase_button).to_be_enabled(timeout=10000)
                kotaeawase_button.click()

                # 3. 正解を確認
                expect(page.locator(".icon__answer--right")).to_be_visible(timeout=10000)

                # 4. 最終問題/中間問題の処理
                is_last_question = (index == total_choice_questions - 1)
                if is_last_question:
                    with allure.step("テスト全体の最終問題の処理"):
                        complete_question(page)
                else:
                    with allure.step("'つぎへ' をクリックして次の問題へ"):
                        next_button = page.get_by_role("button", name="つぎへ")
                        expect(next_button).to_be_enabled(timeout=10000)
                        next_button.click()
                        # 新しいページの読み込みを待機
                        page.wait_for_load_state("networkidle", timeout=10000)

    with allure.step("すべての質問を完了"):
        print("テスト全体を完了しました。")
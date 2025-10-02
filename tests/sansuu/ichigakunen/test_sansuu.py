import pytest
from playwright.sync_api import Page, expect
import json

# ===================================================================
# == FIXTURE SETUP: テスト環境の準備 ==
# ===================================================================

@pytest.fixture(scope="function")
def go_quiz_page(logged_in_page: Page):
    page = logged_in_page
    # ステップ1: 「算数」科目をクリック
    page.get_by_alt_text("算数").click()

    # ページの読み込みを待機
    validate_title = page.get_by_text("わくわく　がっこう", exact=True)
    expect(validate_title).to_be_visible()

    # .nth(0)の代わりに、親コンテナを見つけてから子ボタンを見つける
    go_button = page.get_by_text("プレテスト", exact=True).first
    go_button.click()

    # テスト開始前に「こたえあわせ」ボタンが表示されるのを待機
    expect(page.get_by_role("button", name="こたえあわせ")).to_be_visible(timeout=10000)

    yield page

# これらの関数はフィクスチャの外、ファイルのトップレベルに配置
def get_test_cases_by_topic(path, topic_name):
    with open(path, 'r', encoding='utf-8') as f:
        all_data = json.load(f)
    return [case for case in all_data if case.get("topic") == topic_name]

test_data_path = 'tests/sansuu/ichigakunen/data.json'

# wakuwaku gakkouテストの本体
class TestGo:
    def test_full_quiz_and_review_flow(self, kanji_go_quiz_page: Page):
        page = go_quiz_page()
        test_cases = get_test_cases_by_topic(test_data_path, "wakuwaku_gakkou")

        print("\n--- 問題の解答を開始します ---")

        for test_case in test_cases:
            print(f"--- TC実行中: {test_case['id']} ---")

            # 1つの問題に対する解答ロジック
            correct_answer = page.locator(test_case['correct_answers'][0])
            expect(correct_answer).to_be_visible()
            correct_answer.click()

            check_answer_button = page.get_by_role("button", name="こたえあわせ")
            check_answer_button.click()

            feedback_text = page.get_by_text(test_case['expected_message'])
            expect(feedback_text).to_be_visible()

            # 最後の問題でない場合のみ「つぎへ」をクリック
            if test_case != test_cases[-1]:
                print("--> 次の問題へ移動します...")
                next_button = page.get_by_role("button", name="つぎへ")
                next_button.click()
                # 新しい問題に移動したことを確認
                expect(check_answer_button).to_be_visible(timeout=10000)

        print("\n--- 全ての問題が完了しました。ふりかえりを開始します。 ---")

        review_button = page.get_by_role("button", name="ふりかえり")
        review_button.click()

        review_title = page.get_by_text("ふりかえり", exact=True)
        expect(review_title).to_be_visible()

        finish_button = page.get_by_role("button", name="おわる")
        finish_button.click()

        print("--- テストフローが完了しました。 ---")
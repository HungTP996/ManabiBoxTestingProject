import pytest
from playwright.sync_api import Page, expect
import json
from pathlib import Path

@pytest.fixture(scope="function")
def go_quiz_page(logged_in_page: Page):
    page = logged_in_page

    # Chờ load xong
    page.wait_for_load_state("networkidle")

    # ステップ1: 「計算」科目をクリック
    page.get_by_alt_text("計算").click()

    # ページの読み込みを待機
    validate_title = page.get_by_text("1．かずと　すうじ", exact=True)
    expect(validate_title).to_be_visible()

    # .nth(0)の代わりに、親コンテナを見つけてから子ボタンを見つける
    go_button = page.get_by_text("力だめし", exact=True).first
    go_button.click()

    # テスト開始前に「こたえあわせ」ボタンが表示されるのを待機
    expect(page.get_by_role("button", name="こたえあわせ")).to_be_visible(timeout=10000)

    yield page

def get_test_cases(topic_name):
    current_dir = Path(__file__).parent.absolute()
    json_path = current_dir / "data.json"

    if not json_path.exists():
        json_path = Path('tests/keisan/ichigakunen/data.json')
        if not json_path.exists():
            raise FileNotFoundError(f"Không tìm thấy file data.json tại: {current_dir}")

    with open(json_path, 'r', encoding='utf-8') as f:
        all_data = json.load(f)
    return [case for case in all_data if case.get("topic") == topic_name]


# kazutosuujiテストの本体
class TestKazutoSuuji:
    def test_verify_happycase_kazutosuuji(self, go_quiz_page: Page):
        page = go_quiz_page

        # Load data thông qua hàm helper mới
        test_cases = get_test_cases("kazutosuuji")

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

                # Chờ animation chuyển câu
                page.wait_for_timeout(500)
                # 新しい問題に移動したことを確認
                expect(check_answer_button).to_be_visible(timeout=10000)

        print("\n--- 全ての問題が完了しました。ふりかえりを開始します。 ---")

        review_button = page.get_by_role("button", name="ふりかえり")
        # Đợi nút hiển thị trước khi click
        expect(review_button).to_be_visible(timeout=5000)
        review_button.click()

        review_title = page.get_by_text("ふりかえり", exact=True)
        expect(review_title).to_be_visible()

        finish_button = page.get_by_role("button", name="おわる")
        finish_button.click()

        print("--- テストフローが完了しました。 ---")
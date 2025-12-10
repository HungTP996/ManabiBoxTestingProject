import pytest
from playwright.sync_api import Page, expect
import json
from pathlib import Path

@pytest.fixture(scope="function")
def go_quiz_page(logged_in_page: Page):
    page = logged_in_page

    # ページの読み込み完了を待機
    page.wait_for_load_state("networkidle")

    # ステップ1: 「算数」科目をクリック
    page.get_by_alt_text("算数").click()

    # ページの読み込みを待機
    validate_title = page.get_by_text("わくわく　がっこう", exact=True)
    expect(validate_title).to_be_visible()

    # .nth(0)の代わりに、親コンテナを見つけてから子ボタンを見つける
    # プレテストボタンをクリック
    go_button = page.get_by_text("プレテスト", exact=True).first
    go_button.click()

    # テスト開始前に「こたえあわせ」ボタンが表示されるのを待機
    expect(page.get_by_role("button", name="こたえあわせ")).to_be_visible(timeout=10000)

    yield page


# Helper function: Load data
def get_test_cases_by_topic(topic_name):
    # 現在のファイルパスに基づいて data.json を自動的に検索
    current_dir = Path(__file__).parent.absolute()
    json_path = current_dir / "data.json"

    if not json_path.exists():
        # フォールバック: ハードコードされたパスを試行
        json_path = Path('tests/sansuu/ichigakunen/data.json')
        if not json_path.exists():
            raise FileNotFoundError(f"data.json が見つかりません: {current_dir} またはフォールバックパス")

    with open(json_path, 'r', encoding='utf-8') as f:
        all_data = json.load(f)

    # Topic lọc dữ liệu
    raw_cases = [case for case in all_data if case.get("topic") == topic_name]

    # --- KHẮC PHỤC LỖI TRÙNG LẶP ---
    # Loại bỏ các test case có ID trùng nhau để tránh vòng lặp chạy quá số lượng câu hỏi thực tế
    unique_cases = []
    seen_ids = set()

    for case in raw_cases:
        if case['id'] not in seen_ids:
            unique_cases.append(case)
            seen_ids.add(case['id'])

    return unique_cases


# wakuwaku gakkouテストの本体
class TestSanSuu:
    # 修正: フィクスチャ名 'go_quiz_page' を正しく指定
    def test_full_quiz_and_review_flow(self, go_quiz_page: Page):

        page = go_quiz_page

        # テストデータの読み込み
        test_cases = get_test_cases_by_topic("wakuwaku_gakkou")

        print(f"\n--- Load được {len(test_cases)} câu hỏi (đã lọc trùng) ---")
        print("\n--- 問題の解答を開始します ---")

        # Dùng enumerate để biết chính xác index hiện tại
        for index, test_case in enumerate(test_cases):
            print(f"--- TC実行中: {test_case['id']} ---")

            # 1つの問題に対する解答ロジック
            # 正解を選択
            correct_answer = page.locator(test_case['correct_answers'][0])
            expect(correct_answer).to_be_visible()
            correct_answer.click()

            # 「こたえあわせ」ボタンをクリック
            check_answer_button = page.get_by_role("button", name="こたえあわせ")
            check_answer_button.click()

            # フィードバックメッセージの確認
            feedback_text = page.get_by_text(test_case['expected_message'])
            expect(feedback_text).to_be_visible()

            # Logic chuyển câu: Nếu chưa phải là câu cuối cùng trong danh sách
            if index < len(test_cases) - 1:
                print("--> 次の問題へ移動します...")
                next_button = page.get_by_role("button", name="つぎへ")
                next_button.click()

                # 新しい問題に移動したことを確認
                page.wait_for_timeout(500)  # 安定性のための待機
                expect(check_answer_button).to_be_visible(timeout=10000)
            else:
                print("--> 最後の問題です。次はふりかえりに進みます。")

        print("\n--- 全ての問題が完了しました。ふりかえりを開始します。 ---")

        # 「ふりかえり」ボタンをクリック
        review_button = page.get_by_role("button", name="ふりかえり")
        # Đợi nút hiển thị (quan trọng vì sau câu cuối cần 1 chút thời gian animation)
        expect(review_button).to_be_visible(timeout=5000)
        review_button.click()

        review_title = page.get_by_text("ふりかえり", exact=True)
        expect(review_title).to_be_visible()

        # 「おわる」ボタンをクリック
        finish_button = page.get_by_role("button", name="おわる")
        finish_button.click()

        print("--- テストフローが完了しました。 ---")
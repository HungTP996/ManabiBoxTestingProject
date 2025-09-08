# tests/kokugo/test_ha_wo_tsukaou.py

import pytest
from playwright.sync_api import Page, expect
from .kokugo_data import QUESTIONS_DATA_HA_WO_TSUKAOU


@pytest.fixture(scope="class")
def kokugo_main_page(logged_in_page: Page):
    """
    このFixtureは一度だけ実行されます：ログインして国語の教科ページに移動します。
    (Fixture này chạy 1 lần duy nhất: Đăng nhập và vào trang môn học Kokugo.)
    """
    page = logged_in_page
    print("\n--- [CLASS SETUP] ログインし、国語ページへ遷移します ---")
    page.get_by_alt_text("国語").click()
    expect(page.get_by_text("あめですよ").first).to_be_visible()
    yield page


@pytest.fixture(scope="function")
def quiz_session(kokugo_main_page: Page):
    """
    このFixtureは各テストケースの前に実行されます。
    セットアップ：国語ページからトピックをクリックし、問題画面に移動します。
    (Fixture này chạy TRƯỚC mỗi hàm test.
    Setup: Từ trang Kokugo, click vào chủ đề để vào màn hình làm bài.)
    """
    page = kokugo_main_page
    # --- セットアップ処理（各テストの前に実行） ---
    print(f"\n--- [FUNCTION SETUP] 「はを つかおう」テーマの問題画面へ遷移します ---")
    topic_container = page.locator("p:has-text('はを　つかおう')").locator("..")
    topic_container.get_by_alt_text("basic").click()

    yield page  # テスト関数に制御を渡します (Giao quyền cho hàm test)

    # --- ティアダウン処理（各テストの後に実行） ---
    print(f"--- [FUNCTION TEARDOWN] シナリオを終了します ---")


# ===================================================================
# == テストクラス：テストシナリオを格納 ==
# (LỚP TEST: Chứa các kịch bản test)
# ===================================================================

class TestTopicHaWoTsukaou:

    def test_full_quiz_happy_path(self, quiz_session: Page):
        """
        シナリオ1：問1から問5まで順番に正解します。
        (Kịch bản 1: Trả lời đúng tuần tự từ câu 1 đến câu 5.)
        """
        page = quiz_session
        print("\n--- 問1から問5まで正解するシナリオを開始 ---")

        for index, question in enumerate(QUESTIONS_DATA_HA_WO_TSUKAOU):
            question_type = question.get("type", "text")
            print(f"--> 質問 {question['id']} を実行中（タイプ：{question_type}）")

            # --- 回答選択問題を処理 ---
            if question_type == "text":
                for answer in question["correct_answers"]:
                    page.get_by_text(answer, exact=True).click()

            # --- 穴埋め問題を処理 ---
            elif question_type == "fill_blank":
                for action in question["correct_answers"]:
                    blank_box = page.locator(action["blank_locator"])
                    choice = page.get_by_text(action["choice_text"], exact=True)
                    blank_box.click()
                    choice.click()

            # --- ドラッグ＆ドロップ問題を処理 ---
            elif question_type == "drag_drop":
                for drag_action in question["correct_drag_mapping"]:
                    item_text = question["items_to_drag"][drag_action["item"]]
                    zone_selector = question["drop_zones"][drag_action["zone"]]
                    drop_zone = page.locator(zone_selector).nth(0 if drag_action["zone"] == "zone1" else 1)
                    page.get_by_text(item_text).drag_to(drop_zone)

            # --- 確認と次のステップへ ---
            page.get_by_role("button", name="こたえあわせ").click()

            if index < len(QUESTIONS_DATA_HA_WO_TSUKAOU) - 1:
                page.get_by_role("button", name="つぎへ").click()
            else:
                # 回答終了フロー
                review_button = page.get_by_role("button", name="ふりかえり")
                expect(review_button).to_be_visible()
                review_button.click()

                review_title = page.locator("p:has-text('ふりかえり')")
                expect(review_title).to_be_visible()

                finish_button = page.get_by_text("おわる", exact=True)
                expect(finish_button).to_be_visible()
                finish_button.click()

        print("--- 正解シナリオを完了しました ---")
        expect(page.get_by_text("あめですよ").first).to_be_visible()

    def test_full_quiz_all_incorrect(self, quiz_session: Page):
        """
        シナリオ2：すべての質問に不正解します。
        (Kịch bản 2: Trả lời sai tất cả các câu hỏi.)
        """
        page = quiz_session
        print("\n--- 不正解シナリオを開始 ---")

        for index, question in enumerate(QUESTIONS_DATA_HA_WO_TSUKAOU):
            question_type = question.get("type", "text")
            print(f"--> 質問 {question['id']} を実行中（不正解を選択）")

            # --- 不正解シナリオ「incorrect_answers」から読み込み ---
            if question_type == "text":
                incorrect_answer = question["incorrect_answers"][0]
                page.get_by_text(incorrect_answer, exact=True).click()

            # --- 不正解シナリオ「incorrect_answers」から読み込み ---
            elif question_type == "fill_blank":
                for action in question["incorrect_answers"]:
                    blank_box = page.locator(action["blank_locator"])
                    choice = page.get_by_text(action["choice_text"], exact=True)
                    blank_box.click()
                    choice.click()

            # --- 不正解シナリオ「incorrect_drag_mapping」から読み込み ---
            elif question_type == "drag_drop":
                for drag_action in question["incorrect_drag_mapping"]:
                    item_text = question["items_to_drag"][drag_action["item"]]
                    zone_selector = question["drop_zones"][drag_action["zone"]]
                    drop_zone = page.locator(zone_selector).nth(0 if drag_action["zone"] == "zone1" else 1)
                    page.get_by_text(item_text).drag_to(drop_zone)

            # --- 確認と次のステップへ ---
            page.get_by_role("button", name="こたえあわせ").click()

            # 結果が不正解であることを確認
            expect(page.locator(".icon__answer--wrong")).to_be_visible()

            # 回答後に次のステップへ
            if index < len(QUESTIONS_DATA_HA_WO_TSUKAOU) - 1:
                page.get_by_role("button", name="つぎへ").click()
            else:
                # 終了フロー（上記と同じ）
                review_button = page.get_by_role("button", name="ふりかえり")
                expect(review_button).to_be_visible()
                review_button.click()
                review_title = page.locator("p:has-text('ふりかえり')")
                expect(review_title).to_be_visible()
                finish_button = page.get_by_text("おわる", exact=True)
                expect(finish_button).to_be_visible()
                finish_button.click()

        print("--- 不正解シナリオを完了しました ---")
        expect(page.get_by_text("あめですよ").first).to_be_visible()
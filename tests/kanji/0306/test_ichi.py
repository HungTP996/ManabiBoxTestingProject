import pytest
from playwright.sync_api import Page, expect
import os

# ===================================================================
# == FIXTURE SETUP: テスト環境の準備 ==
# ===================================================================
@pytest.fixture(scope="function")
def kanji_go_quiz_page(logged_in_page: Page):
    """
    このフィクスチャは漢字「一」の練習画面への完全な移動を実行します。
    """
    page = logged_in_page
    print("\n--- [SETUP] 漢字「一」の練習画面への移動を開始 ---")
    # ステップ1: 「漢字」教科を選択
    page.get_by_alt_text("漢字").click()
    # Kanjiページの読み込み完了を待機（「一」ボタンの存在を確認）
    go_button_in_list = page.get_by_text("一　", exact=True)
    expect(go_button_in_list).to_be_visible(timeout=10000)
    # ステップ2: 「一」をクリックして詳細を表示
    go_button_in_list.click()
    # ステップ3: 「つぎにすすむ」をクリックして描画画面へ移動
    page.get_by_text("つぎにすすむ").click()
    # 描画画面が表示されるのを待機
    expect(page.locator(".kanji-canvas.upper-canvas")).to_be_visible()
    print("--- [SETUP] 描画画面に到達し、テストの準備が完了 ---")
    yield page

# ===================================================================
# == TEST CLASS: 漢字「一」のテストシナリオ ==
# ===================================================================

class TestGo:
    def test_kanji_jon_drawing_only(self, kanji_go_quiz_page: Page):
        """
        テストシナリオ: 漢字「一」を描画し、各ステップを進める（AI検証をスキップ）。
        """
        page = kanji_go_quiz_page
        for i in range(3):
            print(f"\n--> {i + 1}回目の描画と検証を開始")

            # 描画キャンバスのロケーターと座標を取得
            drawing_canvas = page.locator(".kanji-canvas.upper-canvas")
            expect(drawing_canvas).to_be_visible()
            expect(drawing_canvas).to_be_enabled()
            page.wait_for_timeout(5000)

            canvas_box = None
            for _ in range(5):
                canvas_box = drawing_canvas.bounding_box()
                if canvas_box:
                    break
                page.wait_for_timeout(200)
            assert canvas_box, "Canvas の bounding_box が取得できません"
            origin_x, origin_y = canvas_box["x"], canvas_box["y"]

            # --- 画1: 横画 ---
            page.mouse.move(origin_x + 45,  origin_y + 172)
            page.mouse.down()
            page.mouse.move(origin_x + 150, origin_y + 165)
            page.mouse.move(origin_x + 275,  origin_y + 160)
            page.mouse.up()


            canvas_to_verify = page.locator(".kanji-canvas.upper-canvas").first
            folder_name = "ai_screenshots"
            os.makedirs(folder_name, exist_ok=True)
            # 各イテレーションでファイル名を変更して上書きを避ける
            screenshot_path = os.path.join(folder_name, f"jon_drawing_to_verify_{i + 1}.png")
            expect(canvas_to_verify).to_be_visible(timeout=10000)
            canvas_to_verify.scroll_into_view_if_needed()
            canvas_to_verify.screenshot(path=screenshot_path)
            print(f"-> 描画キャンバスのスクリーンショットを保存: {screenshot_path}")

            # --- 遷移 ---
            submit_btn = page.get_by_text("つけ").first
            expect(submit_btn).to_be_visible(timeout=10000)
            expect(submit_btn).to_be_enabled(timeout=10000)
            submit_btn.click()
            expect(page.get_by_alt_text("level return")).to_be_visible()
            page.get_by_text("つぎにすすむ").click()

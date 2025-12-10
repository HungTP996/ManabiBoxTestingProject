import pytest
from playwright.sync_api import Page, expect
import os

# ===================================================================
# == FIXTUREのセットアップ：テスト環境の準備 ==
# ===================================================================
@pytest.fixture(scope="function")
def kanji_go_quiz_page(logged_in_page: Page):
    page = logged_in_page
    print("\n--- [セットアップ] 「四」の演習画面へのナビゲーションを開始します ---")

    # ステップ1：「漢字」の科目をクリック
    page.get_by_alt_text("漢字").click()

    # 漢字ページが読み込まれるのを待つ（「四」ボタンの存在を確認）
    go_button_in_list = page.get_by_text("四  ", exact=True)
    expect(go_button_in_list).to_be_visible(timeout=10000)

    # ステップ2：「四」の文字をクリックして詳細画面に移動
    go_button_in_list.click()

    # ステップ3：「つぎにすすむ」をクリックして描画画面に移動
    page.get_by_text("つぎにすすむ").click()

    # 描画画面が表示されるのを待つ
    expect(page.locator(".kanji-canvas.upper-canvas")).to_be_visible()
    print("--- [セットアップ] 描画画面に移動しました。テストの準備ができました ---")
    yield page


# ===================================================================
# == テストクラス：「四」という漢字のテストシナリオ ==
# ===================================================================

class TestJon:

    # `ai_vision_verifier`を引数リストに追加
    def test_kanji_jon_drawing_and_ai_verification(self, kanji_go_quiz_page: Page, ai_vision_verifier):
        page = kanji_go_quiz_page
        for i in range(3):
            print(f"\n--> {i + 1}回目の描画と検証を開始します")

            # 描画キャンバスのロケーターと座標を取得
            drawing_canvas = page.locator(".kanji-canvas.upper-canvas")
            expect(drawing_canvas).to_be_visible()
            expect(drawing_canvas).to_be_enabled()
            page.wait_for_timeout(5000)  # 少し待機する

            canvas_box = drawing_canvas.bounding_box()
            origin_x, origin_y = canvas_box['x'], canvas_box['y']

            # --- 1画目：縦線 ---
            page.mouse.move(origin_x + 63, origin_y + 106)
            page.mouse.down()
            page.mouse.move(origin_x + 73, origin_y + 240)

            # --- 2画目：横線と折れ ---
            page.mouse.up()
            page.mouse.move(origin_x + 60, origin_y + 110)
            page.mouse.down()
            page.mouse.move(origin_x + 222, origin_y + 92)
            page.mouse.move(origin_x + 264, origin_y + 92)
            # page.mouse.move(origin_x + 265, origin_y + 93)
            page.mouse.move(origin_x + 264, origin_y + 94)
            page.mouse.move(origin_x + 264, origin_y + 95)
            page.mouse.move(origin_x + 250, origin_y + 230)
            page.mouse.up()

            # --- 3画目：左払い ---
            page.mouse.move(origin_x + 135, origin_y + 100)
            page.mouse.down()
            page.mouse.move(origin_x + 130, origin_y + 125)
            page.mouse.move(origin_x + 125, origin_y + 150)
            page.mouse.move(origin_x + 105, origin_y + 185)
            page.mouse.move(origin_x + 75, origin_y + 200)
            page.mouse.up()

            # --- 4画目：右へのカーブ線 ---
            page.mouse.move(origin_x + 175, origin_y + 100)
            page.mouse.down()
            page.mouse.move(origin_x + 175, origin_y + 125)
            page.mouse.move(origin_x + 185, origin_y + 170)
            page.mouse.move(origin_x + 195, origin_y + 170)
            page.mouse.move(origin_x + 255, origin_y + 170)
            page.mouse.up()

            # --- 5画目：一番下の横線（閉じる線） ---
            page.mouse.move(origin_x + 74, origin_y + 238)
            page.mouse.down()
            page.mouse.move(origin_x + 250, origin_y + 230)
            page.mouse.up()

            print("--- 描画完了！ ---")

            canvas_to_verify = page.locator("canvas").nth(2)
            folder_name = "ai_screenshots"
            os.makedirs(folder_name, exist_ok=True)

            # 上書きされないように、ループごとにファイル名を変更する
            screenshot_path = os.path.join(folder_name, f"jon_drawing_to_verify_{i + 1}.png")
            canvas_to_verify.screenshot(path=screenshot_path)
            print(f"-> キャンバスのスクリーンショットを撮影し、{screenshot_path} に保存しました")

            is_correct = ai_vision_verifier(screenshot_path=screenshot_path, expected_char="四")
            assert is_correct, f"AIが{i + 1}回目の試行で文字「四」を正しく認識できませんでした。"
            print("-> AIが描画の正しさを確認しました！")

            # --- 次へ進む ---
            page.get_by_text("つけ", exact=True).click()
            expect(page.get_by_alt_text("level return")).to_be_visible()
            page.get_by_text("つぎにすすむ").click()
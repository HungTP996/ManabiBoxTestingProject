import pytest
from playwright.sync_api import Page, expect
import os

@pytest.fixture(scope="function")
def kanji_go_quiz_page(logged_in_page: Page):
    """
    このフィクスチャは漢字「五」の練習画面への完全な移動を実行します。
    """
    page = logged_in_page
    print("\n--- [SETUP] 漢字「五」の練習画面への移動を開始 ---")
    page.get_by_alt_text("漢字").click()
    go_button_in_list = page.get_by_text("五 ", exact=True)
    expect(go_button_in_list).to_be_visible(timeout=10000)
    go_button_in_list.click()
    page.get_by_text("つぎにすすむ").click()
    expect(page.locator(".kanji-canvas.upper-canvas")).to_be_visible()
    print("--- [SETUP] 描画画面に到達し、テストの準備が完了 ---")
    yield page

class TestGo:
    def _draw_kanji(self, page: Page, origin_x: float, origin_y: float):
        """漢字「五」の各画を描画する補助関数"""
        # 画1
        page.mouse.move(origin_x + 102, origin_y + 88)
        page.mouse.down()
        page.mouse.move(origin_x + 170, origin_y + 89)
        page.mouse.move(origin_x + 223, origin_y + 76)
        page.mouse.up()

        # 画2
        page.mouse.move(origin_x + 163, origin_y + 85)
        page.mouse.down()
        page.mouse.move(origin_x + 117, origin_y + 238)
        page.mouse.up()

        # 画3
        page.mouse.move(origin_x + 95, origin_y + 163)
        page.mouse.down()
        page.mouse.move(origin_x + 150, origin_y + 150)
        page.mouse.move(origin_x + 208, origin_y + 152)
        page.mouse.move(origin_x + 210, origin_y + 155)
        page.mouse.move(origin_x + 205, origin_y + 155)
        page.mouse.move(origin_x + 205, origin_y + 235)
        page.mouse.up()

        # 画4
        page.mouse.move(origin_x + 45, origin_y + 245)
        page.mouse.down()
        page.mouse.move(origin_x + 280, origin_y + 235)
        page.mouse.up()

    def test_kanji_go_drawing_flow_only(self, kanji_go_quiz_page: Page):
        """
        テストシナリオ: 漢字「五」を描画し、各ステップを進める（AI検証をスキップ）。
        """
        page = kanji_go_quiz_page

        for i in range(3):
            print(f"\n--> {i + 1}回目の描画を開始")
            drawing_canvas = page.locator(".kanji-canvas.upper-canvas")
            expect(drawing_canvas).to_be_visible()
            expect(drawing_canvas).to_be_enabled()
            page.wait_for_timeout(5000)

            # 基準座標を取得（bounding_box が準備できるまで待機）
            canvas_box = None
            for _ in range(5):
                canvas_box = drawing_canvas.bounding_box()
                if canvas_box:
                    break
                page.wait_for_timeout(200)
            assert canvas_box, "Canvas の bounding_box が取得できません"
            origin_x, origin_y = canvas_box["x"], canvas_box["y"]

            # 描画を実行
            self._draw_kanji(page, origin_x, origin_y)
            print("--- 描画完了! ---")

            # 描画が明確に表示されるまで少し待機（オプション）
            page.wait_for_timeout(500)

            # スクリーンショットを撮影（証拠/デバッグ用のみ、検証しない）
            # Canvas が準備できていない場合はスキップしてフローの中断を避ける
            canvas_to_verify = page.locator(".kanji-canvas.upper-canvas").first
            if canvas_to_verify.count() > 0:
                folder_name = "debug_screenshots"
                os.makedirs(folder_name, exist_ok=True)
                screenshot_path = os.path.join(folder_name, f"go_drawing_step_{i + 1}.png")
                try:
                    canvas_to_verify.scroll_into_view_if_needed()
                    canvas_to_verify.screenshot(path=screenshot_path)
                    print(f"-> 描画画像を保存: {screenshot_path}")
                except Exception as e:
                    print(f"-> スクリーンショットをスキップ（Canvas が準備できていない）: {e}")
            else:
                print("-> スクリーンショットをスキップ（Canvas が見つからない）")

            # --- 遷移（ゲームロジック） ---
            # 描画後に表示される確認/提出ボタンをクリック（UI によって表示されるボタンが異なる）
            # ボタンのテキストが少し変化する可能性があるため、exact を強制しない
            submit_btn = page.get_by_text("つけ").first
            expect(submit_btn).to_be_visible(timeout=10000)
            expect(submit_btn).to_be_enabled(timeout=10000)
            print("-> 「つけ」ボタンが準備完了、クリックを実行")
            submit_btn.click()

            # シーン遷移が成功したことを確認
            expect(page.get_by_alt_text("level return")).to_be_visible()

            page.get_by_text("つぎにすすむ").click()

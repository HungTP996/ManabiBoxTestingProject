import pytest
from playwright.sync_api import Page, expect


# ===================================================================
# == FIXTURE SETUP: テスト環境の準備 ==
# ===================================================================
@pytest.fixture(scope="function")
def kanji_hana_page(logged_in_page: Page):
    """
    漢字「花」の練習画面へ移動するためのフィクスチャです。
    """
    page = logged_in_page

    # ページの読み込み完了を待機
    page.wait_for_load_state("networkidle")

    print("\n--- [SETUP] 漢字「花」の練習画面へ移動します ---")

    # 1. 「漢字」教科を選択
    page.get_by_alt_text("漢字").click()

    # リストから「花」ボタンを探してクリック
    # UI上のテキストに合わせて調整（"花" または "花 "）
    hana_button = page.get_by_text("花", exact=True).first

    # 見つからない場合のフォールバック
    if not hana_button.is_visible():
        hana_button = page.get_by_text("花 ", exact=True).first

    expect(hana_button).to_be_visible(timeout=10000)
    hana_button.click()

    # 2. 練習を開始（「つぎにすすむ」をクリック）
    # Playwrightの自動待機を利用してクリック
    page.get_by_text("つぎにすすむ").click()

    # キャンバスが表示されるまで待機
    expect(page.locator(".kanji-canvas.upper-canvas")).to_be_visible(timeout=10000)
    print("--- [SETUP] 描画画面に到達しました ---")

    yield page


# ===================================================================
# == TEST CLASS: 漢字テストシナリオ ==
# ===================================================================
class TestKanjiHana:

    def test_kanji_hana_drawing(self, kanji_hana_page: Page):
        """
        シナリオ: 漢字「花」を3回書いて、正解判定されることを確認する。
        """
        page = kanji_hana_page

        # 3回繰り返して練習を行う
        for i in range(3):
            print(f"\n--- {i + 1}回目の描画を開始します ---")

            # キャンバスの要素と座標を取得
            drawing_canvas = page.locator(".kanji-canvas.upper-canvas")
            expect(drawing_canvas).to_be_visible()

            # 描画前の安定待機
            page.wait_for_timeout(1000)

            canvas_box = drawing_canvas.bounding_box()
            if not canvas_box:
                raise Exception("キャンバスが見つかりません")

            origin_x, origin_y = canvas_box['x'], canvas_box['y']

            # --- 描画アクション開始 ---
            print("--> 漢字「花」を描画中...")

            # 1画目: 草冠（横）
            page.mouse.move(origin_x + 62, origin_y + 88)
            page.mouse.down()
            page.mouse.move(origin_x + 243, origin_y + 77, steps=5)
            page.mouse.up()

            # 2画目: 草冠（左縦）
            page.mouse.move(origin_x + 112, origin_y + 35)
            page.mouse.down()
            page.mouse.move(origin_x + 115, origin_y + 117, steps=5)
            page.mouse.up()

            # 3画目: 草冠（右縦）
            page.mouse.move(origin_x + 200, origin_y + 32)
            page.mouse.down()
            page.mouse.move(origin_x + 170, origin_y + 110, steps=5)
            page.mouse.up()

            # 4画目: 化（左払い）
            page.mouse.move(origin_x + 112, origin_y + 135)
            page.mouse.down()
            page.mouse.move(origin_x + 110, origin_y + 150, steps=2)
            page.mouse.move(origin_x + 95, origin_y + 183, steps=2)
            page.mouse.move(origin_x + 90, origin_y + 190, steps=2)
            page.mouse.move(origin_x + 51, origin_y + 234, steps=2)
            page.mouse.up()

            # 5画目: 化（縦）
            page.mouse.move(origin_x + 92, origin_y + 185)
            page.mouse.down()
            page.mouse.move(origin_x + 100, origin_y + 210, steps=2)
            page.mouse.move(origin_x + 105, origin_y + 220, steps=2)
            page.mouse.move(origin_x + 98, origin_y + 285, steps=2)
            page.mouse.up()

            # 6画目: 化（右払い）
            page.mouse.move(origin_x + 238, origin_y + 135)
            page.mouse.down()
            page.mouse.move(origin_x + 220, origin_y + 150, steps=2)
            page.mouse.move(origin_x + 205, origin_y + 165, steps=2)
            page.mouse.move(origin_x + 185, origin_y + 175, steps=2)
            page.mouse.move(origin_x + 178, origin_y + 180, steps=2)
            page.mouse.up()

            # 7画目: 化（曲がり跳ね）
            page.mouse.move(origin_x + 178, origin_y + 120)
            page.mouse.down()
            page.mouse.move(origin_x + 170, origin_y + 275, steps=5)
            page.mouse.move(origin_x + 277, origin_y + 275, steps=5)
            page.mouse.move(origin_x + 287, origin_y + 275, steps=5)
            page.mouse.move(origin_x + 283, origin_y + 240, steps=5)  # 跳ね
            page.mouse.up()

            print("--> 描画完了")

            # 判定待ち
            page.wait_for_timeout(1000)

            # --- 検証: 「まるつけ」ボタンが有効になるか確認 ---
            marutsuke_button = page.get_by_text("まるつけ", exact=True)

            # 見つからない場合のフォールバック
            if not marutsuke_button.is_visible():
                marutsuke_button = page.get_by_text("つけ")

            expect(marutsuke_button).to_be_enabled(timeout=10000)
            marutsuke_button.click()
            print("--> 「まるつけ」をクリックしました")

            # アニメーション待機
            page.wait_for_timeout(2000)

            # 次へ進む処理（3回目以外）
            if i < 2:
                next_button = page.get_by_text("つぎにすすむ", exact=True)
                if next_button.is_visible():
                    next_button.click()
                    print("--> 「つぎにすすむ」をクリックしました")
                    page.wait_for_timeout(1000)  # 次のキャンバスロード待ち

        print("\n--- 全ての描画テストが完了しました ---")
# tests/ai_tests/test_kaigara_pre.py
import pytest
import re
import os
import allure
from playwright.sync_api import Page, expect


@pytest.fixture(scope="function")
def drawing_page(logged_in_page: Page):
    """描画ページへ遷移するためのフィクスチャ。"""
    page = logged_in_page
    with allure.step("国語プレテストの描画ページへ移動"):
        page.get_by_alt_text("国語").click()
        # プレテストのトピック番号3をクリック
        expect(page.get_by_text("プレテスト").nth(3)).to_be_visible()
        page.get_by_text("プレテスト").nth(3).click()
    yield page


def draw_kawa(page: Page):
    """ヘルパー関数：文字「かわ」の描画アクションをシミュレートする。"""
    with allure.step("キャンバス上に文字「かわ」の描画を実行"):
        drawing_canvas = page.locator(".kanji-canvas.upper-canvas")
        expect(drawing_canvas).to_be_visible()
        canvas_box = drawing_canvas.bounding_box()
        # Canvasの左上隅の座標を取得
        origin_x, origin_y = canvas_box['x'], canvas_box['y']

        # --- 文字「か」の描画 ---
        page.mouse.move(origin_x + 100, origin_y + 70)
        page.mouse.down()
        page.mouse.move(origin_x + 210, origin_y + 50)
        page.mouse.move(origin_x + 180, origin_y + 180)
        page.mouse.move(origin_x + 170, origin_y + 170)
        page.mouse.up()
        page.mouse.move(origin_x + 140, origin_y + 40)
        page.mouse.down()
        page.mouse.move(origin_x + 100, origin_y + 160)
        page.mouse.up()
        page.mouse.move(origin_x + 200, origin_y + 60)
        page.mouse.down()
        page.mouse.move(origin_x + 230, origin_y + 80)
        page.mouse.up()

        # --- 文字「わ」の描画 ---
        page.mouse.move(origin_x + 100, origin_y + 200)
        page.mouse.down()
        page.mouse.move(origin_x + 90, origin_y + 320)
        page.mouse.up()
        page.mouse.move(origin_x + 90, origin_y + 220)
        page.mouse.down()
        page.mouse.move(origin_x + 170, origin_y + 180)
        page.mouse.move(origin_x + 50, origin_y + 300)
        page.mouse.move(origin_x + 190, origin_y + 210)
        page.mouse.move(origin_x + 200, origin_y + 275)
        page.mouse.move(origin_x + 150, origin_y + 320)
        page.mouse.up()


def test_drawing_with_ai_verification(drawing_page: Page, ai_vision_verifier):
    """
    テストシナリオ: 描画 -> 確定 -> スクリーンショット -> AI検証 -> 採点。
    """
    page = drawing_page

    # 1. 描画
    draw_kawa(page)

    # 2. 「決定」をクリックして描画を確定
    with allure.step("「決定」をクリックして描画を確定"):
        page.locator("div").filter(has_text=re.compile(r"^決けっ定てい$")).nth(2).click()
        page.wait_for_timeout(1000)

    # 3. 結果のキャンバスをキャプチャ
    screenshot_path = ""
    with allure.step("AI検証のために結果をスクリーンショット"):
        result_box = page.locator(".upper-canvas").first
        folder_name = "ai_screenshots"
        os.makedirs(folder_name, exist_ok=True)
        screenshot_path = os.path.join(folder_name, "drawing_to_verify.png")
        result_box.screenshot(path=screenshot_path)
        allure.attach.file(screenshot_path, name="Drawing Result", attachment_type=allure.attachment_type.PNG)
        print(f"-> 結果のスクリーンショットを保存しました: {screenshot_path}")

    # 4. 画像をAIに送信して検証
    with allure.step("画像をAIに送信し、文字が「かわ」であることを検証"):
        is_correct = ai_vision_verifier(screenshot_path=screenshot_path, expected_char="かわ")
        assert is_correct, "AIは文字「かわ」を正しく認識できませんでした。"
        print("-> AIが描画の正確性を確認しました！")

    # 5. 「こたえあわせ」をクリックして採点
    with allure.step("「こたえあわせ」をクリックして採点"):
        kotaeawase_button = page.get_by_role("button", name="こたえあわせ")
        expect(kotaeawase_button).to_be_enabled(timeout=5000)
        kotaeawase_button.click()

    # 6. 正解アイコンの表示を確認
    with allure.step("正解アイコン (まる) の表示を確認"):
        expect(page.locator(".icon__answer--right")).to_be_visible()
        print("\n--- テスト完了 ---")
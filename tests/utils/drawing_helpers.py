# (ファイル: tests/utils/drawing_helpers.py)

from playwright.sync_api import Page, expect
import allure
import time


def draw_character(page: Page, question_data: dict):
    """
    指定されたデータに基づいてCanvas上に文字を描画する。
    """
    # 描画キャンバスのロケーターを取得
    drawing_canvas = page.locator(".kanji-canvas.upper-canvas")

    with allure.step("キャンバスが表示され、安定するのを待機 (バウンディングボックスの確認)"):
        start_time = time.time()
        timeout_seconds = 15
        canvas_box = None

        while True:
            if drawing_canvas.is_visible():
                # バウンディングボックスを取得
                canvas_box = drawing_canvas.bounding_box()

            if canvas_box:
                allure.attach("Canvasがレンダリングされました", f"Box: {canvas_box}")
                break

            if time.time() - start_time > timeout_seconds:
                page.screenshot(path="screenshots/DEBUG_draw_character_fail.png")
                raise Exception(f"Canvasは{timeout_seconds}秒後にレンダリングされませんでした")

            page.wait_for_timeout(100)

    with allure.step("キャンバスのJavaScript初期化のため1200ms待機 (JS init)"):
        page.wait_for_timeout(1200)

    with allure.step("ストロークの実行を開始 (各ストローク後に300ms待機)"):
        if not canvas_box:
            raise Exception("論理エラー: ポーリング後もキャンバスが見つかりません。")

        # Canvasの左上隅の座標
        origin_x, origin_y = canvas_box['x'], canvas_box['y']

        strokes = question_data.get("strokes", [])
        if not strokes:
            print("警告: 描画する「strokes」データがありません。")
            return

        # 最初のストロークを実行
        if strokes and strokes[0].get("action") == "move":
            # 最初の座標に移動
            page.mouse.move(origin_x + strokes[0]["x"], origin_y + strokes[0]["y"])

        # 残りのストロークを描画
        for point in strokes[1:]:
            action = point.get("action")

            if action == "down":
                page.mouse.down()

            elif action == "up":
                page.mouse.up()
                page.wait_for_timeout(300)

            elif action == "move":
                x = point.get("x")
                y = point.get("y")
                # スムーズな移動のために steps=3 を使用
                page.mouse.move(origin_x + x, origin_y + y, steps=3)

from playwright.sync_api import Page, expect
import allure

def is_canvas_drawn(page: Page, canvas_selector: str) -> bool:
    """
    Canvasに描画内容があるかを確認する関数。
    データがある場合はTrue、空白（真っ白）の場合はFalseを返す。
    """
    return page.evaluate("""(selector) => {
        // 1. 実際のCanvas要素を取得
        const realCanvas = document.querySelector(selector);
        if (!realCanvas) return false;

        // 2. 同じサイズの空のCanvas（比較用）を作成
        const emptyCanvas = document.createElement('canvas');
        emptyCanvas.width = realCanvas.width;
        emptyCanvas.height = realCanvas.height;

        // 3. Base64文字列の長さを比較
        return realCanvas.toDataURL().length > emptyCanvas.toDataURL().length;
    }""", canvas_selector)

def draw_character(page: Page, question_data: dict):
    """
    指定されたデータに基づいてCanvas上に文字を描画する。
    """
    # 描画キャンバスのロケーター（セレクター）
    # 注: コードの動作のため、ここはセレクター文字列またはロケーターオブジェクトの扱いに注意してください
    drawing_canvas_selector = ".kanji-canvas.upper-canvas"
    canvas_box = None

    with allure.step("キャンバスが表示され、安定するのを待機 (バウンディングボックスの確認)"):
        try:
            canvas_locator = page.locator(drawing_canvas_selector)
            canvas_locator.wait_for(state="visible", timeout=15000)
            for _ in range(10): # Thử 5 lần, mỗi lần cách nhau 200ms
                canvas_box = canvas_locator.bounding_box()
                if canvas_box:
                    break
                page.wait_for_timeout(200)

            if not canvas_box:
                raise Exception("エラー: Canvasは表示されていますが、座標（Bounding Box）が取得できません (値がnullです)。")
            
            if is_canvas_drawn(page, drawing_canvas_selector):
                raise Exception("環境エラー: Canvasがクリーンではありません（既に描画内容が存在します）。")
            
            print("事前チェックOK: Canvasは空白で、描画の準備ができています。")
                
            allure.attach(str(canvas_box), name="Canvasのバウンディングボックス座標")
            
        except Exception as e:
            page.screenshot(path="screenshots/DEBUG_draw_character_fail.png")
            raise Exception(f"Canvasの検索中にエラーが発生しました: {str(e)}")

    with allure.step("キャンバスのJavaScript初期化のため1200ms待機 (JS init)"):
        page.wait_for_timeout(2000)

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
        # 注: データ構造によってはループ内で処理を統一することも可能です
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
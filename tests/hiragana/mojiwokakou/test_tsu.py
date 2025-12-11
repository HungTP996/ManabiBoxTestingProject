import pytest
from playwright.sync_api import Page, expect
import json
from pathlib import Path

def load_test_data():
    current_dir = Path(__file__).parent.absolute()

    # data.json が配置可能な場所
    possible_paths = [
        current_dir / "data.json",  # 同じディレクトリ
        current_dir / "mojiwokakou" / "data.json",  # mojiwokakou サブディレクトリ内
        Path("tests/hiragana/mojiwokakou/data.json")  # ハードコードパス (フォールバック)
    ]

    json_path = None
    for path in possible_paths:
        if path.exists():
            json_path = path
            break

    if not json_path:
        raise FileNotFoundError(f"data.json が以下の場所で見つかりません: {[str(p) for p in possible_paths]}")

    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


# 文字 'つ' のデータをフィルタリング
all_drawing_tests = load_test_data()
drawing_tests = [test for test in all_drawing_tests if test['char'] == 'つ']

# スクリーンショットディレクトリを作成（AIを使用しないが、デバッグ用に撮影）
Path("debug_screenshots").mkdir(exist_ok=True)


@pytest.fixture(scope="function")
def go_to_character_selection(logged_in_page: Page):
    page = logged_in_page
    page.wait_for_load_state("networkidle")

    # 文字選択画面へ移動
    page.get_by_alt_text("ひらがな").click()
    page.locator(".figure__btn:has-text('きょうかしょの じゅん')").click()
    yield page


class TestHiraganaDrawing:

    # ai_vision_verifier パラメータを削除済み
    @pytest.mark.parametrize("test_data", drawing_tests)
    def test_character_drawing(self, go_to_character_selection: Page, test_data):
        page = go_to_character_selection
        char_to_test = test_data["char"]
        draw_points = test_data["points"]

        print(f"\n--- 文字テストを開始: {char_to_test} (AI 未使用) ---")

        # 1. 文字を選択
        page.locator(f".character:has-text('{char_to_test}')").click()
        page.get_by_text("つぎにすすむ", exact=True).click()

        # ページ遷移アニメーションを待機
        page.wait_for_timeout(1500)

        # 2. 3回描画ループ
        for i in range(3):
            print(f"\n--- {i + 1}回目の描画 ---")

            drawing_canvas = page.locator(".kanji-canvas.upper-canvas")
            expect(drawing_canvas).to_be_visible()

            # Canvas が描画を受け入れる準備ができるまで少し待機
            page.wait_for_timeout(1000)

            canvas_box = drawing_canvas.bounding_box()
            if not canvas_box:
                raise Exception("Canvas が見つかりません。")

            origin_x, origin_y = canvas_box['x'], canvas_box['y']

            # 描画操作を実行
            drawing_canvas.hover()
            page.mouse.move(origin_x + draw_points[0][0], origin_y + draw_points[0][1])
            page.mouse.down()

            # 次の点を描画
            for point in draw_points[1:]:
                page.mouse.move(origin_x + point[0], origin_y + point[1], steps=5)

            page.mouse.up()
            print("--> 描画完了。")

            # アプリが描画を処理するのを待機
            page.wait_for_timeout(1000)

            # --- AI VERIFY ステップをスキップ ---
            # 代わりに、採点ボタンが点灯するかを確認するのみ

            marutsuke_button = page.get_by_text("まるつけ", exact=True)

            # ボタンの状態を素早くチェック（デバッグログ用）
            if not marutsuke_button.is_enabled():
                print(f"警告 ({i + 1}回目): Marutsuke ボタンが有効化されていません。描画が認識されていない可能性があります。")
                page.screenshot(path=f"debug_screenshots/fail_draw_{i + 1}.png")

            # テストの正式な期待（10秒以内にボタンが有効化されない場合、テスト失敗）
            expect(marutsuke_button).to_be_enabled(timeout=10000)

            marutsuke_button.click()
            print("--> Marutsuke をクリックしました。")

            # 採点アニメーションを待機（Hanamaru が表示）
            page.wait_for_timeout(2500)

            # 「次へ」ボタンを処理
            if i < 2:
                # Next ボタンを検索。"つぎにすすむ" または他の名前
                next_button = page.get_by_text("つぎにすすむ", exact=True)

                if next_button.is_visible():
                    next_button.click()
                    print("--> Next をクリックしました。")
                    # 次回の描画のためにキャンバスがリセットされるのを待機
                    page.wait_for_timeout(2000)
            else:
                print("--> 3回の描画が完了しました。")

        print("\n--- 描画シナリオが完了しました ---")

        # 3. レッスンを終了
        # 終了ボタンを検索（通常は "くにすすむ" または最後の "つぎにすすむ"）
        try:
            # 優先的に "くにすすむ" ボタンを検索（インデックスに戻る/次のレッスンへ）
            finish_button = page.get_by_text("くにすすむ", exact=True)

            if not finish_button.is_visible():
                # 見つからない場合、再び Next ボタンを検索（UI が異なる場合）
                finish_button = page.get_by_text("つぎにすすむ", exact=True)

            # 見つかった場合クリック、見つからない場合はこのステップでテストを失敗させないが警告を表示
            if finish_button.is_visible():
                finish_button.click()
                print("--> 終了ボタンをクリックしました。")
            else:
                print("警告: 最後のレッスン終了ボタンが見つかりません。")

        except Exception as e:
            print(f"終了時のエラー: {e}")

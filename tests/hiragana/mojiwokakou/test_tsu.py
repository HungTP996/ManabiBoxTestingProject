import pytest
from playwright.sync_api import Page, expect
import json
from pathlib import Path

# --- JSONファイルからテストデータを読み込み ---
def load_test_data(file_path='tests/hiragana/mojiwokakou/data.json'):
    """JSONファイルからテストデータを読み込むための関数です。"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

all_drawing_tests = load_test_data()
drawing_tests = [test for test in all_drawing_tests if test['char'] == 'つ']

# screenshotsディレクトリが存在することを確認
Path("ai_screenshots").mkdir(exist_ok=True)

@pytest.fixture(scope="function")
def go_to_character_selection(logged_in_page: Page):
    """Fixture: ひらがなの文字選択画面に移動します。"""
    page = logged_in_page
    page.get_by_alt_text("ひらがな").click()
    page.locator(".figure__btn:has-text('きょうかしょの じゅん')").click()
    yield page


class TestHiraganaDrawing:

    @pytest.mark.parametrize("test_data", drawing_tests)
    def test_character_drawing(self, go_to_character_selection: Page, test_data, ai_vision_verifier):
        """テスト：文字を描画し、AIで検証後、採点します。"""
        page = go_to_character_selection

        char_to_test = test_data["char"]
        draw_points = test_data["points"]

        print(f"\n--- 文字「{char_to_test}」の描画シナリオを開始 ---")

        # 1. 文字を選択し、描画画面に移動
        page.locator(f".character:has-text('{char_to_test}')").click()
        page.get_by_text("つぎにすすむ", exact=True).click()

        # 2. 描画アクションを2回繰り返す
        for i in range(3):
            print(f"\n--- 文字「{char_to_test}」の {i + 1}/3 回目の描画を開始 ---")

            drawing_canvas = page.locator(".kanji-canvas.upper-canvas")
            expect(drawing_canvas).to_be_visible()

            canvas_box = drawing_canvas.bounding_box()
            if not canvas_box:
                raise Exception("キャンバスのサイズが見つかりませんでした。")

            origin_x, origin_y = canvas_box['x'], canvas_box['y']

            # 座標に従って文字を描画
            drawing_canvas.hover()
            page.wait_for_timeout(200)

            start_point = draw_points[0]
            page.mouse.move(origin_x + start_point[0], origin_y + start_point[1])
            page.mouse.down()
            page.wait_for_timeout(100)

            for x, y in draw_points[1:]:
                page.mouse.move(origin_x + x, origin_y + y)
                page.wait_for_timeout(50)

            page.mouse.up()
            print("--> 描画完了。")
            page.wait_for_timeout(500)

            # 3. AIによる検証ステップ
            print("--> AIによる検証を開始...")
            screenshot_path = f"screenshots/verify_{char_to_test}_attempt_{i + 1}.png"
            drawing_canvas.screenshot(path=screenshot_path)

            is_correct = ai_vision_verifier(screenshot_path, char_to_test)

            # AIが不正解と判断した場合、テストを停止
            assert is_correct, f"AIが文字「{char_to_test}」を不正解と判断しました（{i + 1}回目）。"
            print("--> AIの検証結果：正解。")

            # 4. 「まるつけ」をクリックして採点
            marutsuke_button = page.get_by_text("まるつけ", exact=True)
            expect(marutsuke_button).to_be_enabled(timeout=10000)
            marutsuke_button.click()
            print("--> 「まるつけ」をクリックしました。")

            # 5. 次の描画へ進むために「つぎにすすむ」をクリック（もしあれば）
            if i < 2:
                next_button = page.get_by_text("つぎにすすむ", exact=True)
                expect(next_button).to_be_enabled()
                next_button.click()
                print("--> 「つぎにすすむ」をクリックしました。")

        print("\n--- 描画シナリオを完了 ---")

        # 6. 「くにすすむ」をクリックして終了
        next_lesson_button = page.get_by_text("くにすすむ", exact=True)
        expect(next_lesson_button).to_be_enabled()
        next_lesson_button.click()
        print("--> 「くにすすむ」をクリックしました。")

        print(f"\n--- 文字「{char_to_test}」の全シナリオを完了 ---")
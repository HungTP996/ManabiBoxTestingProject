# tests/kokugo/drawing/test_drawing_and_record.py

import pytest
import allure
from playwright.sync_api import Page, expect


@pytest.fixture(scope="function")
def drawing_page(logged_in_page: Page):
    """描画ページへ遷移するためのフィクスチャ。"""
    page = logged_in_page
    with allure.step("国語プレテストの描画ページへ移動"):
        page.get_by_alt_text("国語").click()
        page.get_by_text("プレテスト").nth(8).click()
    yield page


def test_record_drawing_coordinates(drawing_page: Page):
    """
    描画ページを開き、ユーザーが手動で描画した座標を記録し、出力するテスト。
    """
    page = drawing_page
    # ユーザー操作のために一時停止
    page.pause()

    with allure.step("座標を記録するためのJavaScriptを注入"):
        # canvas上でのマウスイベントをリッスンし、座標を記録するJavaScriptを注入
        page.evaluate("""
            () => {
    // ロケーターでキャンバスを検索
    const canvas = document.querySelector('.upper-canvas');
    if (!canvas) {
        console.error('キャンバスが見つかりません！');
        return;
    }
    // 描画パスを保存するためのグローバル変数
    window.drawingPath = [];

    // イベントとアクションを記録する関数
    const recordEvent = (e, action) => {
        const rect = canvas.getBoundingClientRect();
        // Canvas左上からの相対座標を計算
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        window.drawingPath.push({ action, x: Math.round(x), y: Math.round(y) });
    };

    // マウスイベントにリスナーを設定
    canvas.addEventListener('mousedown', (e) => recordEvent(e, 'down'));
    canvas.addEventListener('mousemove', (e) => {
        if (e.buttons === 1) {
            recordEvent(e, 'move');
        }
    });
    canvas.addEventListener('mouseup', (e) => recordEvent(e, 'up'));
}
        """)

    # with allure.step("ユーザーによる描画と確認を待機"):
    #     print("\n--- 描画アクションの記録準備ができました ---")
    #     print("1. ブラウザのキャンバス上にマウスで描画してください。")
    #     print("2. 描画が完了したら、このターミナルに戻り Enter を押してください。")
    #     print("3. 記録された座標が出力されます。")
    #     # ユーザーがEnterを押すのを待機
    #     input()

    with allure.step("座標データを取得して出力"):
        # 記録された座標データを取得
        drawing_path = page.evaluate("() => window.drawingPath")

        print("\n--- 記録された座標データ ---")
        # JSON形式で出力するために引用符を置換
        print(str(drawing_path).replace("'", '"'))
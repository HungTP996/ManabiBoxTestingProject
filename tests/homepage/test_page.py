import pytest
from playwright.sync_api import Page, expect


# --- Hàm Assert Helper ---
def assert_answer(page: Page, text: str, timeout: int = 10000):
    """
    Chờ câu trả lời xuất hiện theo 3 lớp.
    """
    try:
        expect(page.get_by_text(text).first).to_be_visible(timeout=timeout // 2)
        return
    except AssertionError:
        pass
    try:
        expect(page.locator(f"text=/{text}/").first).to_be_visible(timeout=timeout // 2)
        return
    except AssertionError:
        pass
    page.wait_for_function(
        "t => document.body && document.body.innerText && document.body.innerText.includes(t)",
        arg=text,
        timeout=timeout
    )

NAVIGATION_TEST_CASES = [
    {
        "description": "国語ページの遷移と「もどる」ボタンのテスト",
        "click_alt": "国語",
        "expected_value": "国語",
        "back_method": "text",
        "back_selector": "もどる"
    },
    {
        "description": "算数ページの遷移と「もどる」ボタンのテスト",
        "click_alt": "算数",
        "expected_value": "算数",
        "back_method": "text",
        "back_selector": "もどる"
    },
    {
        "description": "CBTページの遷移と「もどる」ボタンのテスト",
        "click_alt": "CBT",
        "expected_value": "テストをする　きょうかを　えらんでね",
        "back_method": "text",
        "back_selector": "もどる"
    },
    {
        "description": "漢字ページの遷移とブラウザの戻る機能のテスト",
        "click_alt": "漢字",
        "expected_value": "かんじをえらんでおそう。",
        "back_method": "browser",
        "back_selector": None
    },
    {
        "description": "計算ページの遷移と「もどる」ボタンのテスト",
        "click_alt": "計算",
        "expected_value": "計算",
        "back_method": "text",
        "back_selector": "もどる"
    },
    {
        "description": "ひらがなページの遷移とホームアイコンのテスト",
        "click_alt": "ひらがな",
        "expected_value": "ひらがなをおぼえる",
        "back_method": "alt",
        "back_selector": "icon home"
    },
    {
        "description": "カタカナページの遷移とホームアイコンのテスト",
        "click_alt": "カタカナ",
        "expected_value": "カタカナをおぼえる",
        "back_method": "alt",
        "back_selector": "icon home"
    }
]

@pytest.mark.parametrize("test_case", NAVIGATION_TEST_CASES)
def test_main_menu_navigation(logged_in_page: Page, test_case: dict):
    """
    各テストデータは独立したテストケースとして実行されます。
    フィクスチャ「logged_in_page」により、各ケースで新規にログインが行われます。
    """
    page = logged_in_page
    print(f"テスト開始: {test_case['description']}")

    # --- ステップ1: メインメニューの項目をクリック ---
    if test_case["click_alt"] == "CBT":
        element_to_click = page.locator('img[src*="btn_top_CBT_n"]')
    else:
        element_to_click = page.get_by_alt_text(test_case["click_alt"])

    expect(element_to_click).to_be_visible()
    element_to_click.click()

    # --- ステップ2: 正しい遷移先ページにいることを確認 ---
    assert_answer(page, test_case["expected_value"])
    print(">>> 遷移先のページを正しく表示しました。")

    # --- ステップ3: 戻る操作を実行 ---
    back_method = test_case["back_method"]
    back_selector = test_case["back_selector"]

    if back_method == "text":
        back_button = page.get_by_text(back_selector).first
        expect(back_button).to_be_visible()
        back_button.click()
        print(f">>> 「{back_selector}」テキストをクリックして戻ります。")
    elif back_method == "alt":
        back_button = page.get_by_alt_text(back_selector)
        expect(back_button).to_be_visible()
        back_button.click()
        print(f">>> alt='{back_selector}' のアイコンをクリックして戻ります。")
    elif back_method == "browser":
        page.go_back()
        print(">>> ブラウザの戻る機能で戻ります。")

    # --- ステップ4: メインメニューに正しく戻ったことを確認 ---
    expect(page.get_by_alt_text("まなびボックス")).to_be_visible(timeout=10000)
    print(">>> メインメニューに正しく戻りました。\n")
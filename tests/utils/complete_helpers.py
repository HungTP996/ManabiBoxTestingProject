import re
import allure
from playwright.sync_api import Page, expect


def confirm_score_and_proceed(page: Page) -> bool:
    kettei_button = page.locator("div").filter(has_text=re.compile(r"^決けっ定てい$")).nth(2)
    kotaeawase_button = page.get_by_role("button", name="こたえあわせ")

    with allure.step("作図を確定するため「決定」をクリック"):
        expect(kettei_button).to_be_enabled(timeout=10000)
        kettei_button.click()

    with allure.step("作図処理のために1秒待機 (ハードウェイト)"):
        page.wait_for_timeout(1000)

    with allure.step("採点のため「こたえあわせ」をクリック"):
        expect(kotaeawase_button).to_be_enabled(timeout=5000)
        kotaeawase_button.click()

    is_correct = False
    with allure.step("結果アイコンの表示を確認 (正解・不正解)"):
        try:
            expect(page.locator(".icon__answer--right")).to_be_visible(timeout=3000)
            allure.attach("結果", "正解 (マル)", allure.attachment_type.TEXT)
            is_correct = True
        except Exception:
            try:
                expect(page.locator(".icon__answer--wrong")).to_be_visible(timeout=1000)
                allure.attach("結果", "不正解 (バツ)", allure.attachment_type.TEXT)
            except Exception:
                allure.attach("結果", "不明 (正解・不正解アイコンが見つかりません)", allure.attachment_type.TEXT)

    with allure.step("次のステップへ進むため「つぎへ」をクリック"):
        tsugi_button = page.get_by_role("button", name="つぎへ")
        expect(tsugi_button).to_be_visible(timeout=10000)
        tsugi_button.click()

    with allure.step("次の質問の読み込み完了を待機"):
        try:
            page.wait_for_load_state("networkidle", timeout=10000)
        except Exception as e:
            print(f"「networkidle」を待機できませんでした。SPAの可能性があります: {e}")
            page.wait_for_timeout(500)

    return is_correct


def complete_question(page: Page):
    review_button = page.locator("button:has-text('ふりかえり')")
    expect(review_button).to_be_visible(timeout=10000)
    review_button.click()
    print("-> 「ふりかえり」をクリックしました")

    review_title = page.locator("p:has-text('ふりかえり')")
    expect(review_title).to_be_visible()
    print("-> レビューページに遷移しました")

    finish_button = page.get_by_text("おわる", exact=True)
    expect(finish_button).to_be_visible()
    finish_button.click()
    print("-> 「おわる」をクリックしました")
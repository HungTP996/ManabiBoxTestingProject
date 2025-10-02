from playwright.sync_api import Page, expect

def complete_question(page: Page):
    """
        Hàm này xử lý các bước cuối cùng sau khi trả lời câu hỏi cuối cùng:
        vào trang review và thoát ra trang chủ đề.
        """
    print("--> Hoàn thành câu cuối, bắt đầu luồng kết thúc...")

    # 1. Click nút "ふりかえり" (Review)
    review_button = page.locator("button:has-text('ふりかえり')")
    review_button.wait_for(state="visible", timeout=10000)
    review_button.click()
    print("-> Đã click 'ふりかえり'")

    # 2. Xác nhận đã vào trang review
    review_title = page.locator("p:has-text('ふりかえり')")
    expect(review_title).to_be_visible()
    print("-> Đã vào trang Review")

    # 3. Click nút "おわる" (Finish) để thoát
    finish_button = page.get_by_text("おわる", exact=True)
    expect(finish_button).to_be_visible()
    finish_button.click()
    print("-> Đã click 'おわる'")
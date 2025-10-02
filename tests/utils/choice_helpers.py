from playwright.sync_api import Page, expect
"""
File này chứa các hàm trợ giúp có thể tái sử dụng để xử lý
các loại câu hỏi khác nhau trong bài quiz.
"""
def answer_question(page: Page, question: dict, answer_key: str):
    """
    Hàm tổng hợp, tự động gọi đến hàm xử lý tương ứng
    dựa trên "type" của câu hỏi trong file dữ liệu.

    :param page: Đối tượng Page của Playwright.
    :param question: Dictionary chứa dữ liệu của câu hỏi hiện tại.
    :param answer_key: Chuỗi cho biết nên dùng dữ liệu nào ('correct_answers' hoặc 'incorrect_answers').
    """
    question_type = question.get("type", "text")  # Mặc định là 'text'
    print(f"--> Đang thực hiện câu hỏi {question['id']} (Loại: {question_type})")

    if question_type in ["text", "image", "css", "xpath"]:
        _answer_simple_choice(page, question, answer_key)

    elif question_type == "fill_blank":
        _answer_fill_blank(page, question, answer_key)

    elif question_type == "drag_drop":
        _answer_drag_drop(page, question, answer_key)


def _answer_simple_choice(page: Page, question: dict, answer_key: str):
    """
    Hàm này xử lý các câu hỏi trắc nghiệm đơn giản (text, hình ảnh, css).
    Nó có thể xử lý việc chọn một hoặc nhiều đáp án.
    """
    answers = question[answer_key]
    question_type = question.get("type", "text")

    for answer_locator in answers:
        if question_type == "text":
            page.get_by_text(answer_locator, exact=True).click()
        else:
            page.locator(answer_locator).click()


def _answer_fill_blank(page: Page, question: dict, answer_key: str):
    """Hàm này xử lý các câu hỏi dạng điền vào chỗ trống."""
    actions = question[answer_key]
    for action in actions:
        page.locator(action["blank_locator"]).click()
        page.get_by_text(action["choice_text"], exact=True).click()


def _answer_drag_drop(page: Page, question: dict, answer_key: str):
    mappings = question[answer_key]

    for drag_action in mappings:
        # Lấy thông tin của item cần kéo
        item_data = question["items_to_drag"][drag_action["item"]]
        item_text = item_data["text"]
        item_index = item_data.get("index", 0)

        # Tìm item cần kéo bằng cả text và index
        item_to_drag = page.get_by_text(item_text).nth(item_index)

        # Lấy thông tin của vùng cần thả
        zone_selector = question["drop_zones"][drag_action["zone"]]

        # Xác định đúng zone (1 hay 2) dựa trên locator
        if drag_action["zone"] == "zone1":
            drop_zone = page.locator(zone_selector).nth(0)
        else:
            drop_zone = page.locator(zone_selector).nth(1)
        # Thực hiện hành động kéo thả
        item_to_drag.drag_to(drop_zone)
        # expect(drop_zone).to_contain_text(item_text)

import pytest
import allure
import json
from pathlib import Path
from playwright.sync_api import Page, expect
from tests.utils.complete_helpers import confirm_score_and_proceed, complete_question
from tests.utils.drawing_helpers import draw_character
from tests.utils.choice_helpers import answer_question

@pytest.fixture(scope="module")
def quiz_data():
    current_file_path = Path(__file__)
    suimi_dir = current_file_path.parent
    json_path = suimi_dir / "kodomowo_data.json"

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        pytest.fail(f"LỖI: Không tìm thấy file data tại: {json_path}")
    return data
@pytest.fixture(scope="function")
def drawing_page(logged_in_page: Page):
    page = logged_in_page
    with allure.step("Điều hướng tới trang vẽ Kokugo Pre-test (kodomowo)"):
        page.get_by_alt_text("国語").click()
        page.get_by_text("プレテスト").nth(6).click()
    yield page

def test_full_quiz_flow(drawing_page: Page, quiz_data: dict):
    page = drawing_page
    drawing_data_list = quiz_data.get("DRAWING_QUESTIONS", [])
    if not drawing_data_list:
        pytest.fail("Không tìm thấy 'DRAWING_QUESTIONS' trong file data.")

    total_drawing_questions = len(drawing_data_list)

    with allure.step(f"PHẦN 1: Thực hiện {total_drawing_questions} câu hỏi VẼ"):
        for i, question_data in enumerate(drawing_data_list):
            word = question_data.get("word")
            with allure.step(f"Câu vẽ {i + 1}/{total_drawing_questions}: 「{word}」"):
                draw_character(page, question_data)
                confirm_score_and_proceed(page)

        print(f"Đã hoàn thành {total_drawing_questions} câu vẽ. Chuyển sang Phần 2...")

    choice_questions = quiz_data.get("CHOICE_QUESTIONS", [])
    if not choice_questions:
        pytest.fail("Không tìm thấy 'CHOICE_QUESTIONS' trong file data.")

    total_choice_questions = len(choice_questions)

    with allure.step(f"PHẦN 2: Thực hiện {total_choice_questions} câu hỏi TRẮC NGHIỆM"):
        for index, question in enumerate(choice_questions):
            with allure.step(f"Câu trắc nghiệm {question['id']} (Loại: {question.get('type')})"):
                answer_key = "correct_answers"
                answer_question(page, question, answer_key)
                # 2. Click 'こたえあわせ'
                kotaeawase_button = page.get_by_role("button", name="こたえあわせ")
                expect(kotaeawase_button).to_be_enabled(timeout=10000)
                kotaeawase_button.click()
                expect(page.locator(".icon__answer--right")).to_be_visible(timeout=10000)
                is_last_question = (index == total_choice_questions - 1)
                if is_last_question:
                    with allure.step("Xử lý câu cuối cùng của bài test"):
                        complete_question(page)
                else:
                    with allure.step("Click 'つぎへ' để sang câu tiếp theo"):
                        next_button = page.get_by_role("button", name="つぎへ")
                        expect(next_button).to_be_enabled(timeout=10000)
                        next_button.click()
                        page.wait_for_load_state("networkidle", timeout=10000)

    with allure.step("Hoàn thành tất cả các câu hỏi"):
        print("Đã hoàn thành toàn bộ bài test.")
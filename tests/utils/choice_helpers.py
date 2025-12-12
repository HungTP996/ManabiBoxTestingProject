from playwright.sync_api import Page, expect


def answer_question(page: Page, question: dict, answer_key: str):
    """
    質問タイプに応じて適切な回答関数を呼び出す。
    """
    question_type = question.get("type", "text")
    print(f"--> 質問 {question['id']} を実行中 (タイプ: {question_type})")

    if question_type in ["text", "image", "css", "xpath"]:
        _answer_simple_choice(page, question, answer_key)

    elif question_type == "fill_blank":
        _answer_fill_blank(page, question, answer_key)

    elif question_type == "drag_drop":
        _answer_drag_drop(page, question, answer_key)


def _answer_simple_choice(page: Page, question: dict, answer_key: str):
    answers = question[answer_key]
    question_type = question.get("type", "text")
    for answer_locator in answers:
        if question_type == "text":
            page.get_by_text(answer_locator, exact=True).first.click()
        else:
            page.locator(answer_locator).first.click()


def _answer_fill_blank(page: Page, question: dict, answer_key: str):
    """
    空欄補充形式の質問に回答する。
    """
    actions = question[answer_key]
    for action in actions:
        page.locator(action["blank_locator"]).click()
        page.get_by_text(action["choice_text"], exact=True).click()

def _answer_drag_drop(page: Page, question: dict, answer_key: str):
    """
    ドラッグアンドドロップ形式の質問に回答する（マウス操作シミュレーション）。
    """
    mappings = question[answer_key]

    for drag_action in mappings:
        # 1. ドラッグするアイテムの取得
        item_key = drag_action["item"]
        item_data = question["items_to_drag"][item_key]
        
        if isinstance(item_data, dict):
            item_text = item_data["text"]
            item_index = item_data.get("index", 0)
        else:
            item_text = item_data
            item_index = 0
            
        item_to_drag = page.get_by_text(item_text).nth(item_index)

        # 2. ドロップゾーンの取得（辞書型と文字列型の両方に対応）
        zone_name = drag_action["zone"]
        zone_data = question["drop_zones"][zone_name]

        if isinstance(zone_data, dict):
            zone_selector = zone_data["locator"]
            zone_index = zone_data.get("index", 0)
        else:
            zone_selector = zone_data
            zone_index = 0
        
        drop_zone = page.locator(zone_selector).nth(zone_index)

        print(f"    -> '{item_text}' (index {item_index}) のドラッグを準備中...") 

        try:
            expect(item_to_drag).to_be_visible(timeout=5000)
            expect(drop_zone).to_be_visible(timeout=5000)

            print(f"    -> '{item_text}' をゾーン '{zone_name}' へドラッグ中...")

            # バウンディングボックスの取得
            item_bb = item_to_drag.bounding_box()
            zone_bb = drop_zone.bounding_box()

            if not item_bb or not zone_bb:
                raise Exception(f"アイテムまたはゾーンのバウンディングボックスが見つかりませんでした。")

            # 3. マウス操作によるドラッグ＆ドロップ実行
            
            # アイテムの中心へ移動
            page.mouse.move(
                item_bb['x'] + item_bb['width'] / 2,
                item_bb['y'] + item_bb['height'] / 2
            )
            
            # つかむ
            page.mouse.down()
            page.wait_for_timeout(200)

            # ゾーンの中心へ移動（steps=5 で滑らかに移動）
            page.mouse.move(
                zone_bb['x'] + zone_bb['width'] / 2,
                zone_bb['y'] + zone_bb['height'] / 2,
                steps=5 
            )
            page.wait_for_timeout(300)

            # 放す
            page.mouse.up()
            page.wait_for_timeout(300)

            print(f"    -> '{item_text}' をドロップしました。") 

        except Exception as e:
            print(f"    エラー: '{item_text}' のドラッグに失敗しました: {e}")
            # エラー時のスクリーンショット保存
            page.screenshot(path=f"screenshots/DEBUG_drag_ERROR_{item_text}.png")
            raise e
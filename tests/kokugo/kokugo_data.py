QUESTIONS_DATA_AMEDESUYO = [
    # --- Câu hỏi 1:
    {
        "id": 1, "type": "text",
        "correct_answers": ["ぶた"],
        "incorrect_answers": ["ぶだ", "ぷた"]
    },
    # --- Câu hỏi 2:
    {
        "id": 2, "type": "text",
        "correct_answers": ["えんぴつ"],
        "incorrect_answers": ["えんひつ", "えんびつ"]
    },
    # --- Câu hỏi 3:
    {
        "id": 3, "type": "text",
        "correct_answers": ["ひつじ"],
        "incorrect_answers": ["ひづじ", "ひづし"]
    },
    # --- Câu hỏi 4 ---
    {
        "id": 4, "type": "text",
        "correct_answers": ["はなび"],
        "incorrect_answers": ["はなひ", "はなぴ"]
    },
    # --- Câu hỏi 5 ---
    {
        "id": 5, "type": "css",
        "correct_answers": [
            '[id="1047320"] img'  # donguri
        ],
        "incorrect_answers": [
            '[id="1047322"] img',  # tonkuri
            '[id="1047321"] img'  # tonguri
        ]
    }
]
# ===================================================================
# == DỮ LIỆU CHO CHỦ ĐỀ "ぶんを　つくろう" ==
# ===================================================================

QUESTIONS_DATA_TONKOTOTON = [
        # --- Câu hỏi 1:
        {
            "id": 1, "type": "text",
            "correct_answers": ["およぐ"],
            "incorrect_answers": ["はねる", "たべる"]
        },
        # --- Câu hỏi 2:
        {
            "id": 2, "type": "text",
            "correct_answers": ["ねる"],
            "incorrect_answers": ["はしる", "たべる"]
        },
        # --- Câu hỏi 3:
        {
            "id": 3, "type": "text",
            "correct_answers": ["わらう"],
            "incorrect_answers": ["おこる", "あるく"]
        },
        # --- Câu hỏi 4 ---
        {
            "id": 4, "type": "text",
            "correct_answers": ["あめが　ふる。", "あじさいが　さく。"],
            "incorrect_answers": ["かさが　こわれる。", "かえるが　ねる。"]
        },
        # --- Câu hỏi 5 ---
        {
            "id": 5, "type": "text",
            "correct_answers": ["とりが　おどろく。", "とりが　わらう。"],
            "incorrect_answers": ["とりが　たべる。", "とりが　およぐ。"]
        },
    ]
# ===================================================================
# == DỮ LIỆU CHO CHỦ ĐỀ "はを つかおう" ==
# ===================================================================
QUESTIONS_DATA_HA_WO_TSUKAOU = [
    # --- Câu hỏi 1: Dùng text ---
    {
        "id": 1, "type": "text",
        "correct_answers": ["は"],
        "incorrect_answers": ["わ"]
    },
    # --- Câu hỏi 2: Dùng text ---
    {
        "id": 2, "type": "text",
        "correct_answers": ["は"],
        "incorrect_answers": ["わ"]
    },
    # --- Câu hỏi 3: Dùng text ---
    {
        "id": 3, "type": "text",
        "correct_answers": ["わに"],
        "incorrect_answers": ["はに"]
    },
    # --- Câu hỏi 4: Dùng data-id ---
    {
        "id": 4, "type": "fill_blank",
        "choices": {"わ": "わ", "は": "は"},
        "correct_answers": [  # Đổi tên "answers" thành "correct_answers" cho nhất quán
            {"blank_locator": '[data-id="question-0"]', "choice_text": "わ"},
            {"blank_locator": '[data-id="question-1"]', "choice_text": "は"}
        ],
        # THÊM MỚI: Kịch bản trả lời sai (tráo đổi vị trí)
        "incorrect_answers": [
            {"blank_locator": '[data-id="question-0"]', "choice_text": "は"},
            {"blank_locator": '[data-id="question-1"]', "choice_text": "わ"}
        ]
    },
    # --- Câu hỏi 5: Dùng CSS selector ---
    {
        "id": 5, "type": "drag_drop",
        "items_to_drag": {
            "item1": "にわとりは　とばない。",
            "item2": "ねずみわ　ちいさい。",
            "item3": "はみがきは　だいじだ。",
            "item4": "わにわ　およぐ。"
        },
        "drop_zones": {
            "zone1": ".h-112px",
            "zone2": ".h-112px"
        },
        "correct_drag_mapping": [  # Đổi tên "drag_mapping" thành "correct_drag_mapping"
            {"item": "item1", "zone": "zone1"},
            {"item": "item2", "zone": "zone2"},
            {"item": "item3", "zone": "zone1"},
            {"item": "item4", "zone": "zone2"}
        ],
        # THÊM MỚI: Kịch bản kéo thả sai (ví dụ: tráo đổi 2 item đầu)
        "incorrect_drag_mapping": [
            {"item": "item2", "zone": "zone1"},  # item2 vào zone1 (sai)
            {"item": "item1", "zone": "zone2"},  # item1 vào zone2 (sai)
            {"item": "item3", "zone": "zone1"},
            {"item": "item4", "zone": "zone2"}
        ]
    }
]
# ===================================================================
# == DỮ LIỆU CHO CHỦ ĐỀ "をへを つかおう" ==
# ===================================================================
QUESTIONS_DATA_WOHEWO = [
    # --- Câu hỏi 1 ---
    {
        "id": 1,
        "correct_answer": "を",
        "incorrect_answer": "お", # Thêm đáp án sai
        "expected_message": "ことばを　つなぐ　ときは、「を」を　つかうね。"
    },
    # --- Câu hỏi 2 ---
    {
        "id": 2,
        "correct_answer": "へ",
        "incorrect_answer": "え", # Thêm đáp án sai
        "expected_message": "ことばを　つなぐ　ときは、「へ」と　かくよ。"
    },
    # --- Câu hỏi 3 ---
    {
        "id": 3,
        "correct_answer": "を",
        "incorrect_answer": "へ", # Thêm đáp án sai
        "expected_message": "「を」と　「へ」を　ただしく　つかいわけよう。"
    },
    # --- Câu hỏi 4 ---
    {
        "id": 4,
        "correct_answer": "へ",
        "incorrect_answer": "を", # Thêm đáp án sai
        "expected_message": "「を」と　「へ」を　ただしく　つかいわけよう。"
    },
    # --- Câu hỏi 5 ---
    {
        "id": 5,
        "correct_answer": "わたしは　いちごを　たべます。",
        "incorrect_answer": "わたしは　ゆうえんちえ　いきます。", # Thêm đáp án sai
        "expected_message": "「を」「へ」に　きを　つけて　よもう。"
    }
]
# ===================================================================
# == DỮ LIỆU CHO CHỦ ĐỀ "さとうと しお" (ĐÃ CẬP NHẬT) ==
# ===================================================================
QUESTIONS_DATA_SATOUTOSHIO = [
    # --- Câu hỏi 1 ---
    {
        "id": 1,
        "correct_answer": "を",
        "incorrect_answer": "お",
    },
    # --- Câu hỏi 2 ---
    {
        "id": 2,
        "correct_answer": "へ",
        "incorrect_answer": "え",
    },
    # --- Câu hỏi 3 (nhiều đáp án đúng) ---
    {
        "id": 3,
        "correct_answers": ["は", "へ"],
        "expected_messages": ["は", "へ"]
        # Kịch bản sai cho câu này sẽ là chọn thiếu đáp án
    },
    # --- Câu hỏi 4 (tương tự câu 3) ---
    {
        "id": 4,
        "correct_answers": ["は", "へ"],
        "expected_messages": ["は", "へ"]
    },
    {
        "id": 5,
        "correct_answer": "。",
        "incorrect_answer": "、",
    }
]

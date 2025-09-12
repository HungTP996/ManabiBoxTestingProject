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
# ===================================================================
# == DỮ LIỆU CHO CHỦ ĐỀ "ねこと　ねっこ" ==
# ===================================================================
QUESTIONS_DATA_NEKOTONEKKO = [
    # --- Câu hỏi 1 ---
    {
        "id": 1,
        "type": "text",
        "correct_answers": ["はらっぱ"],
        "incorrect_answers": ["はらつぱ", "はっらぱ"],
        "expected_message": "「は」と　「ぱ」の　ちがいにも　きを　つけよう。"
    },
    # --- Câu hỏi 2 ---
    {
        "id": 2,
        "type": "text",
        "correct_answers": ["もっきん"],
        "incorrect_answers": ["もきっん", "もつきん"],
        "expected_message": "「っ」が　どこに　はいるか　たしかめよう。"
    },
    # --- Câu hỏi 3 (Hình ảnh) ---
    {
        "id": 3,
        "type": "image",
        "correct_answers": ["xpath=//*[@id='1047370']"],
        "incorrect_answers": ["xpath=//*[@id='1047371']"]
    },
    # --- Câu hỏi 4 ---
    {
        "id": 4,
        "type": "text",
        "correct_answers": ["ねっこ"],
        "incorrect_answers": ["ねこ"],
        "expected_message":"「ねこ」と　「ねっこ」では、いみが　かわるね。"
    },
    # --- Câu hỏi 5 ---
    {
        "id": 5,
        "type": "text",
        "correct_answers": ["きって"],
        "incorrect_answers": ["きつて"],
        "expected_message":"ちいさい　「っ」の　かきかたに　きを　つけよう。"
    }
]
QUESTIONS_DATA_NOBASUON = [
# ===================================================================
# == DỮ LIỆU CHO CHỦ ĐỀ "のばす　おん" ==
# ===================================================================
    # --- Câu hỏi 1 ---
    {
        "id": 1,
        "type": "text",
        "correct_answers": ["お"],
        "incorrect_answers": ["う"],
        "expected_message": "「お」の　のばす　おんは、「う」「お」の　どちらを　かくか、きを　つけよう。"
    },
    # --- Câu hỏi 2 ---
    {
        "id": 2,
        "type": "text",
        "correct_answers": ["あ"],
        "incorrect_answers": ["う"],
        "expected_message": "「か」を　ながく　のばすと、「あ」の　おとに　なるね。"
    },
    # --- Câu hỏi 3  ---
    {
        "id": 3,
        "type": "text",
        "correct_answers": ["え"],
        "incorrect_answers": ["い"],
        "expected_message": "「ね」を　ながく　のばすと、「え」の　おとに　なるね。"
    },
    # --- Câu hỏi 4 ---
    {
        "id": 4,
        "type": "text",
        "correct_answers": ["せんせい"],
        "incorrect_answers": ["せんせえ"],
        "expected_message":"」だけど、かく　ときは　「せんせ"
    },
    # --- Câu hỏi 5 ---
    {
        "id": 5,
        "type": "text",
        "correct_answers": ["ぼうし"],
        "incorrect_answers": ["ぼおし"],
        "expected_message":"」だけど、かく　ときは　「せんせ"
    }
]
# ===================================================================
# == DỮ LIỆU CHO CHỦ ĐỀ "どう　やって　みを　まもるのかな" ==
# ===================================================================
QUESTIONS_DATA_DOUYATTEPRE = [
    {
        "id": 1,
        "type": "text",
        "correct_answers": ["あ"],
        "incorrect_answers": ["い"],
        "expected_message": "あ"
    },
    # --- Câu hỏi 2 ---
    {
        "id": 2,
        "type": "text",
        "correct_answers": ["う"],
        "incorrect_answers": ["お"],
        "expected_message": "う"
    },
    # --- Câu hỏi 3  ---
    {
        "id": 3,
        "type": "text",
        "correct_answers": ["え"],
        "incorrect_answers": ["い"],
        "expected_message": "「ね」を　ながく　のばすと、「え」の　おとに　なるね。"
    },
    # --- Câu hỏi 4 ---
    {
        "id": 4,
        "type": "text",
        "correct_answers": ["きって"],
        "incorrect_answers": ["きつて"],
        "expected_message":"きって"
    },
    # --- Câu hỏi 5 ---
    {
        "id": 5,
        "type": "text",
        "correct_answers": ["ねっこ"],
        "incorrect_answers": ["ねこ"],
        "expected_message":"ねっこ"
    }
]
# ===================================================================
# == DỮ LIỆU CHO CHỦ ĐỀ "おおきな　かぶ" ==
# ===================================================================
QUESTIONS_DATA_OOKINAKABU = [
    {
        "id": 1,
        "type": "text",
        "correct_answers": ["しゃ"],
        "incorrect_answers": ["しや"],
        "expected_message": "つづけて　よんで　みて、こたえを　たしかめよう。"
    },
    # --- Câu hỏi 2 ---
    {
        "id": 2,
        "type": "text",
        "correct_answers": ["あくしゅ"],
        "incorrect_answers": ["あくしゆ"],
        "expected_message": "ちいさく　かく　字に　きを　つけよう。"
    },
    # --- Câu hỏi 3  ---
    {
        "id": 3,
        "type": "text",
        "correct_answers": ["はっぴょう"],
        "incorrect_answers": ["はつぴよう"],
        "expected_message": "「つ」と　「よ」を、どちらも　ちいさく　かくよ。"
    },
    # --- Câu hỏi 4 ---
    {
        "id": 4,
        "type": "text",
        "correct_answers": ["しょっき"],
        "incorrect_answers": ["しよつき"],
        "expected_message":"「よ」と　「つ」を、どちらも　ちいさく　かくよ。"
    },
    # --- Câu hỏi 5 ---
    {
        "id": 5,
        "type": "image",
        "correct_answers": ["xpath=//*[@id='1047394']"],
        "incorrect_answers": ["xpath=//*[@id='1047395']","xpath=//*[@id='1047396']"],
        "expected_message":"「よ」と　「ゆ」を、どちらも　ちいさく　かくよ。"
    }
]
# ===================================================================
# == DỮ LIỆU CHO CHỦ ĐỀ "おおきな　かぶ" ==
# ===================================================================
QUESTIONS_DATA_OOKINAKABUPRE = [
    {
        "id": 1,
        "type": "text",
        "correct_answers": ["しゃしん"],
        "incorrect_answers": ["しやしん"],
        "expected_message": "しゃしん"
    },
    # --- Câu hỏi 2 ---
    {
        "id": 2,
        "type": "text",
        "correct_answers": ["びょういん"],
        "incorrect_answers": ["びよういん"],
        "expected_message": "びょういん"
    },
    # --- Câu hỏi 3  ---
    {
        "id": 3,
        "type": "text",
        "correct_answers": ["いしゃ"],
        "incorrect_answers": ["いしや"],
        "expected_message": "いしゃ"
    },
    # --- Câu hỏi 4 ---
    {
        "id": 4,
        "type": "image",
        "correct_answers": ["xpath=//*[@id='1047642']"],
        "incorrect_answers": ["xpath=//*[@id='1047643']"],
        "expected_message": ""
    },
    {
        "id": 5,
        "type": "image",
        "correct_answers": ["xpath=//*[@id='1047644']"],
        "incorrect_answers": ["xpath=//*[@id='1047645']"],
        "expected_message": ""
    }
]
# ===================================================================
# == DỮ LIỆU CHO CHỦ ĐỀ "かたかなを　みつけよう" ==
# ===================================================================
QUESTIONS_DATA_KATAKANAWOMITSUKEYOU = [
    {
        "id": 1,
        "type": "text",
        "correct_answers": ["くれよん"],
        "incorrect_answers": ["えんぴつ", "じょうぎ"],
        "expected_message": "かたかなで　かく　ことばと　ひらがなで　かく　ことばが　あるよ。"
    },
    # --- Câu hỏi 2 ---
    {
        "id": 2,
        "type": "text",
        "correct_answers": ["ぼうる"],
        "incorrect_answers": ["くつ", "つち"],
        "expected_message": "みの　まわりから　かたかなで　かく　ことばを　さがそう。"
    },
    # --- Câu hỏi 3  ---
    {
        "id": 3,
        "type": "text",
        "correct_answers": ["クレヨン"],
        "incorrect_answers": ["クレヨル"],
        "expected_message": "おぼえた　かたかなは　かけるように　しよう。"
    },
    # --- Câu hỏi 4 ---
    {
        "id": 4,
        "type": "text",
        "correct_answers": ["ボール"],
        "incorrect_answers": ["ボル", "ボンル", "ホール"],
        "expected_message": "かたかなでは、のばす　おんは　「ー」を　かくよ。"
    },
    {
        "id": 5,
        "type": "text",
        "correct_answers": ["ルール"],
        "incorrect_answers": ["ルンル", "ルル"],
        "expected_message": "かたかなでは、のばす　おんは　「ー」を　かくよ。"
    }
]
# ===================================================================
# == DỮ LIỆU CHO CHỦ ĐỀ "かぞえうた" ==
# ===================================================================
QUESTIONS_DATA_KAZOEUTA = [
    {
        "id": 1,
        "type": "text",
        "correct_answers": ["びき"],
        "incorrect_answers": ["ひき", "ぴき"],
        "expected_message": "き」と　おとが　かわるよ。"
    },
    # --- Câu hỏi 2 ---
    {
        "id": 2,
        "type": "text",
        "correct_answers": ["さつ"],
        "incorrect_answers": ["にん", "だい"],
        "expected_message": "ほんを　かぞえる　ときは、「さつ」を　つかうよ。"
    },
    # --- Câu hỏi 3  ---
    {
        "id": 3,
        "type": "text",
        "correct_answers": ["まい"],
        "incorrect_answers": ["ぴき", "さつ"],
        "expected_message": "かみを　かぞえる　ときは、「まい」を　つかうよ。"
    },
    # --- Câu hỏi 4 ---
    {
        "id": 4,
        "type": "text",
        "correct_answers": ["ぽん"],
        "incorrect_answers": ["さつ", "にん"],
        "expected_message": "ん」と　おとが　かわるよ。"
    },
    {
        "id": 5,
        "type": "text",
        "correct_answers": ["さらが　四まい。"],
        "incorrect_answers": ["えんぴつが　四まい。", "くるまが　四まい。"],
        "expected_message": "「まい」は、うすくて　ひらたい　ものを　かぞえる　ときに　つかうよ。"
    }
]
# ===================================================================
# == DỮ LIỆU CHO CHỦ ĐỀ "かんじのはなし" ==
# ===================================================================
QUESTIONS_DATA_KANJINOHANASHI = [
    {
        "id": 1,
        "type": "text",
        "correct_answers": ["日"],
        "incorrect_answers":  ["月"],
        "expected_message": "日と　月は　かたちが　にて　いるので、　気を　つけよう。"
    },
    # --- Câu hỏi 2 ---
    {
        "id": 2,
        "type": "text",
        "correct_answers": ["山"],
        "incorrect_answers":  ["上"],
        "expected_message": "山と　いう　かんじは　山の　かたちから　できたよ。"
    },
    # --- Câu hỏi 3  ---
    {
        "id": 3,
        "type": "text",
        "correct_answers": ["川"],
        "incorrect_answers": ["三"],
        "expected_message": "川と　いう　かんじは　川の　ながれる　ようすから　できたよ。"
    },
    # --- Câu hỏi 4 ---
    {
        "id": 4,
        "type": "text",
        "correct_answers": ["下"],
        "incorrect_answers": ["上", "一"],
        "expected_message": "下と　いう　かんじは、下に　ものが　ある　ことを　しめす　しるしから　できたよ。"
    },
    {
        "id": 5, "type": "drag_drop",
        "items_to_drag": {
            "item1": "下",
            "item2": "木",
            "item3": "月",
            "item4": "上"
        },
        "drop_zones": {
            "zone1": ".h-112px",
            "zone2": ".h-112px"
        },
        "correct_drag_mapping": [  # Đổi tên "drag_mapping" thành "correct_drag_mapping"
            {"item": "item1", "zone": "zone2"},
            {"item": "item2", "zone": "zone1"},
            {"item": "item3", "zone": "zone1"},
            {"item": "item4", "zone": "zone2"}
        ],
        # THÊM MỚI: Kịch bản kéo thả sai (ví dụ: tráo đổi 2 item đầu)
        "incorrect_drag_mapping": [
            {"item": "item1", "zone": "zone1"},
            {"item": "item2", "zone": "zone2"},
            {"item": "item3", "zone": "zone2"},
            {"item": "item4", "zone": "zone1"}
        ]
    }
]

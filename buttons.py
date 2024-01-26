from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove



start_t = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton('/start')],
    ],
    resize_keyboard=True,
)

lang = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("🇺🇿 O'zbek tili")],
        [KeyboardButton("🇷🇺 Русский язык")],
        [KeyboardButton("🇬🇧 English")],
    ],
    resize_keyboard=True
)

contact_uz = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton('Ulashish', request_contact=True)]
    ],
    resize_keyboard=True
)

kop = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton("Xa", callback_data='Xa')],
        [InlineKeyboardButton("Yo'q", callback_data="Yo'q")],
        [InlineKeyboardButton("Orqaga", callback_data='Orqaga')],
    ]
)

user_uz = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton('Qarzdorlikni tekshirish')],
        [KeyboardButton('Biz bilan bog’lanish')],
        [KeyboardButton('Akt sverka olish')]
    ],
    resize_keyboard=True
)


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup



lang1 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("🇺🇿")],
        [KeyboardButton("🇺🇿")],
        [KeyboardButton("🇺🇿")],
    ],
    resize_keyboard=True,
)

tel = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton('Ulashish📞', request_contact=True)]
    ],
    resize_keyboard=True,
)

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Qarzdorlikni tekshirish"),
            KeyboardButton("Seriya bo'yicha izlash"),
         ]
    ],
    resize_keyboard=True
)

kop = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Xa"),
            KeyboardButton("Yo'q"),
            KeyboardButton("Orqaga"),
         ]
    ],
    resize_keyboard=True
)


t_list = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Tovarning kategoriyalari"),
            KeyboardButton("Izlash"),
            KeyboardButton("Asosiy menyuga qaytish")
         ]
    ],
    resize_keyboard=True
)

t_k_list = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Tovarlar ro’yxati"),
            KeyboardButton("Asosiy menyuga qaytish")
         ]
    ],
    resize_keyboard=True
)
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

# ---------- Главное меню RU ----------
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📘 Инструкция")],
        [KeyboardButton(text="🔍 Проверка на Refund")],
        [KeyboardButton(text="⬇️ Скачать Nicegram")]
    ],
    resize_keyboard=True
)

# ---------- Главное меню EN ----------
main_kb_en = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📘 Instructions")],
        [KeyboardButton(text="🔍 Refund Check")],
        [KeyboardButton(text="⬇️ Download Nicegram")]
    ],
    resize_keyboard=True
)

# ---------- Выбор языка ----------
lang_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Русский 🇷🇺", callback_data="lang_ru"),
            InlineKeyboardButton(text="English 🇺🇸", callback_data="lang_en")
        ]
    ]
)

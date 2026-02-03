import asyncio
import os
from dotenv import load_dotenv

# Загружаем .env перед всеми остальными импортами
load_dotenv()

from aiogram import Bot, Dispatcher
from handlers import router

# Теперь переменные окружения точно подхватятся
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

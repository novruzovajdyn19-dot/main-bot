from os import getenv
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from files.routes import router

load_dotenv()

TOKEN = getenv("BOT_TOKEN")
ADMIN_ID = int(getenv("ADMIN_ID", 0))
CHANNEL_ID = int(getenv("CHANEL_ID", 0))

dp = Dispatcher()
dp["CHANNEL_ID"] = CHANNEL_ID
dp["ADMIN_ID"] = ADMIN_ID

dp.include_router(router)

async def main():
    bot = Bot(token=TOKEN)
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
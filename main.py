import os
import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from files.routes import router

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))
CHANNEL_ID = int(os.getenv("CHANNEL_ID", 0))

dp = Dispatcher()
dp["CHANNEL_ID"] = CHANNEL_ID
dp["ADMIN_ID"] = ADMIN_ID
dp.include_router(router)
async def health_check(request):
    return web.Response(text="Bot is alive!")
async def start_web_server():
    app = web.Application()
    app.router.add_get("/", health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    bot = Bot(token=TOKEN)
    await start_web_server()
    print("Бот и веб-сервер запущены!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

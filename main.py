import asyncio
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import init_db, async_session, User

BOT_TOKEN = "8758382660:AAFNG9Q4v6BZQv0OqU02oMuc8g12hTZxq7M"
ADMIN_ID = 1678146043

# Sizning aniq, to'g'ri sozlangan GitHub Pages havolangiz:
WEB_APP_URL = "https://jocker7005-web.github.io/EFC-Football-Bot"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="🎮 O'yinni boshlash", web_app=types.WebAppInfo(url=WEB_APP_URL))
    await message.answer("Xush kelibsiz!", reply_markup=kb.as_markup())

async def handle_web(request):
    return web.Response(text="OK")

async def main():
    await init_db()
    try:
        # Doimiy ko'k oynachaga aniq to'g'ri havolani bog'laymiz
        await bot.set_chat_menu_button(
            menu_button=types.MenuButtonWebApp(
                text="🎮 O'yin",
                web_app=types.WebAppInfo(url=WEB_APP_URL)
            )
        )
    except:
        pass
    app = web.Application()
    app.router.add_get('/', handle_web)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    await web.TCPSite(runner, '0.0.0.0', port).start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    

import asyncio
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import init_db, async_session, User

BOT_TOKEN = "8758382660:AAFNG9Q4v6BZQv0OqU02oMuc8g12hTZxq7M"
ADMIN_ID = 1678146043

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    async with async_session() as session:
        async with session.begin():
            pass
    
    # Render hostingingiz o'z havolasini avtomatik aniqlaydi
    render_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME', '://onrender.com')}/"
    
    kb = InlineKeyboardBuilder()
    kb.button(text="🎮 O'yinni boshlash", web_app=types.WebAppInfo(url=render_url))
    await message.answer("Xush kelibsiz!", reply_markup=kb.as_markup())

# Render internetga index.html faylini Mini App ko'rinishida chiqaradi
async def handle_web(request):
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return web.Response(text=f.read(), content_type="text/html")
    return web.Response(text="Mini App fayli topilmadi!")

async def main():
    await init_db()
    render_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME', '://onrender.com')}/"
    try:
        await bot.set_chat_menu_button(
            menu_button=types.MenuButtonWebApp(
                text="🎮 O'yin",
                web_app=types.WebAppInfo(url=render_url)
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
    

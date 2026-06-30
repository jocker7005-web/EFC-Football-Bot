import asyncio
import sqlite3
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiohttp import web

# TOKENni Render'dagi Environment Variables'dan oladi
TOKEN = os.getenv("8758382660:AAFNG9Q4v6BZQv0OqU02oMuc8g12hTZxq7M") 
ADMIN_ID = 1678146043
REVIEW_CHANNEL = -1001908315496
CARD_DETAILS = "9860 3501 0897 5409 Xusanova M"
MIN_LIMIT = 10000 

bot = Bot(token=TOKEN)
dp = Dispatcher()

def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY, 
                        efc_balance INTEGER DEFAULT 0,
                        som_balance INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

# Bot buyruqlari...
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Bot Render'da ishga tushdi! ✅")

# ... (qolgan funksiyalaringizni shu yerga qo'shing) ...

# Render uchun kerakli portni tinglovchi web server
async def handle(request):
    return web.Response(text="Bot ishlamoqda")

async def main():
    init_db()
    
    # Web serverni ishga tushiramiz (Render uchun shart!)
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    # Botni ishga tushiramiz
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    

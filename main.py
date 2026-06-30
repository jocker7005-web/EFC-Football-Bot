import asyncio
import os
import sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart
from aiohttp import web

# TOKENni Render'dagi Environment Variables'dan avtomatik oladi
TOKEN = os.getenv("TOKEN") 
PORT = int(os.environ.get("PORT", 10000)) # Render bergan portni oladi

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Bazani sozlash
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY, 
                        efc_balance INTEGER DEFAULT 0,
                        som_balance INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Bot Render'da muvaffaqiyatli ishga tushdi! ✅")

# ... (boshqa kodlaringizni shu yerga qo'ying) ...

# Render uchun kichik web-server (Bot "o'lib qolmasligi" uchun)
async def handle(request):
    return web.Response(text="Bot ishlamoqda")

async def main():
    init_db()
    
    # 1. Web serverni ishga tushiramiz
    app = web.Application()
    app.router.add_get('/', handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()
    
    # 2. Botni ishga tushiramiz
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    

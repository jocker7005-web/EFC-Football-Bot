import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession

TOKEN = "8758382660:AAFNG9Q4v6BZQv0OqU02oMuc8g12hTZxq7M"

async def main():
    print("Bot ishga tushirilmoqda...")
    # Sessiyani aniq sozlash
    session = AiohttpSession()
    bot = Bot(token=TOKEN, session=session)
    dp = Dispatcher()
    
    print("Bot muvaffaqiyatli ulandi! Polling boshlandi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"Xatolik yuz berdi: {e}")
        

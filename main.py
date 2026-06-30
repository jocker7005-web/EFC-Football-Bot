import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Logingni yoqish
logging.basicConfig(level=logging.INFO)

# BOT TOKENI (Siz so'ragan token)
TOKEN = "8758382660:AAGeaXpafGCFooWtdAHwLogopvqKLWKI6IM"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# /start buyrug'i uchun javob
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Assalomu alaykum! Bot ishga tushdi. ✅")

# Botni ishga tushirish
async def main():
    print("Bot muvaffaqiyatli ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
  

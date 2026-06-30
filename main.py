import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

# BotFather'dan olingan sizning tokeningiz
BOT_TOKEN = "8758382660:AAFNG9Q4v6BZQv0OqU02oMuc8g12hTZxq7M"

# Amvera loglarida xatoliklarni kuzatish uchun loggingni yoqamiz
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher obyektlarini yaratish
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Foydalanuvchi /start buyrug'ini bosganda ishlaydigan qism
@dp.message(CommandStart())
async def command_start_handler(message: types.Message) -> None:
    welcome_text = (
        "Assalomu alaykum! EFC-Futbol-Bot muvaffaqiyatli ishga tushdi! ⚽🤖\n\n"
        "Siz /start tugmasini bosdingiz. Bot endi aiogram orqali xabarlaringizni kutmoqda!"
    )
    await message.answer(welcome_text)

# Botni doimiy (polling) rejimda ishga tushirish funksiyasi
async def main() -> None:
    print("Bot polling rejimida ishga tushmoqda...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    

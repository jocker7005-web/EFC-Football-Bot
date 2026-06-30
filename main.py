import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart

# TOKENINGIZNI SHU YERGA YOZING
TOKEN = "8758382660:AAGeaXpafGCFooWtdAHwLogopvqKLWKI6IM"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# BAZANI SOZLASH
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY, 
                        balance INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

# EFC qo'shish funksiyasi
def add_efc(user_id, amount):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id, balance) VALUES (?, 0)', (user_id,))
    cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount, user_id))
    conn.commit()
    conn.close()

# /start buyrug'i (Referral tizimi bilan)
@dp.message(CommandStart(deep_link=True))
async def cmd_start_referral(message: types.Message, command: types.CommandObject):
    args = command.args # referral ID
    user_id = message.from_user.id
    
    # Yangi foydalanuvchini bazaga qo'shish
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()
    
    # Referral orqali kirsa, 10 EFC berish
    if args and args.isdigit():
        referrer_id = int(args)
        if referrer_id != user_id:
            add_efc(referrer_id, 10)
            await bot.send_message(referrer_id, "Sizga do'stingiz uchun 10 EFC qo'shildi! 💰")
            await message.answer("Siz do'stingiz taklifi bilan kirdingiz!")
    
    await message.answer("Assalomu alaykum! Botga xush kelibsiz. Hisobingizda EFC yig'ishni boshlang! 🚀")

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Assalomu alaykum! Bot ishga tushdi.")

async def main():
    init_db()
    print("Bot muvaffaqiyatli ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    

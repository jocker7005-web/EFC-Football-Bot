import asyncio
import sqlite3
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command, CommandStart

# SIZ BERGAN MA'LUMOTLAR BILAN
TOKEN = "8758382660:AAFNG9Q4v6BZQv0OqU02oMuc8g12hTZxq7M"
ADMIN_ID = 1678146043
REVIEW_CHANNEL = -1001908315496
CARD_DETAILS = "9860 3501 0897 5409 Xusanova M"
MIN_LIMIT = 10000 

bot = Bot(token=TOKEN)
dp = Dispatcher()

# DATABASE
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY, 
                        efc_balance INTEGER DEFAULT 0,
                        som_balance INTEGER DEFAULT 0)''')
    conn.commit()
    conn.close()

# YECHISH (Withdraw) - Faqat SOM
@dp.message(Command("withdraw"))
async def withdraw_request(message: types.Message):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT som_balance FROM users WHERE user_id = ?', (message.from_user.id,))
    row = cursor.fetchone()
    som = row[0] if row else 0
    conn.close()

    if som < MIN_LIMIT:
        await message.answer(f"❌ Xatolik! Yechish uchun kamida {MIN_LIMIT} UZS bo'lishi kerak. Sizda: {som} UZS.")
    else:
        await bot.send_message(REVIEW_CHANNEL, f"📩 YECHISH SO'ROVI!\n\n👤 User ID: {message.from_user.id}\n💰 Summa: {som} UZS\n💳 Karta: {CARD_DETAILS}")
        await message.answer("✅ Yechish so'rovingiz adminlarga yuborildi! Tez orada ko'rib chiqiladi.")

# TO'LDIRISH (Deposit)
@dp.message(Command("deposit"))
async def deposit_request(message: types.Message):
    await message.answer(f"To'ldirish uchun {CARD_DETAILS} kartasiga kamida {MIN_LIMIT} UZS o'tkazing va chekni adminlarga yuboring.")

# ADMIN: So'm qo'shish
@dp.message(F.text.startswith("/add_som"))
async def add_som(message: types.Message):
    if message.from_user.id != ADMIN_ID: return
    try:
        parts = message.text.split()
        target_id = int(parts[1])
        amount = int(parts[2])
        if amount < MIN_LIMIT:
            await message.answer(f"❌ Xatolik! Minimal to'ldirish {MIN_LIMIT} UZS.")
            return
            
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (target_id,))
        cursor.execute('UPDATE users SET som_balance = som_balance + ? WHERE user_id = ?', (amount, target_id))
        conn.commit()
        conn.close()
        await message.answer(f"✅ User {target_id} balansiga {amount} UZS qo'shildi.")
        await bot.send_message(target_id, f"💰 Balansingizga {amount} UZS qo'shildi!")
    except:
        await message.answer("Format: /add_som [ID] [SUMMA]")

# BALANSNI KO'RISH
@dp.message(Command("balance"))
async def show_balance(message: types.Message):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (message.from_user.id,))
    cursor.execute('SELECT efc_balance, som_balance FROM users WHERE user_id = ?', (message.from_user.id,))
    row = cursor.fetchone()
    conn.close()
    
    efc = row[0] if row else 0
    som = row[1] if row else 0
    await message.answer(f"💰 Balansingiz:\n\nEFC Ball: {efc}\nReal Pul: {som} UZS")

async def main():
    init_db()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    

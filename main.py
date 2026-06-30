import asyncio, random, os
from aiohttp import web
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database import init_db, async_session, User, DepositOrder, GlobalSetting
from sqlalchemy import select

BOT_TOKEN = "8758382660:AAFNG9Q4v6BZQv0OqU02oMuc8g12hTZxq7M"
ADMIN_ID = 1678146043
KANAL_ID = -1001908315496
KARTA_RAQAM = "9860 3501 0897 5409 Xusanova M"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    async with async_session() as session:
        async with session.begin():
            stmt = select(User).where(User.telegram_id == message.from_user.id)
            res = await session.execute(stmt)
            if not res.scalar_one_or_none():
                session.add(User(telegram_id=message.from_user.id, username=message.from_user.username or "Noma'lum"))
    kb = InlineKeyboardBuilder()
    kb.button(text="🎮 O'yinni boshlash (Web App)", web_app=types.WebAppInfo(url="https://google.com"))
    kb.button(text="💳 Balansni to'ldirish", callback_data="deposit_info")
    kb.button(text="🎡 Omad G'ildiragi", callback_data="spin_wheel")
    await message.answer("Xush kelibsiz! eFootball Web App botiga xush kelibsiz.", reply_markup=kb.as_markup())

@dp.callback_query(F.data == "deposit_info")
async def deposit_info(callback: types.CallbackQuery):
    await callback.message.answer(f"Balansni to'ldirish uchun pul o'tkazing:\n\n💳 Karta: `{KARTA_RAQAM}`\n\nTo'lovdan so'ng chekni rasm ko'rinishida yuboring!", parse_mode="Markdown")
    await callback.answer()

@dp.message(F.photo)
async def handle_screenshot(message: types.Message):
    async with async_session() as session:
        new_order = DepositOrder(user_telegram_id=message.from_user.id, username=message.from_user.username or "Noma'lum", amount=0.0, file_id=message.photo[-1].file_id)
        session.add(new_order); await session.flush(); order_id = new_order.id; await session.commit()
    kb = InlineKeyboardBuilder()
    kb.button(text="✅ Qabul qilish", callback_data=f"approve_{order_id}")
    kb.button(text="❌ Rad etish", callback_data=f"reject_{order_id}")
    await bot.send_photo(chat_id=ADMIN_ID, photo=message.photo[-1].file_id, caption=f"📥 **Yangi buyurtma: #{order_id}**\n👤 Mijoz: @{message.from_user.username}", reply_markup=kb.as_markup(), parse_mode="Markdown")
    await message.answer(f"Chek adminga yuborildi. Buyurtma: #{order_id}")

@dp.callback_query(F.data.startswith("approve_"))
async def approve_order(callback: types.CallbackQuery):
    order_id = int(callback.data.split("_")[1])
    async with async_session() as session:
        async with session.begin():
            order = await session.get(DepositOrder, order_id)
            if order and order.status == "pending":
                order.status = "approved"
                try: await bot.send_message(chat_id=order.user_telegram_id, text=f"Sizning #{order_id} buyurtmangiz muvaffaqiyatli bajarildi!")
                except: pass
                await callback.message.edit_caption(caption=f"✅ Buyurtma #{order_id} tasdiqlandi!")
        await session.commit()
    await callback.answer()

@dp.callback_query(F.data.startswith("reject_"))
async def reject_order(callback: types.CallbackQuery):
    order_id = int(callback.data.split("_")[1])
    async with async_session() as session:
        async with session.begin():
            order = await session.get(DepositOrder, order_id)
            if order and order.status == "pending":
                order.status = "rejected"
                try: await bot.send_message(chat_id=order.user_telegram_id, text="Xatolik aniqlandi. Admin bilan bog'laning.")
                except: pass
                await callback.message.edit_caption(caption=f"❌ Buyurtma #{order_id} rad etildi!")
        await session.commit()
    await callback.answer()

@dp.callback_query(F.data == "spin_wheel")
async def spin_wheel(callback: types.CallbackQuery):
    async with async_session() as session:
        async with session.begin():
            counter = await session.get(GlobalSetting, "wheel_counter")
            counter.value += 1; current_spin = counter.value
            if current_spin == 60000: reward = "🎉 2000 COIN!"; counter.value = 0
            elif current_spin % 30000 == 0: reward = "🎁 130 COIN!"
            elif current_spin % 15000 == 0: reward = "🔥 250 EFC!"
            else: reward = random.choice(["1 EFC", "10 EFC", "50 EFC", "Yutqazdingiz"])
        await session.commit()
    await callback.message.answer(f"🎡 G'ildirak aylandi.\n\nYutuq: {reward}")
    await callback.answer()

async def handle_web(request): return web.Response(text="Bot ishlamoqda!")
async def main():
    await init_db()
    app = web.Application(); app.router.add_get('/', handle_web)
    runner = web.AppRunner(app); await runner.setup()
    await web.TCPSite(runner, '0.0.0.0', int(os.environ.get("PORT", 10000))).start()
    await dp.start_polling(bot)

if __name__ == "__main__": asyncio.run(main())
    

import asyncio
import random
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

# Botga /start bosilganda foydalanuvchini bazaga qo'shish
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    async with async_session() as session:
        async with session.begin():
            stmt = select(User).where(User.telegram_id == message.from_user.id)
            result = await session.execute(stmt)
            user = result.scalar_one_or_none()
            
            if not user:
                new_user = User(
                    telegram_id=message.from_user.id,
                    username=message.from_user.username or "Noma'lum"
                )
                session.add(new_user)
    
    kb = InlineKeyboardBuilder()
    kb.button(text="🎮 O'yinni boshlash (Web App)", web_app=types.WebAppInfo(url="https://google.com"))
    kb.button(text="💳 Balansni to'ldirish", callback_data="deposit_info")
    kb.button(text="🎡 Omad G'ildiragi", callback_data="spin_wheel")
    
    await message.answer(f"Xush kelibsiz! eFootball Web App botiga xush kelibsiz.", reply_markup=kb.as_markup())

# Balans to'ldirish ma'lumoti
@dp.callback_query(F.data == "deposit_info")
async def deposit_info(callback: types.CallbackQuery):
    text = (
        f"Balansni to'ldirish uchun pul o'tkazing:\n\n"
        f"💳 Karta: `{KARTA_RAQAM}`\n\n"
        f"To'lovni amalga oshirgach, chekni (skrinshot) shu yerga rasm ko'rinishida yuboring!"
    )
    await callback.message.answer(text, parse_mode="Markdown")
    await callback.answer()

# Mijoz chek rasm yuborgandagi mantiq
@dp.message(F.photo)
async def handle_screenshot(message: types.Message):
    file_id = message.photo[-1].file_id
    
    async with async_session() as session:
        new_order = DepositOrder(
            user_telegram_id=message.from_user.id,
            username=message.from_user.username or "Noma'lum",
            amount=0.0,
            file_id=file_id
        )
        session.add(new_order)
        await session.flush()
        order_id = new_order.id
        await session.commit()
    
    admin_kb = InlineKeyboardBuilder()
    admin_kb.button(text="✅ Qabul qilish", callback_data=f"approve_{order_id}")
    admin_kb.button(text="❌ Rad etish", callback_data=f"reject_{order_id}")
    
    user_mention = f"@{message.from_user.username}" if message.from_user.username else f"ID: {message.from_user.id}"
    
    await bot.send_photo(
        chat_id=ADMIN_ID,
        photo=file_id,
        caption=f"📥 **Yangi buyurtma: #{order_id}**\n👤 Mijoz: {user_mention}\n\nTo'lov to'g'ri bo'lsa, qabul qilishni bosing.",
        reply_markup=admin_kb.as_markup(),
        parse_mode="Markdown"
    )
    await message.answer("Sizning chekingiz adminga yuborildi. Buyurtma raqamingiz: #" + str(order_id))

# Admin tasdiqlash tugmalari ishlovi
@dp.callback_query(F.data.startswith("approve_"))
async def approve_order(callback: types.CallbackQuery):
    order_id = int(callback.data.split("_"))
    
    async with async_session() as session:
        async with session.begin():
            order = await session.get(DepositOrder, order_id)
            if order and order.status == "pending":
                order.status = "approved"
                try:
                    await bot.send_message(
                        chat_id=order.user_telegram_id,
                        text=f"Sizning #{order_id} tartibli buyurtmangiz muvaffaqiyatli bajarildi va balansngiz to'ldirildi!"
                    )
                except:
                    pass
                await callback.message.edit_caption(caption=f"✅ Buyurtma #{order_id} tasdiqlandi va bajarildi!")
        await session.commit()
    await callback.answer()

@dp.callback_query(F.data.startswith("reject_"))
async def reject_order(callback: types.CallbackQuery):
    order_id = int(callback.data.split("_"))
    
    async with async_session() as session:
        async with session.begin():
            order = await session.get(DepositOrder, order_id)
            if order and order.status == "pending":
                order.status = "rejected"
                try:
                    await bot.send_message(
                        chat_id=order.user_telegram_id,
                        text="Xatolik aniqlandi. Muammo bo'yicha admin bilan bog'laning."
                    )
                except:
                    pass
                await callback.message.edit_caption(caption=f"❌ Buyurtma #{order_id} rad etildi!")
        await session.commit()
    await callback.answer()

# Omad g'ildiragi algoritmi
@dp.callback_query(F.data == "spin_wheel")
async def spin_wheel(callback: types.CallbackQuery):
    async with async_session() as session:
        async with session.begin():
            counter_obj = await session.get(GlobalSetting, "wheel_counter")
            counter_obj.value += 1
            current_spin = counter_obj.value
            
            reward_text = ""
            if current_spin == 60000:
                reward_text = "🎉 DAXSHAT! Siz 60,000-aylantirish egasisiz! 2000 COIN yutib oldingiz!"
                counter_obj.value = 0
            elif current_spin % 30000 == 0:
                reward_text = "🎁 Ajoyib! 130 COIN yutib oldingiz!"
            elif current_spin % 15000 == 0:
                reward_text = "🔥 Zo'r! 250 EFC yutib oldingiz!"
            else:
                options = ["1 EFC", "10 EFC", "50 EFC", "Yutqazdingiz (Qayta urunib ko'ring)"]
                reward_text = f"Sizning yutuqingiz: {random.choice(options)}"
                
        await session.commit()
    await callback.message.answer(f"🎡 G'ildirak aylandi (Global hisoblagich: {current_spin}).\n\n{reward_text}")
    await callback.answer()

async def main():
    await init_db()
    print("Baza tayyor va Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    

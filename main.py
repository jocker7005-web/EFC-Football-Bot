import os
import telebot

# BotFather'dan olingan token
BOT_TOKEN = "8758382660:AAFNG9Q4v6BZQv0OqU02oMuc8g12hTZxq7M"
bot = telebot.TeleBot(BOT_TOKEN)

# Foydalanuvchi /start buyrug'ini bosganda ishlaydi
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "Assalomu alaykum! EFC-Futbol-Bot muvaffaqiyatli ishga tushdi! ⚽🤖\n\n"
        "Siz /start tugmasini bosdingiz. Bot endi xabarlaringizni qabul qilishga tayyor!"
    )
    bot.reply_to(message, welcome_text)

# Botni doimiy aloqa (polling) rejimida ushlab turish
if __name__ == "__main__":
    print("Bot muvaffaqiyatli ishga tushirildi...")
    bot.infinity_polling()
    

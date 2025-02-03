import os
import instaloader
import requests
import re
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram.utils import executor

# Bot tokenini kiriting
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Instaloader obyektini yaratamiz
L = instaloader.Instaloader()

# Instagram post, reels yoki story yuklab olish funksiyasi
def download_instagram_media(url):
    try:
        post_id = re.findall(r"/p/(\w+)|/reel/(\w+)|/stories/(\w+)", url)
        if post_id:
            os.system(f"instaloader -- -{url}")
            files = [f for f in os.listdir() if f.endswith(".jpg") or f.endswith(".mp4")]
            return files
    except Exception as e:
        return str(e)
    
    return []

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Assalomu alaykum! Instagram yoki Telegram story havolasini yuboring.")

@dp.message_handler()
async def get_instagram_content(message: types.Message):
    url = message.text.strip()
    
    if "instagram.com" in url:
        await message.reply("Yuklab olinmoqda, iltimos kuting...")
        try:
            files = download_instagram_media(url)
            if files:
                for file in files:
                    await message.reply_document(InputFile(file))
                    os.remove(file)
            else:
                await message.reply("Xatolik! Foydalanish mumkin bo'lgan media topilmadi.")
        except Exception as e:
            await message.reply(f"Xatolik yuz berdi: {str(e)}")
    
    elif "t.me/" in url:
        await message.reply("Hozircha faqat Instagram media yuklab olish qo'llab-quvvatlanadi.")
    
    else:
        await message.reply("Iltimos, Instagram yoki Telegram story havolasini yuboring!")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

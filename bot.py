import re
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ChatPermissions
from aiogram.utils import executor
import os

# লগ সেটআপ
logging.basicConfig(level=logging.INFO)

# বট টোকেন সেটআপ (Railway এর Environment Variables থেকে নিবে)
API_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# বট এবং ডিসপ্যাচার ইনিশিয়ালাইজ
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# লিংক চেক করার ফাংশন
def contains_link(text):
    pattern = r"(https?://\S+|www\.\S+)"
    return re.search(pattern, text)

# লিংক থাকলে মেসেজ ডিলিট ও ইউজার ব্যান
@dp.message_handler(lambda message: message.text and contains_link(message.text))
async def delete_and_ban(message: types.Message):
    try:
        await message.delete()  # মেসেজ ডিলিট
        await message.chat.kick(user_id=message.from_user.id)  # ইউজার ব্যান

        # এডমিনদের জন্য নোটিফিকেশন
        admin_msg = f"🚫 {message.from_user.full_name} ব্যান হয়েছে কারণ সে লিংক শেয়ার করেছে!"
        await message.chat.send_message(admin_msg)

    except Exception as e:
        print(f"Error: {e}")

# বট চালু করা
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

⬇

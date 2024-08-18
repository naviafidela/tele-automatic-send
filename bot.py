# bot.py
import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils import markdown as md
from asupanmu_vip import msg_asupanmu_vip
from kontol_monster import msg_kontol_monster
from channel import CHANNELS

API_TOKEN = '7520123514:AAG8JcQ6H0zjV_eTtK2V84jR0J1cf9wq6lg'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def send_random_message():
    while True:
        messages = random.sample(msg_asupanmu_vip + msg_kontol_monster, 3)
        message_text = "\n".join(messages)
        for channel in CHANNELS:
            try:
                await bot.send_message(chat_id=channel, text=message_text, parse_mode=md.ParseMode.HTML)
            except Exception as e:
                print(f"Failed to send message to {channel}: {e}")
        await asyncio.sleep(60)  # Tunggu 1 menit

async def start_handler(message: types.Message):
    await message.answer("Bot ini aktif dan mengirim pesan setiap menit!")

# Daftarkan handler
dp.message_handlers.register(start_handler, Command("start"))

async def main():
    # Start the message sending task
    asyncio.create_task(send_random_message())
    # Start polling
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())

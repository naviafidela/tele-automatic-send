# bot.py
import random
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ParseMode
from asupanmu_vip import msg_asupanmu_vip
from kontol_monster import msg_kontol_monster
from channel import CHANNELS

API_TOKEN = '7520123514:AAG8JcQ6H0zjV_eTtK2V84jR0J1cf9wq6lg'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

async def send_random_message():
    while True:
        all_messages = msg_asupanmu_vip + msg_kontol_monster
        # Pastikan ada cukup link untuk dikirim ke semua channel
        if len(CHANNELS) > len(all_messages) // 2:
            print("Jumlah channel lebih banyak daripada kombinasi link yang tersedia.")
            return

        # Pilih 2 link acak untuk setiap channel
        random.shuffle(all_messages)  # Acak urutan link
        selected_links_per_channel = [all_messages[i:i + 2] for i in range(0, len(CHANNELS) * 2, 2)]

        for idx, channel in enumerate(CHANNELS):
            selected_links = selected_links_per_channel[idx]
            for link in selected_links:
                try:
                    await bot.send_message(chat_id=channel, text=link, parse_mode=ParseMode.HTML)
                    await asyncio.sleep(1)  # Tunggu sebentar antara pengiriman pesan
                except Exception as e:
                    print(f"Failed to send message to {channel}: {e}")

        await asyncio.sleep(7200)  # Tunggu 2 jam sebelum mengirim pesan lagi

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.reply("Bot ini aktif dan mengirim pesan setiap 2 jam!")

async def on_startup(dp):
    asyncio.create_task(send_random_message())

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

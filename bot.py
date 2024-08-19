# bot.py
import random
import asyncio
import sys
import time
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import ParseMode
from asupanmu_vip import msg_asupanmu_vip
from kontol_monster import msg_kontol_monster
from channel import CHANNELS

API_TOKEN = '7520123514:AAG8JcQ6H0zjV_eTtK2V84jR0J1cf9wq6lg'

# Menambahkan request_timeout untuk memperpanjang waktu tunggu
bot = Bot(token=API_TOKEN, request_timeout=60)
dp = Dispatcher(bot)

async def send_random_message():
    while True:
        all_messages = msg_asupanmu_vip + msg_kontol_monster

        if len(all_messages) < len(CHANNELS) * 2:
            print("Jumlah link tidak cukup untuk semua channel.")
            return

        random.shuffle(all_messages)
        selected_links_per_channel = [all_messages[i:i + 2] for i in range(0, len(CHANNELS) * 2, 2)]

        for idx, channel in enumerate(CHANNELS):
            selected_links = selected_links_per_channel[idx]
            message_text = "\n\n".join(selected_links)
            try:
                await bot.send_message(chat_id=channel, text=message_text, parse_mode=ParseMode.HTML)
            except Exception as e:
                print(f"Failed to send message to {channel}: {e}")

        # Countdown timer
        for i in range(120, 0, -1):
            sys.stdout.write(f"\rSend the next message in: {i} seconds")
            sys.stdout.flush()
            time.sleep(1)

            # Tambahkan pesan "Message berhasil terkirim" ketika timer mencapai 1 detik
            if i == 1:
                print("\nMessage berhasil terkirim")

        print()  # Pindah ke baris baru setelah countdown selesai

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.reply("Bot ini aktif dan mengirim pesan setiap menit!")

async def on_startup(dp):
    asyncio.create_task(send_random_message())

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

import random
import asyncio
import sys
import time
from aiogram import Bot, Dispatcher, types
from aiogram.types import parse_mode  # Correct import for parse_mode in Aiogram 3.x
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Application
from aiohttp import ClientTimeout
from message import message
from channel import CHANNELS

API_TOKEN = '7508753099:AAEDEAogPWH2Z13TmfJn0efWKImPLTI-7h8'

# Set timeout lebih lama
timeout = ClientTimeout(total=120)
bot = Bot(token=API_TOKEN, timeout=timeout)
dp = Dispatcher(bot, storage=MemoryStorage())

async def send_random_message():
    while True:
        all_messages = message

        if len(all_messages) < len(CHANNELS) * 2:
            print("Jumlah link tidak cukup untuk semua channel.")
            return

        random.shuffle(all_messages)
        selected_links_per_channel = [all_messages[i:i + 2] for i in range(0, len(CHANNELS) * 2, 2)]

        for idx, channel in enumerate(CHANNELS):
            selected_links = selected_links_per_channel[idx]
            message_text = "\n\n".join(selected_links)
            try:
                # Correct way to use parse_mode for HTML
                await bot.send_message(chat_id=channel, text=message_text, parse_mode=parse_mode.ParseMode.HTML)
            except Exception:
                # Sembunyikan error dan lanjutkan
                pass

        # Countdown timer
        for i in range(7200, 0, -1):
            sys.stdout.write(f"\r[HTTP/1.1 200 OK] - Send the next message in: {i} seconds")
            sys.stdout.flush()
            time.sleep(1)

            # Tambahkan pesan "Message berhasil terkirim" ketika timer mencapai 1 detik
            if i == 1:
                print("\n[HTTP/1.1 SUCCESS] - Message send successfully !")

        print()  # Pindah ke baris baru setelah countdown selesai

# Command handler for /start
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.reply("Bot ini aktif dan mengirim pesan setiap menit!")

async def on_startup(app: Application):
    asyncio.create_task(send_random_message())

# Create an Application instance
app = Application(bot=bot)

# Register the startup function
app.on_startup(on_startup)

# Start the bot
if __name__ == '__main__':
    import logging
    logging.basicConfig(level=logging.INFO)
    app.run_polling()

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram import F
from aiogram import Application
import asyncio
import random
import logging

# Import pesan dan channel dari file
from asupanmu_vip import msg_asupanmu_vip
from kontol_monster import msg_kontol_monster
from channel import CHANNELS

# Gabungkan pesan dari kedua file
messages = msg_asupanmu_vip + msg_kontol_monster

# Konfigurasi logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Konfigurasi bot
API_TOKEN = '7520123514:AAG8JcQ6H0zjV_eTtK2V84jR0J1cf9wq6lg'  # Token bot Anda

bot = Bot(token=API_TOKEN)
app = Application()

async def send_random_messages():
    while True:
        selected_message = random.choice(messages)
        for channel in CHANNELS:
            try:
                await bot.send_message(chat_id=channel, text=selected_message)
                logger.info(f"Pesan terkirim ke {channel}: {selected_message}")
            except Exception as e:
                logger.error(f"Terjadi kesalahan saat mengirim pesan ke {channel}: {e}")
        await asyncio.sleep(60)  # Tunggu 1 menit sebelum mengirim pesan lagi

@app.message(Command('start'))
async def start(message: types.Message):
    await message.reply("Halo! Bot ini aktif.")

async def main():
    # Jalankan tugas pengiriman pesan di latar belakang
    asyncio.create_task(send_random_messages())
    # Mulai polling
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())

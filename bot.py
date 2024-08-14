from telegram import Bot
from telegram.error import TelegramError
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import random
from asupanmu import messages_asupanmu  # Import pesan dari file asupanmu.py
from jav import messages_jav  # Import pesan dari file jav.py
from channel import CHANNELS  # Import daftar channel dari file channel.py

# Gabungkan pesan dari kedua file
messages = messages_asupanmu + messages_jav

# Konfigurasi
TOKEN = 'YOUR_BOT_TOKEN'  # Ganti dengan token bot Anda
NUM_MESSAGES_PER_RUN = 2  # Jumlah pesan yang dikirim setiap interval

# Konfigurasi logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Inisialisasi bot
bot = Bot(token=TOKEN)

def send_random_messages():
    try:
        # Pilih 2 pesan secara acak
        selected_messages = random.sample(messages, NUM_MESSAGES_PER_RUN)
        for chat_id in CHANNELS:
            for message in selected_messages:
                bot.send_message(chat_id=chat_id, text=message)
                logger.info(f"Pesan terkirim ke {chat_id}: {message}")
    except TelegramError as e:
        logger.error(f"Terjadi kesalahan saat mengirim pesan: {e}")

# Inisialisasi scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(send_random_messages, 'interval', minutes=5)  # Ubah interval menjadi 5 menit
scheduler.start()

# Jalankan scheduler
try:
    print("Scheduler dimulai. Tekan Ctrl+C untuk menghentikan.")
    while True:
        pass
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()
    print("Scheduler dihentikan.")

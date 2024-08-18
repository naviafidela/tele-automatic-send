import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
from telegram.error import TelegramError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import logging
import random
import subprocess
from channel import CHANNELS

from asupanmu_vip import msg_asupanmu_vip
from kontol_monster import msg_kontol_monster

# Gabungkan pesan dari kedua file
messages = msg_asupanmu_vip + msg_kontol_monster

# Konfigurasi
TOKEN = '7520123514:AAG8JcQ6H0zjV_eTtK2V84jR0J1cf9wq6lg'  # Ganti dengan token bot Anda
NUM_MESSAGES_PER_RUN = 3  # Jumlah pesan yang dikirim setiap interval

# Konfigurasi logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Inisialisasi bot
application = Application.builder().token(TOKEN).build()

# Inisialisasi scheduler dengan AsyncIOScheduler
scheduler = AsyncIOScheduler()

async def send_random_messages():
    try:
        # Pilih pesan secara acak
        selected_messages = random.sample(messages, NUM_MESSAGES_PER_RUN)
        for chat_id in CHANNELS:
            for message in selected_messages:
                await application.bot.send_message(chat_id=chat_id, text=message)
                logger.info(f"Pesan terkirim ke {chat_id}: {message}")
    except TelegramError as e:
        logger.error(f"Terjadi kesalahan saat mengirim pesan: {e}")

async def gitpull(update: Update, context: CallbackContext):
    try:
        # Menghentikan scheduler untuk melakukan git pull
        scheduler.pause()
        logger.info("Scheduler dihentikan sementara.")
        
        # Melakukan git pull
        result = subprocess.run(['git', 'pull'], capture_output=True, text=True)
        if result.returncode == 0:
            message = "Git pull berhasil!\n" + result.stdout
            logger.info(message)
        else:
            message = "Git pull gagal!\n" + result.stderr
            logger.error(message)

        # Restart scheduler setelah git pull
        scheduler.resume()
        await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    except Exception as e:
        logger.error(f"Terjadi kesalahan saat melakukan git pull: {e}")
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Terjadi kesalahan: {e}")

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text('Halo! Bot ini aktif.')

# Menambahkan handler untuk perintah
application.add_handler(CommandHandler('start', start))
application.add_handler(CommandHandler('gitpull', gitpull))

# Fungsi untuk menjalankan scheduler dan aplikasi bot
async def main():
    # Mulai scheduler
    scheduler.add_job(send_random_messages, trigger='interval', minutes=1)
    scheduler.start()

    # Mulai polling bot
    await application.run_polling()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        # Menjalankan main() di dalam event loop yang ada
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        # Tangani interupsi dari keyboard untuk berhenti dengan bersih
        pass
    finally:
        # Menutup scheduler dan event loop jika sudah ada
        if not loop.is_closed():
            scheduler.shutdown()
            loop.run_until_complete(application.shutdown())
            loop.close()

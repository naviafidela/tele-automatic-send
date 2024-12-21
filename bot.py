import os
import random
import datetime
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, Filters, CallbackContext
from message import message
from channel import CHANNELS

API_TOKEN = '7508753099:AAEDEAogPWH2Z13TmfJn0efWKImPLTI-7h8'

bot = Bot(token=API_TOKEN)
application = Application.builder().token(API_TOKEN).build()

# Variabel global untuk menyimpan waktu pengiriman berikutnya
next_send_time = None

async def send_random_message(context: CallbackContext):
    """Mengirim pesan secara acak dan menjadwalkan ulang dalam 2 jam."""
    global next_send_time

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
            await bot.send_message(chat_id=channel, text=message_text, parse_mode=ParseMode.HTML)
        except Exception as e:
            print(f"Error sending message to {channel}: {e}")

    # Jadwalkan ulang pengiriman pesan 2 jam dari sekarang
    next_send_time = datetime.datetime.now() + datetime.timedelta(seconds=7200)
    context.job_queue.run_once(send_random_message, 7200)  # Jadwalkan ulang
    print(f"Next message scheduled at: {next_send_time}")

async def check(update, context):
    """Handler untuk perintah /check"""
    global next_send_time

    if next_send_time is None:
        await update.message.reply_text("Belum ada pesan yang dijadwalkan.")
    else:
        time_remaining = (next_send_time - datetime.datetime.now()).total_seconds()
        if time_remaining > 0:
            await update.message.reply_text(f"Sisa waktu hingga pengiriman berikutnya: {int(time_remaining)} detik.")
        else:
            await update.message.reply_text("Pengiriman berikutnya akan segera dilakukan.")

async def reset_job(update, context):
    """Handler untuk perintah /reset"""
    global next_send_time
    context.job_queue.scheduler.remove_all_jobs()  # Hapus semua pekerjaan
    next_send_time = None  # Reset waktu pengiriman
    context.job_queue.run_once(send_random_message, 0)  # Jadwalkan ulang segera
    await update.message.reply_text("Job telah direset dan dijadwalkan ulang!")

async def stop_jobs(update, context):
    """Handler untuk perintah /stop"""
    global next_send_time
    context.job_queue.scheduler.remove_all_jobs()  # Hapus semua pekerjaan
    next_send_time = None  # Reset waktu pengiriman
    await update.message.reply_text("Semua jadwal telah dihentikan!")

async def git_pull(update, context):
    """Handler untuk perintah /gitpull"""
    global next_send_time
    # Hentikan semua pekerjaan
    context.job_queue.scheduler.remove_all_jobs()
    next_send_time = None

    # Beri tahu pengguna bahwa jadwal telah dihentikan
    await update.message.reply_text("Menghentikan semua jadwal...")

    # Jalankan git pull
    try:
        await update.message.reply_text("Menarik pembaruan dari repository...")
        os.system("git pull")  # Menjalankan perintah git pull
        await update.message.reply_text("Kode berhasil diperbarui. Memulai ulang proses...")
    except Exception as e:
        await update.message.reply_text(f"Terjadi kesalahan saat menarik pembaruan: {e}")
        return

    # Jalankan ulang pengiriman pesan otomatis
    context.job_queue.run_once(send_random_message, 0)
    await update.message.reply_text("Proses otomatis telah dimulai kembali!")



# Tambahkan handler untuk perintah /check
check_handler = CommandHandler('check', check)
application.add_handler(check_handler)

# Tambahkan handler untuk perintah /reset
reset_handler = CommandHandler('reset', reset_job)
application.add_handler(reset_handler)

# Tambahkan handler untuk perintah /stop
stop_handler = CommandHandler('stop', stop_jobs)
application.add_handler(stop_handler)

# Tambahkan handler untuk perintah /gitpull
gitpull_handler = CommandHandler('gitpull', git_pull)
application.add_handler(gitpull_handler)

if __name__ == '__main__':
    # Menambahkan JobQueue untuk menjalankan pengiriman pesan random
    application.job_queue.run_once(send_random_message, 0)
    application.run_polling()

import random
import time
import sys
import datetime
from telegram import Bot
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, CallbackContext
from message import message
from channel import CHANNELS

API_TOKEN = '7508753099:AAEDEAogPWH2Z13TmfJn0efWKImPLTI-7h8'

bot = Bot(token=API_TOKEN)
application = Application.builder().token(API_TOKEN).build()

# Variabel global untuk menyimpan waktu pengiriman berikutnya
next_send_time = None

async def send_random_message(context: CallbackContext):
    global next_send_time

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
                await bot.send_message(chat_id=channel, text=message_text, parse_mode=ParseMode.HTML)
            except Exception as e:
                print(f"Error sending message to {channel}: {e}")

        # Atur waktu pengiriman berikutnya (2 jam dari sekarang)
        next_send_time = datetime.datetime.now() + datetime.timedelta(seconds=7200)

        # Countdown timer
        for i in range(7200, 0, -1):
            sys.stdout.write(f"\r[HTTP/1.1 200 OK] - Send the next message in: {i} seconds")
            sys.stdout.flush()
            time.sleep(1)

            if i == 1:
                print("\n[HTTP/1.1 SUCCESS] - Message sent successfully!")

        print()  # Pindah ke baris baru setelah countdown selesai


async def check(update, context):
    global next_send_time

    if next_send_time is None:
        await update.message.reply_text("Belum ada pesan yang dijadwalkan.")
    else:
        time_remaining = (next_send_time - datetime.datetime.now()).total_seconds()
        if time_remaining > 0:
            await update.message.reply_text(f"Sisa waktu hingga pengiriman berikutnya: {int(time_remaining)} detik.")
        else:
            await update.message.reply_text("Pengiriman berikutnya akan segera dilakukan.")


# Tambahkan handler untuk perintah /check
check_handler = CommandHandler('check', check)
application.add_handler(check_handler)

if __name__ == '__main__':
    # Menambahkan JobQueue untuk menjalankan pengiriman pesan random
    application.job_queue.run_once(send_random_message, 0)
    application.run_polling()

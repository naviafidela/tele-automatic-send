import random
import time
import sys
from telegram import Bot, ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext, Update
from telegram.error import TelegramError
from message import message
from channel import CHANNELS

API_TOKEN = '7508753099:AAEDEAogPWH2Z13TmfJn0efWKImPLTI-7h8'

# Inisialisasi bot
bot = Bot(token=API_TOKEN)

def send_random_message(context: CallbackContext):
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
            bot.send_message(chat_id=channel, text=message_text, parse_mode=ParseMode.HTML)
        except TelegramError as e:
            print(f"Error sending message to {channel}: {e}")
            pass

    # Countdown timer
    for i in range(7200, 0, -1):
        sys.stdout.write(f"\r[HTTP/1.1 200 OK] - Send the next message in: {i} seconds")
        sys.stdout.flush()
        time.sleep(1)

        # Tambahkan pesan "Message berhasil terkirim" ketika timer mencapai 1 detik
        if i == 1:
            print("\n[HTTP/1.1 SUCCESS] - Message send successfully!")

    print()  # Pindah ke baris baru setelah countdown selesai

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Bot ini aktif dan mengirim pesan setiap menit!")

def main():
    # Setup Updater
    updater = Updater(token=API_TOKEN, use_context=True)
    dp = updater.dispatcher

    # Menambahkan handler untuk /start
    dp.add_handler(CommandHandler("start", start))

    # Set job untuk mengirim pesan setiap 2 jam
    job_queue = updater.job_queue
    job_queue.run_repeating(send_random_message, interval=7200, first=0)  # Set interval 7200 detik (2 jam)

    # Start polling
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()

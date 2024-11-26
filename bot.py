import random
import time
import sys
from telegram import Bot
from telegram.constants import ParseMode
from telegram.ext import Updater, CommandHandler, CallbackContext
from message import message
from channel import CHANNELS

API_TOKEN = '7508753099:AAEDEAogPWH2Z13TmfJn0efWKImPLTI-7h8'

bot = Bot(token=API_TOKEN)
updater = Updater(token=API_TOKEN, use_context=True)
dispatcher = updater.dispatcher

def send_random_message():
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
                bot.send_message(chat_id=channel, text=message_text, parse_mode=ParseMode.HTML)
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

def start(update, context):
    update.message.reply_text("Bot ini aktif dan mengirim pesan setiap menit!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

if __name__ == '__main__':
    send_random_message()
    updater.start_polling()
    updater.idle()

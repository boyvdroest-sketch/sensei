from flask import Flask, request, jsonify
import threading
import time
import os
from datetime import datetime
import json

app = Flask(__name__)

# SEO tracking endpoints
@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>USA Accommodation Bot - Hotel Deals & Discounts</title>
        <meta name="description" content="Find best hotel deals, vacation rentals, and accommodation discounts across USA. New York, LA, Chicago, Miami hotel promotions.">
        <meta name="keywords" content="usa hotels, accommodation deals, vacation rentals, hotel discounts, new york hotels, la vacation, chicago accommodation">
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
            .header { background: #007cba; color: white; padding: 20px; border-radius: 10px; }
            .features { margin: 20px 0; }
            .feature { background: #f8f9fa; padding: 15px; margin: 10px 0; border-radius: 5px; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🏨 USA Accommodation Deals Bot</h1>
            <p>Find the best hotel discounts and vacation rental deals across United States</p>
        </div>
        
        <div class="features">
            <h2>🌟 Features</h2>
            <div class="feature">
                <h3>🏙️ City-Specific Deals</h3>
                <p>New York, Los Angeles, Chicago, Miami hotel promotions</p>
            </div>
            <div class="feature">
                <h3>💰 Exclusive Discounts</h3>
                <p>50% off deals, last-minute offers, luxury stays at budget prices</p>
            </div>
            <div class="feature">
                <h3>🔍 Smart Search</h3>
                <p>Find perfect accommodation based on your preferences and dates</p>
            </div>
        </div>
        
        <div>
            <h2>📱 Get Started</h2>
            <p>Start our Telegram bot to access exclusive accommodation deals:</p>
            <p><strong>Bot Status:</strong> <span style="color: green;">✅ Running</span></p>
            <p><em>Best for: Hotel deals, vacation rentals, business stays, family accommodation USA</em></p>
        </div>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "accommodation-bot",
        "timestamp": datetime.now().isoformat(),
        "keywords": ["usa hotels", "accommodation deals", "hotel discounts", "vacation rentals"]
    })

@app.route('/sitemap')
def sitemap():
    return jsonify({
        "pages": [
            {"url": "/", "title": "USA Accommodation Bot", "description": "Hotel deals and discounts"},
            {"url": "/health", "title": "Health Check", "description": "Service status"},
            {"url": "/deals", "title": "Current Deals", "description": "Latest hotel promotions"}
        ],
        "keywords": [
            "usa accommodation", "hotel deals", "vacation rentals", 
            "new york hotels", "los angeles stays", "chicago lodging"
        ]
    })

@app.route('/deals')
def deals_api():
    return jsonify({
        "featured_deals": [
            {
                "city": "New York",
                "deal": "50% Off Manhattan Hotels",
                "valid_until": "2024-12-31",
                "keywords": ["nyc hotels", "times square accommodation", "manhattan stays"]
            },
            {
                "city": "Los Angeles", 
                "deal": "30% Discount LA Vacation Rentals",
                "valid_until": "2024-11-30",
                "keywords": ["la vacation", "hollywood hotels", "california stays"]
            }
        ]
    })

def run_bot():
    try:
        from bot import bot
        print("🤖 Starting SEO Telegram Bot...")
        bot.infinity_polling(timeout=60, long_polling_timeout=60)
    except Exception as e:
        print(f"❌ Bot error: {e}")
        print("🔄 Restarting bot in 30 seconds...")
        time.sleep(30)
        run_bot()

if __name__ == '__main__':
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    print("🚀 Starting Flask server with SEO features...")
    app.run(host='0.0.0.0', port=5000, debug=False)

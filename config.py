# config.py
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Telegram API Credentials
TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID', '')
TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH', '')

# Telegram Bot Credentials
BOT_TOKEN = os.getenv('BOT_TOKEN', '')
CHAT_ID = os.getenv('CHAT_ID', '')

# Public settings (bisa tetap di file ini)
TELEGRAM_CHANNELS = ['BinanceKillers', 'wolfxsignals']
X_ACCOUNTS = ['BinanceKillers', 'wolfxsignals', 'signal0x']

# Analysis settings
CONFIDENCE_THRESHOLD = 70
CHECK_INTERVAL = 1800

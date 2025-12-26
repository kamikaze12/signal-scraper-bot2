# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram API Credentials
TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID', '')
TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH', '')

# Telegram Bot Credentials
BOT_TOKEN = os.getenv('BOT_TOKEN', '')
CHAT_ID = os.getenv('CHAT_ID', '')

# Channel/Account settings untuk setiap market
TELEGRAM_CHANNELS = {
    'crypto': ['BinanceKillers', 'wolfxsignals'],
    'forex': ['forex_signals', 'forex_trading_signals'],  # Channel forex
    'saham_indonesia': ['idx_signals', 'saham_indonesia'],  # Channel saham Indonesia
    'saham_us': ['wallstreet_signals', 'us_stocks'],  # Channel saham US
    'emas': ['gold_signals', 'preciousmetals']  # Channel emas
}

X_ACCOUNTS = {
    'crypto': ['BinanceKillers', 'wolfxsignals', 'signal0x'],
    'forex': ['ForexSignals', 'DailyFX'],  # Akun forex
    'saham_indonesia': ['idxupdate', 'BisnisID'],  # Akun saham Indonesia
    'saham_us': ['Stocktwits', 'USStocksNews'],  # Akun saham US
    'emas': ['GoldPrice', 'KitcoNews']  # Akun emas
}

# Analysis settings
CONFIDENCE_THRESHOLD = 70
CHECK_INTERVAL = 1800

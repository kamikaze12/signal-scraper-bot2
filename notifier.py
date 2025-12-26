# notifier.py
import requests
from config import BOT_TOKEN, CHAT_ID

def send_to_telegram(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        params = {
            'chat_id': CHAT_ID, 
            'text': message,
            'parse_mode': 'HTML'
        }
        response = requests.get(url, params=params)
        return response.json()
    except Exception as e:
        print(f"Error sending to Telegram: {e}")
        return None

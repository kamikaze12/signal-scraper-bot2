# scraper.py
import asyncio
from telethon import TelegramClient
import requests
from bs4 import BeautifulSoup
from config import TELEGRAM_API_ID, TELEGRAM_API_HASH  # Import dari config kalau perlu

async def scrape_telegram_channels(channels, limit=5):
    client = TelegramClient('session', TELEGRAM_API_ID, TELEGRAM_API_HASH)
    await client.start()
    signals = {}
    for channel in channels:
        messages = []
        async for message in client.iter_messages(channel, limit=limit):
            if message.text and any(word in message.text.upper() for word in ['LONG', 'SHORT', 'TP', 'SL']):
                messages.append(message.text)
        if messages:
            signals[channel] = messages
    return signals

def scrape_x_accounts(accounts, limit=5):
    signals = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }  # Fake user-agent biar gak langsung block
    for account in accounts:
        url = f"https://twitter.com/{account}"  # Ganti ke nitter atau proxy kalau blocked (nitter.net/{account})
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                tweets = []
                # Cari tweet elements – X ubah class sering, ini contoh umum (data-testid='tweet' atau css-901oao)
                for tweet_div in soup.find_all('div', attrs={'data-testid': 'tweet'}):
                    text_elem = tweet_div.find('div', attrs={'data-testid': 'tweetText'})
                    if text_elem:
                        text = text_elem.get_text(strip=True)
                        if any(word in text.upper() for word in ['LONG', 'SHORT', 'TP', 'SL', 'BUY', 'SELL']):
                            tweets.append(text)
                    if len(tweets) >= limit:
                        break
                if tweets:
                    signals[account] = tweets
            else:
                print(f"Error scraping @{account}: Status {response.status_code}")
        except Exception as e:
            print(f"Error scraping @{account}: {e}")
    return signals

import asyncio
from telethon import TelegramClient
import requests
from bs4 import BeautifulSoup

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

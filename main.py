# main.py
import asyncio
import schedule
import time
from scraper import scrape_telegram_channels, scrape_x_accounts
from analyzer import calculate_confidence
from notifier import send_to_telegram
from config import TELEGRAM_CHANNELS, X_ACCOUNTS, CONFIDENCE_THRESHOLD, CHECK_INTERVAL

async def check_signals():
    print("Checking for new signals across all markets...")
    
    all_market_signals = {}
    
    # Scrape all markets
    for market in TELEGRAM_CHANNELS.keys():
        print(f"Scraping {market}...")
        
        # Scrape Telegram
        tg_channels = TELEGRAM_CHANNELS.get(market, [])
        if tg_channels:
            tg_signals = await scrape_telegram_channels(tg_channels)
            for channel, signals in tg_signals.items():
                for sig in signals:
                    conf = calculate_confidence(sig, market)
                    if conf > CONFIDENCE_THRESHOLD:
                        message = f"📈 {market.upper()} Signal from @{channel}:\n{sig[:200]}...\nConfidence: {conf}%"
                        send_to_telegram(message)
                        print(f"Sent {market} signal: {message[:50]}...")
        
        # Scrape X (Twitter)
        x_accounts = X_ACCOUNTS.get(market, [])
        if x_accounts:
            x_signals = scrape_x_accounts(x_accounts)
            for account, signals in x_signals.items():
                for sig in signals:
                    conf = calculate_confidence(sig, market)
                    if conf > CONFIDENCE_THRESHOLD:
                        message = f"📈 {market.upper()} Signal from @{account}:\n{sig[:200]}...\nConfidence: {conf}%"
                        send_to_telegram(message)
                        print(f"Sent {market} signal: {message[:50]}...")

def run_scheduler():
    schedule.every(CHECK_INTERVAL).seconds.do(lambda: asyncio.run(check_signals()))
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    print("Starting multi-market signal analyzer...")
    print("Markets: Crypto, Forex, Saham Indonesia, Saham US, Emas")
    asyncio.run(check_signals())  # Run once first
    run_scheduler()

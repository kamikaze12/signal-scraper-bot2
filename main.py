import asyncio
import schedule
import time
from scraper import scrape_telegram_channels, scrape_x_accounts
from analyzer import calculate_confidence
from notifier import send_to_telegram
from config import TELEGRAM_CHANNELS, X_ACCOUNTS, CONFIDENCE_THRESHOLD, CHECK_INTERVAL

async def check_signals():
    print("Checking for new signals...")
    tg_signals = await scrape_telegram_channels(TELEGRAM_CHANNELS)
    x_signals = scrape_x_accounts(X_ACCOUNTS)
    
    all_signals = {**tg_signals, **x_signals}
    
    for source, sigs in all_signals.items():
        for sig in sigs:
            conf = calculate_confidence(sig)
            if conf > CONFIDENCE_THRESHOLD:
                message = f"New Signal from @{source}:\n{sig[:200]}...\nConfidence: {conf}%"
                send_to_telegram(message)
                print(f"Sent: {message}")

def run_scheduler():
    schedule.every(CHECK_INTERVAL).seconds.do(lambda: asyncio.run(check_signals()))
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    asyncio.run(check_signals())  # Run sekali dulu
    run_scheduler()  # Jalankan scheduler

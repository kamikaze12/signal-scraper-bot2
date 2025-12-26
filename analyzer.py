# analyzer.py
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
import re
nltk.download('vader_lexicon')
from transformers import pipeline

def calculate_confidence(signal_text, market_type='crypto'):
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(signal_text)['compound']
    blob = TextBlob(signal_text)
    subjectivity = blob.sentiment.subjectivity
    
    classifier = pipeline('sentiment-analysis')
    result = classifier(signal_text)[0]
    label, score = result['label'], result['score']
    
    # Base confidence
    conf = (sentiment + 1) * 50
    
    # Market-specific keywords
    market_keywords = {
        'crypto': ['TP', 'SL', 'LONG', 'SHORT', 'BUY', 'SELL', 'BTC', 'ETH', 'BNB', 'USDT'],
        'forex': ['TP', 'SL', 'LONG', 'SHORT', 'BUY', 'SELL', 'USD', 'EUR', 'JPY', 'GBP', 'PIP'],
        'saham_indonesia': ['BELI', 'JUAL', 'TARGET', 'CUT LOSS', 'BBCA', 'BBRI', 'BMRI', 'IDX'],
        'saham_us': ['BUY', 'SELL', 'TARGET', 'STOP LOSS', 'NASDAQ', 'NYSE', 'SPY', 'QQQ'],
        'emas': ['BUY', 'SELL', 'TARGET', 'STOP LOSS', 'GOLD', 'XAU', 'OUNCE', 'GRAM']
    }
    
    # Check for market-specific patterns
    keywords = market_keywords.get(market_type, [])
    keyword_count = sum(1 for keyword in keywords if keyword in signal_text.upper())
    conf += keyword_count * 5
    
    # Check for price patterns (numbers with $, Rp, etc)
    price_patterns = [
        r'\$\d+(\.\d+)?',  # USD
        r'Rp\s?\d+(\.\d+)*',  # Rupiah
        r'\d+(\.\d+)?\s?\%',  # Percentage
        r'\d+(\.\d+)?\s?point[s]?',  # Points
        r'\d+(\.\d+)?\s?pip[s]?'  # Pips
    ]
    
    pattern_count = sum(1 for pattern in price_patterns if re.search(pattern, signal_text, re.IGNORECASE))
    conf += pattern_count * 3
    
    # Timeframe indicators
    timeframe_keywords = ['H1', 'H4', 'D1', 'W1', 'M1', 'DAILY', 'WEEKLY', 'MONTHLY']
    timeframe_count = sum(1 for tf in timeframe_keywords if tf in signal_text.upper())
    conf += timeframe_count * 2
    
    # Sentiment adjustment
    if label == 'POSITIVE':
        conf += score * 15
    
    # Subjectivity penalty
    conf -= subjectivity * 10
    
    return max(0, min(100, conf))

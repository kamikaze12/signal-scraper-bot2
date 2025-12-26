from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')
from transformers import pipeline

def calculate_confidence(signal_text):
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(signal_text)['compound']
    blob = TextBlob(signal_text)
    subjectivity = blob.sentiment.subjectivity
    
    classifier = pipeline('sentiment-analysis')
    result = classifier(signal_text)[0]
    label, score = result['label'], result['score']
    
    conf = (sentiment + 1) * 50
    if 'TP' in signal_text.upper() and 'SL' in signal_text.upper():
        conf += 20
    if label == 'POSITIVE':
        conf += score * 20
    conf -= subjectivity * 10
    return max(0, min(100, conf))

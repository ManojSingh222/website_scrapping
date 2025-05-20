from GoogleNews import GoogleNews
from textblob import TextBlob

def get_headlines(query):
    googlenews = GoogleNews(lang='en')
    googlenews.search(query)
    results = googlenews.results()
    return [item['title'] for item in results]

def analyze_sentiments(headlines):
    results = []
    for text in headlines:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        if polarity > 0:
            sentiment = "Positive"
        elif polarity < 0:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        results.append((text, sentiment))
    return results

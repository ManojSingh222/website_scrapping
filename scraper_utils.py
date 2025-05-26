from GoogleNews import GoogleNews
from textblob import TextBlob

def get_headlines(query):
    googlenews = GoogleNews(lang='en')
    googlenews.search(query)
    results = googlenews.results()
    return [(item['title'], item['media'], item['link'], item['date']) for item in results]

def analyze_sentiments(headline_tuples):
    results = []
    for title, source, link, date in headline_tuples:
        blob = TextBlob(title)
        polarity = blob.sentiment.polarity
        if polarity > 0:
            sentiment = "Positive"
        elif polarity < 0:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        results.append((title, sentiment, polarity, source, link, date))
    return results

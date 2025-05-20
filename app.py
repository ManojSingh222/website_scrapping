
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
from scraper_utils import get_headlines, analyze_sentiments

st.set_page_config(page_title="News Sentiment Scraper")
st.title("📰 Real-Time News Scraper with Sentiment Analysis")

query = st.text_input("Enter a keyword to search for news:")

if st.button("Scrape News"):
    with st.spinner("Scraping and analyzing..."):
        headlines = get_headlines(query)
        if not headlines:
            st.warning("No headlines found.")
        else:
            results = analyze_sentiments(headlines)
            df = pd.DataFrame(results, columns=["Headline", "Sentiment"])
            st.dataframe(df)

            # Chart
            sentiment_counts = df['Sentiment'].value_counts()
            fig, ax = plt.subplots()
            sentiment_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax, startangle=90)
            ax.set_ylabel("")
            st.pyplot(fig)

            # CSV Download
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", csv, "news_sentiment.csv", "text/csv", key='download-csv')

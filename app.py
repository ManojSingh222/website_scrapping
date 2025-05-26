import streamlit as st
import time

import pandas as pd
import matplotlib.pyplot as plt
from scraper_utils import get_headlines, analyze_sentiments
from streamlit_lottie import st_lottie
import requests

def load_lottie_url(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

# Set up page
st.set_page_config(
    page_title="News Sentiment Scraper",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load animation
lottie_news = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_49rdyysj.json")
st_lottie(lottie_news, height=200, key="news")

# Title and description
st.markdown("## 🔍 Real-Time News Sentiment Analyzer")
st.markdown("Get the latest news headlines with sentiment analysis, visualized and downloadable.")

# Input area
col1, col2 = st.columns([3, 1])
query = col1.text_input("Enter a keyword to search for news", placeholder="e.g., AI, Tesla, Economy")
chart_type = col2.selectbox("Chart type", ["Pie", "Bar"])

# Initialize history
if 'history' not in st.session_state:
    st.session_state.history = []

# Sidebar
st.sidebar.markdown("## 🧭 Navigation")
st.sidebar.markdown("### Recent Searches")
for past_query in st.session_state.history[-5:]:
    st.sidebar.write(f"🔎 {past_query}")
st.sidebar.markdown("---")
st.sidebar.markdown("Built with ❤️ using Streamlit")

# Button to scrape
if st.button("Scrape News"):
    st.session_state.history.append(query)
    with st.spinner("Fetching news and analyzing sentiment..."):
        headlines = get_headlines(query)
        time.sleep(1.5)  # simulate delay
        if not headlines:
            st.warning("No headlines found.")
        else:
            results = analyze_sentiments(headlines)
            df = pd.DataFrame(results, columns=["Headline", "Sentiment", "Polarity", "Source", "Link", "Date"])
            df['Sentiment Icon'] = df['Sentiment'].map({
                'Positive': '🟢',
                'Negative': '🔴',
                'Neutral': '🟡'
            })

            # Display enhanced table
            display_df = df[["Sentiment Icon", "Sentiment", "Headline", "Source", "Date", "Link"]]
            st.dataframe(display_df)

            # Visualize
            sentiment_counts = df['Sentiment'].value_counts()
            fig, ax = plt.subplots()
            if chart_type == "Pie":
                sentiment_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax, startangle=90)
                ax.set_ylabel("")
            else:
                sentiment_counts.plot(kind='bar', ax=ax, color=['#2ecc71', '#e74c3c', '#f1c40f'])
                ax.set_ylabel("Count")
            st.pyplot(fig)

            # Download CSV
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", csv, "news_sentiment.csv", "text/csv", key='download-csv')

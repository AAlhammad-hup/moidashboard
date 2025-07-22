
import streamlit as st
import snscrape.modules.twitter as sntwitter
import pandas as pd
from transformers import pipeline
from googletrans import Translator
import subprocess
import json

# Future: for Telegram
# from telethon.sync import TelegramClient
# from telethon.tl.functions.messages import GetHistoryRequest

# Future: for Google Reviews
# from googleplaces import GooglePlaces, types, lang

# Sentiment model setup
sentiment_model = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
translator = Translator()

def simplify_sentiment(label):
    if "1" in label or "2" in label:
        return "Negative"
    elif "4" in label or "5" in label:
        return "Positive"
    else:
        return "Neutral"

def translate_text(text):
    try:
        return translator.translate(text, dest="en").text
    except:
        return text

def analyze_sentiment(text):
    try:
        translated = translate_text(text)
        result = sentiment_model(translated)[0]["label"]
        return simplify_sentiment(result)
    except:
        return "Error"

def collect_from_twitter(query, limit):
    tweets = []
    for tweet in sntwitter.TwitterSearchScraper(query + " lang:ar").get_items():
        if len(tweets) >= limit:
            break
        tweets.append([tweet.date, tweet.user.username, tweet.content])
    return pd.DataFrame(tweets, columns=["Date", "User", "Text"])

def collect_from_youtube(video_url, limit):
    output = subprocess.run([
        "youtube-comment-downloader",
        "--url", video_url,
        "--output", "comments.json",
        "--limit", str(limit)
    ], capture_output=True, text=True)

    try:
        with open("comments.json", "r", encoding="utf-8") as f:
            lines = f.readlines()
        comments = [json.loads(line)["text"] for line in lines]
        return pd.DataFrame(comments, columns=["Text"])
    except:
        return pd.DataFrame(columns=["Text"])

# Placeholder functions for future extension
def collect_from_telegram(channel_username, limit):
    # To be implemented with Telethon and Telegram API
    return pd.DataFrame(columns=["Text"])

def collect_from_google_reviews(place_id, api_key):
    # To be implemented using Google Places API
    return pd.DataFrame(columns=["Text"])

# Streamlit UI
st.set_page_config(page_title="Public Sentiment Dashboard", layout="wide")
st.title("📊 Public Sentiment Analysis Dashboard for Civil Defense Services")

platform = st.selectbox("Select a platform", ["Twitter", "YouTube", "Google Reviews", "Telegram"])
input_text = st.text_input("Enter search keyword (Twitter), video URL (YouTube), place ID (Google), or channel username (Telegram)")
limit = st.slider("Number of posts/comments to analyze", 10, 200, 50)
api_key = st.text_input("🔑 Google API Key (required for Google Reviews)", type="password") if platform == "Google Reviews" else None

if st.button("Start Analysis"):
    if platform == "Twitter":
        st.info("Collecting tweets...")
        df = collect_from_twitter(input_text, limit)
    elif platform == "YouTube":
        st.info("Collecting YouTube comments...")
        df = collect_from_youtube(input_text, limit)
    elif platform == "Telegram":
        st.info("Telegram collection is under development...")
        df = collect_from_telegram(input_text, limit)
    elif platform == "Google Reviews":
        st.info("Google Reviews collection is under development...")
        df = collect_from_google_reviews(input_text, api_key)

    if not df.empty:
        st.info("Analyzing sentiment...")
        df["Sentiment"] = df["Text"].apply(analyze_sentiment)

        st.subheader("📊 Sentiment Distribution")
        st.bar_chart(df["Sentiment"].value_counts())

        st.subheader("📋 Detailed Data")
        st.dataframe(df)
    else:
        st.warning("No results found or feature not implemented yet.")

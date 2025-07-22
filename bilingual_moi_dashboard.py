import streamlit as st
import snscrape.modules.twitter as sntwitter
import pandas as pd
from transformers import pipeline
from googletrans import Translator
import subprocess
import json

# إعداد النموذج والمترجم
sentiment_model = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")
translator = Translator()

# لغة الواجهة
language = st.sidebar.selectbox("🌐 اختر اللغة | Select Language", ["العربية", "English"])
is_arabic = language == "العربية"

# عناوين القطاعات التي سيتم تحليل التغريدات عنها
MOI_SECTORS = [
    "الدفاع المدني",
    "المديرية العامة للأمن العام",
    "المديرية العامة لمكافحة المخدرات",
    "المديرية العامة للجوازات",
    "المديرية العامة للسجون",
    "المديرية العامة لحرس الحدود",
    "القوات الخاصة للأمن البيئي",
    "القوات الخاصة للأمن والحماية",
    "كلية الملك فهد الأمنية",
    "وكالة وزارة الداخلية للأحوال المدنية",
    "مركز المعلومات الوطني",
    "المركز الوطني للعمليات الأمنية الموحدة",
    "مركز أبحاث مكافحة الجريمة",
    "قوات أمن المنشآت",
    "الإدارة العامة للخدمات الطبية",
    "الإدارة العامة لأندية منسوبي وزارة الداخلية",
    "الإدارة العامة للمجاهدين",
    "ديوان وزارة الداخلية"
]

# عرض عنوان الواجهة
st.title("📊 لوحة تحليل الرأي العام لقطاعات وزارة الداخلية" if is_arabic else "📊 Public Sentiment Dashboard for MOI Sectors")

# تحميل وتحليل التغريدات
results = []

for sector in MOI_SECTORS:
    query = f"{sector} lang:ar"
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(query).get_items()):
        if i > 20:
            break
        tweets.append(tweet.content)

    for text in tweets:
        try:
            translated = translator.translate(text, dest="en").text
            sentiment = sentiment_model(translated)[0]
            results.append({
                "القطاع" if is_arabic else "Sector": sector,
                "النص الأصلي" if is_arabic else "Original Text": text,
                "الترجمة" if is_arabic else "Translation": translated,
                "الرأي" if is_arabic else "Sentiment": sentiment["label"],
                "درجة الثقة" if is_arabic else "Confidence": round(sentiment["score"] * 100, 2)
            })
        except Exception as e:
            continue

# عرض النتائج
if results:
    df = pd.DataFrame(results)
    st.dataframe(df)
    sentiment_summary = df.groupby("القطاع" if is_arabic else "Sector")["الرأي" if is_arabic else "Sentiment"].value_counts().unstack().fillna(0)
    st.bar_chart(sentiment_summary)
else:
    st.info("لم يتم العثور على نتائج." if is_arabic else "No results found.")

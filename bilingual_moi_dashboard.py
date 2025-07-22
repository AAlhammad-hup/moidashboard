
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

# قائمة القطاعات
sectors = [
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

# ترجمة الواجهة
def _(ar, en):
    return ar if is_arabic else en

# تحليل المشاعر
def simplify_sentiment(label):
    if "1" in label or "2" in label:
        return _("سلبي", "Negative")
    elif "4" in label or "5" in label:
        return _("إيجابي", "Positive")
    else:
        return _("محايد", "Neutral")

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
        return _("خطأ", "Error")

# جمع بيانات تويتر
def collect_from_twitter(query, limit):
    tweets = []
    for tweet in sntwitter.TwitterSearchScraper(query + " lang:ar").get_items():
        if len(tweets) >= limit:
            break
        tweets.append([tweet.date, tweet.user.username, tweet.content])
    return pd.DataFrame(tweets, columns=[_("التاريخ", "Date"), _("المستخدم", "User"), _("النص", "Text")])

# جمع تعليقات يوتيوب
def collect_from_youtube(video_url, limit):
    subprocess.run([
        "youtube-comment-downloader",
        "--url", video_url,
        "--output", "comments.json",
        "--limit", str(limit)
    ], capture_output=True, text=True)
    try:
        with open("comments.json", "r", encoding="utf-8") as f:
            lines = f.readlines()
        comments = [json.loads(line)["text"] for line in lines]
        return pd.DataFrame(comments, columns=[_("النص", "Text")])
    except:
        return pd.DataFrame(columns=[_("النص", "Text")])

# واجهة المستخدم
st.set_page_config(page_title=_("لوحة تحليل الرأي العام", "Public Sentiment Dashboard"), layout="wide")
st.title(_("📊 لوحة تحليل الرأي العام لقطاعات وزارة الداخلية", "📊 Sentiment Analysis Dashboard for MOI Sectors"))

sector = st.selectbox(_("اختر القطاع", "Select Sector"), sectors)
platform = st.selectbox(_("اختر المنصة", "Select Platform"), ["Twitter", "YouTube", "Google Reviews", "Telegram"])
custom_input = st.text_input(_("🔍 أدخل كلمة بحث أو رابط فيديو", "🔍 Enter search keyword or video URL"))
limit = st.slider(_("عدد النتائج", "Number of results"), 10, 200, 50)
api_key = st.text_input("🔑 Google API Key", type="password") if platform == "Google Reviews" else None

if st.button(_("ابدأ التحليل", "Start Analysis")):
    query = custom_input if custom_input else sector

    if platform == "Twitter":
        st.info(_("📡 يتم جمع التغريدات...", "Collecting tweets..."))
        df = collect_from_twitter(query, limit)
    elif platform == "YouTube":
        st.info(_("📡 يتم جمع تعليقات يوتيوب...", "Collecting YouTube comments..."))
        df = collect_from_youtube(query, limit)
    elif platform == "Telegram":
        st.warning(_("🚧 دعم تيليجرام لم يُفعل بعد.", "🚧 Telegram support not yet implemented."))
        df = pd.DataFrame(columns=[_("النص", "Text")])
    elif platform == "Google Reviews":
        st.warning(_("🚧 دعم Google لم يُفعل بعد.", "🚧 Google Reviews support not yet implemented."))
        df = pd.DataFrame(columns=[_("النص", "Text")])
    else:
        df = pd.DataFrame(columns=[_("النص", "Text")])

    if not df.empty:
        st.info(_("🤖 يتم تحليل المشاعر...", "🤖 Analyzing sentiment..."))
        df[_("المشاعر", "Sentiment")] = df[_("النص", "Text")].apply(analyze_sentiment)

        st.subheader(_("📈 توزيع المشاعر", "📈 Sentiment Distribution"))
        st.bar_chart(df[_("المشاعر", "Sentiment")].value_counts())

        st.subheader(_("📋 التفاصيل", "📋 Detailed Data"))
        st.dataframe(df)
    else:
        st.warning(_("⚠️ لم يتم العثور على نتائج", "⚠️ No results found."))

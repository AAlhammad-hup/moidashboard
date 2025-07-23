import streamlit as st
import snscrape.modules.twitter as sntwitter
import pandas as pd
from transformers import pipeline
from deep_translator import GoogleTranslator

# إعداد نموذج تحليل المشاعر والمترجم
sentiment_model = pipeline("sentiment-analysis", model="nlptown/bert-base-multilingual-uncased-sentiment")

def translate_text(text, target_language):
    return GoogleTranslator(source='auto', target=target_language).translate(text)

# اختيار اللغة
language = st.sidebar.selectbox("🌐 اختر اللغة | Select Language", ["العربية", "English"])
is_arabic = language == "العربية"

# واجهة العنوان
st.title("لوحة الرصد الأمني" if is_arabic else "Security Sentiment Dashboard")
st.markdown("تحليل رأي الجمهور حول خدمات وزارة الداخلية" if is_arabic else "Analyzing public opinion on Ministry of Interior services")

# قائمة القطاعات
sectors_ar = [
    "الدفاع المدني", "الأمن العام", "مكافحة المخدرات", "الجوازات", "السجون", "حرس الحدود", 
    "الأمن البيئي", "قوات الأمن الخاصة", "كلية الملك فهد الأمنية", "الأحوال المدنية", 
    "مركز المعلومات الوطني", "مركز العمليات الموحدة", "مركز أبحاث الجريمة",
    "قوات أمن المنشآت", "الخدمات الطبية", "أندية الوزارة", "الإدارة العامة للمجاهدين", "ديوان الوزارة"
]
sectors_en = [
    "Civil Defense", "Public Security", "Narcotics Control", "Passports", "Prisons", "Border Guards", 
    "Environmental Security", "Special Security Forces", "King Fahd Security College", "Civil Affairs", 
    "National Information Center", "Unified Operations Center", "Crime Research Center", 
    "Facilities Security Forces", "Medical Services", "Ministry Clubs", "Mujahideen Administration", "MOI Diwan"
]

sectors = sectors_ar if is_arabic else sectors_en

# اختيار القطاع وعدد التغريدات
selected_sector = st.selectbox("اختر القطاع الأمني" if is_arabic else "Select Security Sector", sectors)
limit = st.slider("عدد التغريدات" if is_arabic else "Number of tweets", 10, 200, 50)

# استخدام اسم القطاع كاستعلام تلقائي
search_term = selected_sector

# تنفيذ التحليل مباشرة بعد اختيار القطاع
if selected_sector:
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(search_term).get_items()):
        if i >= limit:
            break
        tweets.append(tweet.content)

    df = pd.DataFrame(tweets, columns=["Text"])

    if is_arabic:
        df["Translated"] = df["Text"].apply(lambda x: translate_text(x, "en"))
        df["Sentiment"] = df["Translated"].apply(lambda x: sentiment_model(x)[0]["label"])
    else:
        df["Sentiment"] = df["Text"].apply(lambda x: sentiment_model(x)[0]["label"])

    st.subheader("النتائج" if is_arabic else "Results")
    st.write(df)

    st.subheader("التحليل العام" if is_arabic else "Overall Analysis")
    st.bar_chart(df["Sentiment"].value_counts())

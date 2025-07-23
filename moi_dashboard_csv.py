import streamlit as st
import pandas as pd

# اختيار اللغة
language = st.sidebar.selectbox("🌐 اختر اللغة | Select Language", ["العربية", "English"])
is_arabic = language == "العربية"

# عنوان الصفحة
st.title("لوحة الرصد الأمني" if is_arabic else "Security Sentiment Dashboard")
st.markdown("تحليل رأي الجمهور حول خدمات وزارة الداخلية" if is_arabic else "Analyzing public opinion on Ministry of Interior services")

# قراءة البيانات من ملف CSV
@st.cache_data
def load_data():
    return pd.read_csv("moi_sentiment_data.csv")

df = load_data()

# استخراج قائمة القطاعات من البيانات
sectors = sorted(df["Sector"].unique())

# اختيار القطاع
selected_sector = st.selectbox("اختر القطاع الأمني" if is_arabic else "Select Security Sector", sectors)

# تصفية البيانات حسب القطاع المختار
filtered_df = df[df["Sector"] == selected_sector]

# عرض التغريدات
st.subheader("النتائج" if is_arabic else "Results")

# ترجمة قيم المشاعر إذا كانت اللغة العربية
if is_arabic:
    sentiment_map = {
        "Positive": "إيجابي",
        "Neutral": "محايد",
        "Negative": "سلبي"
    }
    filtered_df["Sentiment"] = filtered_df["Sentiment"].map(sentiment_map)

st.write(filtered_df[["Text", "Sentiment"]])

# عرض الرسم البياني لتحليل المشاعر
st.subheader("التحليل العام" if is_arabic else "Overall Analysis")
st.bar_chart(filtered_df["Sentiment"].value_counts())

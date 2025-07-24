import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
from transformers import pipeline

# ----------------------------
# تحميل البيانات
# ----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("moi_sentiment_data.csv")

df = load_data()

# ----------------------------
# اختيار اللغة
# ----------------------------
language = st.sidebar.selectbox("🌐 اختر اللغة | Select Language", ["العربية", "English"])
is_arabic = language == "العربية"

# ----------------------------
# ترجمات القطاعات
# ----------------------------
sector_translation = {
    "الدفاع المدني": "Civil Defense",
    "الأمن العام": "Public Security",
    "الجوازات": "Passports",
    "المرور": "Traffic",
    "السجون": "Prisons",
    "مكافحة المخدرات": "Narcotics Control",
    "حرس الحدود": "Border Guards",
    "الأحوال المدنية": "Civil Affairs",
    "الأمن البيئي": "Environmental Security",
    "قوات أمن المنشآت": "Facilities Security Forces",
    "الخدمات الطبية": "Medical Services",
    "أندية الوزارة": "Ministry Clubs Administration",
    "الإدارة العامة للمجاهدين": "Mujahideen Administration",
    "كلية الملك فهد الأمنية": "King Fahd Security College",
    "قوات الأمن الخاصة": "Security Protection Forces",
    "مركز العمليات الموحدة": "Unified Operations Center",
    "مركز أبحاث الجريمة": "Crime Research Center",
    "ديوان الوزارة": "MOI Diwan",
    "مركز المعلومات الوطني": "National Information Center"
}
sector_translation_rev = {v: k for k, v in sector_translation.items()}

# ----------------------------
# ترجمات المشاعر
# ----------------------------
sentiment_translation = {
    "Positive": "إيجابي",
    "Negative": "سلبي",
    "Neutral": "محايد"
}
sentiment_translation_rev = {v: k for k, v in sentiment_translation.items()}

# ----------------------------
# عنوان اللوحة
# ----------------------------
st.title("لوحة الرصد الأمني" if is_arabic else "Security Sentiment Dashboard")
st.markdown("تحليل رأي الجمهور حول خدمات وزارة الداخلية" if is_arabic else "Analyzing public opinion on Ministry of Interior services")

# ----------------------------
# القطاعات
# ----------------------------
available_ar_sectors = sorted(df["Sector"].unique())
available_en_sectors = [sector_translation.get(sec, sec) for sec in available_ar_sectors]

selected_sector_display = st.selectbox(
    "اختر القطاع الأمني" if is_arabic else "Select Security Sector",
    available_ar_sectors if is_arabic else available_en_sectors
)

selected_arabic_sector = selected_sector_display if is_arabic else sector_translation_rev.get(selected_sector_display, selected_sector_display)
filtered_df = df[df["Sector"] == selected_arabic_sector].copy()

# ----------------------------
# الترجمة الفعلية
# ----------------------------
def translate_text(text, target="en"):
    try:
        return GoogleTranslator(source='auto', target=target).translate(text)
    except:
        return text  # fallback

# ----------------------------
# عرض النتائج
# ----------------------------
if is_arabic:
    filtered_df["الرأي"] = filtered_df["Sentiment"].map(sentiment_translation).fillna("غير معروف")
    filtered_df["النص"] = filtered_df["Text"]
    display_df = filtered_df[["النص", "الرأي"]]
    chart_data = filtered_df["الرأي"].value_counts()
    st.subheader("النتائج")
    st.write(display_df)
    st.subheader("التحليل العام")
    st.bar_chart(chart_data)
else:
    filtered_df["Translated"] = filtered_df["Text"].apply(lambda x: translate_text(x, "en"))
    display_df = filtered_df[["Translated", "Sentiment"]].rename(columns={"Translated": "Comment"})
    chart_data = filtered_df["Sentiment"].value_counts()
    st.subheader("Results")
    st.write(display_df)
    st.subheader("Overall Sentiment Analysis")
    st.bar_chart(chart_data)

# ----------------------------
# تلخيص التعليقات باستخدام LLM
# ----------------------------
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="facebook/bart-large-cnn")

summarizer = load_summarizer()

def generate_summary(texts, max_chars=2000):
    # دمج النصوص في نص واحد (مع قص الطول إذا زاد عن الحد)
    combined = " ".join(texts)
    combined = combined[:max_chars]
    try:
        summary = summarizer(combined, max_length=100, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        return f"فشل في توليد الملخص: {e}"

st.subheader("ملخص التعليقات" if is_arabic else "Review Summary")
reviews_to_summarize = filtered_df["Text"].astype(str).tolist()
summary_text = generate_summary(reviews_to_summarize)
st.write(summary_text)

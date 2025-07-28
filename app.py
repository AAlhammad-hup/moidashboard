
import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
from textblob import TextBlob

# --- تحميل البيانات ---
@st.cache_data
def load_data():
    df = pd.read_csv("moi_sentimet_data.csv")
    df["Text"] = df["Text"].astype(str).str.strip()
    df["Sector"] = df["Sector"].astype(str).str.strip()
    return df

df = load_data()

# --- إعدادات اللغة ---
language = st.sidebar.selectbox("🌐 اختر اللغة | Select Language", ["العربية", "English"])
is_arabic = (language == "العربية")

# --- ترجمات القطاعات ---
sector_translation = {
    "الدفاع المدني": "Civil Defense",
    "الأمن العام": "Public Security",
    "مكافحة المخدرات": "Narcotics Control",
    "الجوازات": "Passports",
    "السجون": "Prisons",
    "حرس الحدود": "Border Guards",
    "الأمن البيئي": "Environmental Security",
    "قوات الأمن الخاصة": "Security Protection Forces",
    "كلية الملك فهد الأمنية": "King Fahd Security College",
    "الأحوال المدنية": "Civil Affairs",
    "مركز المعلومات الوطني": "National Information Center",
    "مركز العمليات الموحدة": "Unified Operations Center",
    "مركز أبحاث الجريمة": "Crime Research Center",
    "قوات أمن المنشآت": "Facilities Security Forces",
    "الخدمات الطبية": "Medical Services",
    "إدارة أندية الوزارة": "Ministry Clubs Administration",
    "إدارة المجاهدين": "Mujahideen Administration",
    "ديوان الوزارة": "MOI Diwan"
}
sector_translation_rev = {v: k for k, v in sector_translation.items()}

# --- إعدادات الواجهة ---
st.title("لوحة الرصد الأمني" if is_arabic else "Security Sentiment Dashboard")
st.markdown("تحليل رأي الجمهور حول خدمات وزارة الداخلية" if is_arabic else "Analyzing public opinion on Ministry of Interior services")

# --- اختيار القطاع ---
sectors = sorted(df["Sector"].unique())
display_sectors = sectors if is_arabic else [sector_translation.get(s, s) for s in sectors]

selected_display = st.selectbox("اختر القطاع" if is_arabic else "Select Sector", display_sectors)
selected_arabic_sector = selected_display if is_arabic else sector_translation_rev.get(selected_display, selected_display)

# --- تصفية البيانات ---
filtered_df = df[df["Sector"] == selected_arabic_sector].copy()

# --- الترجمة والتحليل ---
def analyze_sentiment(text):
    try:
        translated = GoogleTranslator(source='auto', target='en').translate(text)
        polarity = TextBlob(translated).sentiment.polarity
        if polarity > 0.1:
            return "إيجابي" if is_arabic else "Positive"
        elif polarity < -0.1:
            return "سلبي" if is_arabic else "Negative"
        else:
            return "محايد" if is_arabic else "Neutral"
    except:
        return "غير معروف" if is_arabic else "Unknown"

filtered_df["الرأي" if is_arabic else "Sentiment"] = filtered_df["Text"].apply(analyze_sentiment)

# --- عرض النتائج ---
st.subheader("النتائج" if is_arabic else "Results")
st.write(filtered_df[["Text", "الرأي" if is_arabic else "Sentiment"]])

# --- رسم بياني ---
st.subheader("التحليل العام" if is_arabic else "Overall Analysis")
chart_column = "الرأي" if is_arabic else "Sentiment"
st.bar_chart(filtered_df[chart_column].value_counts())

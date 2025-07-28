import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
from PIL import Image
from textblob import TextBlob
import os

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

# --- عرض شعار وزارة الداخلية في الشريط الجانبي ---
logo = Image.open("moi_logo.png")
st.sidebar.image(logo, use_column_width=True)

# --- النصوص ---
texts = {
    "title": "لوحة الرصد الأمني" if is_arabic else "Security Sentiment Dashboard",
    "desc": "تحليل رأي الجمهور حول خدمات وزارة الداخلية" if is_arabic else "Analyzing public opinion on Ministry of Interior services",
    "select_sector": "اختر القطاع الأمني" if is_arabic else "Select Security Sector",
    "results": "النتائج" if is_arabic else "Results",
    "analysis": "التحليل العام" if is_arabic else "Overall Analysis",
    "text": "النص" if is_arabic else "Text",
    "translated": "الترجمة" if is_arabic else "Translation",
    "sentiment": "الرأي" if is_arabic else "Sentiment"
}

# --- ترجمة أسماء القطاعات ---
sector_names = {
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
sector_names_rev = {v: k for k, v in sector_names.items()}
ordered_sectors = ["الدفاع المدني"] + sorted([s for s in sector_names if s != "الدفاع المدني"])
sectors = ordered_sectors if is_arabic else [sector_names[s] for s in ordered_sectors]

# --- اختيار القطاع ---
selected_sector_display = st.selectbox(texts["select_sector"], sectors)
selected_sector_ar = selected_sector_display if is_arabic else sector_names_rev[selected_sector_display]

# --- صورة القطاع إن وجدت ---
sector_en = sector_names[selected_sector_ar]
image_path = f"sector_images/{sector_en}.png"
if os.path.exists(image_path):
    st.image(image_path, caption=sector_en, use_column_width=True)

# --- تصفية البيانات ---
filtered_df = df[df["Sector"] == selected_sector_ar].copy()
filtered_df["Text"] = filtered_df["Text"].str.replace(f"{selected_sector_ar}[:：،\-]*", "", regex=True).str.strip()

# --- الترجمة وتحليل المشاعر ---
def analyze_sentiment_en(text):
    if not isinstance(text, str) or text.strip() == "":
        return "Neutral"
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "Positive"
    elif polarity < -0.1:
        return "Negative"
    else:
        return "Neutral"

if not is_arabic:
    translator = GoogleTranslator(source='auto', target='en')
    filtered_df["Translated"] = filtered_df["Text"].apply(lambda x: translator.translate(x) if isinstance(x, str) else x)
    filtered_df["Sentiment"] = filtered_df["Translated"].apply(analyze_sentiment_en)
else:
    filtered_df["Translated"] = ""
    filtered_df["Sentiment"] = "قيد التطوير"  # لاحقاً يمكن إدخال محلل مشاعر بالعربية

# --- العناوين ---
st.title(texts["title"])
st.markdown(texts["desc"])

# --- عرض النتائج ---
st.subheader(texts["results"])
display_df = filtered_df[["Text", "Translated", "Sentiment"]].copy()
display_df.columns = [texts["text"], texts["translated"], texts["sentiment"]]
st.write(display_df)

# --- تحليل المشاعر ---
st.subheader(texts["analysis"])
if "Sentiment" in filtered_df.columns:
    sentiment_counts = filtered_df["Sentiment"].value_counts()
    st.bar_chart(sentiment_counts)
else:
    st.warning("لا يوجد عامود للرأي في البيانات." if is_arabic else "No 'Sentiment' column found in the data.")

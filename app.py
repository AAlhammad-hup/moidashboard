import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
import plotly.express as px
from PIL import Image
import os

@st.cache_data
def load_data():
    return pd.read_csv("moi_sentiment_data.csv")

df = load_data()

language = st.sidebar.selectbox("🌐 اختر اللغة | Select Language", ["العربية", "English"])
is_arabic = language == "العربية"

pie_size = st.sidebar.slider("اختر حجم الدائرة (بيكسل)" if is_arabic else "Select Pie Size (px)", 300, 900, 600)
text_size = st.sidebar.slider("اختر حجم النص داخل الدائرة" if is_arabic else "Select Text Size", 10, 40, 20)

# --- عرض شعار وزارة الداخلية في الأعلى ---
logo_path = "moi_logo.png"
if os.path.exists(logo_path):
    logo = Image.open(logo_path)
    st.image(logo, width=120)  # يمكنك تعديل الحجم حسب رغبتك

sector_translation = {
    "جميع القطاعات": "All Sectors",
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

sentiment_translation = {
    "Positive": "إيجابي",
    "Negative": "سلبي",
    "Neutral": "محايد"
}
sentiment_translation_rev = {v: k for k, v in sentiment_translation.items()}

# --- العنوان بعد الشعار ---
st.title("لوحة الرصد الأمني" if is_arabic else "Security Sentiment Dashboard")
st.markdown("تحليل رأي الجمهور حول خدمات وزارة الداخلية" if is_arabic else "Analyzing public opinion on Ministry of Interior services")

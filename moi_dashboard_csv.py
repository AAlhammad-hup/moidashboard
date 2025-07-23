import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator

# --- تحميل البيانات ---
@st.cache_data
def load_data():
    df = pd.read_csv("moi_sentiment_data.csv")
    df["Text"] = df["Text"].astype(str)
    df["Sector"] = df["Sector"].astype(str)
    return df

df = load_data()

# --- إعدادات اللغة ---
language = st.sidebar.selectbox("🌐 اختر اللغة | Select Language", ["العربية", "English"])
is_arabic = (language == "العربية")

# --- النصوص ---
texts = {
    "title": "لوحة الرصد الأمني" if is_arabic else "Security Sentiment Dashboard",
    "desc": "تحليل رأي الجمهور حول خدمات وزارة الداخلية" if is_arabic else "Analyzing public opinion on Ministry of Interior services",
    "select_sector": "اختر القطاع الأمني" if is_arabic else "Select Security Sector",
    "results": "النتائج" if is_arabic else "Results",
    "analysis": "التحليل العام" if is_arabic else "Overall Analysis",
    "text": "النص" if is_arabic else "Text",
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

# إعادة ترتيب القطاعات لتكون "الدفاع المدني" أولًا
ordered_sectors = ["الدفاع المدني"] + sorted([s for s in sector_names if s != "الدفاع المدني"])

# --- تحديد القطاع ---
sector_label = texts["select_sector"]
selected_sector_ar = st.selectbox(sector_label, ordered_sectors)

# --- التصفية ---
filtered_df = df[df["Sector"] == selected_sector_ar].copy()

# --- حذف اسم القطاع من بداية النص ---
filtered_df["Text"] = filtered_df["Text"].str.replace(f"{selected_sector_ar}[:：،\-]*", "", regex=True).str.strip()

# --- الترجمة التلقائية في حال اختيار اللغة الإنجليزية ---
if not is_arabic:
    translator = GoogleTranslator(source='auto', target='en')
    filtered_df["Text"] = filtered_df["Text"].apply(lambda x: translator.translate(x) if isinstance(x, str) else x)
    selected_sector_display = sector_names.get(selected_sector_ar, selected_sector_ar)
else:
    selected_sector_display = selected_sector_ar

# --- العناوين ---
st.title(texts["title"])
st.markdown(texts["desc"])

# --- عرض النتائج ---
st.subheader(texts["results"])
st.write(
    filtered_df[["Text", "Sentiment"]].rename(columns={
        "Text": texts["text"],
        "Sentiment": texts["sentiment"]
    })
)

# --- تحليل المشاعر ---
st.subheader(texts["analysis"])
st.bar_chart(filtered_df["Sentiment"].value_counts())

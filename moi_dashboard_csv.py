import streamlit as st
import pandas as pd

# إعداد الترجمة للواجهة
LANGUAGES = {
    "العربية": {
        "title": "لوحة الرصد الأمني",
        "description": "تحليل رأي الجمهور حول خدمات وزارة الداخلية",
        "select_language": "🌐 اختر اللغة",
        "select_sector": "اختر القطاع الأمني",
        "results": "النتائج",
        "analysis": "التحليل العام",
        "text": "النص",
        "sentiment": "الرأي"
    },
    "English": {
        "title": "Security Sentiment Dashboard",
        "description": "Analyzing public opinion on Ministry of Interior services",
        "select_language": "🌐 Select Language",
        "select_sector": "Select Security Sector",
        "results": "Results",
        "analysis": "Overall Analysis",
        "text": "Text",
        "sentiment": "Sentiment"
    }
}

# ترجمة أسماء القطاعات
SECTOR_TRANSLATIONS = {
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
    "مركز العمليات الموحد": "Unified Operations Center",
    "مركز أبحاث الجريمة": "Crime Research Center",
    "قوات أمن المنشآت": "Facilities Security Forces",
    "الخدمات الطبية": "Medical Services",
    "إدارة الأندية": "Ministry Clubs Administration",
    "إدارة المجاهدين": "Mujahideen Administration",
    "ديوان الوزارة": "MOI Diwan"
}

# اختيار اللغة
language = st.sidebar.selectbox(LANGUAGES["English"]["select_language"], ["العربية", "English"])
texts = LANGUAGES[language]
is_arabic = language == "العربية"

# عنوان الصفحة
st.title(texts["title"])
st.markdown(texts["description"])

# تحميل البيانات
@st.cache_data
def load_data():
    return pd.read_csv("moi_sentiment_data.csv")

df = load_data()

# إعداد القطاع بحسب اللغة
if is_arabic:
    sectors = sorted(df["Sector"].unique())
else:
    sectors = sorted([SECTOR_TRANSLATIONS.get(sec, sec) for sec in df["Sector"].unique()])

# اختيار القطاع
selected_sector_display = st.selectbox(texts["select_sector"], sectors)

# إعادة الترجمة العكسية إذا كانت إنجليزية
if not is_arabic:
    reverse_map = {v: k for k, v in SECTOR_TRANSLATIONS.items()}
    selected_sector = reverse_map.get(selected_sector_display, selected_sector_display)
else:
    selected_sector = selected_sector_display

# تصفية البيانات
filtered_df = df[df["Sector"] == selected_sector].copy()

# إزالة اسم القطاع من بداية النص
filtered_df["Text"] = filtered_df["Text"].str.replace(f"{selected_sector}[:،]*", "", regex=True).str.strip()

# عرض النتائج
st.subheader(texts["results"])
st.write(filtered_df[[texts["text"], texts["sentiment"]]].rename(columns={
    "Text": texts["text"],
    "Sentiment": texts["sentiment"]
}))

# عرض الرسم البياني
st.subheader(texts["analysis"])
st.bar_chart(filtered_df["Sentiment"].value_counts())

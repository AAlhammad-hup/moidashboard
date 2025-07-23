
import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator

# اختيار اللغة
language = st.sidebar.selectbox("🌐 اختر اللغة | Select Language", ["العربية", "English"])
is_arabic = language == "العربية"

# عنوان الصفحة
st.title("لوحة الرصد الأمني" if is_arabic else "Security Sentiment Dashboard")
st.markdown("تحليل رأي الجمهور حول خدمات وزارة الداخلية" if is_arabic else "Analyzing public opinion on Ministry of Interior services")

# تحميل البيانات من CSV
@st.cache_data
def load_data():
    return pd.read_csv("moi_sentiment_data.csv")

df = load_data()

# قاموس ترجمة القطاعات
sector_translation = {
    "الدفاع المدني": "Civil Defense",
    "الأمن العام": "Public Security",
    "مكافحة المخدرات": "Narcotics Control",
    "الجوازات": "Passports",
    "السجون": "Prisons",
    "حرس الحدود": "Border Guards",
    "الأمن البيئي": "Environmental Security",
    "قوات الأمن الخاصة": "Special Security Forces",
    "كلية الملك فهد الأمنية": "King Fahd Security College",
    "الأحوال المدنية": "Civil Affairs",
    "مركز المعلومات الوطني": "National Information Center",
    "مركز العمليات الموحدة": "Unified Operations Center",
    "مركز أبحاث الجريمة": "Crime Research Center",
    "قوات أمن المنشآت": "Facilities Security Forces",
    "الخدمات الطبية": "Medical Services",
    "أندية الوزارة": "Ministry Clubs",
    "الإدارة العامة للمجاهدين": "Mujahideen Administration",
    "ديوان الوزارة": "MOI Diwan"
}

# تحويل أسماء القطاعات حسب اللغة المختارة
if is_arabic:
    sectors = sorted(df["Sector"].unique())
else:
    df["Sector_En"] = df["Sector"].map(sector_translation)
    sectors = sorted(df["Sector_En"].dropna().unique())

# اختيار القطاع
selected_sector = st.selectbox("اختر القطاع الأمني" if is_arabic else "Select Security Sector", sectors)

# تصفية البيانات بناءً على اللغة المختارة
if is_arabic:
    filtered_df = df[df["Sector"] == selected_sector]
else:
    df["Sector_En"] = df["Sector"].map(sector_translation)
    filtered_df = df[df["Sector_En"] == selected_sector].copy()
    filtered_df["Translated_Text"] = filtered_df["Text"].apply(lambda x: GoogleTranslator(source='auto', target='en').translate(x))

# عرض النتائج
st.subheader("النتائج" if is_arabic else "Results")
if is_arabic:
    st.write(filtered_df[["Text", "Sentiment"]])
else:
    st.write(filtered_df[["Translated_Text", "Sentiment"]])

# عرض التحليل العام
st.subheader("التحليل العام" if is_arabic else "Overall Analysis")
st.bar_chart(filtered_df["Sentiment"].value_counts())

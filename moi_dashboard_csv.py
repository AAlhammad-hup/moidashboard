import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator

# تحميل البيانات
@st.cache_data
def load_data():
    return pd.read_csv("moi_sentiment_data.csv")

df = load_data()

# واجهة اللغة
language = st.sidebar.selectbox("🌐 اختر اللغة | Select Language", ["العربية", "English"])
is_arabic = language == "العربية"

# ترجمة القطاع إنجليزي ↔ عربي (ثنائية الاتجاه)
sector_names = {
    "Civil Defense": "الدفاع المدني",
    "Public Security": "الأمن العام",
    "Passports": "الجوازات",
    "Traffic": "المرور",
    "Prisons": "السجون",
    "Narcotics Control": "مكافحة المخدرات",
    "Border Guards": "حرس الحدود",
    "Civil Affairs": "الأحوال المدنية",
    "Environmental Security": "الأمن البيئي",
    "Facilities Security": "أمن المنشآت",
    "Medical Services": "الخدمات الطبية",
    "Ministry Clubs": "أندية الوزارة",
    "Mujahideen": "المجاهدين",
    "King Fahd Security College": "كلية الملك فهد الأمنية",
    "Security Protection": "قوات الأمن الخاصة",
    "Unified Operations": "العمليات الموحدة",
    "Crime Research Center": "مركز أبحاث الجريمة",
    "Diwan": "ديوان الوزارة",
    "National Information Center": "مركز المعلومات الوطني"
}

# ترجمة عكسية
sector_names_ar_to_en = {v: k for k, v in sector_names.items()}

# عنوان الصفحة
st.title("لوحة الرصد الأمني" if is_arabic else "Security Sentiment Dashboard")
st.markdown(
    "تحليل رأي الجمهور حول خدمات وزارة الداخلية" if is_arabic else
    "Analyzing public opinion on Ministry of Interior services"
)

# تحويل أسماء القطاعات للغة المختارة
if is_arabic:
    sector_list = [sector_names.get(sector, sector) for sector in df["Sector"].unique()]
else:
    sector_list = [sector for sector in df["Sector"].unique()]

# اختيار القطاع
selected_sector = st.selectbox(
    "اختر القطاع الأمني" if is_arabic else "Select Security Sector",
    sorted(sector_list) if is_arabic else sorted(df["Sector"].unique())
)

# تحويل الاختيار إلى اسم القطاع الأصلي بالإنجليزية
if is_arabic:
    selected_sector_en = sector_names_ar_to_en.get(selected_sector, selected_sector)
else:
    selected_sector_en = selected_sector

# تصفية البيانات
filtered_df = df[df["Sector"] == selected_sector_en]

# ترجمة المشاعر إذا كانت الواجهة عربية
if is_arabic:
    sentiment_mapping = {"Positive": "إيجابي", "Negative": "سلبي", "Neutral": "محايد"}
    filtered_df["Sentiment"] = filtered_df["Sentiment"].map(sentiment_mapping)

# عرض النتائج
st.subheader("النتائج" if is_arabic else "Results")
st.write(
    filtered_df[["Text", "Sentiment"]].rename(columns={
        "Text": "النص" if is_arabic else "Text",
        "Sentiment": "الرأي" if is_arabic else "Sentiment"
    })
)

# عرض تحليل بياني
st.subheader("التحليل العام" if is_arabic else "Overall Sentiment Analysis")
st.bar_chart(filtered_df["Sentiment"].value_counts())

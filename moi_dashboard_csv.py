import streamlit as st
import pandas as pd

# تحميل البيانات من ملف CSV
@st.cache_data
def load_data():
    return pd.read_csv("moi_sentiment_data.csv")

df = load_data()

# اختيار اللغة
language = st.sidebar.selectbox("🌐 اختر اللغة | Select Language", ["العربية", "English"])
is_arabic = language == "العربية"

# قاموس الترجمة بين العربي والإنجليزي
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

# ترجمة المشاعر
sentiment_translation = {
    "Positive": "إيجابي",
    "Negative": "سلبي",
    "Neutral": "محايد"
}
sentiment_translation_rev = {v: k for k, v in sentiment_translation.items()}

# واجهة المستخدم
st.title("لوحة الرصد الأمني" if is_arabic else "Security Sentiment Dashboard")
st.markdown("تحليل رأي الجمهور حول خدمات وزارة الداخلية" if is_arabic else "Analyzing public opinion on Ministry of Interior services")

# القطاعات من الملف (كلها بالعربية)
available_ar_sectors = sorted(df["Sector"].unique())
available_en_sectors = [sector_translation.get(sec, sec) for sec in available_ar_sectors]

selected_sector_display = st.selectbox(
    "اختر القطاع الأمني" if is_arabic else "Select Security Sector",
    available_ar_sectors if is_arabic else available_en_sectors
)

# تحويل القطاع المختار إلى العربية لتصفية البيانات
if is_arabic:
    selected_arabic_sector = selected_sector_display
else:
    selected_arabic_sector = sector_translation_rev.get(selected_sector_display, selected_sector_display)

# تصفية البيانات
filtered_df = df[df["Sector"] == selected_arabic_sector].copy()

# عرض النتائج
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
    display_df = filtered_df[["Text", "Sentiment"]]
    chart_data = filtered_df["Sentiment"].value_counts()
    st.subheader("Results")
    st.write(display_df)
    st.subheader("Overall Sentiment Analysis")
    st.bar_chart(chart_data)

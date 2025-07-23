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

# ترجمة القطاعات
sector_translation = {
    "Civil Defense": "الدفاع المدني",
    "Public Security": "الأمن العام",
    "Passports": "الجوازات",
    "Traffic": "المرور",
    "Prisons": "السجون",
    "Narcotics Control": "مكافحة المخدرات",
    "Border Guards": "حرس الحدود",
    "Civil Affairs": "الأحوال المدنية",
    "Environmental Security": "الأمن البيئي",
    "Facilities Security Forces": "قوات أمن المنشآت",
    "Medical Services": "الخدمات الطبية",
    "Ministry Clubs Administration": "أندية منسوبي الوزارة",
    "Mujahideen Administration": "الإدارة العامة للمجاهدين",
    "King Fahd Security College": "كلية الملك فهد الأمنية",
    "Security Protection Forces": "قوات الأمن الخاصة",
    "Unified Operations Center": "المركز الوطني للعمليات الأمنية الموحدة",
    "Crime Research Center": "مركز أبحاث مكافحة الجريمة",
    "MOI Diwan": "ديوان وزارة الداخلية",
    "National Information Center": "مركز المعلومات الوطني"
}

# عكس الترجمة
sector_translation_rev = {v: k for k, v in sector_translation.items()}

# ترجمة المشاعر
sentiment_translation = {
    "Positive": "إيجابي",
    "Negative": "سلبي",
    "Neutral": "محايد"
}
sentiment_translation_rev = {v: k for k, v in sentiment_translation.items()}

# إعداد الصفحة
st.title("لوحة الرصد الأمني" if is_arabic else "Security Sentiment Dashboard")
st.markdown("تحليل رأي الجمهور حول خدمات وزارة الداخلية" if is_arabic else "Analyzing public opinion on Ministry of Interior services")

# عرض القطاعات
unique_sectors = df["Sector"].unique()
if is_arabic:
    display_sectors = [sector_translation.get(s, s) for s in unique_sectors]
else:
    display_sectors = list(unique_sectors)

selected_display = st.selectbox("اختر القطاع الأمني" if is_arabic else "Select Security Sector", sorted(display_sectors))

# تحديد اسم القطاع الحقيقي
if is_arabic:
    selected_sector = sector_translation_rev.get(selected_display, selected_display)
else:
    selected_sector = selected_display

# تصفية البيانات
filtered_df = df[df["Sector"] == selected_sector].copy()

# ترجمة الأعمدة والمشاعر
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

import streamlit as st
import pandas as pd

# اختيار اللغة
language = st.sidebar.selectbox("🌐 اختر اللغة | Select Language", ["العربية", "English"])
is_arabic = language == "العربية"

# عنوان الصفحة
st.title("لوحة الرصد الأمني" if is_arabic else "Security Sentiment Dashboard")
st.markdown("تحليل رأي الجمهور حول خدمات وزارة الداخلية" if is_arabic else "Analyzing public opinion on Ministry of Interior services")

# قراءة البيانات من ملف CSV
@st.cache_data
def load_data():
    return pd.read_csv("moi_sentiment_data.csv")

df = load_data()

# قاموس ترجمة القطاعات
sector_translations = {
    "الدفاع المدني": "Civil Defense",
    "الأمن العام": "Public Security",
    "مكافحة المخدرات": "Narcotics Control",
    "المرور": "Traffic",
    "الجوازات": "Passports",
    "الأحوال المدنية": "Civil Affairs",
    "حرس الحدود": "Border Guards",
    "السجون": "Prisons",
    "العمليات الموحدة": "Unified Operations",
    "الأمن البيئي": "Environmental Security",
    "الشرطة": "Police",
    "قوات الأمن الخاصة": "Security Protection Forces",
    "كلية الملك فهد الأمنية": "King Fahd Security College",
    "مركز المعلومات الوطني": "National Information Center",
    "مركز البحوث الأمنية": "Crime Research Center",
    "إدارة الأندية": "Ministry Clubs Administration",
    "الإدارة العامة للمجاهدين": "Mujahideen Administration",
    "ديوان الوزارة": "MOI Diwan",
    "الخدمات الطبية": "Medical Services"
}

# إعداد قائمة القطاعات المعروضة حسب اللغة
sectors_ar = sorted(df["Sector"].unique())
sectors_display = [sector if is_arabic else sector_translations.get(sector, sector) for sector in sectors_ar]

# اختيار القطاع
selected_display = st.selectbox("اختر القطاع الأمني" if is_arabic else "Select Security Sector", sectors_display)

# ربط اسم العرض بالاسم الأصلي لتصفية البيانات
selected_sector = sectors_ar[sectors_display.index(selected_display)]

# تصفية البيانات حسب القطاع
filtered_df = df[df["Sector"] == selected_sector]

# عرض التغريدات
st.subheader("النتائج" if is_arabic else "Results")
st.write(filtered_df[["Text", "Sentiment"]])

# رسم بياني لتحليل المشاعر
st.subheader("التحليل العام" if is_arabic else "Overall Analysis")
st.bar_chart(filtered_df["Sentiment"].value_counts())

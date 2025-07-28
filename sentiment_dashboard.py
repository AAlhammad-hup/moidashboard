import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
import plotly.express as px

# ----------------------------
# تحميل البيانات
# ----------------------------
@st.cache_data
def load_data():
    return pd.read_csv("moi_sentiment_data.csv")

df = load_data()

# ----------------------------
# اختيار اللغة
# ----------------------------
language = st.sidebar.selectbox("🌐 اختر اللغة | Select Language", ["العربية", "English"])
is_arabic = language == "العربية"

# ----------------------------
# اختيار حجم النصوص والدائرة
# ----------------------------
pie_size = st.sidebar.slider("اختر حجم الدائرة (بيكسل)" if is_arabic else "Select Pie Size (px)", 300, 900, 600)
text_size = st.sidebar.slider("اختر حجم النص داخل الدائرة" if is_arabic else "Select Text Size", 10, 40, 20)

# ----------------------------
# ترجمات القطاعات
# ----------------------------
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

# ----------------------------
# ترجمات المشاعر
# ----------------------------
sentiment_translation = {
    "Positive": "إيجابي",
    "Negative": "سلبي",
    "Neutral": "محايد"
}
sentiment_translation_rev = {v: k for k, v in sentiment_translation.items()}

# ----------------------------
# عنوان اللوحة
# ----------------------------
st.title("لوحة الرصد الأمني" if is_arabic else "Security Sentiment Dashboard")
st.markdown("تحليل رأي الجمهور حول خدمات وزارة الداخلية" if is_arabic else "Analyzing public opinion on Ministry of Interior services")

# ----------------------------
# القطاعات (إضافة خيار جميع القطاعات)
# ----------------------------
available_ar_sectors = ["جميع القطاعات"] + sorted([s for s in df["Sector"].unique()])
available_en_sectors = [sector_translation.get(sec, sec) for sec in available_ar_sectors]

selected_sector_display = st.selectbox(
    "اختر القطاع الأمني" if is_arabic else "Select Security Sector",
    available_ar_sectors if is_arabic else available_en_sectors
)
selected_arabic_sector = selected_sector_display if is_arabic else sector_translation_rev.get(selected_sector_display, selected_sector_display)

# ----------------------------
# التصفية
# ----------------------------
if selected_arabic_sector == "جميع القطاعات":
    filtered_df = df.copy()
else:
    filtered_df = df[df["Sector"] == selected_arabic_sector].copy()

# ----------------------------
# اختيار عدد التعليقات المطلوب عرضها
# ----------------------------
max_comments = st.sidebar.slider(
    "عدد التعليقات المراد عرضها" if is_arabic else "Number of comments to display",
    min_value=1,
    max_value=len(filtered_df),
    value=min(10, len(filtered_df))
)

# ----------------------------
# إزالة اسم القطاع من النصوص (لغير جميع القطاعات)
# ----------------------------
def clean_comment(text, sector_name):
    if isinstance(text, str) and text.startswith(sector_name):
        return text.replace(sector_name + ":", "").strip()
    return text

if selected_arabic_sector != "جميع القطاعات":
    filtered_df["Text"] = filtered_df["Text"].apply(lambda x: clean_comment(x, selected_arabic_sector))

# ----------------------------
# الترجمة الفعلية
# ----------------------------
def translate_text(text, target="en"):
    try:
        return GoogleTranslator(source='auto', target=target).translate(text)
    except:
        return text

# ----------------------------
# عرض النتائج (فقط إذا لم يتم اختيار جميع القطاعات)
# ----------------------------
if selected_arabic_sector != "جميع القطاعات":
    if is_arabic:
        filtered_df["الرأي"] = filtered_df["Sentiment"].map(sentiment_translation).fillna("غير معروف")
        filtered_df["النص"] = filtered_df["Text"]
        display_df = filtered_df[["النص", "الرأي"]]
        st.subheader("النتائج")
        st.write(display_df.head(max_comments))
    else:
        filtered_df["Translated"] = filtered_df["Text"].apply(lambda x: translate_text(x, "en"))
        display_df = filtered_df[["Translated", "Sentiment"]].rename(columns={"Translated": "Comment"})
        st.subheader("Results")
        st.write(display_df.head(max_comments))

# ----------------------------
# التحليل العام
# ----------------------------
chart_data = filtered_df["Sentiment"].map(sentiment_translation if is_arabic else lambda x: x).value_counts()
st.subheader("التحليل العام" if is_arabic else "Overall Sentiment Analysis")
st.bar_chart(chart_data)

# ----------------------------
# احصاءات المشاعر (KPIs) بدون النسبة المئوية
# ----------------------------
counts = filtered_df["Sentiment"].value_counts()
pos = counts.get("Positive", 0)
neg = counts.get("Negative", 0)
neu = counts.get("Neutral", 0)
total = pos + neg + neu

title_total = "الإجمالي" if is_arabic else "Total"
title_pos   = "إيجابي"   if is_arabic else "Positive"
title_neu   = "محايد"    if is_arabic else "Neutral"
title_neg   = "سلبي"     if is_arabic else "Negative"

st.subheader("ملخص الأعداد" if is_arabic else "Summary Counts")
c1, c2, c3, c4 = st.columns(4)
c1.metric(title_total, f"{total:,}")
c2.metric(title_pos, f"{pos:,}")
c3.metric(title_neu, f"{neu:,}")
c4.metric(title_neg, f"{neg:,}")

# ----------------------------
# رسم مخطط دائري باستخدام Plotly
# ----------------------------
st.subheader("النسب المئوية للمشاعر" if is_arabic else "Sentiment Percentages")
labels = [title_pos, title_neu, title_neg]
values = [pos, neu, neg]

fig = px.pie(
    names=labels,
    values=values,
    title="النسب المئوية للمشاعر" if is_arabic else "Sentiment Percentages",
    color=labels,
    color_discrete_sequence=['#007bff', '#00cc96', '#ff6361']
)
fig.update_layout(width=pie_size, height=pie_size)
fig.update_traces(textfont_size=text_size)
st.plotly_chart(fig)

# ----------------------------
# ملخص إحصائي نصي
# ----------------------------
def simple_summary(df, is_arabic=True):
    if total == 0:
        return "لا توجد تعليقات متاحة." if is_arabic else "No comments available."
    if is_arabic:
        return f"إجمالي التعليقات: {total}. الإيجابية: {pos}، السلبية: {neg}، المحايدة: {neu}."
    else:
        return f"Total comments: {total}. Positive: {pos}, Negative: {neg}, Neutral: {neu}."

st.subheader("ملخص التعليقات" if is_arabic else "Review Summary")
st.write(simple_summary(filtered_df, is_arabic))

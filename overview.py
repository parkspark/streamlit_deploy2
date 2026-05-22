import streamlit as st
import pandas as pd
import plotly.express as px

# Step 1: 데이터 로드 및 전처리
@st.cache_data
def load_marketing():
    df = pd.read_csv("data/marketing_campaign_dataset.csv")
    df['Acquisition_Cost'] = df['Acquisition_Cost'].replace({'\$': '', ',': ''}, regex=True).astype(float)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

st.title("📊 마케팅 캠페인 대시보드 (요약)")
df = load_marketing()
st.write(f"**전체 데이터 행 수:** {len(df):,}개")

# Step 2: 사이드바 필터
campaign_options = df['Campaign_Type'].unique().tolist()
location_options = ["전체"] + df['Location'].unique().tolist()

if "campaign_types" not in st.session_state:
    st.session_state["campaign_types"] = campaign_options
if "location" not in st.session_state:
    st.session_state["location"] = "전체"

def reset_filters():
    st.session_state["campaign_types"] = campaign_options
    st.session_state["location"] = "전체"

st.sidebar.button("필터 초기화", on_click=reset_filters)

try:
    loc_index = location_options.index(st.session_state["location"])
except ValueError:
    loc_index = 0

campaign_types = st.sidebar.multiselect(
    "캠페인 유형 (Campaign Type)",
    options=campaign_options,
    default=st.session_state["campaign_types"],
    key="campaign_types"
)

location = st.sidebar.selectbox(
    "지역 (Location)",
    options=location_options,
    index=loc_index,
    key="location"
)

# 데이터 필터링
filtered = df.copy()
if campaign_types:
    filtered = filtered[filtered['Campaign_Type'].isin(campaign_types)]

if location != "전체":
    filtered = filtered[filtered['Location'] == location]

# Step 3: Metric
st.subheader("💡 주요 지표")
col1, col2, col3 = st.columns(3)

total_campaigns = len(filtered)
avg_roi = filtered['ROI'].mean() if not filtered.empty else 0
avg_conversion = filtered['Conversion_Rate'].mean() * 100 if not filtered.empty else 0

col1.metric("총 캠페인 수", f"{total_campaigns:,} 개")
col2.metric("평균 ROI", f"{avg_roi:.2f}")
col3.metric("평균 전환율", f"{avg_conversion:.1f}%")

# Step 4: 차트
st.subheader("📈 캠페인 유형별 평균 ROI")
if not filtered.empty:
    roi_by_type = filtered.groupby('Campaign_Type')['ROI'].mean().reset_index()
    fig = px.bar(roi_by_type, x='Campaign_Type', y='ROI', 
                 title="캠페인 유형별 평균 ROI",
                 text_auto='.2f',
                 labels={'Campaign_Type': '캠페인 유형', 'ROI': '평균 ROI'})
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("선택한 조건에 맞는 데이터가 없습니다.")

import streamlit as st
import pandas as pd

@st.cache_data
def load_marketing():
    df = pd.read_csv("data/marketing_campaign_dataset.csv")
    df['Acquisition_Cost'] = df['Acquisition_Cost'].replace({'\$': '', ',': ''}, regex=True).astype(float)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

st.title("🔍 마케팅 캠페인 대시보드 (상세 분석)")
df = load_marketing()

st.subheader("키워드 검색")
with st.form("search_form"):
    keyword = st.text_input("검색할 키워드를 입력하세요:")
    submitted = st.form_submit_button("검색")

    if submitted:
        if keyword:
            mask = df.astype(str).apply(lambda x: x.str.contains(keyword, case=False, na=False)).any(axis=1)
            search_result = df[mask]
            
            st.success(f"총 {len(search_result):,}개의 검색 결과가 있습니다.")
            if not search_result.empty:
                st.write("상위 20행 미리보기:")
                st.dataframe(search_result.head(20))
        else:
            st.warning("검색어를 입력해주세요.")

st.divider()
st.subheader("CSV 파일 업로드 및 분석")

uploaded = st.file_uploader("분석할 CSV 파일을 업로드하세요.", type=['csv'])

if uploaded is not None:
    try:
        user_df = pd.read_csv(uploaded)
        st.success(f"파일 '{uploaded.name}' 로드 성공! (총 {len(user_df):,}행)")
        st.write("### 데이터 요약 통계 (Describe)")
        st.dataframe(user_df.describe())
    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")

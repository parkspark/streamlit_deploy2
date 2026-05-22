import streamlit as st
import pandas as pd

@st.cache_data
def load_marketing():
    df = pd.read_csv("data/marketing_campaign_dataset.csv")
    df['Acquisition_Cost'] = df['Acquisition_Cost'].replace({r'\$': '', ',': ''}, regex=True).astype(float)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

st.title("🔍 마케팅 캠페인 대시보드 (상세 분석) 및 CSV 다운로드")
df = load_marketing()

st.subheader("키워드 검색")
with st.form("search_form"):
    st.caption("💡 검색 예시: 단일 키워드(`Google`), 여러 키워드 중 하나(`Google|Facebook`), 정규표현식(`^New.*`) 등")
    keyword = st.text_input("검색할 키워드 또는 정규표현식을 입력하세요:", placeholder="예: Google|Facebook")
    submitted = st.form_submit_button("검색")

if submitted:
    if keyword:
        try:
            import time
            start_time = time.time()
            # 행(Row) 단위로 데이터를 하나의 문자열로 합친 후 정규식 검사
            mask = df.astype(str).apply(lambda x: ' '.join(x), axis=1).str.contains(keyword, case=False, na=False, regex=True)
            st.session_state['search_result'] = df[mask]
            st.session_state['search_keyword'] = keyword
            st.session_state['search_time'] = time.time() - start_time
        except Exception as e:
            st.error(f"잘못된 정규표현식입니다. 에러 메시지: {e}")
            if 'search_result' in st.session_state:
                del st.session_state['search_result']
    else:
        st.warning("검색어를 입력해주세요.")
        if 'search_result' in st.session_state:
            del st.session_state['search_result']

if 'search_result' in st.session_state:
    search_result = st.session_state['search_result']
    search_time = st.session_state.get('search_time', 0.0)
    st.success(f"총 {len(search_result):,}개의 검색 결과가 있습니다. (⏱️검색 소요 시간: {search_time:.3f}초)")
    
    if not search_result.empty:
        st.write("상위 20행 미리보기:")
        st.dataframe(search_result.head(20))
        
        csv_data = search_result.to_csv(index=False).encode('utf-8-sig')
        kwd = st.session_state.get('search_keyword', 'result')
        st.download_button(
            label="📥 검색 결과 CSV 다운로드",
            data=csv_data,
            file_name=f"search_result_{kwd}.csv",
            mime="text/csv"
        )

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

if st.button("풍선!!!!"):
    st.balloons()

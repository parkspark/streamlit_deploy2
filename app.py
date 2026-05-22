import streamlit as st

st.set_page_config(
    page_title="마케팅 캠페인 대시보드",
    page_icon="📈",
    layout="wide"
)

overview_page = st.Page("overview.py", title="요약", icon="📊")
detail_page = st.Page("detail.py", title="상세 분석", icon="🔍")

pg = st.navigation([overview_page, detail_page])
pg.run()

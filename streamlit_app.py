import streamlit as st

st.title("성단 거리 측정 앱 (준비 중)")
st.write("여기는 성단의 색등급도(C-M도)를 그리고 거리 계산을 할 앱입니다.")
st.write("현재는 기본 구조만 설정되어 있습니다.")

uploaded_file = st.file_uploader("FITS 이미지 파일을 업로드하세요", type=["fits"])

if uploaded_file:
    st.success("FITS 파일이 성공적으로 업로드되었습니다!")
    st.write("파일 이름:", uploaded_file.name)

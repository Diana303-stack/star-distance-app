import streamlit as st
from astropy.io import fits
import numpy as np

st.set_page_config(page_title="성단 거리 측정 앱", layout="centered")

st.title("성단 거리 측정 앱 (1단계: FITS 내용 확인)")

st.write("FITS 이미지를 업로드하면 헤더 정보와 데이터 배열 모양을 보여줍니다.")
st.write("이후 이 데이터를 바탕으로 별의 색과 밝기를 추출할 거예요!")

uploaded_file = st.file_uploader("FITS 이미지 파일을 업로드하세요", type=["fits"])

if uploaded_file:
    st.success("FITS 파일이 업로드되었습니다!")

    # FITS 파일 열기
    with fits.open(uploaded_file) as hdul:
        st.subheader("FITS 헤더 정보")
        st.text(hdul[0].header)

        st.subheader("데이터 구조 (배열 모양)")
        data = hdul[0].data
        st.write("데이터 형태:", np.shape(data))

        # 미리보기용 시각화
        st.subheader("이미지 미리보기 (중앙 500x500)")
        import matplotlib.pyplot as plt
        cutout = data[0:500, 0:500]  # 상위 500x500만 미리보기
        fig, ax = plt.subplots()
        ax.imshow(cutout, cmap="gray", origin="lower")
        st.pyplot(fig)

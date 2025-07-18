import streamlit as st
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt
from photutils.detection import DAOStarFinder
from photutils.background import MedianBackground
from photutils.aperture import CircularAperture, aperture_photometry

st.set_page_config(page_title="성단 거리 측정 앱", layout="centered")
st.title("성단 거리 측정 앱 (2단계: 별 밝기 자동 추출)")

uploaded_file = st.file_uploader("FITS 이미지 파일을 업로드하세요", type=["fits", "fz"])

if uploaded_file:
    st.success("FITS 파일이 업로드되었습니다!")

    with fits.open(uploaded_file) as hdul:
        data = hdul[0].data

    st.subheader("이미지 미리보기 (중앙 500x500)")
    cutout = data[0:500, 0:500]
    fig, ax = plt.subplots()
    ax.imshow(cutout, cmap="gray", origin="lower")
    st.pyplot(fig)

    st.subheader("별 감지 및 밝기 추출 중...")

    # 데이터 전처리 (NaN 제거 + 절댓값 처리)
    clean_data = np.nan_to_num(data)
    clean_data = np.abs(clean_data)

    # 배경 추정 및 별 찾기
    bkg = MedianBackground()
    threshold = bkg(clean_data) + (5 * np.std(clean_data))
    daofind = DAOStarFinder(fwhm=3.0, threshold=threshold)
    sources = daofind(clean_data)

    if sources is not None:
        st.success(f"별 {len(sources)}개 감지됨!")
        positions = np.transpose((sources['xcentroid'], sources['ycentroid']))

        # 밝기 측정 (aperture photometry)
        apertures = CircularAperture(positions, r=4.)
        phot_table = aperture_photometry(clean_data, apertures)
        st.write("상위 100개 별의 측정 결과:")
        st.dataframe(phot_table.to_pandas().head(100))

        # 시각화
        st.subheader("별 위치 시각화")
        fig2, ax2 = plt.subplots()
        ax2.imshow(clean_data, cmap='gray', origin='lower', vmax=np.percentile(clean_data, 99))
        apertures.plot(color='red', lw=1.5, alpha=0.5, axes=ax2)
        st.pyplot(fig2)
    else:
        st.warning("별을 찾지 못했습니다. 다른 FITS 이미지를 시도해보세요.")

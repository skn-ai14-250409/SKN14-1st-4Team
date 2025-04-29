import streamlit as st

# 페이지 설정
st.set_page_config(page_title="전기차 포털", page_icon="🏠", layout="wide")

# 헤더
st.markdown("""
    <h1 style="text-align: center; color: black;">🏠 전기차 포털 🏠</h1>
    <p style="text-align: center; color: black; font-size: 20px;">
        전기차 등록 현황과 가까운 전기차 충전소를 검색할 수 있는 플랫폼입니다.
    </p>
""", unsafe_allow_html=True)

# 배경 이미지
image_url = "https://img.freepik.com/free-vector/flat-man-character-charge-electric-car-ev-charger-station-via-mobile-app_88138-1884.jpg?t=st=1745821879~exp=1745825479~hmac=a501c8471b974b63c5c141ace564874b7ec86e72b3962853d50c9fd12c3df3e4&w=1060"
st.markdown(
    f"""
    <div style="display: flex; justify-content: center;">
        <img src="{image_url}" width="800">
    </div>
    """,
    unsafe_allow_html=True
)

# 기능 섹션
col1, col2 = st.columns(2)

# 1. 전기차 등록 현황
with col1:
    st.markdown("""
        <style>
            .ev-container {
                background-color: #4CAF50;  /* 초록색 배경 */
                border-radius: 12px;
                padding: 30px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                margin: 20px;
            }

            .ev-title {
                color: white;
                text-align: center;
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 10px;
            }

            .ev-description {
                color: white;
                text-align: center;
                font-size: 16px;
                margin-bottom: 20px;
            }

            .ev-button {
                display: inline-block;
                background-color: white;
                color: #4CAF50;  /* 초록색 버튼 */
                padding: 12px 30px;
                border-radius: 30px;
                text-decoration: none;  /* 밑줄 제거 */
                font-weight: bold;
                font-size: 18px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                transition: background-color 0.3s, transform 0.2s;
            }

            .ev-button:hover {
                background-color: #45a049;
                transform: scale(1.05);
            }

            .ev-button:active {
                transform: scale(0.98);
            }

            /* 링크에 밑줄이 생기지 않도록 확실히 설정 */
            a {
                text-decoration: none !important;
            }
        </style>
        <div class="ev-container">
            <h3 class="ev-title">🚗 전기차 등록 현황</h3>
            <p class="ev-description">
                전기차 등록 현황에 대한 최신 통계와 트렌드를 확인하세요. <br>
                관련 데이터를 통해 전기차 시장의 변화와 성장을 빠르게 파악하세요!
            </p>
            <p style="text-align: center;">
                <a href="http://localhost:8501/01_EV_Status" target="_self" class="ev-button">
                    전기차 현황 보기
                </a>
            </p>
        </div>
    """, unsafe_allow_html=True)

# 2. 전기차 충전소 검색
with col2:
    st.markdown("""
        <style>
            .charging-container {
                background-color: #FF5722;  /* 주황색 배경 */
                border-radius: 12px;
                padding: 30px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                margin: 20px;
            }

            .charging-title {
                color: white;
                text-align: center;
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 10px;
            }

            .charging-description {
                color: white;
                text-align: center;
                font-size: 16px;
                margin-bottom: 20px;
            }

            .charging-button {
                display: inline-block;
                background-color: white;  /* 흰색 배경 */
                color: #FF5722;  /* 주황색 글자 */
                padding: 12px 30px;
                border-radius: 30px;
                text-decoration: none;  /* 밑줄 제거 */
                font-weight: bold;
                font-size: 18px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                transition: background-color 0.3s, transform 0.2s;
            }

            .charging-button:hover {
                background-color: #E64A19;
                transform: scale(1.05);
            }

            .charging-button:active {
                transform: scale(0.98);
            }

            /* 링크에 밑줄이 생기지 않도록 확실히 설정 */
            a {
                text-decoration: none !important;
            }
        </style>
        <div class="charging-container">
            <h3 class="charging-title">🔌 전기차 충전소 검색</h3>
            <p class="charging-description">
                전국 전기차 충전소를 검색하고, 가까운 충전소를 빠르게 찾을 수 있습니다. <br>
                필터를 통해 원하는 충전소를 선택하세요!
            </p>
            <p style="text-align: center;">
                <a href="http://localhost:8501/02_Charging_Station" target="_self" class="charging-button">
                    충전소 검색하기
                </a>
            </p>
        </div>
    """, unsafe_allow_html=True)


st.markdown("""
    <hr style="border: 1px solid #eeeeee;">
    <p style="text-align: center; color: #888888;">문의 사항이나 피드백은 <strong>project4team@example.com</strong>으로 보내주세요.</p>
""", unsafe_allow_html=True)
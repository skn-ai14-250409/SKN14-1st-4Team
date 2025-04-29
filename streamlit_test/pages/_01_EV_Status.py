import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium
import plotly.express as px
import matplotlib.ticker as ticker

# 폰트 및 스타일 설정
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams.update({'font.size': 10})

COLOR_MAP = {
    '서울': '#FF0000', '인천': '#0000FF', '경기': '#FFA500', '강원': '#008000',
    '충북': '#800080', '충남': '#FFC0CB', '대전': '#00FFFF', '세종': '#FFFF00',
    '경북': '#228B22', '대구': '#8A2BE2', '전북': '#00008B', '전남': '#20B2AA',
    '광주': '#7FFF00', '경남': '#DC143C', '부산': '#9932CC', '울산': '#4169E1', '제주': '#FFD700'
}

LOCATION_MAP = {
    '서울': [37.5665, 126.9780],
    '인천': [37.4563, 126.7052],
    '경기': [37.4138, 127.5183],
    '강원': [37.8228, 128.1555],
    '충북': [36.6357, 127.4917],
    '충남': [36.5184, 126.8],
    '대전': [36.3504, 127.3845],
    '세종': [36.4801, 127.2890],
    '경북': [36.5760, 128.5056],
    '대구': [35.8722, 128.6025],
    '전북': [35.7167, 127.1442],
    '전남': [34.8161, 126.4630],
    '광주': [35.1595, 126.8526],
    '경남': [35.4606, 128.2132],
    '부산': [35.1796, 129.0756],
    '울산': [35.5384, 129.3114],
    '제주': [33.4996, 126.5312]
}

STATION_TO_CAR_REGION_MAP = {
    '서울특별시': '서울', '인천광역시': '인천', '경기도': '경기', '강원특별자치도': '강원',
    '충청북도': '충북', '충청남도': '충남', '대전광역시': '대전', '세종특별자치시': '세종',
    '경상북도': '경북', '대구광역시': '대구', '전북특별자치도': '전북', '전라남도': '전남',
    '광주광역시': '광주', '경상남도': '경남', '부산광역시': '부산', '울산광역시': '울산',
    '제주특별자치도': '제주'
}

CSV_DIR_CARS = 'ev_cars.csv'
CSV_DIR_STATIONS = 'EV_charging_station_info.csv'
IMAGE_PATH = './img.png'

# CSV_DIR_CARS = 'C:/Users/play data/Desktop/streamlit_test/ev_cars.csv'
# CSV_DIR_STATIONS = 'C:/Users/play data/Desktop/streamlit_test/EV_charging_station_info.csv'
# IMAGE_PATH = 'C:/Users/play data/Desktop/streamlit_test/img.png'

# CSV_DIR_CARS = 'ev_cars.csv'
ev_cars_df = pd.read_csv(CSV_DIR_CARS, encoding='utf-8')
ev_cars_df['기준일'] = pd.to_datetime(ev_cars_df['기준일'])
ev_cars_df['연도'] = ev_cars_df['기준일'].dt.year
region_cols = ev_cars_df.columns.drop(['기준일', '연도'])
ev_cars_df['전국합계'] = ev_cars_df[region_cols].sum(axis=1)

# CSV_DIR_STATIONS = 'EV_charging_station_info.csv'
station_df = pd.read_csv(CSV_DIR_STATIONS, encoding='cp949')
station_df.columns = station_df.columns.str.strip()
station_df['설치년도'] = station_df['설치년도'].astype(int)
station_df_unique = station_df.drop_duplicates(subset=['충전소명'])
station_df_unique['지역'] = station_df_unique['시도'].map(STATION_TO_CAR_REGION_MAP)


st.set_page_config(page_title='전기차 현황',
                   page_icon='⚡',
                   layout='wide')

st.markdown("<h1 style='text-align: center;'>전기차 등록 및 충전소 현황</h1>",
            unsafe_allow_html=True)
st.markdown('  ')
st.markdown('---')

# ========================================
# 첫번째 그래프_연도별 전기차 & 충전소 등록 현황
# ========================================
st.markdown("## 연도별 전기차 & 충전소 등록 현황")
region_cols = ev_cars_df.columns.drop(['기준일', '연도'])

station_summary = []
target_years = sorted(ev_cars_df['연도'].unique())

for year in target_years:
    count = station_df_unique[station_df_unique['설치년도'] <= year]['충전소명'].nunique()
    station_summary.append((year, count))

station_count_df = pd.DataFrame(station_summary, columns=['연도', '충전소 수'])
station_count_df['전기차 수'] = ev_cars_df['전국합계']
station_count_df['충전소 보급률(%)'] = station_count_df['충전소 수'] / station_count_df['전기차 수'] * 100

col1, col2 = st.columns(2)

# ===== 연도별 전기차 등록 수 그래프 =====
with col1:
    st.markdown("### 연도별 전기차 등록 수")
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(ev_cars_df['연도'], ev_cars_df['전국합계'], marker='o')
    ax.set_xlabel('연도')
    ax.set_ylabel('전기차 수')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    st.pyplot(fig)

# ===== 연도별 충전소 수 =====
with col2:
    st.markdown("### 연도별 충전소 수")
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(station_count_df['연도'], station_count_df['충전소 수'], marker='s', color='green')
    ax.set_xlabel('연도')
    ax.set_ylabel('충전소 수')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    st.pyplot(fig)

st.markdown('---')

# ==============================================
# 두번째 그래프(지도)_지역별 전기차 등록 수 및 충전소 수
# ==============================================
latest_year = 2025
st.markdown(f"## {latest_year}년 지역별 전기차 등록 수 및 충전소 수")

# 데이터 준비
car_row_2025 = ev_cars_df[ev_cars_df['연도'] == latest_year].drop(columns=['기준일', '연도', '전국합계']).T
car_row_2025.columns = ['전기차 수']
car_row_2025 = car_row_2025.reset_index().rename(columns={'index': '지역'})

station_filtered_2025 = station_df_unique[station_df_unique['설치년도'] <= latest_year]
station_by_region_2025 = station_filtered_2025.groupby('지역')['충전소명'].nunique().reset_index()
station_by_region_2025.columns = ['지역', '충전소 수']

merged_2025 = pd.merge(car_row_2025, station_by_region_2025, on='지역', how='left').fillna(0)
merged_2025['충전소 수'] = merged_2025['충전소 수'].astype(int)

# ===== 지역별 전기차 등록 수 지도 + 그래프 =====
col3, col4 = st.columns([1.2, 1])

with col3:
    st.markdown("### 지역별 전기차 등록 수 지도")
    m1 = folium.Map(location=[36.5, 127.8], zoom_start=7, tiles='cartodbpositron')
    for idx, row in merged_2025.iterrows():
        region = row['지역']
        value = row['전기차 수']
        if region in LOCATION_MAP:
            radius = min(25, max(5, value / 5000))
            color = 'red' if value > 80000 else 'orange' if value > 30000 else 'green'
            folium.CircleMarker(
                location=LOCATION_MAP[region],
                radius=radius,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7,
                popup=f"<b>{region}</b><br>전기차 수: {value:,}대",
                tooltip=f"{region}: 전기차 {value:,}대"
            ).add_to(m1)
            folium.Marker(
                location=LOCATION_MAP[region],
                icon=folium.DivIcon(html=f"""<div style="font-size: 10pt; color: black; text-align:center;">{region}</div>""")
            ).add_to(m1)
    st_folium(m1, width=600, height=400)

with col4:
    st.markdown("### 지역별 전기차 수")
    fig1 = px.bar(merged_2025.sort_values('전기차 수', ascending=False),
                  x='지역', y='전기차 수', color='지역',
                  color_discrete_map=COLOR_MAP, text_auto=True)
    fig1.update_layout(height=400)
    st.plotly_chart(fig1, use_container_width=True)

# ===== 지역별 충전소 등록 수 지도 + 그래프 =====
col5, col6 = st.columns([1.2, 1])

with col5:
    st.markdown("### 지역별 충전소 수 지도")
    m2 = folium.Map(location=[36.5, 127.8], zoom_start=7, tiles='cartodbpositron')
    for idx, row in merged_2025.iterrows():
        region = row['지역']
        value = row['충전소 수']
        if region in LOCATION_MAP:
            radius = min(25, max(5, value / 200))
            color = 'blue' if value > 1500 else 'skyblue' if value > 500 else 'lightgreen'
            folium.CircleMarker(
                location=LOCATION_MAP[region],
                radius=radius,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.7,
                popup=f"<b>{region}</b><br>충전소 수: {value:,}개",
                tooltip=f"{region}: 충전소 {value:,}개"
            ).add_to(m2)
            folium.Marker(
                location=LOCATION_MAP[region],
                icon=folium.DivIcon(html=f"""<div style="font-size: 10pt; color: black; text-align:center;">{region}</div>""")
            ).add_to(m2)
    st_folium(m2, width=600, height=400)

with col6:
    st.markdown("### 지역별 충전소 수")
    fig2 = px.bar(merged_2025.sort_values('충전소 수', ascending=False),
                  x='지역', y='충전소 수', color='지역',
                  color_discrete_map=COLOR_MAP, text_auto=True)
    fig2.update_layout(height=400)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown('---')

# ==============================================
# 세번째 그래프_연도별 지역별 충전소 보급률 (연도 선택)
# ==============================================
st.markdown("## 연도별 지역별 충전소 보급률")

target_years = sorted(ev_cars_df['연도'].unique())
selected_year = st.selectbox('연도를 선택하세요', target_years, index=len(target_years)-1)

car_row = ev_cars_df[ev_cars_df['연도'] == selected_year].drop(columns=['기준일', '연도', '전국합계']).T
car_row.columns = ['전기차 수']
car_row = car_row.reset_index().rename(columns={'index': '지역'})

station_filtered = station_df_unique[station_df_unique['설치년도'] <= selected_year]
station_by_region = station_filtered.groupby('지역')['충전소명'].nunique().reset_index()
station_by_region.columns = ['지역', '충전소 수']

region_summary = pd.merge(car_row, station_by_region, on='지역', how='left').fillna(0)
region_summary['충전소 수'] = region_summary['충전소 수'].astype(int)
region_summary['충전소 보급률(%)'] = (region_summary['충전소 수'] / region_summary['전기차 수']) * 100
region_summary['충전소 보급률(%)'] = region_summary['충전소 보급률(%)'].round(2)

# ===== 지역별 충전소 보급률 그래프 =====
fig = px.bar(region_summary.sort_values('충전소 보급률(%)', ascending=False),
             x='지역', y='충전소 보급률(%)', color='지역',
             title=f"{selected_year}년 지역별 충전소 보급률", color_discrete_map=COLOR_MAP, text_auto=True)
st.plotly_chart(fig, use_container_width=True)

st.markdown('---')

# ==============================================
# 네번째 그래프_연도별 완속 & 급속 충전기 수 추이
# ==============================================
st.markdown("## 연도별 완속 & 급속 충전기 수 추이")

fast_slow_summary = []
for year in target_years:
    temp = station_df_unique[station_df_unique['설치년도'] <= year]
    fast = temp[temp['기종(대)'].str.contains('급속', na=False)].shape[0]
    slow = temp[temp['기종(대)'].str.contains('완속', na=False)].shape[0]
    total = fast + slow
    fast_slow_summary.append({
        '연도': year,
        '급속 충전기 수': fast,
        '완속 충전기 수': slow,
        '급속 비율(%)': (fast / total) * 100 if total else 0,
        '완속 비율(%)': (slow / total) * 100 if total else 0
    })

fast_slow_df = pd.DataFrame(fast_slow_summary)

# 완속/급속 충전기 수 추이
fig = px.line(fast_slow_df, x='연도', y=['완속 충전기 수', '급속 충전기 수'], markers=True)
st.plotly_chart(fig, use_container_width=True)

st.markdown('---')

# ==============================================
# 다섯번째 그래프(이미지)_지역별 충전소 이용가능|이용제한 비교
# ==============================================
# IMAGE_PATH 위에 저장

st.markdown("## 지역별 충전소 이용가능|이용제한 비교 ")
try:
    st.image(IMAGE_PATH)
except FileNotFoundError:
    st.error(f"'{IMAGE_PATH}' 파일을 찾을 수 없습니다. 경로를 확인해주세요.")
